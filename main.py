from typing import DefaultDict
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage import color

def mergeColors(colors : DefaultDict) -> dict:
    result = colors.copy()
    
    sorted_keys = sorted(result.keys())
    diff = np.diff(sorted_keys)
    delta = np.std(diff) * 2

    for key in range(1, len(sorted_keys)):
        dc = sorted_keys[key] - sorted_keys[key - 1]
        
        if(dc < delta):
            result[sorted_keys[key]] += result[sorted_keys[key-1]]
            result.pop(sorted_keys[key - 1], None)
    return dict(result)

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
        rects[color] += 1
        count_rects += 1
    else:
        count_circles += 1
        circles[color]+=1


rects = mergeColors(rects)
circles = mergeColors(circles)

print("Прямоугольники:", count_rects)
print(rects)
print("Круги:", count_circles)
print(circles)