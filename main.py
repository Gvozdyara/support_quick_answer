from tkinter import messagebox
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
import sqlite3

move_path = []
proceed = False


#  replaces the notebook interface with the moving interface
class MoveSectionInterface():
    global move_path

    def __init__(self, section_to_move, elder_parent_tables, parent_frame: Frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()
        print(parent_frame, " main frame object")

        canvas = Canvas(parent_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scr_bar = Scrollbar(parent_frame, orient=VERTICAL, command=canvas.yview)
        scr_bar.pack(side=RIGHT, fill=Y)
        sections_frame = ttk.Frame(parent_frame)
        sections_frame.bind('<Configure>',
                            lambda e: canvas.configure(
                                scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sections_frame, anchor='nw')

        canvas.configure(yscrollcommand=scr_bar.set)


        layout_btns(sections_frame, "main", section_to_move, elder_parent_tables)


# кнопки, которые отображаются в move_section_interface
class SectionToSelect(ttk.Button):
    def __init__(self, window, section_name, section_to_move, elder_parent_tables):
        super().__init__(window, text=section_name,
                         command=lambda: layout_btns(window,
                                                     section_name,
                                                     section_to_move,
                                                     elder_parent_tables))
        self.pack(side=TOP)

#  the back button of the move interface
class BackBtn(ttk.Button):
    def __init__(self, window, section_to_move, elder_parent_tables):
        super().__init__(window, text="Назад", command=self.go_back)
        self.pack()
        self.window = window
        self.section_to_move = section_to_move
        self.elder_parent_tables = elder_parent_tables

    def go_back(self):
        try:
            if move_path[-1] != "main":
                move_path.pop(-1)
            else:
                print("No way back")
        except IndexError:
            print("IndexError")
        layout_btn_secnd_phase(self.window, move_path[-1], self.section_to_move,
                               self.elder_parent_tables)


# функция, которая привязывается к section_to_select
def layout_btns(frame, current_table, section_to_move, elder_parent_tables):
    move_path.append(current_table)
    layout_btn_secnd_phase(frame, current_table, section_to_move,
                           elder_parent_tables)


def layout_btn_secnd_phase(frame, current_table, section_to_move,
                           elder_parent_tables):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.update()
    conn = sqlite3.connect("sections.db")
    cur = conn.cursor()
    q = """SELECT section_name,
                    inner_table_sqlobject
                    from '{}' """
    to_layout_list = cur.execute(q.format(current_table))
    for item in to_layout_list:
        SectionToSelect(frame, item[0], section_to_move, elder_parent_tables)

    ttk.Button(frame, text="Выбрать текущий раздел",
               command=lambda: select_to_move(current_table, frame, section_to_move,
                                              elder_parent_tables)).pack()
    BackBtn(frame, section_to_move, elder_parent_tables)
    print(move_path)


#  funtion that copies the table and deletes it from the previous place
def select_to_move(parent_table, frame, section_to_move,
                   elder_parent_tables):
    # print(elder_table, " elder table, то, откуда все должно быть удалено")
    # print(parent_table, " parent table, то, куда все доллжно быть перемещено")
    # print(section_to_move, " section to move, то что перемещаем")
    conn = sqlite3.connect("sections.db")
    cur = conn.cursor()

    q = """SELECT * from '{}' where section_name=(?)""".format(elder_parent_tables[-1])
    cur.execute(q, (section_to_move,))
    to_insert_tuple = cur.fetchall()

    q = "INSERT INTO '{}' values(?,?,?)".format(parent_table)
    cur.execute(q, (to_insert_tuple[0][0], to_insert_tuple[0][1], to_insert_tuple[0][2]))
    conn.commit()

    q = "DELETE from '{}' where section_name=(?)".format(elder_parent_tables[-1])
    cur.execute(q, (section_to_move,))
    conn.commit()

    layout_frames()
    open_section(None, "main")
    return True


class App(Tk):
    def __init__(self):
        global main_frame, Data_base_file, path
        super().__init__()
        self.title("AI support notebook")

        self.configure(bg="WHITE")

        path = []
        # sb = ttk.Style()
        # sb.configure("TButton", foreground="BLACK", background="RED", textwrap=15)

        # sl = ttk.Style()
        # sl.configure("TLabel", background="RED")

        # sf = ttk.Style()
        # sf.configure("TFrame", background="BLACK")

        Data_base_file = "sections.db"
        create_data_base(Data_base_file, "main")
        create_tbls_list_table(Data_base_file, "tbls_list")

        main_frame = ttk.Frame(self)
        main_frame.pack()

        layout_frames()
        open_section(None, "main")
        SectionInnerLvlLabel(section_inner_lvl_frame, ["Пусто"], [""], ("",""))

        self.mainloop()


# класс используемый при создании кнопки с именем раздела
class SectionBtn(ttk.Button):
    def __init__(self, frame, button_section_name, click_cmnd, current_table):
        super().__init__(frame, text=button_section_name, width=40,
                         command=lambda: click_cmnd(current_table, button_section_name))

        self.pack(fill=X, padx=3, side=TOP)
        self.current_table = current_table
        self.button_section_name = button_section_name
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    # функция создает таблицу, которая устанавливается в столбец section_name таблицы current_table
    def create_inner_table_add_to_the_row(self, current_table):
        # make the table name where to add new sections
        table_name = self.button_section_name
        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        create_table(cur, conn, table_name)
        #     надо добавить свеже созданую таблицу в таблицу выше уровнем в строку с section_id_var
        q = """UPDATE '{}' 
                SET inner_table_sqlobject = '{}'
                WHERE section_name = '{}' """
        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        cur.execute(q.format(current_table, table_name, table_name))
        conn.commit()
        conn.close()

    # выводим содержимое таблицы, куда наводится курсор к разделу (2 столбец)
    def on_enter(self, e):
        global section_inner_lvl_frame

        try:
            for widget in section_inner_lvl_frame.winfo_children():
                widget.destroy()
            section_inner_lvl_frame.update()
        except:
            pass

        time.sleep(0.1)
        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()

        q = """SELECT description from '{}' 
               WHERE section_name = '{}' """
        cur.execute(q.format(self.current_table, self.button_section_name))
        try:
            description = "".join(cur.fetchall()[0])
        except TypeError:
            description = "Нет описания"
        except IndexError:
            description = "Нет описания"

        q = """SELECT section_name from '{}'"""
        try:
            cur.execute(q.format(self.button_section_name))
        except sqlite3.OperationalError:
            pass
        to_layout_sections_raw = [name[0] for name in cur.fetchall()]
        to_layout_sections = list()
        for i in to_layout_sections_raw:
            to_layout_sections.append(i)

        cur.execute(f"""SELECT created_time,
                                last_edit_time from 'tbls_list' 
                    where existing_sections='{self.button_section_name}'
                    """)
        created_edited_time = cur.fetchall()[0]
        conn.close()

        SectionInnerLvlLabel(section_inner_lvl_frame, to_layout_sections,
                             description, created_edited_time)

        return

    def on_leave(self, e):
        return


#  класс используемый для создания Энтри и кнопки добавения к current_table
class NewSectionEntry(Entry):
    def __init__(self, frame, current_table):
        super().__init__(frame)
        get_entry_btn = ttk.Button(frame, text="Добавить раздел", width=40,
                                   command=lambda: add_section(self, current_table))
        self.pack(side=TOP, pady=(10, 0))
        get_entry_btn.pack(side=TOP, pady=(3, 20))


# класс добавления описания к текущему разделу при помощи Text widget
class DescriptionText(Text):
    def __init__(self, frame, parrent_table, current_table):
        super().__init__(frame, height=25, wrap="word", width=40, font="Font 9")
        get_text_btn = ttk.Button(frame, text="Добавить описание к текущему разделу",
                                  command=lambda: add_description(self, parrent_table,
                                                                  current_table))

        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        try:
            cur.execute(f"""SELECT description from '{parrent_table}' 
                                                where section_name='{current_table}'""")
            description = cur.fetchall()
            conn.close()
            description = description[0][0]
            if description == None:
                description = "Нет описания"
        except sqlite3.OperationalError:
            description = "Нет описания"
        conn.close()
        self.insert(END, description)
        get_text_btn.grid(row=0, column=0, sticky=EW)
        self.grid(row=1, column=0, sticky=N)
        self.descr_from_base = description

        # get_text_btn.grid(row=3,column=0)


# поле для вывода содержимого таблицы при наведении курсора на кнопку
class SectionInnerLvlLabel(ttk.Label):
    def __init__(self, frame, to_layout, description, date):
        to_layout.insert(0, f"{date[0]}\t{date[1]}\nСодержание")
        if len(to_layout) < 2:
            to_layout.insert(1, "Здесь пока пусто")
        tbl_of_cntns = "\n".join(to_layout)
        super().__init__(frame, wraplength=220, font="Font 9",
                         justify=LEFT, width=40,
                         text=tbl_of_cntns + "\n" * 2 + str(description[:500]) + "...",
                         padding=(5, 10, 2, 0))
        self.grid(row=0, column=0, sticky=EW)

        # text_widget = Text(frame, height=10, wrap="word", width=40, font="Font 9")
        # text_widget.grid(row=1, column=0, sticky=W)
        #
        # text_widget.insert(END, f"{description[:500]} ...")
        # text_widget.update()


# добавление описания в таблицу
def add_description(text_widget, parent_table, current_table):
    description = text_widget.get(1.0, "end").strip()
    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    q = '''UPDATE "{}" SET description = "{}" 
                        WHERE section_name = "{}"'''
    try:
        cur.execute(q.format(parent_table, description, current_table))
    except sqlite3.OperationalError:
        messagebox.showinfo("Error", "Unable to add note to the main screen")
    conn.commit()


# функция выкладывания кнопок текущего раздела
def layout_section_btns(current_table):
    # dump_help_base(current_table)
    global section_frame, path

    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    q = """SELECT  
        section_name
        from '{}' """
    cur.execute(q.format(current_table))
    to_layout_list = cur.fetchall()
    conn.close()

    for item in to_layout_list:
        SectionBtn(section_frame,
                   item[0],  # section_name
                   open_section,
                   current_table)


# вызов класса move section interface
def call_move_section(table_name, elder_parent_tables, text_widget):
    try:
        move_path.clear()
        MoveSectionInterface(table_name, elder_parent_tables, main_frame)


    except sqlite3.OperationalError:
        print(sqlite3.OperationalError)


# функция подключения к файлу и создания базовой таблицы
def create_data_base(file_name, table_name):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    create_table(cur, conn, table_name)
    return table_name


# создание таблицы после подключения к базе данных
def create_table(cur, conn, table_name):
    q = '''CREATE TABLE IF NOT EXISTS "{}" (
                section_name TEXT UNIQUE,
                inner_table_sqlobject TEXT UNIQUE, 
                description TEXT
                )'''
    cur.execute(q.format(table_name))
    conn.commit()


# функция добавления нового раздела к базе данных, а также вывода ее в интрефейс в виде кнопки
def add_section(entry, current_table):
    global root, section_frame, path
    section_title = entry.get().strip().upper()
    try:
        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        cur.execute("SELECT existing_sections from 'tbls_list'")
        existing_sections_raw_list = cur.fetchall()
        conn.close()
        existing_sections = []
        for i in existing_sections_raw_list:
            existing_sections.append(i[0])
    except sqlite3.OperationalError:
        existing_sections = []
        messagebox.showinfo("Ошибка", "Ошибка проверки наличия раздела в существующей таблице")
    except IndexError:
        existing_sections = []
        print(IndexError)


    if not section_title in existing_sections:
        add_section_to_db(section_title, current_table)
        add_table_to_tbls_list(Data_base_file, section_title)
        new_section_btn = SectionBtn(section_frame, section_title, open_section, current_table)
        new_section_btn.create_inner_table_add_to_the_row(current_table)
    else:
        messagebox.showinfo("Ошибка", "Такая запись уже существует")


# функция добавления нового раздела к базе данных
def add_section_to_db(section_name, current_table):
    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    q = 'INSERT INTO "{}" (section_name) values(?)'
    try:
        cur.execute(q.format(current_table), (section_name,))
        conn.commit()

    except sqlite3.IntegrityError:
        messagebox.showinfo("Ошибка", "Такой раздел уже существует")
        conn.close()




def layout_frames():
    global buttons_frame, section_frame, section_inner_lvl_frame, notebook_frame, back_btn

    for widget in main_frame.winfo_children():
        widget.destroy()

    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.grid(row=0, column=0, columnspan=3, sticky=W)

    sections_raw_frame = Frame(main_frame)
    sections_raw_frame.grid(row=1, column=0, sticky=NS)
    sections_canvas = Canvas(sections_raw_frame)
    sections_scr_bar = ttk.Scrollbar(sections_raw_frame,
                                     orient="vertical",
                                     command=sections_canvas.yview)
    section_frame = ttk.Frame(sections_raw_frame)
    section_frame.bind("<Configure>",
                       lambda e: sections_canvas.configure(
                           scrollregion=sections_canvas.bbox("all")
                       ))
    sections_canvas.create_window((0, 0), window=section_frame, anchor="nw")
    sections_canvas.configure(yscrollcommand=sections_scr_bar.set)

    sections_canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
    sections_scr_bar.pack(side=RIGHT, fill=Y)

    section_inner_lvl_frame = ttk.Frame(main_frame, width=100)
    section_inner_lvl_frame.grid(row=1, column=1, sticky=NSEW, padx=0)

    notebook_frame = ttk.Frame(main_frame)
    notebook_frame.grid(row=1, column=2)

    back_btn = ttk.Button(buttons_frame, text="Назад", command=lambda: go_to_previous_section(path, None))


# Вернуться к предыдущему разделу, спросить о сохранении, в некоторых случаях text_widget=None
def go_to_previous_section(path, text_widget):
    last_path = path[-1]
    current_table = last_path[0]
    inner_table = last_path[1]
    try:
        current_note = text_widget.get(1.0, "end").strip()
        if current_note != text_widget.descr_from_base:
            if messagebox.askokcancel("Сохранение", "Сохранить изменения в записи?"):
                add_description(text_widget, current_table, inner_table)

        try:
            if path[-1][-1] != "main":
                path.pop(-1)

        except IndexError:
            pop = Tk()
            info_message = ttk.Label(pop, text="No way back")
            OK = Button(pop, text="OK", command=lambda: pop.destroy())
            info_message.pack()
            OK.pack()
    except AttributeError:
        print(AttributeError)
        try:
            if path[-1][-1] != "main":
                path.pop(-1)

        except IndexError:
            pop = Tk()
            info_message = ttk.Label(pop, text="No way back")
            OK = Button(pop, text="OK", command=lambda: pop.destroy())
            info_message.pack()
            OK.pack()

    last_path = path[-1]
    current_table = last_path[0]
    inner_table = last_path[1]
    layout_frames()
    open_section(current_table, inner_table)


# функция для удаления текущего раздела
def ask_delete_section(parrent_table, table_name):
    try:
        if messagebox.askokcancel(f'Delete "{table_name}?"',
                                  f'Are you sure you want to delete "{table_name}"'):
            delete_section(parrent_table, table_name)

    except IndexError:
        pass


# Удаление раздела из базы данных и возврат к предыдущему разделу
def delete_section(parrent_table, table_name):
    try:
        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        q = "DELETE FROM '{}' WHERE section_name='{}'"
        cur.execute(q.format(parrent_table, table_name))
        conn.commit()
        q = "DROP TABLE '{}'"
        cur.execute(q.format(table_name))
        conn.commit()

        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        q = "DELETE FROM 'tbls_list' WHERE existing_sections='{}'"
        cur.execute(q.format(table_name))
        conn.commit()
        print(table_name, " the name to delete")

        go_to_previous_section(path, None)
        print("go back")
    except sqlite3.OperationalError:
        messagebox.showinfo("Ошибка", f"{sqlite3.OperationalError}")


def print_crnt_tbl(current_table):
    print("the content of the table that is currently openned")
    conn = sqlite3.connect("sections.db")
    cur = conn.cursor()
    q = f"SELECT * from '{current_table}'"
    cur.execute(q)
    to_print = cur.fetchall()
    conn.close()
    for row in to_print:
        i = 0
        row_to_print = str()
        while i != len(row):
            row_to_print += str(row[i]) + "\t" + "|"
            i += 1
        print(row_to_print)


def create_tbls_list_table(file_name, table_name):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    q = f'''CREATE TABLE IF NOT EXISTS "{table_name}" (
                   existing_sections TEXT UNIQUE,
                   created_time TEXT,
                   last_edit_time TEXT)'''
    cur.execute(q.format(table_name))
    conn.commit()


def add_table_to_tbls_list(file_name, name):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    q = f'''INSERT into "tbls_list" (existing_sections, 
                                    created_time,
                                    last_edit_time) values ("{name}", 
                                                        {get_time()},
                                                        {get_time()})
                                                                    '''
    print(name)
    cur.execute(q)
    conn.commit()


# Открытие раздела базы данных в интерфейсе (current table - то, где сейчас
# inner table - то, что открываем


def open_section(current_table, inner_table):
    global path

    # удаляем все кнопки с секциями из фрейма-кнопок для заполнения его новыми кнопками

    for widget in section_frame.winfo_children():
        widget.destroy()
    section_frame.update()
    # удаляем все кнопки с секциями из фрейма-энтри для заполнения его новыми кнопками
    for widget in notebook_frame.winfo_children():
        widget.destroy()
    notebook_frame.update()
    for widget in buttons_frame.winfo_children():
        widget.pack_forget()
    buttons_frame.update()

    # отправляем команду на создание нового фрейма, нового Энтри  для добавления разделов внутрь открываемого

    NewSectionEntry(section_frame, inner_table)

    # conn = sqlite3.connect(Data_base_file)
    # cur = conn.cursor()

    # выкладываем имеющиеся разделы
    try:
        if path[-1][0] != current_table:
            path.append((current_table, inner_table))
    except IndexError:
        path.append((current_table, inner_table))
    layout_section_btns(inner_table)

    description_text_widget = DescriptionText(notebook_frame, current_table,
                                              inner_table)

    # for widget in delete_btn_frame.winfo_children():
    #     widget.destroy()
    #
    # delete_btn_frame.update()

    back_btn.configure(command=lambda: go_to_previous_section(path, description_text_widget))
    back_btn.update()
    back_btn.pack(side=LEFT)

    move_btn = ttk.Button(buttons_frame, text="Переместить текущий раздел",
                          command=lambda: call_move_section(inner_table,
                                                            path[-2],
                                                            description_text_widget))
    move_btn.pack(side=LEFT)

    delete_section_btn = ttk.Button(buttons_frame, text="Удалить текущий раздел",
                                    command=lambda: ask_delete_section(path[-1][-2],
                                                                       path[-1][-1]))
    delete_section_btn.pack(side=LEFT)
    if len(path) > 1:
        # delete_section_btn.pack()
        pass


#  this function returns string YYYY-MM-DD HH:MM:SS
def get_time():
    return str(datetime.now())[:-7]


if __name__ == "__main__":
    app = App()
