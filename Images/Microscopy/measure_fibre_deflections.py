import numpy as np
import matplotlib.pyplot as plt

plt.style.use(r'C:\LibsAndApps\Python config files\proplot_style.mplstyle')

# syntax:
# data = {composition #: list of datasets at fixed slider distance from the end of the frame}
# each dataset is a tuple of (slider distance, data)
# there are six lists of data, each corresponding to a different measurement
    # peak deflection (magnet off), peak deflection (magnet on),
    # left contact angle with support (magnet off), left contact angle with support (magnet on),

# lengths of the frames in pixels, used to calculate distances
# actual length of frame is 28 mm
# slider_distance in mm, full length in pixels
# peak deflection (off, on) in pixels
# left contact angle with support (off, on) in degrees
data = {
    2: [
        (24.39, 635.4,
            [58, 57.5, 59, 57.6, 56.5], [65.3, 66.4, 62.3, 66.5, 68.5],
            [22.24, 23.26, 22.29, 21.5, 20.57], [29.79, 31.56, 30.72, 29.01, 28.36]),
        (25.38, 644,
            [55, 60, 53, 56, 56, 53, ], [66, 65, 67, 62, 65, 64, 63],
            [22.99, 24.18, 19.6, 22.4, 26.5, 24.56], [27.04, 26.96, 27.52, 30.54, 33.03, 27.94, 29.8]),
    ],
    3: [
        (26.63, 613,
            [8, 7, 8, 10, 9], [20, 19, 22, 20, 20],
            [2.64, 2.18, 3.06, 2.72, 2.90], [4.66, 4.35, 4.73, 4.46, 4.47]),
        (25.84, 611,
            [51, 49, 52, 50, 51], [59, 61, 59, 59, 59],
            [15.82, 13.3, 17.42, 16.39, 13.91], [19.71, 18.68, 20.02, 19.88, 19.93]),
        (23.44, 595,
            [73, 75, 72, 73, 70], [77, 77, 78, 75, 78],
            [26.59, 26.15, 26.85, 26.66, 26.0], [27.54, 27.14, 27.59, 27.33, 27.2])
    ],
    4: [
        (28, 691.4,
            [32], [47],
            [], [])  # could not be determined - leave this column blank
    ],
    5: [
        (28, 679,
            [9, 9, 9, 8, 9], [17, 18, 19, 18, 18],
            [2.77, 2.53, 3.04, 2.28, 2.75], [8.03, 9.14, 8.76, 8.02, 8.12]),
        (26.28, 667.76,
            [23, 22, 22, 23, 25], [32, 31, 35, 34, 31],
            [12.97, 12.05, 12.67, 13.42, 13.1], [19.21, 18.15, 19.7, 19.5, 19.5]),
    ],
    6: [
        (0, 0,
            [], [],
            [], [])  # could not be determined - leave this column blank
    ],
    7: [
        (27.66, 656,
            [13, 13, 12, 14, 14], [25, 26, 25, 27, 26],
            [1.95, 1.63, 2.41, 2.98, 3.11], [5.5, 5.1, 5.2, 5.1, 5.8]),
        (25.86, 654,
            [46, 46, 43, 48, 47], [59, 58, 61, 60, 60],
            [21.28, 21.85, 22.32, 20.95, 21.36], [36.95, 36.6, 37.24, 36.3, 36.9]),
        (25.94, 666.3,
            [71, 70, 71, 72, 71], [78, 77, 79, 78, 78],
            [29.28, 29.61, 28.99, 29.35, 29.15], [32.02, 31.7, 32.45, 32.05, 31.9])
    ],
    8: [
        (27.85, 667.4,
            [16, 16, 16, 16, 16], [18, 18, 18, 19, 19],
            [3.19, 2.86, 3.54, 2.79, 3.41], [3.71, 3.62, 3.65, 3.91, 3.81]),
        (27.15, 663.03,
            [77, 75, 75, 76, 78], [90, 91, 91, 91, 92],
            [21.37, 21.02, 21.44, 21.35, 21.81], [23.1, 22.8, 23.2, 23.1, 23.4])
    ],

}

