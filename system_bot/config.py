import os
import random
import threading
import time

import bit
import bit.exceptions as bit_ex
import iluxaMod as ilm
import psycopg2
from iluxaMod.tools import pickle

from . import texts

TESTNET = False
if TESTNET:
    print("""[!] TESTNET is turned on!
Remember to set TESTNET variable to negative boolean value after development!""")

database = ilm.postgreSQL_connect(
    user="postgres",
    password="armageddon",
    database="anonym_wallet",
    host="illyashost.ddns.net"
)

database.init_DB(stages=True, sub=True, staff=True, settings=True, balance=True)
db = database.db
sql = database.sql
balance = database.balance
stages = database.stages
staff = database.staff
settings = database.settings

def preDB():
    sql.execute(f"""CREATE TABLE IF NOT EXISTS connections(
    user_id TEXT PRIMARY KEY,
    wif TEXT,
    wallet_id TEXT,
    status TEXT
    )""")
    db.commit()
    sql.execute(f"""CREATE TABLE IF NOT EXISTS payed_wifs(
    wif TEXT PRIMARY KEY,
    user_id TEXT,
    amount TEXT
    )""")
    db.commit()
preDB()

test_wif = "cRMFKC5TKutGJzqSVEMcSPnp44Y5Uq4ynwZ56ATBNFR5HjjdtYVp"

def fake_peoples_num_updater():
    time.sleep(10)
    while True:
        try:
            to_add = random.choice([0, 1, 2])
            settings("fake_peoples_num_he", str(int(settings("fake_peoples_num_he")) + to_add))
            time.sleep(random.randint(30*60, round(60 * 60 * 2)))
        except psycopg2.ProgrammingError:
            pass
        except psycopg2.OperationalError:
            pass
        except ValueError:
            pass







class WifUser:
    def __init__(self, user_id=None):
        database = ilm.postgreSQL_connect(
            user="postgres",
            password="armageddon",
            database="anonym_wallet",
            host="illyashost.ddns.net"
        )

        #database.init_DB(stages=True, sub=True, staff=True, settings=True, balance=True)
        self.db = database.db
        self.sql = database.sql
        self.user_id = user_id
        self.wif = None
        self.wallet_id = None
        self.status = None
        if user_id != None:
            if not self.exists():
                self.wif = Wallet().get_wif()
                self.wallet_id = random.randint(int("1"*10), int("9"*10))
                self.sql.execute(f"SELECT * FROM connections WHERE wallet_id = '{str(self.wallet_id)}'")
                while len(self.sql.fetchall()) > 0:
                    self.wallet_id = random.randint(int("1" * 10), int("9" * 10))
                self.status = "None"

                self.sql.execute(f"INSERT INTO connections VALUES ('{str(self.user_id)}', '{str(self.wif)}', '{str(self.wallet_id)}', '{str(self.status)}')")
                self.db.commit()

    def exists(self):
        self.sql.execute(f"SELECT * FROM connections WHERE user_id = '{str(self.user_id)}'")
        if self.sql.fetchone() is None:
            return False
        else:
            return True

    def remove(self):
        self.sql.execute(f"DELETE FROM connections WHERE user_id = '{str(self.user_id)}'")
        self.db.commit()

    def get(self):
        if self.user_id != None:
            if self.exists():
                self.sql.execute(f"SELECT * FROM connections WHERE user_id = '{str(self.user_id)}'")
                return self.sql.fetchall()[0]
        else:
            self.sql.execute(f"SELECT * FROM connections")
            if self.sql.fetchone() is None:
                pass
            else:
                self.sql.execute(f"SELECT * FROM connections")

                return self.sql.fetchall()

    def set(self, set_column: str, set_value: str):
        sql.execute(f"UPDATE connections SET {set_column} = '{set_value}' WHERE user_id = '{str(self.user_id)}'")
        db.commit()


