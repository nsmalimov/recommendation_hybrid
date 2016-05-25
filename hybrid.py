# -*- coding: utf-8 -*-

import copy
import time

from sklearn import linear_model

import claster_based
import item_based
import metrics


def get_metrics(w1, w2):
    main_predict_array = []

    for index, i in enumerate(predict_array_1):
        if (predict_array_2[index] == 0):
            main_predict_array.append(predict_array_1[index])
        elif (predict_array_1[index] == 0):
            main_predict_array.append(predict_array_2[index])
        else:
            d = w1 * predict_array_1[index] + w2 * predict_array_2[index]
            main_predict_array.append(d)

    rmsd = metrics.root_mean_square_deviation(main_predict_array, actual_array_2)
    mae = metrics.mean_absulutle_error(main_predict_array, actual_array_2)

    print rmsd
    print mae


array_rating = item_based.open_file_users_small("BX-Book-Ratings.csv")

array_users_all = item_based.open_file_users("BX-Users.csv")

array_books = item_based.wich_books(array_rating)

array_users = item_based.wich_users(array_rating)

dict_rate = item_based.rating_dict_create(array_rating)

dict_books_all = item_based.open_file_books("BX-Books.csv")

array_books_real = item_based.wich_books_new(dict_rate)

print len(array_books)
print len(array_users)

print len(dict_rate)
print len(array_books_real)

start = time.time()

# actual_array_1 = actual_array_2
predict_array_1, actual_array_1 = item_based.item_based(array_users_all, dict_rate, array_books, dict_books_all,
                                                        array_books_real)
print len(predict_array_1)

predict_array_2, actual_array_2 = claster_based.use_clastering(array_users_all, dict_rate)
print len(predict_array_2)

# получаем коэффициенты гибридного подхода

X_train = []

for i in xrange(len(predict_array_1)):
    X_train.append([])

# перекрываем (если один не смог предсказать, заменяем другим)
for index, i in enumerate(predict_array_1):
    if (predict_array_1[index] == 0):
        X_train[index].append(predict_array_2[index])
    else:
        X_train[index].append(predict_array_1[index])

    if (predict_array_2[index] == 0):
        X_train[index].append(predict_array_1[index])
    else:
        X_train[index].append(predict_array_2[index])

regr = linear_model.LinearRegression()

# коэффициенты (веса)
regr.fit(X_train, actual_array_1)

coef = regr.coef_

w_1 = coef[0]
w_2 = coef[1]

main_predict_array = []

# на этих коэффициентах заново предскажем значения
for index, i in enumerate(predict_array_1):
    if (predict_array_2[index] == 0):
        main_predict_array.append(predict_array_1[index])
    elif (predict_array_1[index] == 0):
        main_predict_array.append(predict_array_2[index])
    else:
        d = w_1 * predict_array_1[index] + w_2 * predict_array_2[index]
        main_predict_array.append(copy.deepcopy(d))

    print main_predict_array[index]

rmsd = metrics.root_mean_square_deviation(main_predict_array, actual_array_1)
print rmsd

mae = metrics.mean_absulutle_error(main_predict_array, actual_array_1)
print mae

finish = time.time()

t = finish - start
print t
