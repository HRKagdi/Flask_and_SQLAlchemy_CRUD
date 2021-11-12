import requests


def show_menu():
    print('1. Add Students')
    print('2.Fetch All Students')
    print('3. Update Student')
    print('4. Delete student')
    print('5. Exit')


def add_student():
    id = input("Enter ID: ")
    name = input("Enter Name: ")
    stream = input("Enter Stream: ")
    response = requests.post("http://127.0.0.1:8000/create",
                             json={'id': id, 'name': name, 'stream': stream})
    print(response.content)

def show_all():
    response = requests.get("http://127.0.0.1:8000/read")
    print(response.json())

def update_student():
    id = input("Enter ID: ")
    name = input("Enter Name: ")
    stream = input("Enter Stream: ")
    response = requests.put("http://127.0.0.1:8000/update",
                            json={'id': id, 'name': name, 'stream': stream})
    print(response.content)


def delete_student():
    id = input("Enter ID: ")
    response = requests.delete("http://127.0.0.1:8000/delete",
                            json={'id': id})
    print(response.content)


while(1):
    show_menu()
    choice = int(input("Enter Your Choice>> "))
    if choice == 1:
        add_student()
    elif choice == 2:
        show_all()
    elif choice == 3:
        update_student()
    elif choice == 4:
        delete_student()
    elif choice == 5:
        print("Thank You, Byee")
        break
    else:
        print("Invalid Choice")