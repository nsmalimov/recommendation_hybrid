# -*- coding: utf-8 -*-
import csv
import math

import metrics


def open_file_users_small(file_name):
    array_file = []
    restr = 10000
    f = open(file_name)
    reader = csv.reader(f, delimiter=';')
    count = 0
    for i in reader:
        if (count < restr):
            count += 1
            array_file.append(i)
    return array_file


def open_file_users(file_name):
    array_file = []
    f = open(file_name)
    reader = csv.reader(f, delimiter=';')
    for i in reader:
        array_file.append(i)
    return array_file


def wich_users(array_rating):
    users = []
    for i in array_rating:
        users.append(i[0])
    return list(set(users))


def rating_dict_create(array_rating):
    dict_rate = {}

    for i in array_rating:
        if (int(i[2]) != 0):
            try:
                dict_rate[i[0]].update({i[1]: int(i[2])})
            except:
                dict_rate[i[0]] = {i[1]: int(i[2])}

    return dict_rate


def predict_user_based(user_id, book_id, dict_rate, average_rate, array_users_all, array_users_all_dict):
    predict_answer = 0

    sum_up = 0
    sum_down = 0

    new_dict = dict_rate.copy()
    del new_dict[user_id]

    for i in new_dict.keys():
        try:
            s = dict_rate[i][book_id]
        except:
            # если пользователь не оценивал эту книгу то передаём 0
            sum_up += 0
            sum_down += 0
            continue

        sum_up += get_similarity(user_id, i, array_users_all_dict) * (dict_rate[i][book_id] - average_rate[i])
        sum_down += get_similarity(user_id, i, array_users_all_dict)

    if (sum_down != 0):
        predict_answer += (average_rate[user_id] + sum_up / sum_down)
    else:
        predict_answer += average_rate[user_id]

    return predict_answer


def get_similarity(array_id_1, array_id_2, array_users_all_dict):
    sim = euclidean_dist(array_users_all_dict[array_id_1], array_users_all_dict[array_id_2])
    return sim


def user_based(array_users_all, dict_rate):
    array_users_all_dict = {}

    users_array = dict_rate.keys()

    for i in array_users_all:
        if (i[0] in users_array):
            i_place = i[1].replace(",", "")
            i_place_split = i_place.split(" ")

            if (len(i_place_split) == 1):
                city = i_place_split
                state = ""
                country = ""
            elif (len(i_place_split) == 2):
                city = i_place_split[0]
                state = i_place_split[1]
                country = ""
            else:
                city = i_place_split[0]
                state = i_place_split[1]
                country = i_place_split[2]

            try:
                array_users_all_dict[i[0]] = [len(city), len(state), len(country), int(i[2])]
            except:
                array_users_all_dict[i[0]] = [len(city), len(state), len(country), 0]

    predict_array = []
    actual_array = []

    average_rate = {}

    # массив со средним оценок каждого пользователя
    for i in users_array:
        array_rate = dict_rate[i].values()
        average_rate[i] = sum(array_rate) / float(len(array_rate))

    # по юзерам
    for i in dict_rate:
        inner_dict = dict_rate[i]
        # по книгам для кажого пользователя
        for j in inner_dict:
            asses = inner_dict[j]
            actual_array.append(asses)
            predict_answer = predict_user_based(i, j, dict_rate, average_rate, array_users_all, array_users_all_dict)
            if (predict_answer < 0):
                predict_answer = 0
            if (predict_answer > 10):
                predict_answer = 10
            predict_array.append(predict_answer)

    return predict_array, actual_array


def pearsonr_func(x_array, y_array):
    pass


def euclidean_dist(x_array, y_array):
    sum = 0
    for i in xrange(len(x_array)):
        sum += (x_array[i] - y_array[i]) ** 2
    return math.sqrt(sum)


array_rating = []
array_books = []
array_users = []

array_rating = open_file_users_small("BX-Book-Ratings.csv")

array_users_all = open_file_users("BX-Users.csv")

array_users = wich_users(array_rating)

dict_rate = rating_dict_create(array_rating)

array_users_real = dict_rate.keys()

# кластеризуем по 4 параметрам

predict_array, actual_array = user_based(array_users_all, dict_rate)

rmsd = metrics.root_mean_square_deviation(predict_array, actual_array)
mae = metrics.mean_absulutle_error(predict_array, actual_array)

print rmsd
print mae
