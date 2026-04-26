import psycopg2
from config import host, user, password, db_name, port

def test_connection():
    try:
        # Пытаемся подключиться
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            port=port
        )
        print("Успех! Python подключился к серверу Aryn.")
        
        # Проверяем версию базы
        cur = conn.cursor()
        cur.execute('SELECT version()')
        print(f"Версия базы: {cur.fetchone()}")
        
        cur.close()
        conn.close()
    except Exception as error:
        print(f"Ошибка при подключении: {error}")

if __name__ == '__main__':
    test_connection()