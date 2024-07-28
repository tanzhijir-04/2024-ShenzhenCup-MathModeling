import numpy as np
from itertools import combinations

# 定义多个点的坐标
coordinates = {
    'A': (110.241, 27.204, 824),
    'B': (110.780, 27.456, 727),
    'C': (110.712, 27.785, 742),
    'D': (110.251, 27.825, 850),
    'E': (110.524, 27.617, 786),
    'F': (110.467, 27.921, 678),
    'G': (110.047, 27.121, 575)
}


def count_clearance(lat1, lon1, alt1, lat2, lon2, alt2):
    """计算两点在三维空间中的间隔距离."""
    return np.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2 + (alt1 - alt2) ** 2)


# 计算所有坐标对之间的间隔距离
clearances = {}
for station1, coords1 in coordinates.items():
    for station2, coords2 in coordinates.items():
        if station1 < station2:  # 避免重复计算和自身与自身的距离
            clearance = count_clearance(*coords1, *coords2)
            clearances[(station1, station2)] = clearance

# 找到间隔距离最大的点对
furthest_pair = max(clearances, key=clearances.get)
furthest_points = list(furthest_pair)
leftover_coordinates = set(coordinates.keys()) - set(furthest_points)

# 找到距离这对点最远的第三个点
third_point = None
max_clearance_sum = 0
for coordinate in leftover_coordinates:
    clearance_sum = (clearances.get((furthest_points[0], coordinate), 0) +
                     clearances.get((furthest_points[1], coordinate), 0))
    if clearance_sum > max_clearance_sum:
        max_clearance_sum = clearance_sum
        third_point = coordinate
leftover_coordinates.remove(third_point)
furthest_points.append(third_point)

# 找到距离这对点最远的第四个点
fourth_point = None
max_clearance_sum = 0
for coordinate in leftover_coordinates:
    clearance_sum = (clearances.get((furthest_points[0], coordinate), 0) +
                     clearances.get((furthest_points[1], coordinate), 0) +
                     clearances.get((furthest_points[2], coordinate), 0))
    if clearance_sum > max_clearance_sum:
        max_clearance_sum = clearance_sum
        fourth_point = coordinate
furthest_points.append(fourth_point)

# 打印出四个最远的坐标点
print("四个最远的坐标点是:", furthest_points)

# 在三维空间中绘制这些点
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制所有坐标点
for coordinate, coords in coordinates.items():
    ax.scatter(coords[0], coords[1], coords[2], label=coordinate)

# 以红色和较大的点绘制最远的点
for point in furthest_points:
    coords = coordinates[point]
    ax.scatter(coords[0], coords[1], coords[2], color='red', s=100)

# 添加坐标轴标签和图例
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Altitude')
ax.legend()
ax.legend(loc='upper right')
plt.show()
