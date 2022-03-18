import json
import telebot
from telebot import types

token = 'There must be telegram bot token'

bot = telebot.TeleBot(token)

f = open('users.json', encoding='utf-8-sig')
users_data = json.load(f)
f.close()

f = open('problems.json', encoding='utf-8-sig')
problems = json.load(f)
f.close()


@bot.message_handler(commands=['start'])
def start_welcome(message):
    global users_data
    global user_data
    for user in users_data:
        if user['id'] == message.chat.id:
            break
    else:
        user_data = {
            'id': message.chat.id,
            'problems': [],
            'active_problem': 0,
            'разное': [0, 0],
            'планиметрия': [0, 0],
            'функционалка': [0, 0],
            'уравнения': [0, 0],
            'неравенства': [0, 0],
            'текстовые задачи': [0, 0],
            'теория чисел': [0, 0],
            'all': [0, 0]
        }
        users_data.append(user_data)
        f = open('users.json', 'w', encoding='utf-8-sig')
        f.write(json.dumps(users_data, ensure_ascii=False))
        f.close()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ask_for_problem_button = types.KeyboardButton(text='Боря, задачу!')
    statistics_button = types.KeyboardButton(text='Статистика')
    choose_button = types.KeyboardButton(text='Выбрать тему')
    keyboard.add(ask_for_problem_button)
    keyboard.add(statistics_button, choose_button)
    bot.send_message(message.chat.id, '''Привет!
    \nЯ Борис из Новосибирска.
    \nМоя цель - помочь тебе стать призёром Всесиба и в 11 классе пройти на заключительный этап минуя отборочный.
    \nЯ, как и все, несовершенен, поэтому пока я не могу проверять твои решения, но зато буду тренировать твои навыки самопроверки и ты научишься находить свои ошибки. Если твой ход мысли будет отличаться от авторского, то ничего страшного, это абсолютно нормально. Конечно, твоё решение необязательно будет правильным, но я работаю над тем, как организовать проверку задач.
    \nКак только ты захочешь порешать - жми на кнопку "Боря, задачу!" и я сразу отправлю тебе задачку. После того, как ты решишь задачу, нажимай на кнопку "Решение" и сравнивай его со своим.
    \nТакже ты можешь посмотреть статистику, она поможет понять, каким темам нужно уделить больше внимания. Если окажется, что какая-то тема действительно хромает, то ты можешь выбрать её для следующей задачи, нажав на кнопку "Выбрать тему"
    ''', reply_markup=keyboard)


@bot.message_handler(func=lambda m: m.text == 'Боря, задачу!')
def give_problem(message):
    global user_data
    f = open('users.json', encoding='utf-8-sig')
    users_data = json.load(f)
    f.close()
    f = open('problems.json', encoding='utf-8-sig')
    problems = json.load(f)
    f.close()
    for user in users_data:
        if user['id'] == message.chat.id:
            users_data.remove(user)
            user_data = user
    if user_data['active_problem'] != 0:
        keyboard = types.InlineKeyboardMarkup()
        solution_button = types.InlineKeyboardButton(text='Посмотреть решение прошлой задачи', callback_data='solution_button')
        keyboard.add(solution_button)
        bot.send_message(message.chat.id, 'Ты ещё не решил прошлую задачу. Я не могу выдать тебе новую', reply_markup=keyboard)
    else:
        for problem in problems:
            if problem['number'] not in user_data['problems']:
                user_data['active_problem'] = problem['number']
                users_data.append(user_data)
                f = open('users.json', 'w', encoding='utf-8-sig')
                f.write(json.dumps(users_data, ensure_ascii=False))
                f.close()
                keyboard = types.InlineKeyboardMarkup()
                solution_button = types.InlineKeyboardButton(text='Посмотреть решение', callback_data='solution_button')
                keyboard.add(solution_button)
                bot.send_photo(message.chat.id, open(problem['problem'], 'rb'), caption=f'''
Источник: {problem['source']}\nТема: {problem['topic']}''', reply_markup=keyboard)
                break
        else:
            bot.send_message(message.chat.id, '''Внезапно, но закончились все задачи. Молодец, ты проделал(-a) огромную работу!\nПопробуй попросить меня дать тебе задачу чуть позже, я переодически загружаю новые задания!''')


