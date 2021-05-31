import sys
import sqlite3
from sqlite3.dbapi2 import Cursor
from typing import Dict
from telegram import update, message, user
import telegram
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters


def main():
    global cursor
    cursor = create_database_connection()

    global triggers
    triggers = get_triggers(cursor)

    token = sys.argv[1:]
    init_telegram_connection(token)


def init_telegram_connection(token: str):
    updater = Updater(token)
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, handle_message))
    updater.start_polling()
    updater.idle()


def handle_message(update: telegram.Update, context: CallbackContext) -> None:
    print(f'Message in {update.message.chat.title}')

    trigger_id = search_trigger_in_message(triggers, update.message.text)

    if trigger_id is None:
        return

    answer = get_random_answer_by_searchstring(cursor, trigger_id)
    update.message.reply_text(answer)


def create_database_connection() -> Cursor:
    connection = sqlite3.connect('text.sqlite', check_same_thread=False)
    _cursor = connection.cursor()

    return _cursor


def search_trigger_in_message(triggers: Dict, message: str) -> any:
    for trigger in triggers:
        if trigger[1] in message.lower():
            return trigger[0]

    return None


def get_random_answer_by_searchstring(_cursor: Cursor, trigger_id: int) -> str:
    result = _cursor.execute("""SELECT
                                answer
                            FROM Triggers
                            JOIN Answers
                                ON (Answers.trigger_id=Triggers.id)
                            WHERE
                                trigger_id = :id
                            ORDER BY random() limit 1
                                """, {'id': trigger_id})
    return result.fetchone()[0]


def get_triggers(_cursor: Cursor) -> Dict:
    return _cursor.execute('SELECT id, searchstring FROM Triggers').fetchall()


if __name__ == "__main__":
    main()
