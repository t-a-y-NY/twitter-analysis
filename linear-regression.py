import csv
from nltk.corpus import sentiwordnet as swn

class Pair:
    def __init__(self, my_sentiment, pol_tweet_length):
        self.my_sentiment = my_sentiment
        self.pol_tweet_length = pol_tweet_length

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

def main():
    csv_file = open("first-3-thousand-and-last-3-thousand.csv")
    csv_rows = csv.reader(csv_file)

    list = []
    i = 0
    for row in csv_rows:
        sentiment = row[0]
        tweet = row[5]

        my_guess = measure_sentiment(tweet)

        entry = Pair(my_guess, (1+float(sentiment))/len(find_words(tweet)))
        list.append(entry)
    x_sum = 0
    y_sum = 0
    for x in list:
        x_sum += x.my_sentiment
        y_sum += x.pol_tweet_length
    x_mean = x_sum/len(list)
    y_mean = y_sum/len(list)

    sum_1 = 0
    sum_2 = 0
    for n in list:
        sum_1 += (n.my_sentiment-x_mean)*(n.pol_tweet_length-y_mean)
        sum_2 += (n.my_sentiment-x_mean)**2



    ''' 
    r-squared is 1-RSS/TSS
    '''


    print("b1 value is", sum_1/sum_2)
    print("b0 value is", y_mean-(sum_1/sum_2)*x_mean)

    with open("linear-post.csv", 'w') as write_file:
        for x in list:
            row = str(x.my_sentiment) + ',' + str(x.pol_tweet_length)

            write_file.write(row)
            write_file.write('\n')

    print("Made it to the end.")
main()