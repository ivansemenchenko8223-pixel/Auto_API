import requests
import random
import string

# Базовый URL API (измените при необходимости)
BASE_URL = "http://localhost:4000/api/v1"

def random_string(length=7):
    """Генерирует случайную строку из букв и цифр."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def random_phone():
    """Генерирует случайный номер телефона в формате 8XXXXXXXXXX"""
    return "8" + ''.join(random.choices(string.digits, k=10))

def test_api():
    # 1. Регистрация нового пользователя
    username = f"user_{random_string()}"
    email = f"{username}@example.com"
    password = "testpass1234"
    phone = random_phone()
    
    register_data = {
        "username": username,
        "email": email,
        "password": password,
        "phone_number": phone
    }
    
    print("1. Регистрация пользователя...")
    resp = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if resp.status_code == 200:
        print("   Успешно:", resp.json())
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)
        return

    # 2. Логин (получение токена)
    print("\n2. Логин...")
    login_data = {
        "username": username,
        "password": password
    }
    resp = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if resp.status_code == 200:
        token = resp.json().get("access_token")
        print("   Токен получен")
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Создание детали (не требует авторизации, но можно передать заголовок)
    print("\n3. Создание детали...")
    article = f"ART-{random_string(6).upper()}"
    detal_data = {
        "article_number": article,
        "name": f"Тестовая деталь {random_string(4)}",
        "description": "Описание детали",
        "price": 199.99,
        "stock": 10
    }
    resp = requests.post(f"{BASE_URL}/detals/create_new_detal", json=detal_data, headers=headers)
    if resp.status_code == 200:
        detal = resp.json()
        detal_id = detal.get("id")  # предполагаем, что возвращается объект с полем id
        print(f"   Деталь создана, ID: {detal_id}, артикул: {detal.get('article')}")
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)
        return

    # 4. Получение списка деталей (без авторизации)
    print("\n4. Получение списка деталей...")
    resp = requests.get(f"{BASE_URL}/detals/get_all_detal_from_db", params={"offset": 0, "limit": 10})
    if resp.status_code == 200:
        detals = resp.json()
        print(f"   Получено деталей: {len(detals)}")
        if detals:
            print(f"   Первая деталь: {detals[0].get('name')}")
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)

    # 5. Получение детали по артикулу
    print("\n5. Получение детали по артикулу...")
    resp = requests.get(f"{BASE_URL}/detals/get_detal_by_article", params={"detal_id": article})
    if resp.status_code == 200:
        detal = resp.json()
        print(f"   Найдена деталь: {detal.get('name')}")
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)

    # 6. Создание заказа (требует авторизации)
    print("\n6. Создание заказа...")
    order_data = {
        "items": [
            {
                "detal_id": detal_id,   # предполагаем, что заказ использует ID детали
                "quantity": 2
            }
        ]
    }
    resp = requests.post(f"{BASE_URL}/orders/order", json=order_data, headers=headers)
    if resp.status_code == 200:
        print("   Заказ создан:", resp.json())
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)

    print("\nТестирование завершено.")

if __name__ == "__main__":
    test_api()