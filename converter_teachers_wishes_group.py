
# from data_generator import studentGroup_name_list, studentGroup_quantity
#
# studentGroup_list = [(i + 1, name) for i, name in enumerate(studentGroup_name_list)]
# studentGroup_nums = studentGroup_quantity[0] + studentGroup_quantity[1] + studentGroup_quantity[2]
# studentGroup_nums_sum = [sum(studentGroup_nums[:i + 1]) for i in range(len(studentGroup_nums))]
# double_x_template = {
#     '1-x-x': [i[0] for i in studentGroup_list[:sum(studentGroup_quantity[0])]],
#     '2-x-x': [i[0] for i in studentGroup_list[sum(studentGroup_quantity[0]):sum(studentGroup_quantity[0]+studentGroup_quantity[1])]],
#     '3-x-x': [i[0] for i in studentGroup_list[sum(studentGroup_quantity[0]+studentGroup_quantity[1]):sum(studentGroup_nums)]]
# }
# single_templates_list = ['1-1-x', '1-2-x', '1-3-x', '1-4-x', '1-5-x', '1-6-x',
#                          '2-1-x', '2-2-x', '2-3-x', '2-4-x', '2-5-x', '2-6-x',
#                          '3-2-x', '3-4-x']
# single_x_template = dict()
# for a in single_templates_list:
#     mas = []
#     for group in studentGroup_list:
#         if a[:-1] in group[1]:
#             mas.append(group[0])
#     single_x_template[a] = mas
#
# zero_x_template = dict([(i[1], i[0]) for i in studentGroup_list])
#
# print(zero_x_template)
# print(single_x_template)
# print(double_x_template)

# Hardcoding!!!! Закоменченный выше код даёт значения zero_x_template, single_x_template, double_x_template

import sqlite3 as sq


zero_x_template = {'1-1-1': 1, '1-1-2': 2, '1-1-3': 3, '1-1-4': 4, '1-1-5': 5, '1-1-6': 6, '1-1-7': 7, '1-1-8': 8, '1-1-9': 9, '1-1-10': 10, '1-2-1': 11, '1-2-2': 12, '1-2-3': 13, '1-2-4': 14, '1-2-5': 15, '1-2-6': 16, '1-2-7': 17, '1-2-8': 18, '1-2-9': 19, '1-2-10': 20, '1-2-11': 21, '1-2-12': 22, '1-2-13': 23, '1-2-14': 24, '1-3-1': 25, '1-3-2': 26, '1-3-3': 27, '1-3-4': 28, '1-3-5': 29, '1-3-6': 30, '1-4-1': 31, '1-4-2': 32, '1-4-3': 33, '1-4-4': 34, '1-4-5': 35, '1-4-6': 36, '1-4-7': 37, '1-4-8': 38, '1-4-9': 39, '1-5-1': 40, '1-5-2': 41, '1-5-3': 42, '1-5-4': 43, '1-5-5': 44, '1-5-6': 45, '1-5-7': 46, '1-5-8': 47, '1-5-9': 48, '1-5-10': 49, '1-6-1': 50, '1-6-2': 51, '1-6-3': 52, '1-6-4': 53, '1-6-5': 54, '1-6-6': 55, '1-6-7': 56, '2-1-1': 57, '2-1-2': 58, '2-1-3': 59, '2-1-4': 60, '2-1-5': 61, '2-1-6': 62, '2-1-7': 63, '2-1-8': 64, '2-1-9': 65, '2-1-10': 66, '2-1-11': 67, '2-1-12': 68, '2-2-1': 69, '2-2-2': 70, '2-2-3': 71, '2-2-4': 72, '2-2-5': 73, '2-2-6': 74, '2-2-7': 75, '2-2-8': 76, '2-2-9': 77, '2-2-10': 78, '2-2-11': 79, '2-2-12': 80, '2-2-13': 81, '2-2-14': 82, '2-2-15': 83, '2-3-1': 84, '2-3-2': 85, '2-3-3': 86, '2-3-4': 87, '2-3-5': 88, '2-3-6': 89, '2-4-1': 90, '2-4-2': 91, '2-4-3': 92, '2-4-4': 93, '2-4-5': 94, '2-4-6': 95, '2-4-7': 96, '2-4-8': 97, '2-5-1': 98, '2-5-2': 99, '2-5-3': 100, '2-5-4': 101, '2-5-5': 102, '2-5-6': 103, '2-5-7': 104, '2-5-8': 105, '2-5-9': 106, '2-5-10': 107, '2-6-1': 108, '2-6-2': 109, '2-6-3': 110, '2-6-4': 111, '2-6-5': 112, '2-6-6': 113, '2-6-7': 114, '3-2-1': 115, '3-2-2': 116, '3-2-3': 117, '3-2-4': 118, '3-2-5': 119, '3-2-6': 120, '3-2-7': 121, '3-2-8': 122, '3-2-9': 123, '3-2-10': 124, '3-2-11': 125, '3-2-12': 126, '3-2-13': 127, '3-2-14': 128, '3-4-1': 129, '3-4-2': 130, '3-4-3': 131, '3-4-4': 132, '3-4-5': 133, '3-4-6': 134, '3-4-7': 135}
single_x_template = {'1-1-x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], '1-2-x': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], '1-3-x': [25, 26, 27, 28, 29, 30], '1-4-x': [31, 32, 33, 34, 35, 36, 37, 38, 39], '1-5-x': [40, 41, 42, 43, 44, 45, 46, 47, 48, 49], '1-6-x': [50, 51, 52, 53, 54, 55, 56], '2-1-x': [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68], '2-2-x': [69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83], '2-3-x': [84, 85, 86, 87, 88, 89], '2-4-x': [90, 91, 92, 93, 94, 95, 96, 97], '2-5-x': [98, 99, 100, 101, 102, 103, 104, 105, 106, 107], '2-6-x': [108, 109, 110, 111, 112, 113, 114], '3-2-x': [115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128], '3-4-x': [129, 130, 131, 132, 133, 134, 135]}
double_x_template = {'1-x-x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56], '2-x-x': [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114], '3-x-x': [115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135]}

