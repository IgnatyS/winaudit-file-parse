from bs4 import BeautifulSoup
import psycopg2
import os


def network_adapters():
    first_column_list = []  # Список значений из первой колонки
    second_column_list = []

    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all("tr"):  # (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                # if data.text == 'Сетевые адаптеры' or data.text == 'Network adapters' or data.text == 'Сетевые платы':
                if data.text == 'Adapter Name':
                    # Если данные ('Driver ODBC Version') равны 'Сетевые адаптеры'
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        first_column_list.append(data2[0].text)
                        second_column_list.append(data2[1].text)

                    na_dict = dict(zip(first_column_list, second_column_list))
                    con.commit()
                    cur.execute(
                        "SELECT na_id, adapter_name, dns_host_name, ip_address, ip_subnet,"
                        "adapter_status,mac_address, connection_status, connection_speed, fk_na_id, default_gw"
                        " from network_adapters")
                    na_rows = cur.fetchall()
                    na_id = len(na_rows) + 1  # Индекс для новой строки
                    cur.execute(
                        "INSERT INTO network_adapters (na_id, adapter_name, dns_host_name, ip_address,"
                        " ip_subnet, adapter_status, mac_address, connection_status, connection_speed,"
                        " fk_na_id, default_gw) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (na_id, na_dict['Adapter Name'], na_dict['DNS Host Name'],
                            na_dict['IP Address'],
                            na_dict['IP Subnet'], na_dict['Adapter Status'], na_dict['MAC Address'],
                            na_dict['Connection Status'], na_dict['Connection Speed'], machine_id,
                         na_dict['Default IP Gateway'])
                    )

    print("Данные успешно добавлены в таблицу network_adapters")


def setevye_adapters():
    # Добавляем данные в таблицу Setevye_adapters
    # Цикл парсинга файла и в цикле добавления данных спаршенных в базу
    sa_first_column_list = []  # Список значений из первой колонки
    sa_second_column_list = []
    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all("tr"):  # Для всех строк всех таблиц
            # (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                if data.text == 'Сетевые адаптеры' or data.text == 'Network adapters' \
                        or data.text == 'Сетевые платы':
                    # Если данные('Driver ODBC Version') равны 'Сетевые адаптеры'
                    # ПРОВЕРИТЬ КАК ЭТА ХУЕТА РАБОТАЕТ когда одинаковые network_adaapters
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        sa_first_column_list.append(data2[0].text)
                        sa_second_column_list.append(data2[1].text)

                    sa_dict = dict(zip(sa_first_column_list, sa_second_column_list))
                    con.commit()
                    cur.execute(
                        "SELECT sa_id, device_name, manufacturer, location_info, fk_sa_id"
                        " from setevye_adapters")
                    sa_rows = cur.fetchall()
                    sa_id = len(sa_rows) + 1  # Индекс для новой строки
                    cur.execute(
                        "INSERT INTO setevye_adapters (sa_id, device_name, manufacturer, location_info,"
                        "fk_sa_id) VALUES (%s, %s, %s, %s, %s)",
                        (sa_id, sa_dict['Device Name'], sa_dict['Manufacturer'],
                         sa_dict['Location'], machine_id)
                    )
    print("Данные успешно добавлены в таблицу setevye_adapters")


def users():
    # Добавляем данные в таблицу Users
    # Цикл парсинга файла и в цикле добавления данных спаршенных в базу
    first_column_list = []  # Список значений из первой колонки
    second_column_list = []

    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all("tr"):  # Для всех строк всех таблиц
            # (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                if data.text == 'Local Groups':  # Если данные ('Driver ODBC Version') равны 'Сетевые адаптеры'
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        first_column_list.append(data2[0].text)
                        second_column_list.append(data2[1].text)

                    dictionary = dict(zip(first_column_list, second_column_list))

                    con.commit()
                    cur.execute(
                        "SELECT users_id, user_name, group_list, account_status, fk_users_id, description from users")
                    users_rows = cur.fetchall()
                    users_id = len(users_rows) + 1  # Индекс для новой строки
                    cur.execute(
                        "INSERT INTO users (users_id, user_name, group_list, account_status, fk_users_id, description) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (users_id, dictionary['User Account'], dictionary['Local Groups'],
                         dictionary['Account Status'],
                         machine_id, dictionary['Description'])
                    )
    print("Данные успешно добавлены в таблицу users")


