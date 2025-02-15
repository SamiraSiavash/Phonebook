from tkinter import Tk, Label, Entry, Button
from tkinter.ttk import Treeview
from Data.working_file import load_data, replace_data
from Entities.phone_book import PhoneBook

contact_list = load_data()
phonebook = PhoneBook(contact_list)

window = Tk()
window.title("Phone Book Application")

window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_columnconfigure(3, weight=1)


def show_contact_form(contact=None):
    contact_form = Tk()

    if contact:
        contact_form.title("Update Contact")
    else:
        contact_form.title("New Contact")

    firstname_label = Label(contact_form, text="First name")
    firstname_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    firstname_entry = Entry(contact_form, width=50)
    firstname_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

    lastname_label = Label(contact_form, text="Last name")
    lastname_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")
    lastname_entry = Entry(contact_form, width=50)
    lastname_entry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="e")

    phone_label = Label(contact_form, text="Phone number")
    phone_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
    phone_entry = Entry(contact_form, width=50)
    phone_entry.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="e")

    if contact:
        firstname_entry.insert(0, contact.first_name)
        lastname_entry.insert(0, contact.last_name)
        phone_entry.insert(0, contact.phone_number)

    def submit():
        firstname = firstname_entry.get()
        lastname = lastname_entry.get()
        phone = phone_entry.get()

        if contact:
            contact.update(firstname, lastname, phone)
            phonebook.show_contact_list = phonebook.contact_list.copy()
        else:
            phonebook.insert(firstname, lastname, phone)

        replace_data(phonebook.contact_list)
        load_data_treeview()
        contact_form.destroy()

    submit_button = Button(contact_form, text="Submit", command=submit)
    submit_button.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")

    contact_form.mainloop()


insert_button = Button(window, text="New Contact", command=show_contact_form)
insert_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")


def update_button_clicked():
    update_id = int(phonebook_treeview.selection()[0])
    update_contact = phonebook.get_contact(update_id)
    show_contact_form(update_contact)


update_button = Button(window, text="Update Contact", state="disabled", command=update_button_clicked)
update_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")


def delete_button_clicked():
    delete_rows = phonebook_treeview.selection()

    for delete_row in delete_rows:
        delete_id = int(delete_row)
        phonebook.delete(delete_id)

    replace_data(phonebook.contact_list)
    load_data_treeview()


delete_button = Button(window, text="Delete Contact", state="disabled", command=delete_button_clicked)
delete_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")


def sms_button_clicked():
    contact_id = int(phonebook_treeview.selection()[0])
    sms_contact = phonebook.get_contact(contact_id)

    def send():
        sms_contact.sms(url_entry.get(),
                        line_number_entry.get(),
                        api_key_entry.get(),
                        phone_entry.get(),
                        message_entry.get())

        sms_form.destroy()

    sms_form = Tk()
    sms_form.title("Send SMS")

    sms_form.grid_rowconfigure(0, weight=1)
    sms_form.grid_columnconfigure(0, weight=1)

    url_label = Label(sms_form, text="URL:")
    url_label.grid(row=0, column=0, padx=10, pady=10)
    url_entry = Entry(sms_form, width=30)
    url_entry.grid(row=0, column=1, columnspan=2, padx=(0, 30), pady=10, sticky="e")
    url_entry.insert(0, "")

    line_number_label = Label(sms_form, text="Line Number:")
    line_number_label.grid(row=1, column=0, padx=10, pady=(0, 10))
    line_number_entry = Entry(sms_form, width=30)
    line_number_entry.grid(row=1, column=1, columnspan=2, padx=(0, 30), pady=(0, 10), sticky="e")
    line_number_entry.insert(0, "")

    api_key_label = Label(sms_form, text="API Key:")
    api_key_label.grid(row=2, column=0, padx=10, pady=(0, 10))
    api_key_entry = Entry(sms_form, width=30)
    api_key_entry.grid(row=2, column=1, columnspan=2, padx=(0, 30), pady=(0, 10), sticky="e")
    api_key_entry.insert(0, "")

    phone_label = Label(sms_form, text="Phone:")
    phone_label.grid(row=3, column=0, padx=10, pady=(0, 10))
    phone_entry = Entry(sms_form, width=30)
    phone_entry.grid(row=3, column=1, columnspan=2, padx=(0, 30), pady=10, sticky="e")
    phone_entry.insert(0, f"{sms_contact.phone_number}")

    message_label = Label(sms_form, text="Message:")
    message_label.grid(row=4, column=0, padx=10, pady=(0, 10))
    message_entry = Entry(sms_form, width=30)
    message_entry.grid(row=4, column=1, columnspan=2, padx=(0, 30), pady=(0, 10), sticky="e")

    send_button = Button(sms_form, text="Send", width=10, command=send)
    send_button.grid(row=5, column=1, padx=(0, 100), pady=(0, 10), sticky="e")


sms_button = Button(window, text="SMS", state="disabled", command=sms_button_clicked)
sms_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

search_entry = Entry(window)
search_entry.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")


def search_button_clicked():
    term = search_entry.get()
    phonebook.search(term)
    load_data_treeview()


search_button = Button(window, text="Search", command=search_button_clicked)
search_button.grid(row=1, column=3, padx=10, pady=(0, 10), sticky="ew")

phonebook_treeview = Treeview(window, columns=("firstname", "lastname", "phone"))
phonebook_treeview.grid(row=2, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="nsew")

phonebook_treeview.heading("#0", text="ID")
phonebook_treeview.heading("#1", text="First_name")
phonebook_treeview.heading("#2", text="Last_name")
phonebook_treeview.heading("#3", text="Phone_number")

phonebook_treeview.column("#0", width=50)

row_list = []


def load_data_treeview():
    for row in row_list:
        phonebook_treeview.delete(row)
    row_list.clear()

    contact_data = phonebook.show_contact_list
    row_number = 1

    for contact in contact_data:
        row = phonebook_treeview.insert("", "end", iid=contact.id, text=str(row_number),
                                        values=(contact.first_name, contact.last_name, contact.phone_number))
        row_list.append(row)
        row_number += 1


def manage_buttons(event):
    select_count = len(phonebook_treeview.selection())
    if select_count == 1:
        update_button.config(state="normal")
        delete_button.config(state="normal")
        sms_button.config(state="normal")
    elif select_count > 1:
        update_button.config(state="disabled")
        delete_button.config(state="normal")
        sms_button.config(state="disabled")
    else:
        update_button.config(state="disabled")
        delete_button.config(state="disabled")
        sms_button.config(state="disabled")


phonebook_treeview.bind("<<TreeviewSelect>>", manage_buttons)
load_data_treeview()

window.mainloop()
