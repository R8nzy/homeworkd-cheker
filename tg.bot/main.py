import telebot
from config import TOKEN, DATABASE
from logic import DB_Manager


bot = telebot.TeleBot(TOKEN)
db = DB_Manager(DATABASE)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        'Привет! Я бот для домашних заданий класса.\n'
        'Здесь хранится один общий список ДЗ на один день.\n\n'
        '/show - посмотреть ДЗ\n'
        '\n'
        '/add Предмет - Задание\n'
        'Пример: /add Математика - №15, №16\n'
        '/clear - очистить весь список перед новым днём\n\n'
        'Чтобы исправить ДЗ, добавь его ещё раз с тем же названием предмета.'
    )


@bot.message_handler(commands=['add'])
def add_task(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or '-' not in parts[1]:
        bot.reply_to(message, 'Напиши так: /add Математика - №15, №16')
        return

    subject, task = parts[1].split('-', 1)
    subject = subject.strip()
    task = task.strip()

    if not subject or not task:
        bot.reply_to(message, 'Нужно указать и предмет, и задание.')
        return

    if len(subject) > 100 or len(task) > 1500:
        bot.reply_to(message, 'Слишком длинный текст. Предмет — до 100 символов, задание — до 1500.')
        return

    db.add_homework(subject, task)
    bot.reply_to(message, f'ДЗ сохранено!\n{subject}: {task}')


@bot.message_handler(commands=['show'])
def show_tasks(message):
    homework_list = db.get_homework()

    if not homework_list:
        bot.reply_to(message, 'Домашние задания пока не добавлены.')
        return

    bot.reply_to(message, 'Домашнее задание на текущий день:')
    for subject, task in homework_list:
        bot.send_message(message.chat.id, f'{subject}: {task}')


@bot.message_handler(commands=['clear'])
def clear_tasks(message):
    db.clear_homework()
    bot.reply_to(message, 'Список очищен. Теперь можно добавить ДЗ на новый день.')


if __name__ == '__main__':
    print('Бот запущен и работает...')
    bot.infinity_polling()