@bot.message_handler(func=lambda m: m.text == 'Статистика')
def stat(message):
    global user_data
    f = open('users.json', encoding='utf-8-sig')
    users_data = json.load(f)
    f.close()
    for user in users_data:
        if user['id'] == message.chat.id:
            user_data = user
    if user_data['active_problem'] is True:
        keyboard = types.InlineKeyboardMarkup()
        solution_button = types.InlineKeyboardButton(text='Посмотреть решение прошлой задачи', callback_data='solution_button')
        keyboard.add(solution_button)
        bot.send_message(message.chat.id, 'Ты ещё не решил(-a) задачу. Я не могу показать тебе статистику', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, f'''
Текстовые задачи: {user_data['текстовые задачи'][0]}/{user_data['текстовые задачи'][1]}
Теория чисел: {user_data['теория чисел'][0]}/{user_data['теория чисел'][1]}
Планиметрия: {user_data['планиметрия'][0]}/{user_data['планиметрия'][1]}
Уравнения: {user_data['уравнения'][0]}/{user_data['уравнения'][1]}
Неравенства: {user_data['неравенства'][0]}/{user_data['неравенства'][1]}
Функционалка: {user_data['функционалка'][0]}/{user_data['функционалка'][1]}
Разное: {user_data['разное'][0]}/{user_data['разное'][1]}

Всего: {user_data['all'][0]}/{user_data['all'][1]}
''')


