from itertools import groupby
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

new_contacts_list = []
for element in contacts_list[1:]:
    new_list = []
    full_name = " ".join(element[:3])
    list_full_name = full_name.split(" ")
    lastname = list_full_name[0]
    firstname = list_full_name[1]
    surname = list_full_name[2]
    organization = element[3]
    position = element[4]
    phone = element[5]
    email = element[6]

    # Приводим номера телефонов в нужный формат
    pattern1 = r"(\+7|8)?\s*(\d{3})[-]?(\d{3})[-]?(\d{2})(\d{2})"
    pattern2 = r"(\+7|8)?\s*\((\d+)\)\s*(\d+)[\s-]+(\d+)[\s-]+(\d+)\s*[(]*([доб.]*)\s*(\d*)[)]*"
    phone1 = re.findall(pattern1, phone)
    # phone2 = re.findall(pattern2, phone)
    if len(phone1) > 0:
        new_phone = re.sub(pattern1, r"+7(\2)\3-\4-\5", phone)
    else:
        new_phone = re.sub(pattern2, r"+7(\2)\3-\4-\5 \6\7", phone)

    new_list.append(lastname)
    new_list.append(firstname)
    new_list.append(surname)
    new_list.append(organization)
    new_list.append(position)
    new_list.append(new_phone)
    new_list.append(email)
    new_contacts_list.append(new_list)

sort_new_contacts_list = sorted(new_contacts_list, key=lambda x: x[:2])
groups_contacts = []
for k, g in groupby(sort_new_contacts_list, key=lambda x: x[:2]):
    groups_contacts.append(list(g))
final_contacts_list = []
for group in groups_contacts:
    if len(group) > 1:
        dict_group = {}
        list1 = group[0]
        list2 = group[1]
        dict_group['lastname'] = list1[0]
        dict_group['firstname'] = list1[1]
        dict_group['surname'] = list1[2]
        dict_group['organization'] = list1[3]
        dict_group['position'] = list1[4]
        dict_group['phone'] = list1[5]
        dict_group['email'] = list1[6]
        if dict_group['lastname'] == '':
            dict_group['lastname'] = list2[0]
        if dict_group['firstname'] == '':
            dict_group['firstname'] = list2[1]
        if dict_group['surname'] == '':
            dict_group['surname'] = list2[2]
        if dict_group['organization'] == '':
            dict_group['organization'] = list2[3]
        if dict_group['position'] == '':
            dict_group['position'] = list2[4]
        if dict_group['phone'] == '':
            dict_group['phone'] = list2[5]
        if dict_group['email'] == '':
            dict_group['email'] = list2[6]
        list_group = []
        lastname = dict_group['lastname']
        firstname = dict_group['firstname']
        surname = dict_group['surname']
        organization = dict_group['organization']
        position = dict_group['position']
        phone = dict_group['phone']
        email = dict_group['email']
        list_group.append(lastname)
        list_group.append(firstname)
        list_group.append(surname)
        list_group.append(organization)
        list_group.append(position)
        list_group.append(phone)
        list_group.append(email)
        final_contacts_list.append(list_group)
    else:
        final_contacts_list.append(group[0])

title = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
final_contacts_list.insert(0, title)

# Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts_list)