def services():
    first_column_list = []  # Список значений из первой колонки
    second_column_list = []

    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all(
                "tr"):  # Для всех строк всех таблиц (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                if data.text == 'Service Type':  # Если данные ('Driver ODBC Version') равны 'Сетевые адаптеры'
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        first_column_list.append(data2[0].text)
                        second_column_list.append(data2[1].text)

                    dictionary = dict(zip(first_column_list, second_column_list))
                    con.commit()
                    cur.execute(
                        "SELECT service_id, service_name, path_name, fk_service_id from services")
                    services_rows = cur.fetchall()
                    services_id = len(services_rows) + 1  # Индекс для новой строки
                    cur.execute(
                        "INSERT INTO services (service_id, service_name, path_name, fk_service_id) "
                        "VALUES (%s, %s, %s, %s)",
                        (services_id, dictionary['Name'], dictionary['Path Name'], machine_id)
                    )
    print("Данные успешно добавлены в таблицу services")


def install_programs():
    first_column_list = []  # Список значений из первой колонки
    second_column_list = []

    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all(
                "tr"):  # Для всех строк всех таблиц (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                if data.text == 'Executable Description':
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        first_column_list.append(data2[0].text)
                        second_column_list.append(data2[1].text)

                    dictionary = dict(zip(first_column_list, second_column_list))
                    con.commit()
                    cur.execute(
                        "SELECT prog_id, prog_name, install_sourse, install_location, local_package,"
                        "fk_prog_id from install_progs")
                    prog_rows = cur.fetchall()
                    prog_id = len(prog_rows) + 1  # Индекс для новой строки
                    cur.execute(
                        "INSERT INTO install_progs (prog_id, prog_name, install_sourse, "
                        "install_location, local_package,"
                        "fk_prog_id) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (prog_id, dictionary['Name'], dictionary['Install Source'],
                         dictionary['Install Location'],
                         dictionary['Local Package'], machine_id)
                    )
    print("Данные успешно добавлены в таблицу install_progs")


def ntp():
    first_column_list = []  # Список значений из первой колонки
    second_column_list = []

    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all(
                "tr"):  # Для всех строк всех таблиц (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                if data.text == 'ServiceDllUnloadOnStop':
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        first_column_list.append(data2[0].text)
                        second_column_list.append(data2[1].text)

                    dictionary = dict(zip(first_column_list, second_column_list))
                    con.commit()
                    cur.execute(
                        "SELECT ntp_server_id, ntp_server, servicedll, service_dll_uos, service_main,"
                        "fk_ntp_server_id from ntp")
                    ntp_server_rows = cur.fetchall()
                    ntp_server_id = len(ntp_server_rows) + 1  # Индекс для новой строки

                    try:
                        cur.execute(
                            "INSERT INTO ntp (ntp_server_id, ntp_server, servicedll, service_dll_uos, service_main,"
                            "fk_ntp_server_id) "
                            "VALUES (%s, %s, %s, %s, %s, %s)",
                            (ntp_server_id, dictionary['NtpServer'], dictionary['ServiceDll'],
                            dictionary['ServiceDllUnloadOnStop'], dictionary['ServiceMain'], machine_id)
                        )
                        print("Данные успешно добавлены в таблицу ntp")
                    except KeyError:
                        print("Таблица NTP отсутствует в отчёте")



def rsv():
    first_column_list = []  # Список значений из первой колонки
    second_column_list = []

    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all(
                "tr"):  # Для всех строк всех таблиц (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                if data.text == 'System\EnableLUA':
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        first_column_list.append(data2[0].text)
                        second_column_list.append(data2[1].text)

                    dictionary = dict(zip(first_column_list, second_column_list))
                    con.commit()
                    cur.execute(
                        "SELECT rsv_id, enablelua, fk_rsv_id from rsv")
                    rsv_rows = cur.fetchall()
                    rsv_id = len(rsv_rows) + 1  # Индекс для новой строки
                    cur.execute(
                        "INSERT INTO rsv (rsv_id, enablelua, fk_rsv_id) "
                        "VALUES (%s, %s, %s)",
                        (rsv_id, dictionary['System' + '\\' + 'EnableLUA'], machine_id)
                    )
    print("Данные успешно добавлены в таблицу rsv")


