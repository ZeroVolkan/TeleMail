import pymongo

from setting import get_setting
from pymongo.errors import PyMongoError

class Database:
    def __init__(self) -> None:
        self.setting = get_setting()["database"]

        self.client = pymongo.MongoClient(self.setting['url'])
        self.database = self.client[self.setting['database']]
        self.users = self.database['users']


    def create_user(self, chat_id):
        """Создает нового пользователя в базе данных."""
        if not self.get(chat_id):
            try:
                self.users.insert_one({
                    "chat_id": chat_id,
                    "last_mail": None,
                    "auth_token": None
                })

            except PyMongoError as e:
                print(f"Error creating user {chat_id}: {e}")
        else:
            print(f"User {chat_id} already exists.")

    def del_user(self, chat_id):
        """Удаляет пользователя по chat_id."""
        try:
            self.users.delete_one({"chat_id": chat_id})
        except PyMongoError as e:
            print(f"Error deleting user {chat_id}: {e}")

    def get(self, chat_id):
        """Получает данные пользователя по chat_id."""
        return self.users.find_one({"chat_id": chat_id})


    def change_mail(self, chat_id, email):
        """Добавляет письмо пользователю."""
        try:
            self.users.update_one(
                {"chat_id": chat_id},
                {"$set": {"mail": email}}
            )
        except PyMongoError as e:
            print(f"Error adding mail to user {chat_id}: {e}")


    def update_last_mail(self, chat_id, last_mail):
        """Обновляет последнее письмо пользователя."""
        try:
            self.users.update_one(
                {"chat_id": chat_id},
                {"$set": {"last_mail": last_mail}}
            )

        except PyMongoError as e:
            print(f"Error updating last mail for user {chat_id}: {e}")


    def close(self):
        """Закрывает соединение с базой данных."""
        try:
            self.client.close()
        except PyMongoError as e:
            print(f"Error closing MongoDB connection: {e}")