@bot.message_handler(func=lambda m: m.text == 'Выбрать тему')
def choose(message):
    global user_data
    global users_data
    f = open('users.json', encoding='utf-8-sig')
    users_data = json.load(f)
    f.close()
    for user in users_data:
        if user['id'] == message.chat.id:
            user_data = user
    if user_data['active_problem'] is True:
        keyboard = types.InlineKeyboardMarkup()
        solution_button = types.InlineKeyboardButton(text='Посмотреть решение прошлой задачи', callback_data='solution_button')
        keyboard.add(solution_button)
        bot.send_message(message.chat.id, 'Ты ещё не решил(-a) прошлую задачу. Я не могу выдать тебе новую', reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        text_button = types.InlineKeyboardButton(text='Текстовые задачи', callback_data='текствоые задачи')
        tch_button = types.InlineKeyboardButton(text='Теория чисел', callback_data='теория чисел')
        planik_button = types.InlineKeyboardButton(text='Планиметрия', callback_data='планиметрия')
        urav_button = types.InlineKeyboardButton(text='Уравнения', callback_data='уравнения')
        nerav_button = types.InlineKeyboardButton(text='Неравенства', callback_data='неравенства')
        func_button = types.InlineKeyboardButton(text='Функционалка', callback_data='функционалка')
        razn_button = types.InlineKeyboardButton(text='Разное', callback_data='разное')
        keyboard.add(text_button, tch_button)
        keyboard.add(urav_button, nerav_button)
        keyboard.add(planik_button, func_button)
        keyboard.add(razn_button)
        bot.send_message(message.chat.id, 'Выбери тему для следующей задачи', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'solution_button')
def solution(call):
    f = open('problems.json', encoding='utf-8-sig')
    problems = json.load(f)
    f.close()
    for problem in problems:
        if problem['number'] == user_data['active_problem']:
            keyboard = types.InlineKeyboardMarkup()
            good_button = types.InlineKeyboardButton(text='Задача решена', callback_data='good')
            bad_button = types.InlineKeyboardButton(text='Задача не решена', callback_data='bad')
            keyboard.add(good_button)
            keyboard.add(bad_button)
            bot.send_photo(call.message.chat.id, open(problem['solution'], 'rb'), caption='После того как сравнишь своё и авторское решения, отметь всё ли хорошо. Эти данные помогут мне со статистикой.', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'good')
def good(call):
    global user_data
    f = open('users.json', encoding='utf-8-sig')
    users_data = json.load(f)
    f.close()
    f = open('problems.json', encoding='utf-8-sig')
    problems = json.load(f)
    f.close()
    for user in users_data:
        if user['id'] == call.message.chat.id:
            users_data.remove(user)
            user_data = user
    for problem in problems:
        if user_data['active_problem'] == problem['number']:
            user_data[problem['topic']][0] += 1
            user_data[problem['topic']][1] += 1
            user_data['all'][0] += 1
            user_data['all'][1] += 1
            user_data['active_problem'] = 0
            user_data['problems'].append(problem['number'])
            users_data.append(user_data)
            f = open('users.json', 'w', encoding='utf-8-sig')
            f.write(json.dumps(users_data, ensure_ascii=False))
            f.close()
            bot.send_message(call.message.chat.id, 'Спасибо за ответ. Можешь продолжать решать')


@bot.callback_query_handler(func=lambda call: call.data == 'bad')
def bad(call):
    global user_data
    f = open('users.json', encoding='utf-8-sig')
    users_data = json.load(f)
    f.close()
    f = open('problems.json', encoding='utf-8-sig')
    problems = json.load(f)
    f.close()
    for user in users_data:
        if user['id'] == call.message.chat.id:
            users_data.remove(user)
            user_data = user
    for problem in problems:
        if user_data['active_problem'] == problem['number']:
            user_data[problem['topic']][1] += 1
            user_data['all'][1] += 1
            user_data['active_problem'] = 0
            user_data['problems'].append(problem['number'])
            users_data.append(user_data)
            f = open('users.json', 'w', encoding='utf-8-sig')
            f.write(json.dumps(users_data, ensure_ascii=False))
            f.close()
            bot.send_message(call.message.chat.id, 'Спасибо за ответ. Можешь продолжать решать')


@bot.callback_query_handler(func=lambda call: True)
def choose(call):
    global user_data
    f = open('problems.json', encoding='utf-8-sig')
    problems = json.load(f)
    f.close()
    f = open('users.json', encoding='utf-8-sig')
    users_data = json.load(f)
    f.close()
    for user in users_data:
        if user['id'] == call.message.chat.id:
            users_data.remove(user)
            user_data = user
    if user_data['active_problem'] != 0:
        keyboard = types.InlineKeyboardMarkup()
        solution_button = types.InlineKeyboardButton(text='Посмотреть решение прошлой задачи', callback_data='solution_button')
        keyboard.add(solution_button)
        bot.send_message(call.message.chat.id, 'Ты ещё не решил прошлую задачу. Я не могу выдать тебе новую', reply_markup=keyboard)
    else:
        for problem in problems:
            if problem['topic'] == call.data and problem['number'] not in user_data['problems']:
                user_data['active_problem'] = problem['number']
                users_data.append(user_data)
                f = open('users.json', 'w', encoding='utf-8-sig')
                f.write(json.dumps(users_data, ensure_ascii=False))
                f.close()
                keyboard = types.InlineKeyboardMarkup()
                solution_button = types.InlineKeyboardButton(text='Посмотреть решение', callback_data='solution_button')
                keyboard.add(solution_button)
                bot.send_photo(call.message.chat.id, open(problem['problem'], 'rb'), caption=f'''
                Источник: {problem['source']}
                Тема: {problem['topic']}''', reply_markup=keyboard)
                break
        else:
            bot.send_message(call.message.chat.id, 'Внезапно, но закончились все задачи по этой теме. Молодец, ты проделал(-a) огромную работу!\nПопробуй попросить меня дать тебе задачу чуть позже, я переодически загружаю новые задания!')


bot.infinity_polling()
