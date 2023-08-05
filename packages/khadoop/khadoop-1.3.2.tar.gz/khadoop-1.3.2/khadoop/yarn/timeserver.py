from typing import List
import humanize
from datetime import timedelta, datetime
import pandas as pd


def human_elapsed(nb: int) -> str:
    """milliseconds to human readable"""
    _t = humanize.i18n.activate("fr")
    return humanize.precisedelta(timedelta(milliseconds=nb), minimum_unit='hours')


def human_dt(dt: datetime) -> str:
    return dt.strftime('%d/%m/%Y à %Hh%M')

def flatten(raw: dict) -> list:
    return [elt for elt in raw['apps']['app']]

def to_minutes(milliseconds:int)->int:
    return round((milliseconds/1000)/60)


def get_long_run(payload: dict, threshold: int,queue = '') -> List[dict]:
    """
    Retrieve all application currently running for more than `threshold` minutes

    Parameters
    ----------
    payload:
        json returned py Yarn TimeServer
    threshold:
        number of minutes
    
    """
    apps = flatten(payload)
    filtered = [elt for elt in apps if elt['state'] == 'RUNNING' and queue in elt['queue'].lower()]
    df = pd.DataFrame(filtered)
    for dt in ['startedTime', 'finishedTime']:
        df[dt] =pd.to_datetime(df[dt],unit='ms')
    df['elapsed_minutes'] = df['elapsedTime'].apply(to_minutes)
    df['started_time'] = df.startedTime.dt.strftime('%d/%m/%Y %Hh%M')
    df_threshold = df[df.elapsed_minutes>threshold]
    
    return df_threshold[['id','user','started_time','queue','elapsed_minutes']].to_dict(orient='records')
