from datetime import datetime as dt
from datetime import timedelta as td

import pytz
from hbt_tools import utils_hbt as uh

probenehmer_infos = [
    {
        'name': 'SABA Hagnau',
        'id': 1078,
        'dt_from': dt(2023, 7, 24, 12, tzinfo=pytz.timezone('Europe/Zurich')),
        'sample_vol': 20 # m3
    },

    {
        'name': 'SABA Enge-Biberist',
        'id': 1931,
        'dt_from': dt(2023, 6, 16, 12, tzinfo=pytz.timezone('Europe/Zurich')),
        'sample_vol': 3 # m3
    },

    {
        'name': 'SABA Birchi',
        'id': 1922,
        'dt_from': dt(2023, 8, 4, 12, tzinfo=pytz.timezone('Europe/Zurich')),
        'sample_vol': 29 # m3
    },
]

f_dt = lambda x: dt.strftime(x, "%d.%m.%y")

dt_to = dt.today() - td(days=1)
dt_to = dt_to.astimezone(pytz.timezone('Europe/Zurich'))

max_samples = 160 * 4

for pb in probenehmer_infos:
    n_samples, tot_flow = uh.samples_from_flow(pb['id'], pb['dt_from'],
        dt_to, pb['sample_vol'], print_res=False)
    
    pb.update({'n_samples': n_samples})

for pb in probenehmer_infos:
    if pb['n_samples'] > max_samples:
        str_max_samples = (f"ATTENTION: more samples taken than max! "
        f"({max_samples})")
    else:
        str_max_samples = f"Max samples = {max_samples}"
    print(f"{pb['name']}: {pb['n_samples']} samples collected "
        f"({f_dt(pb['dt_from'])} - {f_dt(dt_to)}). "
        f"{str_max_samples}")
