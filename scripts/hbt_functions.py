from datetime import datetime

import pandas as pd
import requests
from pytz import BaseTzInfo, timezone


def hbtdb_get_data(
    hbt_id: int | str,
    dt_from: str | datetime,
    dt_to: str | datetime,
    dt_format: str = '%d.%m.%Y %H:%M:%S',
    time_zone: BaseTzInfo = timezone('Europe/Zurich'),
    server: str = 'http://dataserver.hunziker-betatech.ch:5000',
    endpoint: str = '/messdaten/API/v1.0/',
    limit: int | str = 0
    ) -> pd.DataFrame:
    """
    Gets data from the HBT Messdatenbank given the 'Messeinheit-ID'.

    Parameters
    ----------
    hbt_id: int, str
        ID of the desired 'Messeinheit' (cf. http://dataserver.hunziker-betatech
        .ch:5000/messdaten/API/v1.0/messeinheit)
    dt_from: str, datetime
        Date-time from when the data have to be downloaded. The format has to
        match 'dt_format' (default format: 'DD.MM.YYYY HH:MM:SS')
    dt_to: str, datetime
        Date-time from when the data have to be downloaded. The format has to
        match 'dt_format' (default format: 'DD.MM.YYYY HH:MM:SS')
    dt_format: str, default '%d.%m.%Y %H:%M:%S'
        Date-time format in which 'dt_from' and 'dt_to' are given. Default is
        'DD.MM.YYYY HH:MM:SS'.
    server: str, default 'http://dataserver.hunziker-betatech.ch:5000'
        Adress of the server from which the data are downloaded. Default is the
        adress of the 'HBT Messdatenbank'
    endpoint: str, default '/messdaten/API/v1.0/'
        Endpoint from which the data are downloaded
    limit: int, str, default 0
        Limits the amount of data points that are downloaded from the database.
        The default value is '0', which means no limit is applied

    Returns
    -------
        DataFrame
        DataFrame containing the downloaded data
    """
    # Set dates
    if isinstance(dt_from, str):
        dt_from = datetime.strptime(dt_from, dt_format)

    if isinstance(dt_to, str):
        dt_to = datetime.strptime(dt_to, dt_format)
    
    dt_from = dt_from.isoformat()
    dt_to = dt_to.isoformat()

    # Set ID, limit
    hbt_id = str(hbt_id)
    limit = str(limit)

    # Set params
    params = {
        'format': 'json',
        'time_from': dt_from,
        'time_to': dt_to,
        'limit': limit
    }

    # Build URL
    url = f"{server}{endpoint}messeinheit/{hbt_id}/messresultat"

    # Get the data
    r = requests.get(url, params=params)

    # Convert from JSON
    data = r.json()

    # Read data to DataFrame
    df = pd.DataFrame(data['messresultate'])

    # Set 'zeit_phaenomen' as index and remove timezone
    df['datum'] = pd.to_datetime(df['zeit_phaenomen'].apply(str), 
        format="%Y-%m-%dT%H:%M") 
    df['datum'] = df['datum'].apply(lambda dt: dt.replace(tzinfo=None))
    df.set_index('datum', inplace=True)

    # Remove unnecessary columns
    df.drop(columns=['zeit_phaenomen', 'id', 'qualitaet'], inplace=True)

    return df
