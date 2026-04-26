import psycopg2
import config
import csv

def get_connection():
    return psycopg2.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.db_name,
        port=config.port
    )

def insert_contact(name, phone):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO phonebook(name, phone) VALUES(%s, %s)", (name, phone))
                conn.commit()
        print(f"Контакт {name} добавлен!")
    except Exception as e:
        print(f"Ошибка при вставке: {e}")

def search_contacts(name_part):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", (f'%{name_part}%',))
                rows = cur.fetchall()
                if not rows:
                    print("Контакты не найдены.")
                for row in rows:
                    print(f"ID: {row[0]} | Имя: {row[1]} | Тел: {row[2]}")
    except Exception as e:
        print(f"Ошибка поиска: {e}")

def delete_contact(name):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
                conn.commit()
        print(f"Контакт {name} удален!")
    except Exception as e:
        print(f"Ошибка удаления: {e}")

def upload_from_csv(filename):
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        if len(row) == 2:
                            cur.execute("INSERT INTO phonebook(name, phone) VALUES(%s, %s)", (row[0], row[1]))
                    conn.commit()
        print(f"Данные из {filename} успешно загружены!")
    except Exception as e:
        print(f"Ошибка при чтении CSV: {e}")

if __name__ == "__main__":
    while True:
        print("\n--- Телефонная Книга ---")
        print("1. Добавить контакт")
        print("2. Найти контакт")
        print("3. Удалить контакт")
        print("4. Загрузить из CSV")
        print("5. Выход")
        
        choice = input("Выбери действие: ")

        if choice == '1':
            n = input("Имя: ")
            p = input("Телефон: ")
            insert_contact(n, p)
        elif choice == '2':
            n = input("Введите имя для поиска (или пусто для всех): ")
            search_contacts(n)
        elif choice == '3':
            n = input("Кого удалить? ")
            delete_contact(n)
        elif choice == '4':
            f = input("Введите имя файла (например, data.csv): ")
            upload_from_csv(f)
        elif choice == '5':
            print("До свидания!")
            break
        else:
            print("Неверный ввод, попробуй еще раз.")
