import numpy as np
import matplotlib.pyplot as plt

plt.style.use(r'C:\LibsAndApps\Python config files\proplot_style.mplstyle')

slider_dist = 0
peak_def_off = [1, 2, 3, 4]
peak_def_on = [1, 2, 3, 4]
left_angle_off = [1, 2, 3, 4]
left_angle_on = [1, 2, 3, 4]
right_angle_off = [1, 2, 3, 4]
right_angle_on = [1, 2, 3, 4]

# syntax:
# data = {composition #: list of datasets at fixed slider distance from the end of the frame}
# each dataset is a tuple of (slider distance, data)
# there are six lists of data, each corresponding to a different measurement
    # peak deflection (magnet off), peak deflection (magnet on),
    # left contact angle with support (magnet off), left contact angle with support (magnet on),
    # right contact angle with support (magnet off), right contact angle with support (magnet on)

# lengths of the frames in pixels, used to calculate distances
# actual length of frame is 28 mm
calibration = {
    2: 634.4588,
    3: 

}



data = {
    2: [
        (79.3,
            [58, 57.5, 59, 57.6, 56.5], [65.3, 66.4, 62.3, 66.5, 68.5],
            [left_angle_off], [left_angle_on]),
        (slider_dist,
            [peak_def_off], [peak_def_on],
            [left_angle_off], [left_angle_on]),
    ],
    3: [
        (slider_dist,
            [peak_def_off], [peak_def_on],
            [left_angle_off], [left_angle_on]),
        (slider_dist,
            [peak_def_off], [peak_def_on],
            [left_angle_off], [left_angle_on],),
    ],
}