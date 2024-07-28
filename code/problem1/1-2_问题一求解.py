import numpy as np
from scipy.optimize import minimize

# 声速常量，单位为米/秒
v = 340

# 定义设施及其相关信息
facilities = {
    'D': {'longitude': 110.251, 'latitude': 27.825, 'altitude': 850, 'arrival_time': 258.985},
    'E': {'longitude': 110.524, 'latitude': 27.617, 'altitude': 786, 'arrival_time': 118.443},
    'F': {'longitude': 110.467, 'latitude': 27.921, 'altitude': 678, 'arrival_time': 266.871},
    'G': {'longitude': 110.047, 'latitude': 27.121, 'altitude': 575, 'arrival_time': 163.024}
}


def target(vars):
    """
    目标函数，用于优化追踪目标的位置和时间。

    Args:
        vars (list): 待优化的变量，包括经度、纬度、高程和时间。

    Returns:
        float: 优化目标函数的结果，包括残差平方和、高程惩罚和时间惩罚。
    """
    x, y, z, t = vars
    remainders = []

    # 计算各设施的预测到达时间与实际到达时间的残差
    for facility in facilities.values():
        lon, lat, alt, time = facility['longitude'], facility['latitude'], facility['altitude'], facility[
            'arrival_time']
        distance = ((x - lon) ** 2 + (y - lat) ** 2 + (z - alt) ** 2) ** 0.5
        predicted_time = t + distance / v
        remainders.append(predicted_time - time)

    # 添加高程惩罚项以确保高程不低于某个值
    penalty = 0
    min_altitude = 10000
    if z < min_altitude:
        penalty = (min_altitude - z) ** 2

    # 添加时间惩罚项以确保到达时间不超过某个值
    time_penalty = 0
    max_arrival_time = 110
    if t > max_arrival_time:
        time_penalty = (t - max_arrival_time) ** 2

    # 计算总的优化目标函数值
    return np.sum(np.array(remainders) ** 2) + penalty + time_penalty


# 初始化猜测值（用于循环迭代，优化结果，设定初始值）
initial_guess = [110.5, 27.5, 1000, 33]

# 使用 minimize 函数进行优化
result = minimize(target, initial_guess)

# 获取优化结果
x, y, z, t = result.x

# 输出优化结果
print("残骸发生音爆时的位置和时间：")
print(f"经度 = {x:.5f}°, 纬度 = {y:.5f}°, 高程 = {z:.2f} m, 时间 = {t:.3f} s")
