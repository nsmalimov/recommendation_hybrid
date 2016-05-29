# -*- coding: utf-8 -*-
from sklearn import cluster


def make_clast(array_users_all, dict_rate):
    dict_users_clasters = {}

    all_users = dict_rate.keys()

    for i in array_users_all:
        if (i[0] in all_users):
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
                dict_users_clasters[i[0]] = [len(city), len(state), len(country), int(i[2])]
            except:
                dict_users_clasters[i[0]] = [len(city), len(state), len(country), 0]

    X_array = dict_users_clasters.values()

    num_clusters = len(X_array) / 50

    k_means = cluster.KMeans(n_clusters=num_clusters)
    k_means.fit(X_array)
    # номер показывает номер кластера
    clusterized_array = list(k_means.labels_)

    for index, i in enumerate(dict_users_clasters.keys()):
        dict_users_clasters[i] = clusterized_array[index]

    return dict_users_clasters


def make_clast_books(dict_books_all, array_books_real):
    dict_books_clasters = {}

    for i in array_books_real:
        try:
            dict_books_clasters[i] = dict_books_all[i]
        except:
            dict_books_clasters[i] = [1, 1, 1, 1]

    X_array = dict_books_clasters.values()

    num_clusters = len(X_array) / 50

    k_means = cluster.KMeans(n_clusters=num_clusters)
    k_means.fit(X_array)
    # номер показывает номер кластера
    clusterized_array = list(k_means.labels_)

    for index, i in enumerate(dict_books_clasters.keys()):
        dict_books_clasters[i] = clusterized_array[index]

    return dict_books_clasters, num_clusters
