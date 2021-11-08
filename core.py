from random import *
import numpy as np
from time import sleep
from math import *

avgprice, trades, pnl, pos = 0, 0, 0, 0
f = 0


def var(results):
    """
    Given a sample of experimental results,
    compute the variance in the sample

    :param results: the sample of outcomes

    :return var: the variance in the sample
    """
    m = sum(results) / len(results)
    var = sqrt(sum((xi - m) ** 2 for xi in results) / len(results))
    return var


def buy(x, bid, vol):
    """
    Given the 'true' value of the market and the bid price,
    execute a sell order for another participant

    :param x: the true value of the market
    :param bid: the bid price - can be that of yourself or
    that of an opposing market maker
    :param vol: the volume traded

    :return 'sell': the action that another market participant
    takes on your market
    """
    global pnl, pos, avgprice
    pnl += (x - bid) * vol
    pos += vol
    if pos:
        avgprice = ((pos - vol) * avgprice + bid * vol) / pos
    else:
        avgprice = 0
    return 'sell'


def sell(x, ask, vol):
    """
    Given the 'true' value of the market and the ask price,
    execute a buy order

    :param x: the true value of the market
    :param ask: the ask price - can be that of yourself or
    that of an opposing market maker
    :param vol: the volume traded

    :return 'buy': the action that another market participant
    takes on your market
    """
    global pnl, pos, avgprice
    pnl += (ask - x) * vol
    pos -= vol
    if pos:
        avgprice = ((pos + vol) * avgprice - ask * vol) / pos
    else:
        avgprice = 0
    return 'buy'


def avmarkets(x, function, par, n=3, m=3):
    """
    Given the 'true' value, the function
    and corresponding parameters for the traded markets,
    show the available markets to trade

    :param x: the 'true' value of the traded object
    :param function: the utility function traders and interns
    will be making markets on
    :param par: the parameters corresponding to the type of
    function in case

    :return markets: the available markets that other
    participants made - take care of adverse selection!
    (traders are OP in this game)
    """
    spread = x * 0.2
    markets = []
    ut = utility(function, par)
    for i in range(n):
        # trader markets that are centered around
        # the true value of the parameter
        vb = randint(0, 5)
        va = randint(0, 5)
        bid = uniform(x - spread, x)
        ask = bid + spread
        markets.append((vb, bid, ask, va))
    for j in range(m):
        # intern wannabe markets that are centered
        # around some expected value calculation
        va = randint(0, 5)
        vb = randint(0, 5)
        spread = ut[2][1]
        bid = uniform(ut[2][0] - spread, ut[2][0])
        ask = bid + spread
        markets.append((vb, bid, ask, va))
    print(markets)
    return markets


def hedge(function, par, x):
    """
    Given the 'true' value of the market, give the trader
    the opportunity to hedge his position by trading
    on available markets or by simply betting

    :param x: the true value of the market
    :param function: the utility function traders and interns
    will be making markets on
    :param par: the parameters corresponding to the type of
    function in case
    """
    global pnl
    print('Want to hedge?')
    ans = input()
    if ans == 'yes':
        print('Want to trade an available market?')
        markets = avmarkets(x, function, par, n=3, m=3)
        ans = input()
        if ans == 'yes':
            print('Choose a market to trade')
            number = int(input())
            print('Buy or sell?')
            ans = input()
            print('What size ?')
            size = int(input())
            if ans == 'buy':
                buy(x, markets[number][2], size)
                print('You bought', size, 'at', markets[number][2])
            else:
                sell(x, markets[number][1], size)
                print('You sold', size, 'at', markets[number][1])

        print('Want to bet?')
        ans = input()
        if ans == 'yes':
            print('Propose me a bet')
            # bet has three components: b0, b1, b2
            # b0 = -1 or 1 determining the bet
            # ans < b1 or ans > b1
            # b2 = size of bet
            bet = list(map(int, input().strip().split()))[:4]
            pnl += bet[0] * bet[2] * np.sign(x - bet[1])


def market(function, par):
    """
    Given an utility function to trade on, be a trader!
    Make markets and be prepared to trade against others.

    :param function: the utility function traders and interns
    will be making markets on
    :param par: the parameters corresponding to the type of
    function in case

    :prints the decision of other market participants on your
    markets
    """
    print('Make me a market on', end=" ")
    text(function, par)
    ut = utility(function, par)
    ba = list(map(int, input().strip().split()))[:4]
    vb, bid, ask, va = ba[0], ba[1], ba[2], ba[3]
    spread = ask - bid
    x = ut[0]
    dec = uniform(0, spread)
    if dec <= x - bid:
        vol = randint(1, va)
        dec = sell(x, ask, vol)
    else:
        vol = randint(1, vb)
        dec = buy(x, bid, vol)
    print(dec, vol)
    hedge(function, par, x)
    return x


def gameinfo(function, par):
    """
    Given an utility function and the corresponding parameters
    show the relevant info for the trading game i.e mean, variance

    :param function: the utility function
    :param par: the parameters corresponding to the type of
    function in case

    :return mean, var(sample): the mean and variance of an
    hypothetical game
    """

    n = 10
    sample = []
    for i in range(n):
        sample.append(function(par))
    return meanv(sample), var(sample), min(sample), max(sample)


def text(function, par):
    function(par)
    if f == 1:
        print('the mean of the elements in', par)
    elif f == 2:
        print('a random element of', v)
    elif f == 3:
        print('the outcome of a', par, 'sided dice')
    elif f == 4:
        print('the maximum roll of', par[0], par[1], '-sided dice')
    elif f == 5:
        print('the sum of', par[1], 'random elements from', par[0])


def utility(function, par):
    return function(par), par, gameinfo(function, par)


def meanv(v):
    global f
    f = 1
    x = sum(v) / len(v)
    return x


def extract(v):
    global f
    f = 2
    k = choice(v)
    return k


def dnroll(n):
    global f
    f = 3
    k = randint(1, n)
    return k


def maximum(par):
    m = par[0]
    n = par[1]
    global f
    f = 4
    v = [randint(1, n) for i in range(m)]
    maximum = max(v)
    return maximum


def suma(par):
    v = par[0]
    k = par[1]
    global f
    f = 5
    s = 0
    vc = v.copy()
    for i in range(k):
        c = choice(vc)
        vc.remove(c)
        s += c
    return s


v = [1, 2, 3, 4, 5, 6]
print(meanv(v))
for i in range(1):
    k = market(suma, [v, 3])
    print('Outcome was', k)

print('Current position is', pos,
      'Current P&L is', pnl, 'Average price',
      avgprice
      )
