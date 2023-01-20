import random

from .config import *
from . import stg, texts


@bot.message_handler(commands=['start'])
def start_msg(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        stg.start_msg(chat_id)

    elif message.chat.type != "private":
        pass



@bot.message_handler(commands=['admin'])
def admin_command(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        if database.staff(chat_id) in ["admin", 'designer', 'tester']:
            #stg.admin_panel(chat_id)
            pass



@bot.message_handler(content_types=['text'])
def text_message_global(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        stage = stages(chat_id)

        if stage == "send_money":
            try:
                summ = int(message.text.replace("$", "").replace(" ", ""))
                if float(balance(chat_id)) >= summ:
                    k = kmarkup()
                    msg = texts.send_money_address_msg
                    k.row(back("home"))
                    send(chat_id, msg, reply_markup=k)
                    stages(chat_id, f"send_money_address||{str(summ)}")
                else:
                    send(chat_id, texts.error_big_num_msg, reply_markup=kmarkup().row(back("home")))
            except ValueError:
                send(chat_id, texts.error_only_num_msg, reply_markup=kmarkup().row(back("home")))
        elif stage.split("||")[0] == "send_money_address":
            user_id = system_wallet_address_input(message)
            if user_id != False:
                summ = stage.split("||")[1]
                my_balance = balance(chat_id)

                balance(chat_id, my_balance - round(float(summ), 2))

                user_balance = balance(int(user_id))
                summ = float(summ) / 100 * 95
                admins_summ = float(summ) / 100 * 5
                balance('admin', str(admins_summ))
                balance(user_id, user_balance + round(summ, 2))

                msg = texts.money_sended_msg
                send(chat_id, msg)
                stages(chat_id, "None")

            else:
                send(chat_id, texts.error_only_wallet_msg, reply_markup=kmarkup().row(back("send_money")))
        elif stage == "withrow":
            try:
                if float(message.text) <= balance(chat_id):
                    k = kmarkup()
                    msg = texts.value_to_withrow_msg
                    k.row(back("withrow"))
                    send(chat_id, msg, reply_markup=k)
                    stages(chat_id, f"withrow_address||{str(message.text)}")
            except ValueError:
                send(chat_id, texts.error_only_num_msg, reply_markup=kmarkup().row(back("home")))
        elif stage.split("||")[0] == "withrow_address":
            amount = stage.split("||")[1]
            wallet = message.text
            my_address = Wallet(settings("global_wif")).get_address()
            balance(chat_id, balance(chat_id) - int(amount))
            tr_id = Wallet(settings("global_wif")).send(address=wallet, mount=float(amount), currency="usd", leftover=my_address)
            send(chat_id, texts.money_withrow_sended_msg.format(**{"tr_id": tr_id}), reply_markup=kmarkup().row(back("home")))
            stages(chat_id, "None")

@bot.callback_query_handler(func=lambda m: True)
def global_calls(call):
    chat_id = call.message.chat.id

    def dm():
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass

    if call.message.chat.type == "private":
        if call.data == "home":
            stages(chat_id, "None")
            start_msg(call.message)
            dm()
        elif call.data == "send_money":
            stages(chat_id, "None")
            stg.send_money(chat_id)
            dm()
        elif call.data == "add_money":
            stages(chat_id, "None")
            if len(Wallet(user_id=chat_id).get_unspents()) != 0:
                new_wif = Wallet().get_wif()
                WifUser(user_id=chat_id).set("wif", str(new_wif))
            stg.add_money(chat_id)
            dm()
        elif call.data == "withrow":
            stg.withrow(chat_id)
            dm()
        elif call.data == "change_wallet_id":
            bot.answer_callback_query(call.id, texts.message_id_changed_msg, show_alert=True)
            stg.change_wallet_id(chat_id)
            dm()


    elif call.message.chat.type != "private":
        pass




@detected_payment(sleep_before_check=10)
def payment_detected(tr_data, wallet_data: Wallet):
    user_id = int(tr_data[0])
    balance_to_add = float(wallet_data.get_balance("usd"))

    new_wif = Wallet().get_wif()

    balance(user_id, balance(user_id) + balance_to_add)

    PayedWifs(wallet_data.get_wif()).set(user_id, int(round(float(wallet_data.get_balance("usd")))))

    WifUser(user_id=user_id).set("wif", str(new_wif))

    send(user_id, texts.payment_done_msg)


def start():
    while True:
        try:
            bot.polling()
        except:
            pass
