from Entities.contact import Contact


def load_data():
    contact_list = []
    with open("Data\\ContactData.txt") as file:
        lines = file.readlines()
        for line in lines:
            line = line.replace("\n", "")
            line_splitted = line.split(",")
            contact = Contact(int(line_splitted[0]), line_splitted[1], line_splitted[2], line_splitted[3])
            contact_list.append(contact)

    return contact_list


def replace_data(contact_list):
    data_text = ""
    last_contact_item = contact_list[-1]
    new_id = 1
    for contact in contact_list:
        contact.id = new_id
        data_text += f"{contact.id},{contact.first_name},{contact.last_name},{contact.phone_number}"
        new_id += 1
        if contact.id != last_contact_item.id:
            data_text += "\n"

    with open("Data\\ContactData.txt", mode="w") as file:
        file.write(data_text)