def soft_updates():
    first_column_list = []  # Список значений из первой колонки
    second_column_list = []
    third_column_list = []

    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all("tr"):  # Для всех строк всех таблиц
            # (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                if data.text == 'Installed On':  # Если данные ('Driver ODBC Version') равны 'Сетевые адаптеры'
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        first_column_list.append(data2[0].text)
                        second_column_list.append(data2[1].text)
                        third_column_list.append(data2[2].text)

                    elements = len(first_column_list) - 1
                    i = 0
                    while i < elements:
                        con.commit()
                        cur.execute(
                            "SELECT su_id, update_id, update_date, description, fk_su_id from soft_updates")
                        su_rows = cur.fetchall()
                        su_id = len(su_rows) + 1  # Индекс для новой строки
                        i = i + 1
                        cur.execute(
                            "INSERT INTO soft_updates (su_id, update_id, update_date, description, fk_su_id) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            (su_id, first_column_list[i], second_column_list[i], third_column_list[i],
                             machine_id)
                        )
    print("Данные успешно добавлены в таблицу soft_updates")


def network_share():
    first_column_list = []  # Список значений из первой колонки
    second_column_list = []
    third_column_list = []
    four_column_list = []

    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all("tr"):  # Для всех строк всех таблиц
            # (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                if data.text == 'Share Path':
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        first_column_list.append(data2[0].text)
                        second_column_list.append(data2[1].text)
                        third_column_list.append(data2[2].text)
                        four_column_list.append(data2[3].text)

                    elements = len(first_column_list) - 1
                    i = 0
                    while i < elements:
                        con.commit()
                        cur.execute(
                            "SELECT ns_id, share_name, share_type, connections, share_path, fk_ns_id from "
                            "network_shares")
                        ns_rows = cur.fetchall()
                        ns_id = len(ns_rows) + 1  # Индекс для новой строки
                        i = i + 1

                        cur.execute(
                            "INSERT INTO network_shares (ns_id, share_name, share_type, connections,"
                            " share_path, "
                            "fk_ns_id) "
                            "VALUES (%s, %s, %s, %s, %s, %s)",
                            (ns_id, first_column_list[i], second_column_list[i], third_column_list[i],
                             four_column_list[i], machine_id)
                        )
    print("Данные успешно добавлены в таблицу network_shares")


def logic_disc():
    first_column_list = []  # Список значений из первой колонки
    second_column_list = []

    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all(
                "tr"):  # Для всех строк всех таблиц (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                if data.text == 'Letter':  # Если данные ('Driver ODBC Version') равны 'Сетевые адаптеры'
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        first_column_list.append(data2[0].text)
                        second_column_list.append(data2[1].text)

                    dictionary = dict(zip(first_column_list, second_column_list))
                    con.commit()
                    cur.execute(
                        "SELECT ld_id, disc_name, drive_type, percent_used, used_space, "
                        "free_space, total_space,"
                        " fk_ld_id from logic_disc")
                    ld_rows = cur.fetchall()
                    ld_id = len(ld_rows) + 1  # Индекс для новой строки

                    try:
                        cur.execute(
                            "INSERT INTO logic_disc (ld_id,  disc_name, drive_type, percent_used, used_space, "
                            "free_space, total_space, fk_ld_id)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (ld_id, dictionary['Letter'], dictionary['Drive Type'], dictionary['Percent Used'],
                             dictionary['Used Space'], dictionary['Free Space'], dictionary['Total Space'],
                             machine_id)
                        )
                    except KeyError:
                        cur.execute(
                            "INSERT INTO logic_disc (ld_id,  disc_name, drive_type, fk_ld_id)"
                            "VALUES (%s, %s, %s, %s)",
                            (ld_id, dictionary['Letter'], dictionary['Drive Type'], machine_id)
                        )

                    first_column_list = []  # Список значений из первой колонки
                    second_column_list = []
    print("Данные успешно добавлены в таблицу logic_disc")


