#!venv/bin/python
from system_bot.config import *
from system_bot.bots import start as bot_system_start


threading.Thread(target=bot_system_start, daemon=True).start()
threading.main_thread()
threading.Thread(target=fake_peoples_num_updater, daemon=True).start()
threading.main_thread()
while True:
    try:
        time.sleep(120)
    except KeyboardInterrupt:
        break
