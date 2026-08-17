import json
import os
import hashlib
import getpass


USERS_FILE = "users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register():
    users = load_users()

    print("\nREGISTER")

    username = input("Username: ")

    if username in users:
        print("Bu username mavjud.")
        return

    name = input("Ism: ")
    surname = input("Familiya: ")

    password = getpass.getpass("Parol: ")
    confirm_password = getpass.getpass("Parolni takrorlang: ")

    if password != confirm_password:
        print("Parollar mos kelmadi.")
        return

    if len(password) < 6:
        print("Parol kamida 6 ta belgidan iborat bo'lishi kerak.")
        return

    users[username] = {
        "name": name,
        "surname": surname,
        "password": hash_password(password),
        "balance": 0,
        "login_attempts": 0,
        "blocked": False
    }

    save_users(users)

    print("Ro'yxatdan o'tish muvaffaqiyatli.")


def login():
    users = load_users()

    print("\nLOGIN")

    username = input("Username: ")

    if username not in users:
        print("Foydalanuvchi topilmadi.")
        return None

    user = users[username]

    if user["blocked"]:
        print("Account bloklangan.")
        return None

    password = getpass.getpass("Parol: ")

    if hash_password(password) == user["password"]:

        user["login_attempts"] = 0
        save_users(users)

        print("Login muvaffaqiyatli.")

        return username

    user["login_attempts"] += 1

    if user["login_attempts"] >= 3:
        user["blocked"] = True
        print("3 marta xato kiritildi.")
        print("Account bloklandi.")
    else:
        print("Parol noto'g'ri.")
        print("Qolgan urinish:",
              3 - user["login_attempts"])

    save_users(users)

    return None


def show_profile(username):
    users = load_users()

    user = users[username]

    print("\nPROFILE")
    print("Username:", username)
    print("Ism:", user["name"])
    print("Familiya:", user["surname"])
    print("Balans:", user["balance"])


def edit_profile(username):
    users = load_users()

    user = users[username]

    print("\nPROFILE EDIT")

    name = input("Yangi ism: ")
    surname = input("Yangi familiya: ")

    if name:
        user["name"] = name

    if surname:
        user["surname"] = surname

    save_users(users)

    print("Profil o'zgartirildi.")


def change_password(username):
    users = load_users()

    user = users[username]

    print("\nCHANGE PASSWORD")

    old_password = getpass.getpass("Eski parol: ")

    if hash_password(old_password) != user["password"]:
        print("Eski parol noto'g'ri.")
        return

    new_password = getpass.getpass("Yangi parol: ")
    confirm_password = getpass.getpass("Yangi parolni takrorlang: ")

    if new_password != confirm_password:
        print("Parollar mos kelmadi.")
        return

    if len(new_password) < 6:
        print("Parol juda qisqa.")
        return

    user["password"] = hash_password(new_password)

    save_users(users)

    print("Parol o'zgartirildi.")


def delete_account(username):
    users = load_users()

    print("\nACCOUNT DELETE")

    confirmation = input(
        "Accountni o'chirish uchun DELETE yozing: "
    )

    if confirmation != "DELETE":
        print("Amal bekor qilindi.")
        return False

    password = getpass.getpass("Parol: ")

    if hash_password(password) != users[username]["password"]:
        print("Parol noto'g'ri.")
        return False

    del users[username]

    save_users(users)

    print("Account o'chirildi.")

    return True


def user_menu(username):

    while True:

        print("\n1. Profil")
        print("2. Profilni o'zgartirish")
        print("3. Parolni o'zgartirish")
        print("4. Accountni o'chirish")
        print("5. Logout")

        choice = input("Tanlang: ")

        if choice == "1":
            show_profile(username)

        elif choice == "2":
            edit_profile(username)

        elif choice == "3":
            change_password(username)

        elif choice == "4":
            if delete_account(username):
                break

        elif choice == "5":
            break

        else:
            print("Noto'g'ri tanlov.")


def main():

    while True:

        print("\n1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Tanlang: ")

        if choice == "1":
            register()

        elif choice == "2":
            username = login()

            if username:
                user_menu(username)

        elif choice == "3":
            break

        else:
            print("Noto'g'ri tanlov.")


if __name__ == "__main__":
    main()