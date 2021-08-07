"""
DOCSTRING:

Crypto Notifier V1

This program in its first iteration will store information for a single coin and send an email if a desired buy/sell
price has been reached. if it has, once it sends the email, it will terminate the program.

==============================================================================================

In the next version, this information will be stored externally for multiple coins, and will simply be imported every
time the file is re-run. The program will also run constantly, and be more of a script that runs on a separate device.

There will be the opportunity to add other coins, alongside a simple GUI being present to easily interact.

Ideally, email replies will be available, and these will be part of V2-3.

A follow-up program might involve automated trading of coins given certain metrics, instantaneous rate of change
in coin price, etc.

Created by Zaheer MacDonald.
"""

from typing import List, Union, Any, Optional
from pycoingecko import CoinGeckoAPI
import time
import yagmail
from login_info import pw, to_mail, from_mail
DEFAULT_CURR = 'cad'
cg = CoinGeckoAPI()


class Coin:
    """
    The data structure used to store data about cryptocurrencies
    of interest.

    === Preconditions ===
    - name: will only contain lowercase values.
    - buy_or_sell = will be one of the two, represented
    in lowercase.
    - currency: must be represented as an understood abbreviation
    (e.g. cad) in lowercase.

    """

    name: str
    buy_or_sell = str
    curr_amount: float
    order_price: float
    buy: bool
    sell: bool
    currency: str

    def __init__(self, name, buy_or_sell, future_order, curr_amount = 0.0):
        self.curr_amount = curr_amount
        self.currency = DEFAULT_CURR
        self.name = name
        self.buy_or_sell = buy_or_sell
        if buy_or_sell == 'buy':
            self.buy = True
            self.sell = False
            self.order_price = future_order
        else:
            self.buy = False
            self.sell = True
            self.order_price = future_order

    def attempt_order(self) -> True:
        if self.sell is True:
            return self._attempt_sell()
        elif self.buy is True:
            return self._attempt_buy()

    def get_curr_price(self) -> float:
        price_dict = cg.get_price(ids=f'{self.name}', vs_currencies=f'{self.currency}')
        curr_price = price_dict[self.name][self.currency]
        return curr_price

    def _attempt_buy(self) -> True:
        if self.get_curr_price() <= self.order_price:
            return True
        else:
            return False

    def _attempt_sell(self) -> True:
        if self.get_curr_price() >= self.order_price:
            return True
        else:
            return False


class CoinPurse:
    """
    The purse should store coins. You should be able to add coins without difficulty, etc.

    Importantly, there should be a way to update every coin in the purse if the market reaches the buy/sell price.
    This information should be updated according to a set schedule, which will be timed in some sort of run function.


    These coins should potentially be imported from a CSV or text file, and maybe updated information should be stored
    in one of those files. This is to account for problems that would emerge if the program were stopped due to power
    issues or something of the sort.


    Alternatively,
    """
    coin_list: List


def mail_with_yag(coin: Coin) -> str:
    """
    Sends an email with the coin's contents via the yagmail library.
    """
    receiver = to_mail
    msg = f"""\
            Crypto order for Coin {coin.name} to be filled.

            Order type: {coin.buy_or_sell}

            This email is being sent to inform you that your coin has 
            reached or exceeded the desired {coin.buy_or_sell} price of {coin.order_price},
            and that you should fill your order as soon as possible if you wish to
            {coin.buy_or_sell} it at this price.

            This message has been sent automatically.
            """
    yag = yagmail.SMTP(from_mail, pw)
    yag.send(to=receiver, subject='action required: coin order ready', contents=msg)
    return 'message sent'


def main(coin):
    keep_going = True
    while keep_going:
        print(coin.get_curr_price())
        if coin.attempt_order():
            print(mail_with_yag(coin))
            keep_going = False
        print('nothing yet, will check back in 30 minutes.')
        time.sleep(60*30)


if __name__ == '__main__':
    btc = Coin('bitcoin', 'sell', 55000.0, 0.002)
    main(btc)




