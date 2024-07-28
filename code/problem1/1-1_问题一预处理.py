import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 声速常量，单位为米/秒
v_sound = 340


def count_clearance(lat1, lon1, lat2, lon2):
    """
    计算两点之间的水平距离（在地球表面上）。

    Args:
        lat1, lon1: 第一个点的纬度和经度（度数）。
        lat2, lon2: 第二个点的纬度和经度（度数）。

    Returns:
        float: 两点之间的水平距离（米）。
    """
    # 计算纬度差的距离
    lat_clearance = 111.263 * 1000 * abs(lat2 - lat1)
    # 计算经度差的距离，考虑纬度影响
    mid_lat = (lat1 + lat2) / 2
    lon_clearance = 97.304 * 1000 * abs(lon2 - lon1) * np.cos(np.radians(mid_lat))
    # 计算总的距离（直线距离）
    return np.sqrt(lat_clearance ** 2 + lon_clearance ** 2)


# 定义监测点的坐标和海拔
coordinates = {
    'A': (110.241, 27.204, 824),
    'B': (110.780, 27.456, 727),
    'C': (110.712, 27.785, 742),
    'D': (110.251, 27.825, 850),
    'E': (110.524, 27.617, 786),
    'F': (110.467, 27.921, 678),
    'G': (110.047, 27.121, 575),
}

# 创建三维图表
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制监测点
for coordinate, data in coordinates.items():
    lon, lat, elev = data
    ax.scatter([lon], [lat], [elev], color='red', s=100)

# 绘制监测点之间的近似间隔
for coordinate1, data1 in coordinates.items():
    for coordinate2, data2 in coordinates.items():
        if coordinate1 < coordinate2:
            lon1, lat1, elev1 = data1
            lon2, lat2, elev2 = data2
            clearance_m = count_clearance(lat1, lon1, lat2, lon2)
            ax.plot([lon1, lon2], [lat1, lat2], [elev1, elev2], color='gray', linestyle=':')

# 设置坐标轴标签和图表标题
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Elevation (m)')
plt.title('Monitoring coordinates and Approximate clearances')
plt.show()
