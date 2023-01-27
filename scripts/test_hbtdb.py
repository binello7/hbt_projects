from hbt import utils_hbt as uh
import matplotlib.pyplot as plt

id = 1078
dt_from = '24.09.2022 00:00:00'
dt_to = '27.09.2022 00:00:00'

data = uh.hbtdb_get_data(hbt_id=id, dt_from=dt_from, dt_to=dt_to)
data.plot()
plt.show()
