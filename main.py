# step 1: Take a string (the tweet), and iterate through it, looking for words in any of the three lists given

'''

twitter dataset taken from:

https://www.kaggle.com/kazanova/sentiment140/data

'''

import csv
from nltk.corpus import sentiwordnet as swn


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
        return 2
    else:
        raw_sentiment = sum/num_buzz_words
        return round_sentiment(raw_sentiment)

    # sum = 0
    # if ( != None):
    #     sum += search_list(find_words(tweet))

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


    # breakdown = swn.senti_synset("worthless.a.01")
    # print(breakdown.neg_score())

def search_list(word):
    with open("positive-words.txt") as positive_words:
        for line in positive_words:
            line_word = line[0:len(line)-1]
            if word == line_word:
                return 4
    with open("negative-words.txt") as negative_words:
        for line in negative_words:
            line_word = line[0:len(line)-1]
            if word == line_word:
                return 0
    return None

# def search_list(word, positive_words, negative_words):
#     i = 1
#     for line in positive_words:
#         line_word = line[0:len(line)-1]
#         if (i <= 6):
#             i += 1
#         elif line_word == word:
#             return 4
#
#     j = 1
#     for line in negative_words:
#         line_word = line[0:len(line)-1]
#         if (i <= 6):
#             i += 1
#         elif line_word == word:
#             return 0
#
#     return None
#
#     # if word in positive_words:
#     #     return 4
#     # elif word in negative_words:
#     #     return 0
#     # else:
#     #     return None

# FOLLOWING FUNCTION VERIFIED WORKS. Returns a list of words from any given tweet
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


def grab_csv_rows():
    csv_file = open("first-thousand.csv")
    csv_file_rows = csv.reader(csv_file)

    for row in csv_file_rows:
        sentiments_list = row[0]
        tweets_list = row[5]

def test():
    csv_file = open("first-3-thousand-and-last-3-thousand.csv")
    csv_rows = csv.reader(csv_file)

    num_correct = 0
    i = 0
    for row in csv_rows:
        sentiment = row[0]
        tweet = row[5]

        my_guess = measure_sentiment(tweet)


        if my_guess == int(sentiment):
            num_correct += 1
        print(i)
        i += 1
    print(num_correct)


    # for x in range(0, 1000):
    #     print(tweets_list[x])
    #     # my_guess = measure_sentiment(tweets_list[x], positive_words, negative_words)
    #     # print(my_guess, sentiments_list[x])


def main():
    example_tweet = "a+ "
    positive_words = open("positive-words.txt", 'r')
    negative_words = open("negative-words.txt", 'r')

    # positive_file = open("positive-words.txt", 'r')
    # for line in file:
    #     print(line, end='\0')

    print(measure_sentiment(example_tweet))

    grab_csv_rows()

    # test(positive_words, negative_words)

    # print("Sentiment of ", example_tweet, "is ", measure_sentiment(example_tweet))

    print("End of test.")

# main()

def search_list_test():

    print(search_list("not"))


    print(measure_sentiment("@Kwesidei not the whole crew "))



    print("End of test.")

test()

# USE WITH TO CLOSE FILES