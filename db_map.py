import sqlite3

# Создание таблицы
def create_table():
    connection = sqlite3.connect("find_shina.dp")
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY, data_shina TEXT)')
    connection.commit()
    connection.close()



def create_data_shina(user_id, data):
    connection = sqlite3.connect("find_shina.dp")
    cursor = connection.cursor()
    cursor.execute("SELECT data_shina FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE Users SET data_shina = ? WHERE id = ?", (data, user_id))
    else:
        # Добавляем нового пользователя
        cursor.execute(f'INSERT INTO Users (id, data_shina) VALUES (?, ?)', (user_id, data))



    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()



# Получение данных
def select_shina(id):
    connection = sqlite3.connect("find_shina.dp")
    cursor = connection.cursor()

    cursor.execute("SELECT data_shina FROM users WHERE id = ?", (id,))
    result = cursor.fetchone()
    return result

    connection.close()




