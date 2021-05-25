from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
from cryptography.fernet import Fernet
import os

# ---------------------------- ENCRYPTION KEY ------------------------------- #
home = os.path.expanduser('~')

try:
    with open(f"{home}\\Documents\\pwmanager\\sec_file.key", "rb") as sec_file:
        encryption_key = sec_file.read()
except FileNotFoundError:
    encryption_key = Fernet.generate_key()
    with open(f"{home}\\Documents\\pwmanager\\sec_file.key", "wb") as sec_file:
        sec_file.write(encryption_key)
finally:
    with open(f"{home}\\Documents\\pwmanager\\sec_file.key", "rb") as sec_file:
        encryption_key = sec_file.read()
    crypter = Fernet(encryption_key)
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    input_password.delete(0, 'end')
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list.extend([choice(symbols) for _ in range(randint(2, 4))])
    password_list.extend([choice(numbers) for _ in range(randint(2, 4))])

    shuffle(password_list)

    password = "".join(password_list)

    input_password.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    website = input_website.get()
    user = input_user.get()
    passwd = input_password.get()
    passwd = crypter.encrypt(bytes(passwd, 'utf-8'))
    new_data_dict = {
        website: {
            "email": user,
            "password": str(passwd, "utf8"),
        }
    }

    if not website or not user or not passwd:
        messagebox.showinfo(title="Warning", message="Please don't leave fields empty!")
    else:
        try:
            with open("data.json", "r") as file:
                # reading old data
                data = json.load(file)

        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("data.json", "w") as file:
                # saving updated data
                json.dump(new_data_dict, file, indent=4)
        else:
            # updating old data with new data
            data.update(new_data_dict)
            with open("data.json", "w") as file:
                # saving updated data
                json.dump(data, file, indent=4)
        finally:
            input_password.delete(0, END)
            input_website.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = input_website.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message=f"There is no data file created:\n "
                                                   f"Add at least 1 account before searching")

    else:
        if website in data:
            email = data[website]["email"]
            password = crypter.decrypt(bytes(data[website]["password"], "utf8"))
            messagebox.showinfo(title=website, message=f"Email: {email}\n"
                                                       f"Password: {str(password,'utf8')}")
            pyperclip.copy(str(password,'utf8'))
        else:
            messagebox.showinfo(title="Error", message=f"There are no details for {input_website.get()} website")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("password manager")
window.minsize(width=570, height=450)
window.maxsize(width=570, height=450)
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

lbl_website = Label(text="Website:", bg="white")
lbl_website.grid(column=0, row=1)
lbl_website.focus()
lbl_user = Label(text="Email/Username:", bg="white")
lbl_user.grid(column=0, row=2)
lbl_password = Label(text="Password:", bg="white")
lbl_password.grid(column=0, row=3)

input_website = Entry(width=21)
input_website.grid(column=1, row=1)
input_user = Entry(width=38)
input_user.grid(column=1, row=2, columnspan=2)
input_password = Entry(width=21)
input_password.grid(column=1, row=3)
input_user.insert(0, "fedexj@gmail.com")

btn_generate = Button(text="Generate password", command=generate_password)
btn_generate.grid(column=2, row=3)
btn_search = Button(text="Search", command=find_password, width=16)
btn_search.grid(column=2, row=1)
btn_add = Button(text="Add", width=38, command=save_data)
btn_add.grid(column=1, row=4, columnspan=2)

window.mainloop()
