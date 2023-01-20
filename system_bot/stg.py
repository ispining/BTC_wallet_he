from .config import *
from . import texts

settings("fake_peoples_num_he", '50')

def start_msg(chat_id):
    """
    Главная страница

    :param chat_id: Ай ди пользователя
    """
    k = kmarkup()
    b = balance(chat_id)
    if len(str(b).split(".")) != 1:
        b = round(b, 2)

    msg = texts.start_msg.format(**{
        "balance": str(b),
        "wallet_id": str(WifUser(user_id=chat_id).get()[2]),
        "fake_peoples_num": str(settings("fake_peoples_num_he"))
    })
    k.row(btn(texts.send_money_btn, callback_data="send_money"))
    k.row(btn(texts.add_money_btn, callback_data="add_money"),
          btn(texts.withrow_btn, callback_data="withrow"))
    k.row(btn(texts.change_wallet_id_btn, callback_data="change_wallet_id"))

    send(chat_id, msg, reply_markup=k)

def add_money(chat_id):
    """
    Меню пополнения баланса

    :param chat_id: Ай ди пользователя
    """
    k = kmarkup()
    msg = texts.add_money_msg.format(**{
        "balance": str(balance(chat_id)),
        "btc_address": str(Wallet(user_id=chat_id).get_address())
    })
    k.row(back("home"))
    send(chat_id, msg, reply_markup=k)

def send_money(chat_id):

    k = kmarkup()
    msg = texts.send_money_amount_msg
    k.row(back("home"))
    send(chat_id, msg, reply_markup=k)
    stages(chat_id, "send_money")

def withrow(chat_id):
    k = kmarkup()
    msg = texts.insert_output_withrow_mount_msg
    k.row(back("home"))
    send(chat_id, msg, reply_markup=k)
    stages(chat_id, "withrow")

def change_wallet_id(chat_id):
    WifUser(user_id=chat_id).set(set_column="wallet_id", set_value=str(random.randint(int("1"*10), int("9"*10))))
    start_msg(chat_id)



def admin_panel(chat_id):
    k = kmarkup()
    b = balance("admin")
    if len(str(b).split(".")) != 1:
        b = round(b, 2)
    msg = texts.admin_panel_msg.format(**{
        "total_admin_balance": str(b),
        "subs_num": str(subs_num())
    })
    k.row(back("home"))
    send(chat_id, msg, reply_markup=k)