# plot the data

fig, ax1 = plt.subplots(1, 1, figsize=(6, 6))

colors = ['r', 'g', 'b']

# [58, 57.5, 59, 57.6, 56.5], [65.3, 66.4, 62.3, 66.5, 68.5],
'''
# plot peak displacements
for i in data:
    for slider_j, (slider_mm, len_px, disp_px_off, disp_px_on, _angle_off, _angle_on) in enumerate(data[i]):
        try:
            sf = 28 / len_px
            disp_px_off = np.array(disp_px_off)
            disp_px_on = np.array(disp_px_on)
        except ZeroDivisionError:
            continue  # no data
        # mark points with x's
        ax1.plot([i - 1/6 for _ in range(len(disp_px_off))], disp_px_off * sf, 'x', color=colors[slider_j], alpha=0.5)
        ax1.plot([i + 1/6 for _ in range(len(disp_px_on))], disp_px_on * sf, 'x', color=colors[slider_j], alpha=0.5)
        # draw error bar at mean and standard deviation
        ax1.errorbar(i - 1/6, np.mean(disp_px_off * sf),
                     yerr=np.std(disp_px_off * sf), fmt='o', color=colors[slider_j])
        ax1.errorbar(i + 1/6, np.mean(disp_px_on * sf),
                     yerr=np.std(disp_px_on * sf), fmt='o', color=colors[slider_j])
    # add shaded region for 'on' and 'off'
    ax1.fill_between([i - 1/3, i], 0, 4, color='r', alpha=0.2, label='off' if (i == 2) else None)
    ax1.fill_between([i, i + 1/3], 0, 4, color='g', alpha=0.2, label='on' if (i == 2) else None)

ax1.set_xticks(range(2, 9))
ax1.set_xticklabels(range(2, 9))
ax1.set_ylim(0, 4)
ax1.tick_params(axis='x', which='minor', bottom=False)
ax1.set_xlabel('Composition #')
ax1.set_ylabel('Peak deflection (mm)')
ax1.set_title('Peak deflection vs. composition #')
plt.legend()
plt.tight_layout()

plt.show()
'''

# plot contact angles
for i in data:
    for slider_j, (slider_mm, len_px, _disp_px_off, _disp_px_on, angle_off, angle_on) in enumerate(data[i]):
        try:
            sf = 28 / len_px
            angle_off = np.array(angle_off)
            angle_on = np.array(angle_on)
        except ZeroDivisionError:
            continue  # no data
        # mark points with x's
        ax1.plot([i - 1/6 for _ in range(len(angle_off))], angle_off, 'x', color=colors[slider_j], alpha=0.5)
        ax1.plot([i + 1/6 for _ in range(len(angle_on))], angle_on, 'x', color=colors[slider_j], alpha=0.5)
        # draw error bar at mean and standard deviation
        ax1.errorbar(i - 1/6, np.mean(angle_off),
                     yerr=np.std(angle_off), fmt='o', color=colors[slider_j])
        ax1.errorbar(i + 1/6, np.mean(angle_on),
                     yerr=np.std(angle_on), fmt='o', color=colors[slider_j])
    # add shaded region for 'on' and 'off'
    ax1.fill_between([i - 1/3, i], 0, 38, color='r', alpha=0.2, label='off' if (i == 2) else None)
    ax1.fill_between([i, i + 1/3], 0, 38, color='g', alpha=0.2, label='on' if (i == 2) else None)

ax1.set_xticks(range(2, 9))
ax1.set_xticklabels(range(2, 9))
ax1.set_ylim(0, 38)
ax1.tick_params(axis='x', which='minor', bottom=False)
ax1.set_xlabel('Composition #')
ax1.set_ylabel('Contact angle (degrees)')
ax1.set_title('Contact angle vs. composition #')
plt.legend()
plt.tight_layout()

plt.show()