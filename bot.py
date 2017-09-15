import datetime
from credentials import api_token
import telebot
from pathlib import Path

journal_dir = Path('~/Dropbox/journal/').expanduser()

bot = telebot.TeleBot(api_token)


@bot.message_handler(func=lambda msg: True)
def receive_all(message):
    if message.content_type == 'text':
        append_to_journal(current_journal_file_name(), message.text)
        bot.reply_to(message, f'Added message to {current_journal_file_name()}')


def current_journal_file_name():
    date = datetime.date.today()
    while not (journal_dir / date.strftime("%Y%m%d")).exists():
        date -= datetime.timedelta(days=1)
        if date.year < 2000:
            raise RuntimeError('No current journal entry found')
    return journal_dir / date.strftime("%Y%m%d")


def append_to_journal(filename, text):
    with open(filename, 'a') as entry:
        entry.write("\n** ")
        headline, *body = text.splitlines()
        entry.write(headline)
        entry.write("\n")
        for line in body:
            entry.write(line)
            entry.write("\n")


if __name__ == "__main__":
    bot.polling()
