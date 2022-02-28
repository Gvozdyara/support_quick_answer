from tkinter import *
import os
import sqlite3


# класс используемый при создании кнопки с именем раздела
class section_btns:
    def __init__(self, frame, section_id, text, click_cmnd, current_table, path):
        name = "btn_" + str(section_id)
        self.name = Button(frame, text=text, command=lambda: click_cmnd(section_id, current_table, text))
        self.name.pack(fill=X)
        self.id = section_id
        self.current_table = current_table
        self.text = text
        self.name.bind("<Enter>", self.on_enter)
        self.name.bind("<Leave>", self.on_leave)


    # функция создает таблицу, которая устанавливается в столбец section_name таблицы current_table
    def create_inner_table_add_to_the_row(self, section_id, current_table):
        # make the table name where to add new sections
        table_name = self.text
        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        create_table(cur, conn, table_name)
        #     надо добавить свеже созданую таблицу в таблицу выше уровнем в строку с section_id_var
        q = """UPDATE '{}' 
                SET section_inner_lvl = '{}'
                WHERE rowid = '{}' """
        cur.execute(q.format(current_table, table_name, section_id))
        conn.commit()


    # выводим содержимое таблицы, куда наводится курсор к разделу (2 столбец)
    def on_enter(self, e):
        global section_inner_lvl_frame
        # чистим фрэйм
        try:
            for widget in section_inner_lvl_frame.winfo_children():
                widget.destroy()
            section_inner_lvl_frame.update()
        except:
            print("No section inner level frame to destroy")
            pass

        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()

        # q = """
        #         SELECT section_inner_lvl from '{}' WHERE id = ('{}') """
        # cur.execute(q.format(self.text, self.id))
        # description = cur.fetchall()
        # print(description, " description")
        q = """SELECT section_name from '{}'"""
        try:
            cur.execute(q.format(self.text))
        except sqlite3.OperationalError:
            print("there is only row, but not the section")
        to_layout_sections = ["{}\n".format(name[0]) for name in cur.fetchall()]
        to_layout_label = section_inner_lvl_label(self.text, section_inner_lvl_frame, to_layout_sections, None)
        return

    def on_leave(self, e):
        return


#  класс используемый для создания Энтри и кнопки добавения к current_table
class new_section_entry:
    def __init__(self, name, frame, current_table, current_id):
        self.name = Entry(frame)
        get_entry_btn = Button(frame, text="Add section", command=lambda: add_section(self.name, current_table, current_id))
        self.current_id = current_id

        self.name.pack(side=LEFT, expand=0)
        get_entry_btn.pack(side=RIGHT, expand=1)


# поле для вывода содержимого таблицы при наведении курсора на кнопку
class section_inner_lvl_label:
    def __init__(self, name, frame, to_layout, current_id):
        self.name = Label(frame, wraplength=100, justify=CENTER, text=to_layout, background="RED")
        self.name.pack()


# функция вывода таблицы в консоль
def dump_help_base(table):
    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    to_print = cur.execute('''SELECT * FROM "{}"'''.format(table))
    print([row for row in to_print])


# функция выкладывания кнопок текущего раздела
def layout_section_btns(current_table):
    # dump_help_base(current_table)
    global section_frame, path

    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    q = """SELECT rowid, section_name from '{}' """
    to_layout_list = cur.execute(q.format(current_table))
    for item in to_layout_list:
        section_btns(section_frame, item[0], item[1], open_section, current_table, path)


# функция создания файла базы данных
def create_data_base(file_name, table_name):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    create_table(cur, conn, table_name)
    return table_name


# создание таблицы после подключения к базе данных
def create_table (cur, conn, table_name):
    q = '''CREATE TABLE IF NOT EXISTS "{}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section_name TEXT, 
                section_inner_lvl TEXT)'''
    cur.execute(q.format(table_name))
    conn.commit()


# функция добавления нового раздела к базе данных, а также вывода ее в интрефейс в виде кнопки
def add_section(entry, current_table, current_id):
    global root, section_frame, path
    section_title = entry.get()
    section_id = add_section_to_db(section_title, current_table, current_id)
    #     for now we have unique section ID of the new section from the previous func
    new_section_btn = section_btns(section_frame, section_id, section_title, open_section, current_table, path)
    new_section_btn.create_inner_table_add_to_the_row(id, current_table)