def system_slots():
    # Добавляем данные в таблицу Users
    # Цикл парсинга файла и в цикле добавления данных спаршенных в базу
    first_column_list = []  # Список значений из первой колонки
    second_column_list = []

    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all("tr"):  # Для всех строк всех таблиц
            # (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                if data.text == 'Slot Designation':
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        first_column_list.append(data2[0].text)
                        second_column_list.append(data2[1].text)

                    dictionary = dict(zip(first_column_list, second_column_list))
                    con.commit()
                    cur.execute(
                        "SELECT sys_slots_id, slot_designation, slot_type, data_bus_width, current_usage,"
                        "slot_length, slot_characteristics1, fk_sys_slots_id from system_slots")
                    sys_slots_rows = cur.fetchall()
                    sys_slots_id = len(sys_slots_rows) + 1  # Индекс для новой строки
                    cur.execute(
                        "INSERT INTO system_slots (sys_slots_id, slot_designation, slot_type, data_bus_width, "
                        "current_usage, slot_length, slot_characteristics1, fk_sys_slots_id) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (sys_slots_id, dictionary['Slot Designation'], dictionary['Slot Type'],
                         dictionary['Data Bus Width'], dictionary['Current Usage'],
                         dictionary['Slot Length'], dictionary['Slot Characteristics 1'],
                         machine_id)
                    )
    print("Данные успешно добавлены в таблицу system_slots")

def processor():
    first_column_list = []  # Список значений из первой колонки
    second_column_list = []

    for table in soup.find_all("table"):  # Для всех элементов с тегом "table" в файле test
        for row in table.find_all("tr"):  # (<tr><td>Driver ODBC Version</td><td>02.50</td></tr>)
            for data in row.find_all("td"):  # Для всех данных строк ( <td>Driver ODBC Version</td> )
                # if data.text == 'Сетевые адаптеры' or data.text == 'Network adapters' or data.text == 'Сетевые платы':
                if data.text == 'External Clock':
                    # Если данные ('Driver ODBC Version') равны 'Сетевые адаптеры'
                    for row2 in table.find_all("tr"):  # То для всех строк таблиц в которых есть эти данные
                        data2 = row2.find_all("td")  # Ищем все поля данных ([<td>Status Code</td>, <td>0</td>])
                        first_column_list.append(data2[0].text)
                        second_column_list.append(data2[1].text)

                    p_dict = dict(zip(first_column_list, second_column_list))
                    con.commit()
                    cur.execute(
                        "SELECT proc_id, proc_number, proc_type, proc_family, proc_manufacturer, processor_ID,"
                        "proc_version, proc_upgrade, core_count, core_enabed, fk_proc_id"
                        " from Processor")
                    p_rows = cur.fetchall()
                    p_id = len(p_rows) + 1  # Индекс для новой строки
                    cur.execute(
                        "INSERT INTO Processor (proc_id, proc_number, proc_type, proc_family, "
                        "proc_manufacturer, processor_ID, proc_version, proc_upgrade, core_count, core_enabed, "
                        "fk_proc_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (p_id, p_dict['Processor Number'], p_dict['Processor Type'],
                            p_dict['Processor Family'],
                            p_dict['Processor Manufacturer'], p_dict['Processor ID'], p_dict['Processor Version'],
                            p_dict['Processor Upgrade'], p_dict['Core Count'], p_dict['Core Enabled'], machine_id)
                    )
    print("Данные успешно добавлены в таблицу Processor")

# Основная часть говнокода


main_folder_name = input("Введи имя папки : ")
plant_list = os.listdir(main_folder_name)
print("Список установок :", plant_list)

