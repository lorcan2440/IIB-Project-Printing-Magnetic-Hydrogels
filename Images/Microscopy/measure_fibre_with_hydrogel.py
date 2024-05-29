import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

plt.style.use(r'C:\LibsAndApps\Python config files\proplot_style.mplstyle')

# slider distance: 25.5 mm
# video 7.MOV: frame width = 623 px, slider width = 571 px
# video 8.MOV: frame width = 1204 px, slider width = 1087 px

# 
video_7_fibres_data = {
    'on': [30, 29, 32, 30, 31, 30, 29, 29],
    'off': [26, 25, 27, 26, 26, 27, 26, 27]
}

video_7_hydrogel_data = {
    'on': [7, 7, 7, 7, 6, 6, 6, 6],
    'off': [9, 9, 9, 9, 9, 9, 9, 9]
}

video_8_fibres_data = {
    'on': [28, 26, 27, 26, 27, 27],
    'off': [19, 20, 21, 20, 19, 20]
}

video_8_hydrogel_data = {
    'on': [17, 16, 16, 15, 15, 15],
    'off': [20, 19, 19, 19, 19, 19]
}

video_7_sf = 28 / 623
video_8_sf = 28 / 1204

video_7_fibres_data['on'] = np.array(video_7_fibres_data['on']) * video_7_sf
video_7_fibres_data['off'] = np.array(video_7_fibres_data['off']) * video_7_sf
video_7_hydrogel_data['on'] = np.array(video_7_hydrogel_data['on']) * video_7_sf
video_7_hydrogel_data['off'] = np.array(video_7_hydrogel_data['off']) * video_7_sf

video_8_fibres_data['on'] = np.array(video_8_fibres_data['on']) * video_8_sf
video_8_fibres_data['off'] = np.array(video_8_fibres_data['off']) * video_8_sf
video_8_hydrogel_data['on'] = np.array(video_8_hydrogel_data['on']) * video_8_sf
video_8_hydrogel_data['off'] = np.array(video_8_hydrogel_data['off']) * video_8_sf

''' this data is too low resolution to be useful
fibres_data_on = np.concatenate((video_7_fibres_data['on'], video_8_fibres_data['on']))
fibres_data_off = np.concatenate((video_7_fibres_data['off'], video_8_fibres_data['off']))
hydrogel_data_on = np.concatenate((video_7_hydrogel_data['on'], video_8_hydrogel_data['on']))
hydrogel_data_off = np.concatenate((video_7_hydrogel_data['off'], video_8_hydrogel_data['off']))
'''

fibres_data_on = video_8_fibres_data['on']
fibres_data_off = video_8_fibres_data['off']
hydrogel_data_on = video_8_hydrogel_data['on']
hydrogel_data_off = video_8_hydrogel_data['off']

# calculate mean change in fibre deflection and hydrogel deflection
fibres_change = fibres_data_on - fibres_data_off
hydrogel_change = hydrogel_data_on - hydrogel_data_off

mean_fibre_change = np.mean(fibres_change)
mean_hydrogel_change = np.mean(hydrogel_change)
std_dev_fibre_change = np.std(fibres_change)
std_dev_hydrogel_change = np.std(hydrogel_change)

print(mean_fibre_change, std_dev_fibre_change, mean_hydrogel_change, std_dev_hydrogel_change)

# t-test for independent means between 'magnet on' and 'magnet off' states for fibres and hydrogel
t_stat_fibres, p_val_fibres = ttest_ind(fibres_data_on, fibres_data_off)
t_stat_hydrogel, p_val_hydrogel = ttest_ind(hydrogel_data_on, hydrogel_data_off)
print(t_stat_fibres, p_val_fibres, t_stat_hydrogel, p_val_hydrogel)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

ax1.plot([1] * len(fibres_data_on), fibres_data_on, 'x', label='Magnet on', color='r', alpha=0.5)
ax1.errorbar(1, np.mean(fibres_data_on), yerr=np.std(fibres_data_on), fmt='o', color='r', capsize=5)
ax1.plot([2] * len(fibres_data_on), fibres_data_off, 'x', label='Magnet off', color='b', alpha=0.5)
ax1.errorbar(2, np.mean(fibres_data_off), yerr=np.std(fibres_data_off), fmt='o', color='b', capsize=5)

ax2.plot([1] * len(hydrogel_data_on), hydrogel_data_on, 'x', label='Magnet on', color='r', alpha=0.5)
ax2.errorbar(1, np.mean(hydrogel_data_on), yerr=np.std(hydrogel_data_on), fmt='o', color='r', capsize=5)
ax2.plot([2] * len(hydrogel_data_on), hydrogel_data_off, 'x', label='Magnet off', color='b', alpha=0.5)
ax2.errorbar(2, np.mean(hydrogel_data_off), yerr=np.std(hydrogel_data_off), fmt='o', color='b', capsize=5)

ax1.set_xticks([1, 2])
ax1.set_xticklabels(['Magnet on', 'Magnet off'])
ax1.tick_params(axis='x', which='minor', bottom=False)
ax1.set_ylabel('Fibre deflection (mm)')
ax1.set_title('Fibre deflection vs. magnet state')
ax1.set_xlim(0.5, 2.5)
ax1.legend()

ax2.set_xticks([1, 2])
ax2.set_xticklabels(['Magnet on', 'Magnet off'])
ax2.tick_params(axis='x', which='minor', bottom=False)
ax2.set_ylabel('Hydrogel deflection (mm)')
ax2.set_title('Hydrogel deflection vs. magnet state')
ax2.set_xlim(0.5, 2.5)
ax2.legend()

plt.tight_layout()
plt.show()