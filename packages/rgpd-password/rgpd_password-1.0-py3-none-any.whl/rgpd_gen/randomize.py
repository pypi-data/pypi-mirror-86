from random import randint, sample


def generate_rgpd_password():
    letters = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ"
    specials = "*/^~²#@àéèù%ç&-'_"
    passwd = ""
    for k in range(0, 10):
        passwd += letters[randint(0, len(letters) - 1)]
    for i in range(0, 5):
        passwd += specials[randint(0, len(specials) - 1)]
    for j in range(0, 3):
        passwd += str(randint(0, 9))
        
    return ''.join(sample(passwd,len(passwd)))