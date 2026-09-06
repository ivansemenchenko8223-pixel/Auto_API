import requests
import random
import string


BASE_URL = "http://localhost:4000/api/v1"


def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def random_phone_number():
    return "8" + ''.join(random.choices(string.digits, k=10))



def test_api():

    username = "qwertyuiop1" #f"user_{random_string()}"
    email = "username99@yandex.ru" #f"{username}@example.com"
    phone_number = "89061852827" #f"{random_phone_number()}"
    password = "testpass123"


    # 1. Регистрация нового пользователя
    register_data = {
        "username": username,
        "email": email,
        "phone_number" : phone_number,
        "password": password
    }
      
    print("1. Регистрация пользователя")
    resp = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if resp.status_code == 200:
        print("Успешно", resp.json())
    else:
        print(f"Ошибка {resp.status_code}" , resp.text)
        return


    # 2. Логин
    print("2. Логин")
    login_data = {
        "username": username,
        #"email": email,
        "password": password
    }
    
    resp = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if resp.status_code == 200:
        #token = resp.json().get("access_token")
        print("   Токен получен")
    else:
        print(f"   Ошибка {resp.status_code}:", resp.text)
        return

    
    #headers = {"Authorization": f"Bearer {token}"}
    


if __name__ == "__main__":
    test_api()
    