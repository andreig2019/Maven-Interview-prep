from random import *
import numpy as np
from time import sleep


avgprice, trades, pnl, pos = 0, 0, 0, 0

def buy(x, bid):
    global pnl, pos, avgprice
    pnl += x - bid
    pos += 1
    if pos:
        avgprice = ((pos-1) * avgprice + bid)/pos
    else:
        avgprice = 0
    return 'sell'


def sell(x, ask):
    global pnl, pos, avgprice
    pnl += ask - x
    pos -= 1
    if pos:
        avgprice = ((pos+1) * avgprice - ask)/pos
    else:
        avgprice = 0
    return 'buy'

def avmarkets(x, n = 3):
    spread = x * 0.2
    markets = []
    for i in range(n):
        bid = uniform(x - spread, x)
        ask = bid + spread
        markets.append((bid,ask))
    print(markets)
    return markets
    
    

def hedge(x):
    global pnl
    print('Want to hedge?')
    ans = input()
    if ans == 'yes':
        print('Want to trade an available market?')
        markets = avmarkets(x, n = 3)
        ans = input()
        if ans == 'yes':
            print('Choose a market to trade')
            number = int(input())
            print('Buy or sell?')
            ans = input()
            if ans == 'buy':
                buy(x, markets[number][1])
                print('You bought at', markets[number][1])
            else:
                sell(x, markets[number][0])
                print('You sold at', markets[number][0])
                
        print('Want to bet?')
        ans = input()
        if ans == 'yes':
            print('Propose me a bet')
            # bet has three components: b0, b1, b2
            # b0 = -1 or 1 determining the bet
            # ans < b1 or ans > b1
            # b2 = size of bet
            bet = list(map(int,input().strip().split()))[:4]
            pnl += bet[0] * bet[2] * np.sign(x - bet[1])

            
def market(utility):
    print('Make me a market on', utility[0])
    ba  = list(map(int,input().strip().split()))[:2]
    bid, ask = ba[0], ba[1]
    spread = ask - bid
    x = utility[1]
    dec = uniform(0, spread)
    if dec <= x - bid:
        dec = sell(x, ask)
    else:
        dec = buy(x, bid)
    print(dec)
    hedge(x)
    
    
def meanv(v):
    x = sum(v)/len(v)
    utility = [('The mean of v',v), x]
    return utility


def extract(v):
    k = choice(v)
    utility = [('A random element of v',v), k]
    return utility

def dnroll(n):
    k = randint(1, n)
    utility = [('Outcome of a dice roll with',n, 'sides'), k]
    return utility

    
def maximum(n, m):
    v = [randint(1, n) for i in range(n)]
    maximum = max(v)
    utility = [('The maximum of',m,'dice rolls with',n,'sides'), maximum]
    return utility

def suma(v, k):
    s = 0
    vc = v.copy()
    for i in range(k):
        c = choice(vc)
        vc.remove(c)
        s += c
    utility = [("The sum of",k,'random elements from',v), s]
    return utility

v = [1,2,3,4,5,6]

for i in range(1):
    utility = maximum(10, 3)
    market(utility)
    print('Outcome was', utility[1])

print('Current position is', pos,
'Current P&L is', pnl, 'Average price',
avgprice
)