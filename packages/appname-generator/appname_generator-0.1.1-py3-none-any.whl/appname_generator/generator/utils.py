CONSONANTS = "BCDFGHJKLMNPQRSTVWXZ"


def max_siblings_vowels(word, n):
        counter = 0
        for l in word:
            if l not in CONSONANTS:
                counter += 1
            else:
                counter = 0
            if counter > n:
                return False
        return True


def max_siblings_consonants(word, n):
    counter = 0
    for l in word:
        if l in CONSONANTS:
            counter += 1
        else:
            counter = 0
        if counter > n:
            return False
    return True