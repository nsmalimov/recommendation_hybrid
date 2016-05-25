# -*- coding: utf-8 -*-
import csv
import clastering
import metrics
import time

def open_file_users_small(file_name):
    array_file =[]
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
    array_file =[]
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
                dict_rate[i[0]].update({i[1]:int(i[2])})
            except:
                dict_rate[i[0]] = {i[1]:int(i[2])}

    return dict_rate

def use_clastering(array_users_all, dict_rate):
    dict_users_clasters = clastering.make_clast(array_users_all, dict_rate)

    predict_array = []
    actual_array = []

    for i in dict_rate:
        inner_dict = dict_rate[i]
        for j in inner_dict:
            assess = inner_dict[j]
            actual_array.append(assess)
            cluster = dict_users_clasters[i]
            books_id = j

            array_assess = []

            for i in dict_users_clasters:
                if (dict_users_clasters[i] == cluster):
                    inner_dict_new = dict_rate[i]
                    if (books_id in inner_dict_new.keys()):
                        array_assess.append(inner_dict_new[books_id])

            if (len(array_assess) != 0):
                predict_array.append(sum(array_assess) / float(len(array_assess)))
            else:
                predict_array.append(0)

    return predict_array, actual_array

def main():
    start = time.time()

    array_rating = []
    array_books = []
    array_users = []

    array_rating = open_file_users_small("BX-Book-Ratings.csv")

    array_users_all = open_file_users("BX-Users.csv")

    print array_users_all

    array_users = wich_users(array_rating)

    dict_rate = rating_dict_create(array_rating)

    #кластеризуем по 4 параметрам
    predict_array, actual_array = use_clastering(array_users_all, dict_rate)

    rmsd = metrics.root_mean_square_deviation(predict_array, actual_array)
    mae = metrics.mean_absulutle_error(predict_array, actual_array)

    print rmsd
    print mae

    finish = time.time()
    t = finish - start

    print t

main()
