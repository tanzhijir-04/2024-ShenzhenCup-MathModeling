import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# 声速常量，单位为米/秒
speed_of_sound = 343

# 定义监测设备的位置和信息
facilities = {
    'A': [110.241, 27.204, 824],
    'B': [110.783, 27.456, 727],
    'C': [110.762, 27.785, 742],
    'D': [110.251, 28.025, 850],
    'E': [110.524, 27.617, 786],
    'F': [110.467, 28.081, 678],
    'G': [110.047, 27.521, 575]
}

# 转换设施数据为 numpy 数组
invigilators_data = np.array(list(facilities.values()))

# 随机生成残骸的真实位置和时间
num_debris = 4
true_debris_places = np.random.rand(num_debris, 3) * 1000  # 单位：米
true_debris_times = np.random.rand(num_debris) * 100  # 100秒以内
true_debris_times = np.clip(true_debris_times, 0, 100)


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
        clearances = np.sqrt(np.sum((invigilators[:, :2] - debris_pos[:2]) ** 2, axis=1))
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
    predicted_places = variables[:num_debris * 3].reshape(num_debris, 3)
    predicted_times = variables[num_debris * 3:]
    predicted_arrival_times = count_arrival_times(predicted_places, predicted_times, invigilators[:, :2])
    return np.sum((predicted_arrival_times - invigilator_times) ** 2)


# 初始化最小波动性和最佳设备数量
min_volatility = float('inf')
best_configurations = []
num_iterations = 7

# 开始循环迭代，优化结果
while len(best_configurations) < num_iterations:
    # 随机生成不同数量的监测设备
    num_invigilators = np.random.randint(4, 8)  # 随机选择设备数量
    invigilators = invigilators_data[np.random.choice(len(facilities), num_invigilators, replace=False)]

    valid_debris_places = []
    for _ in range(num_debris):
        while True:
            pos = np.random.rand(3) * 1000
            if np.all(np.sqrt(np.sum((invigilators[:, :2] - pos[:2]) ** 2, axis=1)) < 1000):
                valid_debris_places.append(pos)
                break

    true_debris_places = np.array(valid_debris_places)
    simulated_arrival_times = count_arrival_times(true_debris_places, true_debris_times, invigilators)

    # 使用优化算法估计残骸的位置和时间
    initial_guess = np.concatenate((np.random.rand(num_debris * 3), np.random.rand(num_debris)))
    result = minimize(target_function, initial_guess, args=(simulated_arrival_times, invigilators, num_debris))
    estimated_debris_places = result.x[:num_debris * 3].reshape(num_debris, 3)
    estimated_debris_times = result.x[num_debris * 3:]

    # 计算波动性
    volatility = np.mean((true_debris_places - estimated_debris_places) ** 2) + \
                 np.mean((true_debris_times - estimated_debris_times) ** 2)

    # 保存结果
    if num_invigilators == 7:
        best_configurations.append((volatility, num_invigilators, tuple(map(tuple, invigilators))))

# 统计设备被选中的次数
facility_counts = {key: 0 for key in facilities.keys()}
for _, _, invigilators in best_configurations:
    for facility in invigilators:
        facility_counts[chr(65 + np.where((invigilators_data == facility).all(axis=1))[0][0])] += 1

# 找到出现次数最多的设备组合
most_common_configuration = max(set(best_configurations), key=best_configurations.count)

# 输出结果
print("最佳设备组合:")
for i, facility in enumerate(most_common_configuration[2]):
    print(f"设备 {chr(65 + i)}: 经度 {facility[0]}, 纬度 {facility[1]}, 高度 {facility[2]}")
print(f"最佳监测设备数量: {most_common_configuration[1]}")
