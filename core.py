from random import *
import numpy as np
from time import sleep


avgprice, trades, pnl, pos = 0, 0, 0, 0


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


def avmarkets(x, n=3):
    """
    Given the 'true' value of the market and preferred
    number of markets, show the available markets to trade

    :param x: the true value of the market
    :param n: number of available markets - pre-set to 3

    :return markets: the available markets that other
    participants made - take care of adverse selection!
    """
    spread = x * 0.2
    markets = []
    for i in range(n):
        vb = randint(0, 5)
        va = randint(0, 5)
        bid = uniform(x - spread, x)
        ask = bid + spread
        markets.append((vb, bid, ask, va))
    print(markets)
    return markets


def hedge(x):
    """
    Given the 'true' value of the market, give the trader
    the opportunity to hedge his position by trading
    on available markets or by simply betting

    :param x: the true value of the market
    """
    global pnl
    print('Want to hedge?')
    ans = input()
    if ans == 'yes':
        print('Want to trade an available market?')
        markets = avmarkets(x, n=3)
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


def market(utility):
    """
    Given an utility function to trade on, be a trader!
    Make markets and be prepared to trade against others.

    :param utility: a two-dimensional array comprising of a
    text description of the market you are making and the
    'true' value of the parameter the market is made on

    :prints the decision of other market participants on your
    markets
    """
    print('Make me a market on', utility[0])
    ba = list(map(int, input().strip().split()))[:4]
    vb, bid, ask, va = ba[0], ba[1], ba[2], ba[3]
    spread = ask - bid
    x = utility[1]
    dec = uniform(0, spread)
    if dec <= x - bid:
        vol = randint(1, va)
        dec = sell(x, ask, vol)
    else:
        vol = randint(1, vb)
        dec = buy(x, bid, vol)
    print(dec, vol)
    hedge(x)


def meanv(v):
    x = sum(v) / len(v)
    utility = [('The mean of v', v), x]
    return utility


def extract(v):
    k = choice(v)
    utility = [('A random element of v', v), k]
    return utility


def dnroll(n):
    k = randint(1, n)
    utility = [('Outcome of a dice roll with', n, 'sides'), k]
    return utility


def maximum(n, m):
    v = [randint(1, n) for i in range(n)]
    maximum = max(v)
    utility = [('The maximum of', m, 'dice rolls with', n, 'sides'), maximum]
    return utility


def suma(v, k):
    s = 0
    vc = v.copy()
    for i in range(k):
        c = choice(vc)
        vc.remove(c)
        s += c
    utility = [("The sum of", k, 'random elements from', v), s]
    return utility


v = [1, 2, 3, 4, 5, 6]

for i in range(1):
    utility = maximum(10, 3)
    market(utility)
    print('Outcome was', utility[1])

print('Current position is', pos,
      'Current P&L is', pnl, 'Average price',
      avgprice
      )
