import csv
import random
import math
from nltk.corpus import sentiwordnet as swn

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

def round_sentiment(raw_sentiment):
    if (raw_sentiment <= 1):
        return 0
    elif (raw_sentiment > 1 and raw_sentiment < 3):
        return 2
    elif (raw_sentiment >= 3):
        return 4

def measure_sentiment(tweet):
    list = find_words(tweet)

    sum = 0
    num_buzz_words = 0
    for word in list:
        result = search_swn(word)
        if result is not None:
            sum += result
            num_buzz_words += 1
    if num_buzz_words == 0:
        return 0
    else:
        raw_sentiment = sum/num_buzz_words
        return raw_sentiment

def search_swn(word):
    try:
        sum_positive = (swn.senti_synset(word + ".a.01")).pos_score() # + (swn.senti_synset(word + ".n.01")).pos_score()
        sum_negative = (swn.senti_synset(word + ".a.01")).neg_score() + (swn.senti_synset(word + ".n.01")).neg_score()

        if sum_positive > sum_negative:
            return sum_positive
        elif sum_positive < sum_negative:
            return sum_negative*(-1)
        return 0
    except:
        return 0

def find_words(tweet):
    list = []

    start_pos = 0
    for pos in range(0, len(tweet)):
        if tweet[pos] == ' ':
            list.append(tweet[start_pos:pos])
            start_pos = pos+1
        elif pos == len(tweet)-1:
            list.append(tweet[start_pos:pos+1])
    return list

def write_kmeans():
    with open("first-3-thousand-and-last-3-thousand.csv") as r_file:
        with open("kmeans.csv", "w") as w_file:

            reader = csv.reader(r_file)

            i = 0
            for row in reader:
                sentiment = row[0]
                tweet = row[5]

                w_row = str(measure_sentiment(tweet)) + ',' + sentiment

                w_file.write(w_row)
                w_file.write("\n")

                print(i)
                i += 1

def distance_bw(point_1, point_2):
    x_delta = point_2.x - point_1.x
    y_delta = point_2.y - point_1.y

    return math.sqrt(x_delta**2 + y_delta**2)

# def closest_centr(point, centr_1, centr_2):
#     dist_1 = math.sqrt( (point.x-centr_1.x)**2 - (point.y-centr_1.y)**2 )
#     dist_2 = math.sqrt( (point.x-centr_2.x)**2 - (point.y-centr_2.y)**2 )
#     if dist_1 > dist_2:
#         return dist_2
#     elif dist_1 < dist_2:
#         return dist_1



def point_at(place, read_file):
    i = 0
    for row in csv.reader(read_file):
        if i == place:
            point = Point(float(row[0]), float(row[1]))
            return point
        else:
            i += 1

def recalc_centr(cluster, centr):
    sum_x = 0
    sum_y = 0
    for n in cluster:
        sum_x += n.x
        sum_y += n.y
    return Point(sum_x/len(cluster), sum_y/len(cluster))

def measure_accuracy():
    with open("cluster-1.csv", 'r') as clus_1:
        count_rows = 0
        count_failures = 0
        clus_1_rows = csv.reader(clus_1)
        for row in clus_1_rows:
            if float(row[0]) < -0.1:
                if float(row[0]) < 0 and float(row[1]) > 0:
                    count_failures += 1
            count_rows += 1
        print("Rows:", count_rows, "Failures:", count_failures)

    with open("cluster-2.csv", 'r') as clus_2:
        count_rows = 0
        count_failures = 0
        clus_2_rows = csv.reader(clus_2)
        for row in clus_2_rows:
            if float(row[0]) > 0.1:
                if float(row[0]) > 0 and float(row[1]) == 0:
                    count_failures += 1
            count_rows += 1
        print("Rows:", count_rows, "Failures:", count_failures)

def kmeans():
    with open("kmeans.csv") as read_file:
        rand_1 = random.randint(0, 6000)
        rand_2 = random.randint(0, 6000)
        while rand_2 == rand_1:
            rand_2 = random.randint(0, 6000)
        centr_1 = point_at(rand_1, read_file)
        centr_2 = point_at(rand_2, read_file)

        cluster_1 = []
        cluster_2 = []

        for x in range(20):
            i = 0
            for row in csv.reader(read_file):
                row_point = Point(float(row[0]), float(row[1]))
                if distance_bw(row_point, centr_1) < distance_bw(row_point, centr_2):
                    cluster_1.append(row_point)
                elif distance_bw(row_point, centr_2) < distance_bw(row_point, centr_1):
                    cluster_2.append(row_point)
            centr_1 = recalc_centr(cluster_1, centr_1)
            centr_2 = recalc_centr(cluster_2, centr_2)

    with open("cluster-1-post.csv", 'w') as clus_1:
        for x in cluster_1:
            if x.x < -.1:
                w_row = str(x.x) + ',' + str(x.y)

                clus_1.write(w_row)
                clus_1.write("\n")
    with open("cluster-2-post.csv", 'w') as clus_2:
        for x in cluster_2:
            if x.x > .1:
                w_row = str(x.x) + ',' + str(x.y)

                clus_2.write(w_row)
                clus_2.write("\n")

    print("End.")

measure_accuracy()

'''
this k-means clustering algorithm requires the word sentiment to be continuous
'''