# функция добавления нового раздела к базе данных
def add_section_to_db(section_name_var, current_table, current_id):
    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    q = 'INSERT INTO "{}" (section_name) VALUES (?)'
    cur.execute(q.format(current_table), (section_name_var,))
    conn.commit()
    # возвращаем rowid добавленного раздела
    q = """SELECT id FROM '{}' WHERE rowid=last_insert_rowid()"""
    cur.execute(q.format(current_table))
    section_id = cur.fetchone()
    conn.commit()
    return section_id[0]


# Открытие раздела базы данных в интерфейсе
def open_section(current_id, current_table, inner_table):
    global section_frame, entry_frame, path

    # удаляем все кнопки с секциями из фрейма-кнопок для заполнения его новыми кнопками
    for widget in section_frame.winfo_children():
        widget.destroy()
    entry_frame.update()
    # удаляем все кнопки с секциями из фрейма-энтри для заполнения его новыми кнопками
    for widget in entry_frame.winfo_children():
        widget.destroy()
    entry_frame.update()
    # выкладываем имеющиеся разделы
    layout_section_btns(inner_table)

    # отправляем команду на создание нового фрейма, нового Энтри  для добавления разделов внутрь открываемого
    new_entry_name = "entry_" + str(current_id)
    new_entry = new_section_entry(new_entry_name, entry_frame, inner_table, current_id)
    try:
        if path[-1][1] != current_table:
            path.append((current_id, current_table, inner_table))
    except IndexError:
        path.append((current_id, current_table, inner_table))

    for widget in delete_btn_frame.winfo_children():
        widget.destroy()
    delete_btn_frame.update()
    delete_section_btn = Button(delete_btn_frame, text="Удалить текущий раздел",
                                command=lambda: ask_delete_section(path[-1][1], path[-1][2], current_id))
    if len(path) > 0:
        delete_section_btn.pack(side=BOTTOM)

    print(path, " Путь где мы сейчас")

    back_btn.configure(command=lambda: go_to_previous_section(path))
    back_btn.update()


# Вернуться к предыдущему разделу
def go_to_previous_section(path):
    print([i for i in path], "call of go_back")

    try:
        if path[-1][2] != "main":
            path.pop(-1)
            print([i for i in path], " last item is poped")

    except IndexError:
        pop = Tk()
        info_message = Label(pop, text="No way back")
        OK = Button(pop, text="OK", command=lambda: pop.destroy())
        info_message.pack()
        OK.pack()

    last_path = path[-1]
    current_id = last_path[0]
    current_table = last_path[1]
    inner_table = last_path[2]
    open_section(current_id, current_table, inner_table)

    print([i for i in path], "section is openned")


# функция для удаления текущего раздела
def ask_delete_section(parrent_table, table_name, current_id):
    try:
        pop = Tk()
        info_message = Label(pop, text="Вы действительно хотите удалить {}?".format(table_name))
        OK = Button(pop, text="Yes", command=lambda: delete_section(parrent_table, table_name, pop, current_id))
        info_message.pack()
        OK.pack()
    except IndexError:
        pass


# Удаление раздела из базы данных и возврат к предыдущему разделу
def delete_section(parrent_table, table_name, window, current_id):
    try:
        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        q = "DELETE FROM '{}' WHERE section_name='{}'"
        cur.execute(q.format(parrent_table, table_name))
        print(table_name, " имя удалеяемой таблицы")
        conn.commit()
        print("the row was deleted")
        q = "DROP TABLE '{}'"
        cur.execute(q.format(table_name))
        conn.commit()
        print("the table was deleted")

        window.destroy()
        go_to_previous_section(path)
        print("Содержание текущий таблицы")
        dump_help_base(parrent_table)
    except sqlite3.OperationalError:
        if table_name == "main":
            print("Невозможно удалить корневой раздел")
            window.destroy()
        else:
            print("Fatal Error")

    return


# Основной алгоритм
root = Tk()
root.title("Quick respond")
path = []


Data_base_file = "sections.db"
table_name = create_data_base(Data_base_file, "main")
section_frame = Frame(root, background="RED")
section_frame.pack(side=LEFT, fill=X)
section_inner_lvl_frame = Frame(root)
section_inner_lvl_frame.pack(side=RIGHT)

entry_frame = Frame(root)
entry_frame.pack()
section_entry = new_section_entry("main_section_entry", entry_frame, table_name, None)
delete_btn_frame = Frame(root)
delete_btn_frame.pack(side=BOTTOM)

back_btn = Button(root, text="Назад", command=lambda: go_to_previous_section(path))
back_btn.pack(side=BOTTOM)
open_section(None, None, "main")



root.mainloop()



        
        