for plant_folder in plant_list:
    machine_list = os.listdir(main_folder_name + '/' + plant_folder)
    print("Станция : ", plant_folder)
    print("Список машин : ", machine_list)

    for machine in machine_list:
        con = psycopg2.connect(
            database="NEW",
            user="",
            password="",
            host="",
            port=""
        )
        cur = con.cursor()

        file = open(main_folder_name + "/" + plant_folder + "/" + machine)
        soup = BeautifulSoup(file, 'lxml')  # переменная для хранения спаршенной страницы

        # Получение данных от пользователя
        plant = plant_folder

        # Заполнение таблицы №1 PLANT
        # Получение значения primary key и foreign key из вышестоящего объекта, если пусто то все равно 1

        cur.execute("SELECT plant_name_id, plant_name from plant")  # Извлекаем 2 столбца из таблицы
        plant_rows = cur.fetchall()  # Получаем кортеж значений
        id_plant_list = []  # Список уже имеющихся айпишников
        items_plant_list = []  # Список уже имеющихся строк
        select_plant_dict = []  # Словарь имеющихся данных

        for row in plant_rows:
            id_plant_list.append(row[0])
            items_plant_list.append(row[1])
        select_plant_dict = dict(zip(id_plant_list, items_plant_list))  # Собирем все прогнанное через цикл в кучу
        print("")
        print("СЛОВАРЬ ТАБЛИЦЫ PLANT ID-НАИМЕНОВАНИЕ : ", select_plant_dict)

        if plant in items_plant_list:  # Если установка уже есть в таблице
            plant_id = list(select_plant_dict.keys())[
                list(select_plant_dict.values()).index(plant)]  # индекс имеющейся уст-ки
            print("УСТАНОВКА " + plant + " УЖЕ ЕСТЬ В БАЗЕ ПРОДОЛЖАЕМ РАБОТУ С НЕЙ!, УСТАНОВКА : ",
                  plant, "| ИНДЕКС УСТАНОВКИ : ", plant_id)
        else:
            plant_id = len(plant_rows) + 1  # Индекс для новой установке ( макс индекс + 1)
            print("УСТАНОВКИ" + plant + "НЕТ В БАЗЕ ! ДОБАВЛЯЕМ ЕЕ НОВОЙ СТРОКОЙ В ТАБЛИЦУ PLANT С ID : ", plant_id)
            cur.execute("INSERT INTO PLANT (plant_name_id, plant_name) VALUES (%s, %s)", (plant_id, plant))

        # Парсинг таблицы about table

        first_column_list = []  # Список значений из первой колонки
        second_column_list = []  # Список значений из второй колонки

        about_table = soup.find_all("table")[0]  # Таблица About_table
        for about_table_row in about_table.find_all("tr"):  # Для всех строк в таблице About_table
            about_table_data = about_table_row.find_all("td")  # [<td>Computer Name</td>, <td>NB-201351</td>]
            first_column_list.append(about_table_data[0].text)  # Добавляем в список значений первый элемент строки
            second_column_list.append(about_table_data[1].text)  # Добавляем в список значений второй элемент строки

        about_table_dict = dict(zip(first_column_list, second_column_list))

        cur.execute("SELECT machine_name_id, machine_name from MACHINE")  # Извлекаем 2 столбца из таблицы
        machine_rows = cur.fetchall()  # Получаем кортеж значений
        id_machine_list = []  # Список уже имеющихся айпишников
        items_machine_list = []  # Список уже имеющихся строк

        for row in machine_rows:
            id_machine_list.append(row[0])
            items_machine_list.append(row[1])
        machine_dict = dict(zip(id_machine_list, items_machine_list))  # Собирем все прогнанное через цикл в кучу
        print("СЛОВАРЬ ТАБЛИЦЫ MACHINE : ", machine_dict)

        machine_id = len(machine_rows) + 1  # Индекс для новой машины
        print("ПАРСИМ ИНФУ О МАШИНЕ :  " + about_table_dict['Computer Name'] + "  ID МАШИНЫ: ", machine_id)
        cur.execute("INSERT INTO MACHINE (machine_name_id, machine_name, operation_system, manufacturer, "
                    "model, serial_number, ram, fk_machine_name_id, hard ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (machine_id,
                     about_table_dict['Computer Name'],
                     about_table_dict['Operating System'],
                     about_table_dict['Manufacturer'],
                     about_table_dict['Model'],
                     about_table_dict['Serial Number'],
                     about_table_dict['Total Memory'],
                     plant_id,
                     about_table_dict['Total Hard Drive']))

        network_adapters()
        setevye_adapters()
        users()
        services()
        install_programs()
        ntp()
        rsv()
        soft_updates()
        network_share()
        logic_disc()
        system_slots()
        processor()

        con.commit()
        print("")
        print("МАШИНА  " + about_table_dict['Computer Name'] + "  ДОБАВЛЕНА УСПЕШНО")
        print("________________________________________________________________________________________________")

        con.close()
