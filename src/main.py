import asyncio

from gmail import get_last_email_sender
from telemail import *
from database import Database

def main():
    loop = asyncio.new_event_loop()
    try:
        loop.create_task(main_loop(), name="Main loop")
        loop.create_task(telegram_loop(), name='Telegram loop')
        loop.run_forever()
    finally:
        print("Shut down")
        loop.stop()
        loop.close()

async def main_loop():
    while True:
        db = Database()
        for user in db.users.find():
            last = user["last_mail"]
            now = get_last_email_sender(user["auth_token"])

            if last != now:
                db.update_last_mail(user["chat_id"], now)
                await send_message(user["chat_id"], now)
        db.close()
        await asyncio.sleep(5)



if __name__ == "__main__":
    main()
