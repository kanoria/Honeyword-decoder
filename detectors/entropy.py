import math
import numpy


def compute_entropy(password):
    """ Computes the entropy of a password. The entropy is defined by the
    length of the password times the number of possibilities for each character.
    :param password: password to get the entropy
    :return: entropy.
    """

    lowercase = False
    uppercase = False
    number = False
    other = False

    for char in password:
        if char.isdigit():
            number = True
        elif char.islower():
            lowercase = True
        elif char.isupper():
            uppercase = True
        else:
            other = True

    n = 0

    if lowercase:
        n += 26
    if uppercase:
        n += 26
    if number:
        n += 10
    if other:
        n += 32

    return len(password) * math.log(n, 2)


def detect_password(password_list):
    """ Execute detection on an entropy basis. If one password has an entropy
    very different for the others then it may be the real password.
    :param password_list: list of password of which we should detect the real password
    :return: index of the detected password, returns -1 if nothing was found
    """

    scores = numpy.array(map(compute_entropy, password_list))
    maximum = 0
    index = -1

    for i in xrange(len(password_list)):
        temp = numpy.delete(scores, i)
        mu = temp.mean()
        sigma = temp.std()

        if scores[i] < (mu - sigma):
            d_interval = (mu - sigma) - scores[i]
        elif scores[i] > (mu + sigma):
            d_interval = scores[i] - (mu + sigma)
        else:
            d_interval = 0

        if d_interval > maximum:
            maximum = d_interval
            index = i

    return index
