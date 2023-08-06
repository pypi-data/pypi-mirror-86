from lib_back_hubot import list_cube, check_kpi_function_exist, \
    filter_cube_date
from os.path import join, dirname
from json import loads
import pytest
import pandas as pd


def load_payload(directory, filename):
    file_path = join(dirname(__file__), 'payloads', 'fonction_cubes',
                     directory,  f"{filename}.json")
    return loads(open(file_path).read())


def load_expectation(directory, filename):
    file_path = join(dirname(__file__), 'expectation', 'fonction_cubes',
                     directory, f"{filename}.json")
    return loads(open(file_path).read())


@pytest.mark.parametrize("directory, filename", [
    ("list_cube", "list_cube_nominal"),
    ("list_cube", "list_cube_none_cube_name")])
def test_list_cube_nominal(directory, filename):
    payload = load_payload(directory, filename)
    expectation = load_expectation(directory, filename)["result"]
    assert list_cube(payload['list_kpi'], payload['dico_function']) \
           == (set(expectation[0]), set(expectation[1]))


@pytest.mark.filterwarnings('ignore::Warning')
@pytest.mark.parametrize("directory, filename", [
    ("check_kpi_function_exist", "nominal"),
    ("check_kpi_function_exist", "inexistant_kpi")])
def test_check_kpi_function_exist(directory, filename):
    payload = load_payload(directory, filename)
    expectation = load_expectation(directory, filename)["result"]
    assert check_kpi_function_exist(payload['list_kpi'],
                                    payload['dico_function']) \
           == tuple(expectation)


def test_check_kpi_function_exist_warning():
    payload = load_payload("check_kpi_function_exist", "inexistant_kpi")
    with pytest.warns(Warning):
        check_kpi_function_exist(payload['list_kpi'], payload['dico_function'])


@pytest.mark.parametrize("directory, filename", [
    ("filter_cube_date", "nominal"),
    ("filter_cube_date", "nominal_2"),
    ("filter_cube_date", "nominal_3"),
    ("filter_cube_date", "nominal_4")])
def test_filter_cube_date(directory, filename):
    payload = load_payload(directory, filename)
    expectation = load_expectation(directory, filename)
    data = pd.DataFrame(payload["data"])
    data["tstamp"] = pd.to_datetime(data["tstamp"], format="%d-%m-%Y")

    expectation = pd.DataFrame(expectation)
    expectation["tstamp"] = pd.to_datetime(expectation["tstamp"],
                                           format="%d-%m-%Y")

    result = filter_cube_date(data, payload["filtres"])
    pd.testing.assert_frame_equal(result, expectation)
