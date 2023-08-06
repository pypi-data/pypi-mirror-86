
from typing import Tuple, List
import warnings
import pandas as pd


def check_kpi_function_exist(
            list_kpi: List[str], dico_fct: dict
        ) -> Tuple[bool, list, list]:
    """
    Check if each kpi of list_kpi is in dico_function
    Parameters :
    - list_kpi : list of KPI to calculate
    - dico_function : the dictionnar containing the information for each KPI
    Return a tuple containing :
    - True if all kpi are in the dictionnary, False otherwise
    - The list of kpi from list_kpi present in dico_function
    - The list of kpi absent from dico_function
    """
    list_existing_kpi = [x for x in list_kpi if x in dico_fct]
    missing_kpi = [x for x in list_kpi if x not in list_existing_kpi]
    result = len(missing_kpi) == 0
    if not result:
        msg = 'all KPI are not in the function dictionnary : '+(" - ".join(missing_kpi))
        warnings.warn(msg, Warning)

    return result, list_existing_kpi, missing_kpi


def list_cube(list_kpi: list, dico_fonction: dict) -> Tuple[set, set]:
    """
    Return the list of all cube necessary to calculate the wanted kpi
    and the list of cube necessary to calculate metric kpi
    list_kpi : a list of kpi present in dico_function
    dico_function : the dictionnar containing the information for each KPI
    """
    cube_needed = []
    cube_metric = []
    for kpi in list_kpi:
        kpi_function = dico_fonction[kpi]["func"]
        kpi_type = dico_fonction[kpi]["type"]
        if not type(kpi_function[0]) is list:
            kpi_function = [kpi_function]

        for sub_kpi_function in kpi_function:
            if kpi_type == 'metric':
                cube_metric.append(sub_kpi_function[1])
            cube_needed.append(sub_kpi_function[1])

    cube_needed = set([x for x in cube_needed if x is not None])
    cube_metric = set([x for x in cube_metric if x is not None])
    return cube_needed, cube_metric


def filter_cube_date(
            cube: pd.DataFrame, date_filter: dict, format: str = "%d-%m-%Y"
        ) -> pd.DataFrame:
    """
    Filter the cube with the selected date and return it
    Params :
    - cube : the cube of data (a dataframe)
    - date_filter : a dictionnary containing the date filter
    - format : the format of the date present in the date filter, must be accepted by
    panda.to_datetime
    """
    if date_filter['mode'] == "ALL":
        return cube
    else:
        tz = cube['tstamp'].dt.tz
        from_date, to_date = date_to_pd_timestamp(
                                date_filter['from'], date_filter['to'],
                                tz, format
                            )
        data = cube[cube['tstamp'].between(from_date, to_date, inclusive=True)]
    return data


def date_to_pd_timestamp(from_date: str, to_date: str, tz, format: str):
    if from_date is None:
        from_date = pd.Timestamp.min
    else:
        from_date = pd.to_datetime(from_date, utc=tz, format=format)

    if to_date is None:
        to_date = pd.Timestamp.max
    else:
        to_date = pd.to_datetime(to_date, utc=tz, format=format)

    if from_date > to_date:
        tmp_date = from_date
        from_date = to_date
        to_date = tmp_date

    return from_date, to_date


def convert_filters(filters: dict, filter_to_cube_col: dict) -> dict:
    return 0
