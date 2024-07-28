import numpy as np
from scipy.optimize import minimize

# 声速常量，单位为米/秒
c = 340.0

# 各监测点的位置和到达时间数据
facilities = {
    'A': {'x': 110.241, 'y': 27.204, 'z': 824, 'times': [100.767, 164.229, 214.850, 270.065]},
    'B': {'x': 110.783, 'y': 27.456, 'z': 727, 'times': [92.453, 112.220, 169.362, 196.583]},
    'C': {'x': 110.762, 'y': 27.785, 'z': 742, 'times': [75.560, 110.696, 156.936, 188.020]},
    'D': {'x': 110.251, 'y': 28.025, 'z': 850, 'times': [94.653, 141.409, 196.517, 258.985]},
    'E': {'x': 110.524, 'y': 27.617, 'z': 786, 'times': [78.600, 86.216, 118.443, 126.669]},
    'F': {'x': 110.467, 'y': 28.081, 'z': 678, 'times': [67.274, 166.270, 175.482, 266.871]},
    'G': {'x': 110.047, 'y': 27.521, 'z': 575, 'times': [103.738, 163.024, 206.789, 210.306]}
}


def target_function(variables):
    """
    目标函数，计算残差的平方和。

    Args:
        variables (list): 待优化的变量，包括位置和时间。

    Returns:
        float: 残差的平方和。
    """
    x, y, z, t1, t2, t3, t4 = variables
    leftovers = []
    for key, facility in facilities.items():
        dx = x - facility['x']
        dy = y - facility['y']
        dz = z - facility['z']
        clearance = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        forecasted_times = [clearance / c + ti for ti in [t1, t2, t3, t4]]
        leftovers.extend([(atime - ptime) ** 2 for atime, ptime in zip(facility['times'], forecasted_times)])
    return sum(leftovers)


# 初始猜测值
x0 = [110.5, 27.5, 800, 50, 70, 100, 126]

# 约束条件
constraints = [
    {'type': 'ineq', 'fun': lambda x: x[2] - 10000},  # 高程约束
    {'type': 'ineq', 'fun': lambda x: x[3] - 20},  # t1 下界约束
    {'type': 'ineq', 'fun': lambda x: 67 - x[3]},  # t1 上界约束
    {'type': 'ineq', 'fun': lambda x: 86 - x[4]},  # t2 上界约束
    {'type': 'ineq', 'fun': lambda x: 118 - x[5]},  # t3 上界约束
    {'type': 'ineq', 'fun': lambda x: 126 - x[6]},  # t4 上界约束
]

# 使用 minimize 函数进行优化
management = minimize(target_function, x0, constraints=constraints)

# 输出优化结果
if management.success:
    x, y, z, t1, t2, t3, t4 = management.x
    print(f"残骸在空中发生音爆时的预估时间: {t1}, {t2}, {t3}, {t4}")
else:
    print("Optimization failed.")
