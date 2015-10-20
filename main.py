import math

import matplotlib.pyplot as plt

import finmath

__author__ = 'gcolasurdo'


def snigma(t):
    """
    here be dragons set the standard deviation as a function of time
    :param t: denotes the time variable as this should be dependent on time only
    :return: a map of time t to variance sigma
    """
    return math.exp(-t/500)


def miyu(t):
    """
    Ok so this will be the u(t) for the mean of my stochastic crap
    :return: The mapping of the stochastic's mean at time t
    """
    return math.sin(t / 180)


a = 100
y = finmath.Stochastic(a, snigma, miyu, 100)

for x in y.XCollection:
    plt.plot(x)

plt.show()

'''
with open("MainResults.csv", 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    wr.writerow(range(a))
    for x in y.XCollection:
        wr.writerow(x)

'''