class netConnect:
    def __init__(self, wif=None, user_id=None):
        if TESTNET:
            from bit import PrivateKeyTestnet as private_key

        else:
            #
            from bit import PrivateKey as private_key

        self.user_id = user_id
        if wif is not None:
            self.key = private_key(wif=wif)
        elif self.user_id != None:
            user_wif = WifUser(user_id=self.user_id).get()[1]
            self.key = private_key(wif=user_wif)
        else:
            self.key = private_key()


class Wallet(netConnect):

    def get_address(self):
        return self.key.segwit_address

    def get_wif(self):
        return self.key.to_wif()

    def get_balance(self, currency="usd"):
        return self.key.get_balance(currency=currency)

    def get_transactions(self):
        return self.key.get_transactions()

    def get_unspents(self):
        return self.key.get_unspents()

    def send(self, address: str, mount: float, currency: str, leftover) -> str:
        try:
            tx_id = self.key.send([(address, int(mount), currency)], leftover=leftover, unspents=self.key.get_unspents())
            return tx_id
        except bit_ex.InsufficientFunds:
            return "Balance is less then mount for send"

    def __str__(self):

        return f"""
[+] PrivateKey: {self.get_wif()}
[+] Address: {self.get_address()}
[+] Balance: {str(self.get_balance())}
[+] Transactions: {str(self.key.get_transactions())}
[+] Unspents: {str(self.key.get_unspents())}"""


class PayedWifs:
    def __init__(self, wif=None):
        database = ilm.postgreSQL_connect(
            user="postgres",
            password="armageddon",
            database="anonym_wallet",
            host="illyashost.ddns.net"
        )

        #database.init_DB(stages=True, sub=True, staff=True, settings=True, balance=True)
        self.db = database.db
        self.sql = database.sql
        self.wif = wif

    def exists(self):
        self.sql.execute(f"SELECT * FROM payed_wifs WHERE wif = '{str(self.wif)}'")
        if self.sql.fetchone() is None:
            return False
        else:
            return True

    def remove(self):
        self.sql.execute(f"DELETE FROM payed_wifs WHERE wif = '{str(self.wif)}'")
        self.db.commit()

    def get(self):
        if self.wif != None:
            self.sql.execute(f"SELECT * FROM payed_wifs WHERE wif = '{str(self.wif)}'")
            if self.sql.fetchone() is None:
                pass
            else:
                self.sql.execute(f"SELECT * FROM payed_wifs WHERE wif = '{str(self.wif)}'")
                for row in self.sql.fetchall():
                    return row
        else:
            self.sql.execute(f"SELECT * FROM payed_wifs")
            return self.sql.fetchall()

    def set(self, user_id, amount):
        if not self.exists():
            self.sql.execute(f"INSERT INTO payed_wifs VALUES ('{str(self.wif)}', '{str(user_id)}', '{str(amount)}')")
            self.db.commit()




def detected_payment(sleep_before_check: int = 10) -> [bit.PrivateKey, bit.PrivateKeyTestnet]:
    def decorator(func):
        def f():
            while True:
                try:
                    lst = WifUser().get()
                    if lst != None:
                        for data in lst:
                            wallet = Wallet(user_id=data[0])
                            if round(float(wallet.get_balance("usd"))) > 0:
                                func(data, wallet)
                    time.sleep(sleep_before_check)
                except psycopg2.ProgrammingError:
                    pass
                except psycopg2.OperationalError:
                    pass

        threading.Thread(target=f, daemon=True).start()
        threading.main_thread()
    return decorator





TOKEN = "5986561125:AAEta-nz8umw_cUv2cfer1VqIB0P144J5NU"
tgbot = ilm.tgBot(token=TOKEN)
kmarkup = tgbot.kmarkup
bot = tgbot.bot
bot.parse_mode = "HTML"
send = tgbot.send
btn = tgbot.btn

def back(callback):
    return tgbot.back(callback_data=callback, bname="חזרה")

def system_wallet_address_input(message):
    value = message.text.replace("$", "").replace(" ", "")
    sql.execute(f"SELECT * FROM connections WHERE wallet_id = '{value}'")
    if sql.fetchone() is None:
        return False
    else:
        sql.execute(f"SELECT * FROM connections WHERE wallet_id = '{value}'")
        return sql.fetchall()[0][0]



