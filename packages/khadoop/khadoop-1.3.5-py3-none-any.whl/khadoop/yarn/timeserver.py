from typing import List
import humanize
from datetime import timedelta, datetime
import pandas as pd
import arrow

DATA_DOC = {
    'id': 'yarn application ID',
    'user': 'who submitted this job',
    'name': 'job reference, for hive usually an ID',
    'startedTime': 'timestamp in milliseconds',
    'finishedTime': 'timestamp in milliseconds',
    'queue': 'yarn queue name for this job',
    'state': 'yarn state (ACCEPTED,RUN...)',
    'finalStatus': 'state in which this job stopped (FINISHED when everything is fine)',
    'progress': 'relevant only for RUNNING state',
    'trackingUI': 'from where the data are fetched. Could be History if the job is finished or ApplicationMaster if ongoing',
    'diagnostics': 'information for SUCCEDED or FAILED job. Sometimes useful for FAIL',
    'applicationType': 'TEZ,SPARK...',
    'elapsedTime': 'how long it tooks to finish the job in milliseconds',
}


def human_elapsed(nb: int) -> str:
    """milliseconds to human readable"""
    _t = humanize.i18n.activate("fr")
    return humanize.precisedelta(timedelta(milliseconds=nb), minimum_unit='hours')


def shift_ts(ts: int, tz) -> str:
    """convert UTC timestamp (ms) to europe/Paris tz in a standard string"""
    return arrow.get(ts, tzinfo='UTC').to(tz).format()


def flatten(raw: dict) -> list:
    return [elt for elt in raw['apps']['app']]


def to_minutes(milliseconds: int) -> int:
    return round((milliseconds/1000)/60)


def get_long_run(payload: dict, threshold: int, queue='') -> List[dict]:
    """
    Retrieve all application currently running for more than `threshold` minutes

    Parameters
    ----------
    payload:
        json returned py Yarn TimeServer
    threshold:
        number of minutes

    """
    if not payload:
        return []
    apps = flatten(payload)
    filtered = [elt for elt in apps if elt['state'] ==
        'RUNNING' and queue in elt['queue'].lower()]
    if not filtered:
        return []
    df = pd.DataFrame(filtered)
    df['elapsed_minutes'] = df['elapsedTime'].apply(to_minutes)
    df['started_time'] = df.startedTime.apply(
        lambda ts: shift_ts(ts, 'Europe/Paris'))
    df_threshold = df[df.elapsed_minutes > threshold]
    df_threshold['threshold_minutes'] = threshold
    fields = ['id',
              'user',
              'started_time',
              'queue',
              'elapsed_minutes',
              'progress',
              'allocatedMB',
              'allocatedVCores',
              'queueUsagePercentage',
              'threshold_minutes']
    return df_threshold[fields].to_dict(orient='records')
