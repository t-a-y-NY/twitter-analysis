from nltk.corpus import sentiwordnet as swn

def launch():
    breakdown = swn.senti_synset("worthless.a.01")
    print(breakdown.neg_score())

    print("Made it to the end.")

launch()