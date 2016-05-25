# -*- coding: utf-8 -*-
import csv
import metrics
import math
import time

def open_file_books(file_name):
    dict_books_all = {}
    f = open(file_name)
    reader = csv.reader(f, delimiter=';')
    for i in reader:
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
            dict_books_all[i[0]] = [len(city), len(state), len(country), int(i[2])]
        except:
            dict_books_all[i[0]] = [len(city), len(state), len(country), 0]

    return dict_books_all

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

def get_similarity(array_id_1, array_id_2, array_users_all_dict):
    sim = euclidean_dist(array_users_all_dict[array_id_1], array_users_all_dict[array_id_2])
    return sim

def predict_item_based(user_id, book_id, dict_rate, average_rate, array_users_all, data_books):
    predict_answer = 0

    sum_up = 0
    sum_down = 0

    new_dict = data_books.copy()
    del new_dict[book_id]

    for i in new_dict.keys():
        try:
            s = dict_rate[user_id][i]
        except:
            #если пользователь не оценивал эту книгу то передаём 0
            sum_up += 0
            sum_down += 0
            continue

        sum_up += get_similarity(i, book_id, data_books) * (dict_rate[user_id][i] - average_rate[i])
        sum_down += get_similarity(i, book_id, data_books)

    if (sum_down != 0):
        predict_answer += (average_rate[book_id] + sum_up/sum_down)
    else:
        predict_answer += average_rate[book_id]
    return predict_answer

def item_based(array_users_all, dict_rate, array_books, dict_books_all, array_books_real):
    predict_array = []
    actual_array = []

    data_books = {}

    for i in array_books_real:
        try:
            data_books[i] = dict_books_all[i]
        except:
            #атрибуты по умолчанию
            #элемент не найден
            data_books[i] = [1, 1, 1, 1]

    average_rate = {}
    for i in data_books:
        average_rate[i] = []

    for i in dict_rate:
        array_dict = dict_rate[i]
        for j in array_dict.keys():
            average_rate[j].append(array_dict[j])

    for i in average_rate:
        #print i
        average_rate[i] = sum(average_rate[i]) / float(len(average_rate[i]))

    predict_answer = 0
    #по юзерам
    count = 0
    for i in dict_rate:
        inner_dict = dict_rate[i]
        #по книгам для кажого пользователя
        for j in inner_dict:

            assess = inner_dict[j]
            actual_array.append(assess)
            predict_answer = predict_item_based(i, j, dict_rate, average_rate, array_users_all, data_books)
            predict_array.append(predict_answer)
        count += 1
    return predict_array, actual_array

def item_based_cold(array_users_all, dict_rate, array_books, dict_books_all, array_books_real, user, book):
    predict_array = []
    actual_array = []

    data_books = {}

    for i in array_books_real:
        try:
            data_books[i] = dict_books_all[i]
        except:
            #атрибуты по умолчанию
            #элемент не найден
            data_books[i] = [1, 1, 1, 1]

    average_rate = {}
    for i in data_books:
        average_rate[i] = []

    for i in dict_rate:
        array_dict = dict_rate[i]
        for j in array_dict.keys():
            average_rate[j].append(array_dict[j])

    for i in average_rate:
        if (len(average_rate[i]) == 0):
            average_rate[i] = 0
        else:
            average_rate[i] = sum(average_rate[i]) / float(len(average_rate[i]))

    predict_answer = 0
    #по юзерам
    predict_answer = predict_item_based(user, book, dict_rate, average_rate, array_users_all, data_books)
    predict_array.append(predict_answer)
    return predict_array, actual_array

def pearsonr_func(x_array, y_array):
    pass

def euclidean_dist(x_array, y_array):
    sum = 0
    for i in xrange(len(x_array)):
        sum += (x_array[i] - y_array[i]) ** 2
    return math.sqrt(sum)

def rating_dict_create(array_rating):
    dict_rate = {}

    for i in array_rating:
        if (int(i[2]) != 0):
            try:
                dict_rate[i[0]].update({i[1]:int(i[2])})
            except:
                dict_rate[i[0]] = {i[1]:int(i[2])}

    return dict_rate

def wich_books(array_rating):
    books = []
    for i in array_rating:
        books.append(i[1])
    return list(set(books))

def wich_users(array_rating):
    users = []
    for i in array_rating:
        users.append(i[0])
    return list(set(users))

def open_file_users(file_name):
    array_file =[]
    f = open(file_name)
    reader = csv.reader(f, delimiter=';')
    for i in reader:
        array_file.append(i)
    return array_file


def wich_books_new(dict_rate):
    books = []
    for i in dict_rate:
        for j in dict_rate[i].keys():
            books.append(j)
    return list(set(books))

def main():
    start = time.time()

    array_rating = []
    array_books = []
    array_users = []

    array_rating = open_file_users_small("BX-Book-Ratings.csv")

    array_users_all = open_file_users("BX-Users.csv")

    array_books = wich_books(array_rating)

    array_users = wich_users(array_rating)

    dict_rate = rating_dict_create(array_rating)

    dict_books_all = open_file_books("BX-Books.csv")

    array_books_real = wich_books_new(dict_rate)

    predict_array, actual_array = item_based(array_users_all, dict_rate, array_books, dict_books_all, array_books_real)

    rmsd = metrics.root_mean_square_deviation(predict_array, actual_array)
    mae = metrics.mean_absulutle_error(predict_array, actual_array)

    print rmsd
    print mae

    finish = time.time()

    t = finish - start
    print t
    
main()
