from hbt_tools import utils_hbt as uh
from datetime import datetime as dt
from datetime import timedelta as td

probenehmer_infos = [
    {
        'name': 'SABA Hagnau',
        'id': 1078,
        'dt_from': dt(2023, 1, 31, 10),
        'sample_vol': 20 # m3
    },

    {
        'name': 'SABA Mühlestrasse',
        'id': 466,
        'dt_from': dt(2023, 4, 3),
        'sample_vol': 5 # m3
    },
]

f_dt = lambda x: dt.strftime(x, "%d.%m.%y")

dt_to = dt.today() - td(days=1)
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
