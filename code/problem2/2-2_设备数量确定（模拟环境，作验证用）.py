import numpy as np
from scipy.optimize import minimize

# 声速常量，单位为米/秒
speed_of_sound = 340

# 随机生成残骸的真实位置和时间
num_debris = 4
true_debris_places = np.random.rand(num_debris, 3) * 1000  # 单位：米
true_debris_times = np.random.rand(num_debris) * 10  # 单位：秒


def count_arrival_times(debris_places, debris_times, invigilators):
    """
    计算残骸到达各监测设备的预计时间。

    Args:
        debris_places (ndarray): 残骸的位置数组。
        debris_times (ndarray): 残骸的到达时间数组。
        invigilators (ndarray): 监测设备的位置数组。

    Returns:
        ndarray: 各残骸到达各监测设备的预计时间。
    """
    arrival_times = np.zeros((num_debris, len(invigilators)))
    for i, (debris_pos, debris_time) in enumerate(zip(debris_places, debris_times)):
        clearances = np.sqrt(np.sum((invigilators - debris_pos) ** 2, axis=1))
        arrival_times[i, :] = clearances / speed_of_sound + debris_time
    return arrival_times


def target_function(variables, invigilator_times, invigilators, num_debris):
    """
    目标函数，用于优化追踪目标的位置和时间。

    Args:
        variables (list): 待优化的变量，包括残骸位置和时间。
        invigilator_times (ndarray): 各监测设备的预计到达时间。
        invigilators (ndarray): 监测设备的位置数组。
        num_debris (int): 残骸数量。

    Returns:
        float: 优化目标函数的结果，包括残差平方和。
    """
    forecast_places = variables[:num_debris * 3].reshape(num_debris, 3)
    forecast_times = variables[num_debris * 3:]
    forecast_arrival_times = count_arrival_times(forecast_places, forecast_times, invigilators)
    return np.sum((forecast_arrival_times - invigilator_times) ** 2)


# 初始化最小波动性和最佳设备数量
min_volatility = float('inf')
best_num_invigilators = 0
best_estimates = None

# 评估不同数量的监测设备
for num_invigilators in range(4, 8):  # 从4到7的设备数量
    invigilators = np.random.rand(num_invigilators, 3) * 1000  # 随机生成监测设备位置
    simulated_arrival_times = count_arrival_times(true_debris_places, true_debris_times, invigilators)

    # 使用优化算法估计残骸的位置和时间
    initial_guess = np.concatenate((np.random.rand(num_debris * 3), np.random.rand(num_debris)))
    result = minimize(target_function, initial_guess, args=(simulated_arrival_times, invigilators, num_debris))
    estimated_debris_places = result.x[:num_debris * 3].reshape(num_debris, 3)
    estimated_debris_times = result.x[num_debris * 3:]

    # 计算波动性
    volatility = np.mean((true_debris_places - estimated_debris_places) ** 2) + \
                 np.mean((true_debris_times - estimated_debris_times) ** 2)

    # 比较并保存最佳结果
    if volatility < min_volatility:
        min_volatility = volatility
        best_num_invigilators = num_invigilators
        best_estimates = (estimated_debris_places, estimated_debris_times)

# 输出最佳结果
print(f"最佳监测设备数量: {best_num_invigilators}")
print("最佳估计的残骸位置:")
print(best_estimates[0])
print("最佳估计的残骸时间:")
print(best_estimates[1])
