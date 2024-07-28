import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 声速常量，单位为米/秒
v = 343

# 定义各监测点的位置和到达时间数据
coordinates = {
    'A': (110.241, 27.204, 824, [100.767, 164.229, 214.850, 270.065]),
    'B': (110.783, 27.456, 727, [92.453, 112.220, 169.362, 196.583]),
    'C': (110.762, 27.785, 742, [75.560, 110.696, 156.936, 188.020]),
    'D': (110.251, 28.025, 850, [94.653, 141.409, 196.517, 258.985]),
    'E': (110.524, 27.617, 786, [78.600, 86.216, 118.443, 126.669]),
    'F': (110.467, 28.081, 678, [67.274, 166.270, 175.482, 266.871]),
    'G': (110.047, 27.521, 575, [103.738, 163.024, 206.789, 210.306])
}


def leftovers(vars, coordinate_data):
    """
    计算预测时间与实际时间的残差。

    Args:
        vars (list): 待优化的变量，包括位置和时间。
        coordinate_data (list): 包含经度、纬度、高程、到达时间的数据列表。

    Returns:
        ndarray: 残差数组。
    """
    x, y, z, t = vars
    leftovers = []
    for coordinate in coordinate_data:
        lon, lat, alt, time = coordinate
        forecasted_time = (np.sqrt((x - lon) ** 2 + (y - lat) ** 2 + (z - alt) ** 2) / v) + t
        leftovers.append(forecasted_time - time)
    return leftovers


initial_guess = [110.5, 27.5, 750, 0]  # 初始猜测值

sources_places_times = []  # 用于存储音爆源的位置和时间

# 对每个音爆源进行计算
for i in range(4):
    coordinate_data = [(coordinates[coordinate][0], coordinates[coordinate][1], coordinates[coordinate][2],
                        coordinates[coordinate][3][i]) for coordinate in coordinates]
    result = least_squares(leftovers, initial_guess, args=(coordinate_data,))
    sources_places_times.append(result.x)
    print(f"音爆源 {i + 1} 的计算结果：", result.x)

# 绘制三维散点图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i, source in enumerate(sources_places_times):
    x, y, z, _ = source
    ax.scatter(x, y, z, label=f'Sonic boom source {i + 1}', s=100)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

plt.show()
