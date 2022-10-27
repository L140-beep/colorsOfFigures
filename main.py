from typing import DefaultDict
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage import color

image = plt.imread('files/balls_and_rects.png')

hsv = color.rgb2hsv(image)[:, :, 0]

bin_image = np.mean(image, 2)
bin_image[bin_image > 0] = 1

labeled = label(bin_image)
props = regionprops(labeled)

circles = DefaultDict(lambda: 0)
rects = DefaultDict(lambda: 0)
count_rects = 0
count_circles = 0

for figure in range(0, labeled.max()):
       
    cy, cx = props[figure].centroid
    color = hsv[int(cy), int(cx)]
    
    if (props[figure].eccentricity):
        count_rects += 1
        rects[color] += 1
    else:
        count_circles += 1
        circles[color]+=1

print(count_rects, count_circles, labeled.max())


sorted_rect = sorted(rects.keys())
diff_rect = np.diff(sorted_rect)
delta_rect = np.std(diff_rect) * 2

for key in range(1, len(sorted_rect)):
    dc = sorted_rect[key] - sorted_rect[key - 1]
    
    if(dc < delta_rect):
        rects[sorted_rect[key]] += rects[sorted_rect[key-1]]
        rects.pop(sorted_rect[key - 1], None)

print(dict(rects))
# plt.subplot(121)
# plt.title("rects")
# plt.plot(diff_rect)
# plt.subplot(122)
# plt.title("circles")
# plt.plot(sorted(rects), "o")
# plt.show()