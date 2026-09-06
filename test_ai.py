import requests

BASE_URL = "http://localhost:8000/api/v1"

# Данные пользователя с учётом ограничений длины
TEST_USER = {
    "username": "testuser_req",
    "email": "test_req@example.com",
    "phone_number": "+7123456799",   # 11 символов (плюс + 10 цифр)
    "password": "pass12345"            # 7 символов, ≤12
}

<<<<<<< HEAD
detal_id = None
=======
detal_id = None 
>>>>>>> 8860929115287add61d8bfc6ecb21363bdda5a75

# Данные для создания детали – все обязательные поля из схемы
TEST_DETAL = {
    # "id": 1,                         # если автоинкремент, можно передать 0 или None, но требуется – оставим
    "article": "ART002",             # возможно, необязательно
    "article_number": "ART002",
    "name": "Деталь для теста requests",
    "price": 250.75,
    "description": "Тестовое описание",
    "manufacturer": "Test Manufacturer",
    "quantity_in_stock": 10
}

def test_register():
    url = f"{BASE_URL}/auth/register"
    resp = requests.post(url, json=TEST_USER)
    assert resp.status_code == 200, f"Ошибка регистрации: {resp.text}"
    data = resp.json()
    assert "id" in data
    assert data["username"] == TEST_USER["username"]
    assert data["email"] == TEST_USER["email"]
    print("[OK] Регистрация прошла успешно")
    return data

def test_register_duplicate():
    url = f"{BASE_URL}/auth/register"
    resp = requests.post(url, json=TEST_USER)
    assert resp.status_code == 400, f"Ожидалась 400, получено {resp.status_code}"
    assert "уже есть" in resp.text or "already exists" in resp.text
    print("[OK] Дубликат обработан правильно")

def test_login():
    url = f"{BASE_URL}/auth/login"
    resp = requests.post(url, data={"username": TEST_USER["username"], "password": TEST_USER["password"]})
    assert resp.status_code == 200, f"Ошибка входа: {resp.text}"
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    print("[OK] Вход выполнен, токен получен")
    return data["access_token"]

def test_create_detal():
    global detal_id
    url = f"{BASE_URL}/detals/create_new_detal"
    resp = requests.post(url, json=TEST_DETAL)
    assert resp.status_code == 200, f"Ошибка создания детали: {resp.text}"
    data = resp.json()
    # Проверяем, что вернулся объект с идентификатором
    assert "id" in data or "article_number" in data
    print("[OK] Деталь создана")
    return data

def test_get_all_detals():
    url = f"{BASE_URL}/detals/get_all_detal_from_db"
    resp = requests.get(url, params={"offset": 0, "limit": 10})
    assert resp.status_code == 200, f"Ошибка получения деталей: {resp.text}"
    data = resp.json()
    assert isinstance(data, list)
    # Ищем созданную деталь по article_number или id
    found = any(item.get("article_number") == TEST_DETAL["article_number"] for item in data)
    assert found, "Созданная деталь не найдена в списке"
    print("[OK] Список деталей получен, созданная деталь присутствует")

def test_get_detal_by_article():
    url = f"{BASE_URL}/detals/get_detal_by_article"
    resp = requests.get(url, params={"detal_id": TEST_DETAL["article_number"]})
    assert resp.status_code == 200, f"Ошибка получения детали: {resp.text}"
    data = resp.json()
    assert data is not None
    # Проверяем, что вернулась нужная деталь
    assert data.get("article_number") == TEST_DETAL["article_number"] or data.get("id") == TEST_DETAL["id"]
    print("[OK] Деталь найдена по артикулу")

def test_create_order():
    global detal_id
    # 1. Сначала логинимся и получаем токен
    login_resp = requests.post(f"{BASE_URL}/auth/login", data={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    })
    token = login_resp.json()["access_token"]

    # 2. Формируем заголовок с токеном
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Отправляем запрос на создание заказа с этим заголовком
    order_data = {"items": [{"detal_id": 1, "quantity": 2}]}
    resp = requests.post(
        f"{BASE_URL}/orders/order",
        json=order_data,
        headers=headers  # <-- Вот это критически важно!
    )
    assert resp.status_code == 200

def test_create_order_without_auth():
    url = f"{BASE_URL}/orders/order"
    resp = requests.post(url, json={"items": [{"detal_id": "ART001", "quantity": 1}]})
    assert resp.status_code == 401, f"Ожидалась 401, получено {resp.status_code}"
    print("[OK] Заказ без авторизации отклонён")

def test_create_order_invalid_detal(token):
    url = f"{BASE_URL}/orders/order"
    headers = {"Authorization": f"Bearer {token}"}
    # Передаём несуществующий числовой ID (например, 9999)
    resp = requests.post(
        url,
        json={"items": [{"detal_id": 9999, "quantity": 1}]},
        headers=headers
    )
    assert resp.status_code == 400, f"Ожидалась 400, получено {resp.status_code}"
    assert "не найдена" in resp.text.lower() or "not found" in resp.text.lower()
    print("[OK] Ошибка при создании заказа с несуществующей деталью обработана")

def run_all_tests():
    print("=== Запуск тестов API ===\n")
    try:
        test_register()
    except AssertionError as e:
        print(f"[FAIL] Регистрация: {e}")
    try:
        test_register_duplicate()
    except AssertionError as e:
        print(f"[FAIL] Дубликат: {e}")
    try:
        token = test_login()
    except AssertionError as e:
        print(f"[FAIL] Логин: {e}")
        return
    try:
        test_create_detal()
    except AssertionError as e:
        print(f"[FAIL] Создание детали: {e}")
    try:
        test_get_all_detals()
    except AssertionError as e:
        print(f"[FAIL] Получение всех деталей: {e}")
    try:
        test_get_detal_by_article()
    except AssertionError as e:
        print(f"[FAIL] Получение по артикулу: {e}")
    try:
        test_create_order()
    except AssertionError as e:
        print(f"[FAIL] Создание заказа: {e}")
    try:
        test_create_order_without_auth()
    except AssertionError as e:
        print(f"[FAIL] Заказ без авторизации: {e}")
    try:
        test_create_order_invalid_detal(token)
    except AssertionError as e:
        print(f"[FAIL] Заказ с неверной деталью: {e}")
    print("\n=== Все тесты завершены ===")

if __name__ == "__main__":
    run_all_tests()
    