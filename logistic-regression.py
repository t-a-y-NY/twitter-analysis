import csv
from nltk.corpus import sentiwordnet as swn

class PolSent():
    def __init__(self, polarity, sentiment):
        self.polarity = polarity
        self.sentiment = sentiment

def search_swn(word):
    try:
        sum_positive = (swn.senti_synset(word + ".a.01")).pos_score() # + (swn.senti_synset(word + ".n.01")).pos_score()
        sum_negative = (swn.senti_synset(word + ".a.01")).neg_score() + (swn.senti_synset(word + ".n.01")).neg_score()

        if sum_positive > sum_negative:
            return 4
        elif sum_positive < sum_negative:
            return 0
        return None
    except:
        return None

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

def sample():
    csv_file = open("first-3-thousand-and-last-3-thousand.csv")
    csv_rows = csv.reader(csv_file)

    i = 0

    list = []
    for row in csv_rows:
        sentiment = row[0]
        tweet = row[5]

        my_guess = measure_sentiment(tweet)

        entry = PolSent(float(sentiment), my_guess)
        list.append(entry)

        print(i)
        i += 1
    return list

# def maximum_likelihood(list):
#     b_zero = 100000
#     b_one = 1
#
#     record_closeness = 100000000
#     while b_one <= 1000:
#         closeness_sum = 0
#         for polsent in list:
#             if polsent.polarity == 4:
#                 closeness_sum += abs(1-(b_zero + b_one*polsent.sentiment))
#         if closeness_sum/len(list) < record_closeness:
#             best_b_one = b_one
#         b_one += 1
#     print(best_b_one)

# def maximum_likelihood(list):
#     b0 = 1
#     b1 = 1
#     best_pos_closeness = 100000000
#     best_b0 = -1000
#     best_b1 = 1
#
#     while b0 <= 10:
#         b1 = 1
#         while b1 <= 1000:
#             for polsent in list:
#                 if abs(1-(b0+b1*polsent.sentiment)) < best_pos_closeness:
#                     best_b0 = b0
#                     best_b1 = b1
#                     best_pos_closeness = abs(1-(b0+b1*polsent.sentiment))
#             b1 += 1
#         b0 += 1
#     print(best_b0, best_b1)

def maximum_likelihood(list):
    best_closeness = 1000
    b0 = -395

    for b1 in range(70, 400, 1):
        for polsent in list:
            if abs(1-(b0+b1*polsent.sentiment)) < best_closeness:
                best_closeness = abs(1-(b0+b1*polsent.sentiment))
                print("New best b0 and b1:", b0, b1)

    b0 = -395
    b1 = 99

def equation(sentiment):
    determinant = -395+99*sentiment
    return (2.71828**determinant)/(1+2.71828**determinant)

def main():
    list = sample()

    # with open("logistic-regression.csv", 'w') as write_file:
    #     for x in list:
    #         w_row = str(x.sentiment) + ',' + str(equation(x.sentiment))
    #
    #         write_file.write(w_row)
    #         write_file.write('\n')

    successes = 0
    count = 0
    for x in list:
        if x.sentiment > 2:
            print(x.sentiment)
            guess = equation(x.sentiment)
            if guess < .001:
                guess = 0
            if guess != 0 and x.polarity != 0:
                successes += 1
            count += 1
    print(successes)
    print(count)

    print("Made it to the end.")
main()