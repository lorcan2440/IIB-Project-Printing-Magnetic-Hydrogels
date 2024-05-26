
import numpy as np
import matplotlib.pyplot as plt

plt.style.use(r'C:\LibsAndApps\Python config files\proplot_style.mplstyle')

scale_bar_size = 180  # microns
scale_bar_img_width = 711  # pixels

microscopy_widths = {  # widths of imaged fibres in pixels {sample: [widths]}
    1: [111, 136, 50, 42, 69, 60, 55, 158, 157, 152],
    2: [24, 32, 21, 41, 58, 40, 70, 63, 25, 38],
    3: [60, 53, 62, 52, 50, 58, 57, 57, 110, 138],
    4: [21, 39, 33, 39, 35, 41, 27, 31, 18, 26],
    5: [42, 39, 30, 36, 132, 90, 60, 60, 46, 64],
    6: [60, 118, 62, 52, 63, 58, 67, 67, 107, 131],
    7: [52, 34, 16, 40, 29, 19, 24, 25, 27, 30],
    8: [50, 43, 91, 53, 48, 37, 106, 55, 51, 58]
}

# want to compute the mean and std dev of the widths in microns for each sample
# plot as bar chart with error bars at plus minus one standard deviation

# compute the mean and std dev of the widths in microns for each sample
microscopy_means = {}
microscopy_std_devs = {}
for sample, widths in microscopy_widths.items():
    widths = np.array(widths)
    widths_microns = (widths / scale_bar_img_width) * scale_bar_size
    microscopy_means[sample] = np.mean(widths_microns)
    microscopy_std_devs[sample] = np.std(widths_microns)

# print overall mean and std dev of all widths
all_widths = np.concatenate(list(microscopy_widths.values()))
all_widths_microns = (all_widths / scale_bar_img_width) * scale_bar_size
print('Overall mean width:', np.mean(all_widths_microns))
print('Overall std dev width:', np.std(all_widths_microns))
print('Minimum width:', np.min(all_widths_microns))
print('Maximum width:', np.max(all_widths_microns))

iron_10 = microscopy_widths[1] + microscopy_widths[2] + microscopy_widths[3]
iron_20 = microscopy_widths[4] + microscopy_widths[5] + microscopy_widths[6]
iron_30 = microscopy_widths[7] + microscopy_widths[8]

iron_10_mean = np.mean(iron_10) * scale_bar_size / scale_bar_img_width
iron_20_mean = np.mean(iron_20) * scale_bar_size / scale_bar_img_width
iron_30_mean = np.mean(iron_30) * scale_bar_size / scale_bar_img_width

iron_10_std_dev = np.std(iron_10) * scale_bar_size / scale_bar_img_width
iron_20_std_dev = np.std(iron_20) * scale_bar_size / scale_bar_img_width
iron_30_std_dev = np.std(iron_30) * scale_bar_size / scale_bar_img_width

polystyrene_10 = microscopy_widths[1] + microscopy_widths[4] + microscopy_widths[7]
polystyrene_20 = microscopy_widths[2] + microscopy_widths[5] + microscopy_widths[8]
polystyrene_30 = microscopy_widths[3] + microscopy_widths[6]

polystyrene_10_mean = np.mean(polystyrene_10) * scale_bar_size / scale_bar_img_width
polystyrene_20_mean = np.mean(polystyrene_20) * scale_bar_size / scale_bar_img_width
polystyrene_30_mean = np.mean(polystyrene_30) * scale_bar_size / scale_bar_img_width

polystyrene_10_std_dev = np.std(polystyrene_10) * scale_bar_size / scale_bar_img_width
polystyrene_20_std_dev = np.std(polystyrene_20) * scale_bar_size / scale_bar_img_width
polystyrene_30_std_dev = np.std(polystyrene_30) * scale_bar_size / scale_bar_img_width

solvent_50 = microscopy_widths[6] + microscopy_widths[8]
solvent_60 = microscopy_widths[3] + microscopy_widths[5] + microscopy_widths[7]
solvent_70 = microscopy_widths[2] + microscopy_widths[4]
solvent_80 = microscopy_widths[1]

solvent_50_mean = np.mean(solvent_50) * scale_bar_size / scale_bar_img_width
solvent_60_mean = np.mean(solvent_60) * scale_bar_size / scale_bar_img_width
solvent_70_mean = np.mean(solvent_70) * scale_bar_size / scale_bar_img_width
solvent_80_mean = np.mean(solvent_80) * scale_bar_size / scale_bar_img_width

solvent_50_std_dev = np.std(solvent_50) * scale_bar_size / scale_bar_img_width
solvent_60_std_dev = np.std(solvent_60) * scale_bar_size / scale_bar_img_width
solvent_70_std_dev = np.std(solvent_70) * scale_bar_size / scale_bar_img_width
solvent_80_std_dev = np.std(solvent_80) * scale_bar_size / scale_bar_img_width

# plot as bar chart with error bars at plus minus one standard deviation
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
cols_list = ['tomato'] * 3 + ['skyblue'] * 3 + ['mediumseagreen'] * 2

ax1.bar(microscopy_means.keys(), microscopy_means.values(), yerr=microscopy_std_devs.values(), 
        color=cols_list, capsize=5)
ax1.bar([1], [0], color='tomato', label='10% Iron')
ax1.bar([1], [0], color='skyblue', label='20% Iron')
ax1.bar([1], [0], color='mediumseagreen', label='30% Iron')
ax1.set_xticks(range(1, 9))
ax1.set_xlabel('Composition #')
ax1.set_ylabel('Width (microns)')
ax1.set_title('Fibre Widths in Microscopy Images')
ax1.legend()

for sample, widths in microscopy_widths.items():
    ax2.plot([sample] * len(widths), np.array(widths) * scale_bar_size / scale_bar_img_width, 
             'x', color=cols_list[sample - 1], markersize=3)
ax2.set_xticks(range(1, 9))
ax2.set_xlabel('Composition #')
ax2.set_ylabel('Width (microns)')
ax2.set_title('Data points')

ax3.bar([1, 4, 7], [iron_10_mean, iron_20_mean, iron_30_mean], 
        yerr=[iron_10_std_dev, iron_20_std_dev, iron_30_std_dev], 
        color='tomato', capsize=5, label='Iron %')
ax3.bar([2, 5, 8], [polystyrene_10_mean, polystyrene_20_mean, polystyrene_30_mean],
        yerr=[polystyrene_10_std_dev, polystyrene_20_std_dev, polystyrene_30_std_dev],
        color='skyblue', capsize=5, label='Polystyrene %')
#ax2.set_xticks([1, 2, 4, 5, 7, 8])
ax3.set_xticklabels(['10%', '20%', '30%'])
ax3.set_xticks([1.5, 4.5, 7.5])
ax3.minorticks_off()
ax3.set_xlabel('Component %')
ax3.set_ylabel('Width (microns)')
ax3.legend()

ax4.bar([1, 2, 3, 4], [solvent_50_mean, solvent_60_mean, solvent_70_mean, solvent_80_mean],
        yerr=[solvent_50_std_dev, solvent_60_std_dev, solvent_70_std_dev, solvent_80_std_dev],
        color='mediumseagreen', capsize=5, label='Solvent %')
ax4.set_xticks([1, 2, 3, 4])
ax4.set_xticklabels(['50%', '60%', '70%', '80%'])
ax4.set_xlabel('Solvent %')
ax4.set_ylabel('Width (microns)')
ax4.legend()

plt.show()