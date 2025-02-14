import telebot  # type: ignore
import datasever as ds
from telebot import types
from token_1 import token, admin_password

# Инициализация бота с токеном
bot = telebot.TeleBot(token)


# Обработчик команды /reg
@bot.message_handler(commands=['reg'])
def registration(message):
    bot.send_message(message.chat.id, "Введите информацию о вас в формате (Фамилия, имя): ")  
    bot.register_next_step_handler(message, reg)


# Обработчик команды /admin_reg
@bot.message_handler(commands=['admin_reg'])
def registration(message):
    bot.send_message(message.chat.id, "Введите информацию о вас в формате (Фамилия, имя , пароль) или 'отмена' если зашли сюда случайно: ")  
    bot.register_next_step_handler(message, reg_admin)

def create_admin_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    info_all = types.KeyboardButton('Информация по всем')
    exit_ = types.KeyboardButton('Назад')
    markup.add(info_all, exit_)
    return markup

# Функция для создания кнопок
def create_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    eat_start_btn = types.KeyboardButton('начать обедать')
    eat_stop_btn = types.KeyboardButton('закончить обедать')
    smoke_start_btn = types.KeyboardButton('начать курить')
    smoke_stop_btn = types.KeyboardButton('закончить курить')
    information_button = types.KeyboardButton('информация')
    admin_button = types.KeyboardButton('Администрирование')
    markup.add(eat_start_btn, eat_stop_btn, smoke_start_btn, smoke_stop_btn,information_button,admin_button)
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = create_buttons()
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите действие:", reply_markup=markup)


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.lower()  # Преобразуем текст в нижний регистр для удобства сравнения
    print(text)
    if text == 'начать курить':
        smoke_start(message)
    elif text == 'закончить курить':
        smoke_stop(message)
    elif text == 'начать обедать':
        eat_start(message)
    elif text == 'закончить обедать':
        eat_stop(message)
    elif text == 'информация':
        information(message)
    elif text == 'администрирование':
        if find_admin_by_chat_id(message.chat.id):
            admin(message)
        else:
            bot.send_message(message.chat.id, "Извините, вы не администратор.")

    elif text == 'информация по всем':
        if find_admin_by_chat_id(message.chat.id):
            information_all(message)
        else:
            bot.send_message(message.chat.id, "Извините, вы не администратор.")

    elif text == 'назад':
        if find_admin_by_chat_id(message.chat.id):
            markup = create_buttons()
            bot.send_message(message.chat.id, "Дабро пожаловать в режим сотрудника! Выберите действие: " , reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Извините, вы не администратор.")
    else:
        bot.send_message(message.chat.id, "Извините, я не могу понять ваш запрос.")



#Поиск админа по chat_id
def find_admin_by_chat_id(chat_id):
    lines = open("admin.txt", 'r').readlines()
    for line in lines:
        lines_split = line.split()
        if str(lines_split[2]) == str(chat_id):
            return lines_split[0] + " " + lines_split[1]
    return None



# Функция для поиска пользователя по chat_id
def find_user_by_chat_id(chat_id):
    lines = open("reg.txt", 'r').readlines()
    for line in lines:
        lines_split = line.split()
        if str(lines_split[2]) == str(chat_id):
            return lines_split[0] + " " + lines_split[1]
    return None

# Проверка, ест ли пользователь
def is_user_eating(user):
    file = open("eating.txt", "r").readlines()
    for line in file:
        if line.strip() == user:
            return True
    return False

# Проверка, курит ли пользователь
def is_user_smoking(user):
    file = open("smoking.txt", "r").readlines()
    for line in file:
        if line.strip() == user:
            return True
    return False

def admin(message):
    markup = create_admin_buttons()
    bot.send_message(message.chat.id, "Добро пожаловать в режим администратора! Выберите действие:", reply_markup=markup)

def information_all(message):
        with open("reg.txt", "r") as file:
            lines = file.readlines()
        
        for i in range(len(lines)):
            line = lines[i].split()
            del line[2]
            time = ds.find_user_info(line[0],line[1])
            if time[0] != 1:
                smoke,eat = ds.find_data(line[0],line[1])
                bot.send_message(message.chat.id, f"{line[0] + " " + line[1]} : \n - Время отдыха: {time[0]} \n - Обедал {eat}, Курил {smoke} \n - Статус: В торговом зале")
            else:
                if is_user_eating(find_user_by_chat_id(message.chat.id)):
                    bot.send_message(message.chat.id, f"{line[0] + " " + line[1]} : \n - Сейчас обедает. \n - Обед продолжается {time[1]} ")
                else:
                    bot.send_message(message.chat.id, f"{line[0] + " " + line[1]} : \n - Сейчас курит. \n - Курение продолжается {time[1]} ")


def information(message):
     user = find_user_by_chat_id(message.chat.id)

     if not user:
        bot.send_message(message.chat.id, "Ты не зарегистрирован.")
        return

     if is_user_smoking(user):
        user_split = user.split(); 
        print(user_split[0], user_split[1])
        user_info = ds.find_user_info(user_split[0], user_split[1])
        print(user_info)
        bot.send_message(message.chat.id,f"Ты сейчас куришь. Время курения: {user_info[1]}")
     elif is_user_eating(user):
        user_split = user.split(); 
        print(user_split[0], user_split[1])
        user_info = ds.find_user_info(user_split[0], user_split[1])
        print(user_info)
        bot.send_message(message.chat.id,f"Ты сейчас обедаешь. Время обеда: {user_info[1]}")
     else:
        user_split = user.split(); 
        print(user_split[0], user_split[1])
        user_info1 = ds.find_data(user_split[0], user_split[1])
        print(user_info1)
        user_info = ds.find_user_info(user_split[0], user_split[1])
        print(user_info)
        bot.send_message(message.chat.id,f"Ты сегодня отдыхал: {user_info[0]}, кол-во обедов: {user_info1[1]}, кол-во раз курил: {user_info1[0]}")

    

# Обработчик команды /eat_start
@bot.message_handler(commands=["начать обедать"])
def eat_start(message):
    chat_id = message.chat.id
    user = find_user_by_chat_id(chat_id)

    # Если пользователь не зарегистрирован
    if not user:
        bot.send_message(chat_id, "Ты не зарегистрирован.")
        return

    # Проверка, ест ли или курит ли сотрудник сейчас
    if is_user_eating(user):
        bot.send_message(chat_id, "Ты уже обедаешь.")
    elif is_user_smoking(user):
        bot.send_message(chat_id, "Ты не можешь начать обедать, пока куришь.")
    else:
        # Запись пользователя в список обедающих
        with open("eating.txt", "a") as eat_list:
            eat_list.write(user + "\n")

        # Добавление действия в базу данных
        user_split = user.split()
        user_name = user_split[0]
        user_last_name = user_split[1]
        smoking, eating = ds.find_data(user_name, user_last_name)
        data = [user, smoking, eating,"s", "eat"]
        ds.add_data(data)

        bot.send_message(chat_id, "Ты начал обедать.")

# Обработчик команды /eat_stop
@bot.message_handler(commands=['закончить обедать'])
def eat_stop(message):
    chat_id = message.chat.id
    user = find_user_by_chat_id(chat_id)

    # Если пользователь не зарегистрирован
    if not user:
        bot.send_message(chat_id, "Ты не зарегистрирован.")
        return

    file2 = open("eating.txt").readlines()
    is_eating = False

    if len(file2) != 0:
        for i in range(len(file2)):
            if str(user) in file2[i]:
                is_eating = True
                user_split = user.split()
                user_name = user_split[0]
                user_last_name = user_split[1]
                smoking, eating = ds.find_data(user_name, user_last_name)
                data = [user]
                data.append(smoking)
                data.append(int(eating) + 1)
                data.append("e")
                data.append("eat")
                ds.add_data(data)

                # Обновление файла, удаление пользователя из списка обедающих
                with open("eating.txt", 'r') as file:
                    lines = file.readlines()

                updated_lines = [line for line in lines if line.strip() != user]

                with open("eating.txt", 'w') as file:
                    file.writelines(updated_lines)

                break

    if is_eating:
        bot.send_message(chat_id, "Ты прекратил обедать.")
    else:
        bot.send_message(chat_id, "Ты не обедаешь.")

# Обработчик команды /smoke_start
@bot.message_handler(commands=["начать курить"])
def smoke_start(message):
    chat_id = message.chat.id
    user = find_user_by_chat_id(chat_id)

    # Если пользователь не зарегистрирован
    if not user:
        bot.send_message(chat_id, "Ты не зарегистрирован.")
        return

    # Проверка, ест ли или курит ли сотрудник сейчас
    if is_user_smoking(user):
        bot.send_message(chat_id, "Ты уже куришь.")
    elif is_user_eating(user):
        bot.send_message(chat_id, "Ты не можешь начать курить, пока обедаешь.")
    else:
        # Запись пользователя в список курящих
        with open("smoking.txt", "a") as smoke_list:
            smoke_list.write(user + "\n")

        # Добавление действия в базу данных
        user_split = user.split()
        user_name = user_split[0]
        user_last_name = user_split[1]
        smoking, eating = ds.find_data(user_name, user_last_name)
        data = [user, int(smoking), eating, "s","smoke"]
        ds.add_data(data)

        bot.send_message(chat_id, "Ты начал курить.")

# Обработчик команды /smoke_stop
@bot.message_handler(commands=['закончить курить'])
def smoke_stop(message):
    chat_id = message.chat.id
    user = find_user_by_chat_id(chat_id)

    # Если пользователь не зарегистрирован
    if not user:
        bot.send_message(chat_id, "Ты не зарегистрирован.")
        return

    file2 = open("smoking.txt").readlines()
    is_smoking = False

    if len(file2) != 0:
        for i in range(len(file2)):
            if str(user) in file2[i]:
                is_smoking = True
                user_split = user.split()
                user_name = user_split[0]
                user_last_name = user_split[1]
                smoking, eating = ds.find_data(user_name, user_last_name)
                data = [user]
                data.append(int(smoking) + 1)
                data.append(eating)
                data.append("e")
                data.append("smoke")
                ds.add_data(data)

                # Обновление файла, удаление пользователя из списка курящих
                with open("smoking.txt", 'r') as file:
                    lines = file.readlines()

                updated_lines = [line for line in lines if line.strip() != user]

                with open("smoking.txt", 'w') as file:
                    file.writelines(updated_lines)

                break

    if is_smoking:
        bot.send_message(chat_id, "Ты прекратил курить.")
    else:
        bot.send_message(chat_id, "Ты не куришь.")

#функция регестрации админа
def reg_admin(message):
    """
    Регистрирует нового администратора. Проверяет текст сообщения, пароль и статус пользователя.
    """
    # Открываем файл admin.txt для добавления новой записи
    with open("admin.txt", 'a') as file:
        text = message.text
        data = text.split()
        print(data)
        
        # Проверяем, если сообщение содержит 'отмена', прерываем выполнение функции
        if 'отмена' in text:
            return

        # Проверяем, зарегистрирован ли пользователь как админ
        if not find_admin_by_chat_id(message.chat.id):
            # Проверяем правильность пароля
            if int(data[2]) == int(admin_password):
                # Проверяем, зарегистрирован ли пользователь как сотрудник
                if not find_user_by_chat_id(message.chat.id):
                    # Записываем данные нового админа в файл
                    file.write(f"{data[0]} {data[1]} {message.chat.id}\n")
                    bot.send_message(message.chat.id, "Админ зарегистрирован")
                else:
                    bot.send_message(message.chat.id, "Ты уже зарегистрирован как сотрудник")
            else:
                bot.send_message(message.chat.id, "Пароль не верный")
        else:
            bot.send_message(message.chat.id, "Ты уже зарегистрирован как админ")



# Функция регистрации пользователя
def reg(message):
    if not find_admin_by_chat_id(message.chat.id):
        with open("reg.txt", 'a') as file:
            text = message.text
            file.write(str(text) + " " + str(message.chat.id) + "\n")
    else:
        bot.send_message(message.chat.id, "Ты админ.")

# Запуск бота
bot.polling()
