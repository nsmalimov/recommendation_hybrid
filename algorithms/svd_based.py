# -*- coding: utf-8 -*-
import csv
import time

import numpy as np

import metrics


def svd_used(rate_array):
    R = np.array(rate_array)

    U, s, V = np.linalg.svd(R, full_matrices=False)

    slice = 20

    s_sort = np.sort(s)
    s_sort = s_sort[::-1]
    s_less = s_sort[0:slice]
    s_diag = np.diag(s_less)

    U = U.T
    U = U[0:slice]
    U = U.T

    U = np.dot(U, s_diag)

    V = V[0:slice]
    V = V.T

    return U, V


def rating_dict_create(array_rating):
    dict_rate = {}

    for i in array_rating:
        if (int(i[2]) != 0):
            try:
                dict_rate[i[0]].update({i[1]: int(i[2])})
            except:
                dict_rate[i[0]] = {i[1]: int(i[2])}

    return dict_rate


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


def wich_users(array_rating):
    users = []
    for i in array_rating:
        users.append(i[0])
    return list(set(users))


def wich_books(dict_rate):
    books = []
    for i in dict_rate:
        for j in dict_rate[i].keys():
            books.append(j)
    return list(set(books))


def rating_array_create(dict_rate, array_books):
    array_rating = []

    index = 0

    for i in dict_rate.keys():
        array_rating.append([])
        for j in array_books:
            array_rating[index].append(j)
        index += 1

    index = 0

    dict_rating_new = {}

    for i in dict_rate.keys():
        help_array = array_rating[index]
        for index1, j in enumerate(help_array):
            try:
                s = dict_rate[i][j]
                array_rating[index][index1] = s
            except:
                array_rating[index][index1] = 0
        dict_rating_new[i] = array_rating
        index += 1

    return array_rating, dict_rating_new


def predict_svd_based(user_id, item_id, U, V, rate_dict, array_books):
    num_user = rate_dict.keys().index(user_id)
    num_book = array_books.index(item_id)

    predict_answer = np.dot(U[num_user], V[num_book])

    return predict_answer


def svd_based(dict_rate, rate_dict, U, V, array_books):
    predict_array = []
    actual_array = []

    # по юзерам
    for i in dict_rate:
        inner_dict = dict_rate[i]
        # по книгам для кажого пользователя
        for j in inner_dict:
            asses = inner_dict[j]
            actual_array.append(asses)
            predict_answer = predict_svd_based(i, j, U, V, rate_dict, array_books)

            y = round(predict_answer)
            if (y == 0):
                predict_answer = 0
            if (predict_answer > 10):
                predict_answer = 10
            if (predict_answer < 0):
                predict_answer = 0
            predict_array.append(predict_answer)

    return predict_array, actual_array


def get_average_r(dict_rate):
    rate_array = []

    for i in dict_rate:
        inner_dict = dict_rate[i]
        for i in inner_dict:
            rate_array.append(inner_dict[i])

    average_r = sum(rate_array) / float(len(rate_array))

    return average_r


def main():
    start = time.time()

    array_rating = open_file_users_small("BX-Book-Ratings.csv")

    array_users = wich_users(array_rating)

    dict_rate = rating_dict_create(array_rating)

    array_users_real = dict_rate.keys()
    array_books_real = wich_books(dict_rate)

    rate_array, rate_dict = rating_array_create(dict_rate, array_books_real)

    U, V = svd_used(rate_array)

    predict_array, actual_array = svd_based(dict_rate, rate_dict, U, V, array_books_real)

    rmsd = metrics.root_mean_square_deviation(predict_array, actual_array)
    mae = metrics.mean_absulutle_error(predict_array, actual_array)

    print rmsd
    print mae

    finish = time.time()

    t = finish - start
    print t


if __name__ == "__main__":
    main()
