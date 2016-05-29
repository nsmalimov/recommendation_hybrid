# -*- coding: utf-8 -*-
# среднеквадратическое отклонение
import math


# 0 - значит не оценено, не учитываем
def root_mean_square_deviation(predict_array, actual_array):
    diference_array = []

    for i in xrange(len(predict_array)):
        if (predict_array[i] != 0):
            diference_array.append((predict_array[i] - actual_array[i]) ** 2)
    answer = math.sqrt(sum(diference_array) / float(len(diference_array)))
    return answer


def mean_absulutle_error(predict_array, actual_array):
    diference_array = []

    for i in xrange(len(predict_array)):
        if (predict_array[i] != 0):
            diference_array.append(abs(predict_array[i] - actual_array[i]))

    answer = sum(diference_array) / float(len(diference_array))
    return answer
