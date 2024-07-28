import numpy as np
from scipy.optimize import least_squares

v = 340  # m/s

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
    x, y, z, t, time_error_param = vars
    leftovers = []
    for lon, lat, alt, time in coordinate_data:
        forecasted_time = (np.sqrt((x - lon) ** 2 + (y - lat) ** 2 + (z - alt) ** 2) / v) + t
        leftovers.append(forecasted_time - time + time_error_param)
    return leftovers


initial_guess = [110.5, 27.5, 750, 0, 0]


def add_time_error(coordinate_data, error_std=0.5):
    coordinate_data_with_error = []
    for lon, lat, alt, time in coordinate_data:
        time_with_error = time + np.random.normal(0, error_std)
        coordinate_data_with_error.append((lon, lat, alt, time_with_error))
    return coordinate_data_with_error


def optimized_places_times(coordinate_data, num_iterations=100):
    all_results = []
    for i in range(num_iterations):
        coordinate_data_with_error = add_time_error(coordinate_data)
        result = least_squares(leftovers, initial_guess, args=(coordinate_data_with_error,))
        result.x = np.maximum(result.x, 0)  # Ensure non-negative values
        all_results.append(result.x)
    return np.mean(all_results, axis=0)


# 计算不同情况下的音爆源位置和时间
for i in range(4):
    coordinate_data = [(coordinates[coordinate][0], coordinates[coordinate][1], coordinates[coordinate][2],
                        coordinates[coordinate][3][i]) for
                       coordinate in coordinates]
    average_result = optimized_places_times(coordinate_data)
    print(f"音爆源 {i + 1} 的平均计算结果：", average_result)

# 添加额外的监测站后重新计算
coordinates['H'] = (110.3, 27.4, 700, [120.0, 180.0, 240.0, 300.0])
coordinates['I'] = (110.6, 27.9, 780, [110.0, 170.0, 230.0, 290.0])

for i in range(4):
    coordinate_data = [(coordinates[coordinate][0], coordinates[coordinate][1], coordinates[coordinate][2],
                        coordinates[coordinate][3][i]) for
                       coordinate in coordinates]
    average_result = optimized_places_times(coordinate_data)
    print(f"增加监测站后，音爆源 {i + 1} 的平均计算结果：", average_result)
