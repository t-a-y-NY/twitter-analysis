def search(word):
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
    return 2


def run():
    print(search("not"))

    print("Made it to the end.")

run()