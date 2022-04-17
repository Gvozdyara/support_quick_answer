from tkinter import messagebox
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk
import sqlite3

proceed = False


 #  search interface
 #  class of the search interface, appears instead of the description text
#
#  When the search button is clicked the search frame will appear
#  in the place of the notebook_frame.
#  An entry widget will appear where user inputs a string
#  search in table name, in description buttons will be placed lower,
#  when clicked the strip.upper string will be to search
#  after that from each table from tbls-list (description or table name) will be selected,
#  changed to lower case and  checked if the search string is there or no
#  the list of the descriptions (tables) as buttons will be shown in the scrollable frame
#  description should be shortened to +-100 symbols - when clicked:
# select parents table from tbls-list and open_section(parent_table, current_table)
#


class SearchInTableDescription:
    def __init__(self, frame):

        self.layout_frame = ttk.Frame(frame)
        self.search_entry = Entry(frame, width=40)
        self.search_table_name = ttk.Button(frame, text="Search name", command=lambda:self.set_search_mode("table"))
        self.search_description = ttk.Button(frame, text="Search note",
                                             command=lambda: self.set_search_mode("description"))
        self.search_string = None
        self.table_description_dict = dict()
        self.found_tables = list()
        self.search_mode = None

        self.search_entry.grid(row=0, column=0, columnspan=2, pady=(5,0))
        self.search_table_name.grid(row=1, column=0)
        self.search_description.grid(row=1, column=1)
        self.layout_frame.grid(row=2, column=0, columnspan=2)

    def set_search_mode(self, mode):
        self.search_mode = mode
        self.get_search_string()

    def get_search_string(self):
        self.search_string = self.search_entry.get().strip().upper()
        self.search_entry.delete(0, "end")
        self.get_table_name_description_dict()

    def get_table_name_description_dict(self):

        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        try:
            cur.execute(f"""SELECT existing_section, description, parent_table
                              FROM tbls_list""")
            table_description_list = cur.fetchall()
            for i in table_description_list:
                self.table_description_dict[i[0]] = (i[1], i[2])
        except sqlite3.OperationalError:
            print(sqlite3.OperationalError)
        conn.close()
        if self.search_mode == "table":
            self.find_table_name()
        else:
            self.find_from_description()


    def find_table_name(self):
        for key in self.table_description_dict:
            print(key)
            if self.search_string in key.upper():
                self.found_tables.append(key)
        self.layout_found_table()

    def find_from_description(self):
        for (key, value) in self.table_description_dict.items():
            try:
                if self.search_string.lower() in value[0].lower():
                    #  make a short substring from description (i[1])
                    if len(value[0])>202:
                        start_index = value[0].find(self.search_string)
                        if start_index>99:
                            short_description = value[0][start_index-100:start_index+100]
                        else:
                            short_description = value[0][0:start_index+200]
                    else:
                        short_description = value[0]
                    self.table_description_dict[key] = (short_description, self.table_description_dict[key][1])
                    self.found_tables.append(key)
            except AttributeError:
                print(AttributeError)

        if self.search_mode == "table":
            self.layout_found_table()
        else:
            self.layout_description()


    def layout_found_table(self):
        for i in self.found_tables:
            FoundResult(self.layout_frame, i, self)

    def layout_description(self):
        print("layout_description")
        for i in self.found_tables:
            FoundResult(self.layout_frame, self.table_description_dict[i][0], i, self)
            print(i, "inner table")



class FoundResult(ttk.Button):
    def __init__(self, frame, string, table, search_interface):
        super().__init__(frame, text=string, width=40,
                         command=lambda: open_section(search_interface.table_description_dict[table][1], table))
        self.pack()


def layout_search_interface(frame):
    print("layout_search_interface()")
    for widget in frame.winfo_children():
        widget.destroy()
    SearchInTableDescription(frame)


#  replaces the notebook interface with the moving interface
class MoveSectionInterface:

    def __init__(self, section_to_move):
        for widget in main_frame.winfo_children():
            widget.destroy()

        canvas = Canvas(main_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scr_bar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
        scr_bar.pack(side=RIGHT, fill=Y)
        sections_frame = ttk.Frame(main_frame)
        sections_frame.bind('<Configure>',
                            lambda e: canvas.configure(
                                scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sections_frame, anchor='nw')

        canvas.configure(yscrollcommand=scr_bar.set)

        layout_btns(sections_frame, "main", section_to_move)


# кнопки, которые отображаются в move_section_interface
class SectionToSelect(ttk.Button):
    def __init__(self, window, section_name, section_to_move):
        super().__init__(window, text=section_name, width=40,
                         command=lambda: layout_btns(window,
                                                     section_name,
                                                     section_to_move))
        self.pack(side=TOP)


#  the back button of the move interface
class BackBtn(ttk.Button):
    def __init__(self, window, current_table, section_to_move):
        super().__init__(window, text="Назад", command=self.go_back, width=40)
        self.pack()
        self.window = window
        self.section_to_move = section_to_move
        self.current_table = current_table

    def go_back(self):
        conn = sqlite3.connect()
        cur = conn.cursor()
        cur.execute(f"""
                        SELECT parent_table
                          FROM 'tbls_list'
                         WHERE existing_section='{self.current_table}'
                        """)
        parent_table = cur.fetchall()[0][0]
        conn.close()
        layout_btn_secnd_phase(self.window, parent_table, self.section_to_move)


# функция, которая привязывается к section_to_select
def layout_btns(frame, current_table, section_to_move):
    layout_btn_secnd_phase(frame, current_table, section_to_move)


def layout_btn_secnd_phase(frame, current_table, section_to_move):
    for widget in frame.winfo_children():
        widget.destroy()
    frame.update()
    conn = sqlite3.connect("sections.db")
    cur = conn.cursor()
    q = """SELECT section_name
             from '{}' """
    cur.execute(q.format(current_table))
    to_layout_list = cur.fetchall()
    conn.close()
    for item in to_layout_list:
        SectionToSelect(frame, item[0], section_to_move)

    ttk.Button(frame, text="Выбрать текущий раздел", width=40,
               command=lambda: select_to_move(current_table, section_to_move)).pack()
    BackBtn(frame, current_table, section_to_move)

#  funtion that copies the table and deletes it from the previous place
def select_to_move(parent_table, section_to_move):
    # print(elder_table, " elder table, то, откуда все должно быть удалено")
    # print(parent_table, " parent table, то, куда все доллжно быть перемещено")
    # print(section_to_move, " section to move, то что перемещаем")

    #  take the parent table, description of the section to move
    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    cur.execute(f"""
                SELECT parent_table, description
                  FROM 'tbls_list'
                 WHERE existing_section='{section_to_move}'
                """)
    to_move_tuple = cur.fetchall()[0]
    print(to_move_tuple)

    #  change the parent table of the section to move
    cur.execute(f"""UPDATE 'tbls_list'
                       SET parent_table='{parent_table}'
                     WHERE existing_section='{section_to_move}'
                    """)
    # conn.commit()

    #  change the layout of the previous parent_table
    cur.execute(f"""DELETE from '{to_move_tuple[0]}'
                     WHERE section_name='{section_to_move}'
                    """)
    # conn.commit()

    #  change the layout of the new parent table
    cur.execute(f"""INSERT INTO '{parent_table}'(section_name)
                            VALUES ('{section_to_move}')
                        """)
    conn.commit()

    layout_frames()
    open_section(parent_table, section_to_move)


class App(Tk):
    def __init__(self):
        global main_frame, Data_base_file, current_section_var, current_section_indicator, app
        super().__init__()
        self.title("AI support notebook")
        self.configure(background="#F4F6F7")

        current_section_var = StringVar()

        sf = ttk.Style()
        sf.configure("Mainframe.TFrame", background="#FEF5E7")
        sf.configure("Label.TLabel", background="#FEF5E7")

        Data_base_file = "sections.db"
        create_data_base(Data_base_file, "main")
        create_tbls_list_table(Data_base_file, "tbls_list")

        main_frame = ttk.Frame(self, style="Mainframe.TFrame")
        main_frame.pack()

        layout_frames()
        open_section(None, "main")
        SectionInnerLvlLabel(section_inner_lvl_frame, ["Пусто"], [""], ("", ""))

        self.mainloop()


# класс используемый при создании кнопки с именем раздела
class SectionBtn(ttk.Button):
    def __init__(self, frame, button_section_name, click_cmnd, current_table):
        self.section_name = StringVar(value=button_section_name)
        super().__init__(frame, textvariable=self.section_name,
                         width=40, command=lambda: click_cmnd(current_table, self.section_name.get()))

        self.pack(fill=X, padx=3, side=TOP)
        self.current_table = current_table
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-3>", self.section_btn_right_clck_menu)
        self.frame = frame
        self.right_clck_menu = Menu(self.frame, tearoff=0)
        self.right_clck_menu.add_command(label="Rename", command=self.rename_section_interface)

    # функция создает новую таблицу current_table
    def create_inner_table_add_to_the_row(self, current_table):
        # make the table name where to add new sections
        table_name = self.section_name.get()
        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        create_table(cur, conn, table_name)

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

        q = """SELECT description from 'tbls_list' 
               WHERE existing_section = '{}' """
        cur.execute(q.format(self.section_name.get()))
        try:
            description = "".join(cur.fetchall()[0])
        except TypeError:
            description = "Нет описания"
        except IndexError:
            description = "Нет описания"

        q = """SELECT section_name from '{}'"""
        try:
            cur.execute(q.format(self.section_name.get()))
        except sqlite3.OperationalError:
            pass
        to_layout_sections_raw = [name[0] for name in cur.fetchall()]
        to_layout_sections = list()
        for i in to_layout_sections_raw:
            to_layout_sections.append(i)

        cur.execute(f"""SELECT created_time,
                                last_edit_time from 'tbls_list' 
                    where existing_section='{self.section_name.get()}'
                    """)
        created_edited_time = cur.fetchall()[0]
        conn.close()

        SectionInnerLvlLabel(section_inner_lvl_frame, to_layout_sections,
                             description, created_edited_time)

        return

    def on_leave(self, e):
        return

    def rename_section_interface(self):
        self.rename_win = Toplevel(self.frame)
        self.entry_widget = Entry(self.rename_win)
        self.entry_widget.pack()
        self.rename_button = ttk.Button(self.rename_win, text="Rename", command=self.rename_section)
        self.rename_button.pack()
        self.rename_win.mainloop()

    def rename_section(self):
        new_table_name = self.entry_widget.get().strip().upper()
        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        try:
            cur.execute(f"""UPDATE tbls_list 
                               SET existing_section='{new_table_name}'
                             WHERE existing_section='{self.section_name.get()}'""")
            cur.execute(f"""UPDATE tbls_list SET parent_table='{new_table_name}'
                             WHERE parent_table='{self.section_name.get()}'""")
            cur.execute(f""" ALTER TABLE '{self.section_name.get()}' 
                               RENAME TO '{new_table_name}' """)
            cur.execute(f"""UPDATE '{self.current_table}' 
                               SET section_name='{new_table_name}'
                             WHERE section_name='{self.section_name.get()}'""")
            conn.commit()
            self.section_name.set(new_table_name)
            self.rename_win.destroy()
        except sqlite3.OperationalError:
            messagebox.showinfo("Error", f'{sqlite3.OperationalError}')
            conn.close()
        except sqlite3.IntegrityError:
            messagebox.showinfo("Error", f'{sqlite3.IntegrityError}')
            conn.close()
        # open_section(self.current_table, self.section_name.get())

    def section_btn_right_clck_menu(self, event):
        try:
            self.right_clck_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_clck_menu.grab_release()


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
    def __init__(self, frame, current_table):
        super().__init__(frame, height=25, wrap="word", width=40, font="Font 9")
        get_text_btn = ttk.Button(frame, text="Добавить описание к текущему разделу",
                                  command=lambda: add_description(self,
                                                                  current_table))

        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()
        try:
            cur.execute(f"""SELECT description from 'tbls_list' 
                             WHERE existing_section ='{current_table}'""")
            description = cur.fetchall()
            conn.close()
            description = description[0][0]
            if description == None:
                description = "Нет описания"
        except IndexError:
            description = "Нет описания"
        conn.close()
        self.insert(END, description)
        get_text_btn.grid(row=0, column=0, sticky=EW)
        self.grid(row=1, column=0, sticky=N)
        self.descr_from_base = description
        self.table = current_table

    def update_descr_from_base(self, new_description):
            self.descr_from_base = new_description

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
                         padding=(5, 10, 2, 0), style="Label.TLabel")
        self.grid(row=0, column=0, sticky=EW)

        # text_widget = Text(frame, height=10, wrap="word", width=40, font="Font 9")
        # text_widget.grid(row=1, column=0, sticky=W)
        #
        # text_widget.insert(END, f"{description[:500]} ...")
        # text_widget.update()


# добавление описания в таблицу
def add_description(text_widget, current_table):
    description = text_widget.get(1.0, "end").strip()
    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    q = '''UPDATE "tbls_list" SET description = "{}" 
            WHERE existing_section = "{}"'''
    try:
        cur.execute(q.format(description, current_table))
        conn.commit()
        cur.execute(f"""UPDATE 'tbls_list' set last_edit_time = '{get_time()}' 
                                        where existing_section='{current_table}'""")
        conn.commit()
    except sqlite3.OperationalError:
        messagebox.showinfo("Error", "Unable to add note to the main screen")
    conn.close()

    text_widget.update_descr_from_base(description)


# функция выкладывания кнопок текущего раздела
def layout_section_btns(current_table):
    # dump_help_base(current_table)
    global section_frame

    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    q = """SELECT section_name
             FROM '{}' """
    cur.execute(q.format(current_table))

    to_layout_list = cur.fetchall()
    conn.close()
    #  experimental feature to sort by last edit
    # sections_list = []
    # for i in to_layout_list:
    #     sections_list.append(i[0])
    # cur.execute('''SELECT existing_section,
    #                         last_edit_time
    #             from "tbls_list" where existing_section="{}"
    #             "{}"'''.format(sections_list[0], "AND where existing_section=".join(sections_list[1:])))
    # section_edit_time = cur.fetchall()
    # conn.close()
    # print(section_edit_time, "section edit_time list of tuples")
    # modified_list = []
    # for tup in section_edit_time:
    #     modified_list.append(time_to_sec(tup[1]))
    # sorted(modified_list, key=lambda seconds: seconds[1])

    for item in to_layout_list:
        SectionBtn(section_frame,
                   item[0],  # section_name
                   open_section,
                   current_table)


# функция подключения к файлу и создания базовой таблицы
def create_data_base(file_name, table_name):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    create_table(cur, conn, table_name)
    return table_name


# создание таблицы после подключения к базе данных
def create_table(cur, conn, table_name):
    q = '''CREATE TABLE IF NOT EXISTS "{}" (
                section_name TEXT UNIQUE
                )'''
    cur.execute(q.format(table_name))
    conn.commit()


def print_crnt_tbl(current_table):
    print("the content of the table that is currently openned")
    conn = sqlite3.connect("sections.db")
    cur = conn.cursor()
    q = f"SELECT * from '{current_table}'"
    cur.execute(q)
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
                   existing_section TEXT UNIQUE, 
                   description TEXT,
                   parent_table TEXT,                   
                   created_time TEXT,
                   last_edit_time TEXT)'''
    cur.execute(q.format(table_name))
    conn.commit()
    try:
        cur.execute(f"""INSERT INTO tbls_list(existing_section, parent_table)
                             VALUES ('main', 'None1')""")
    except sqlite3.IntegrityError:
        print("Inserting parent table into main failure")
        pass
    conn.commit()


# функция добавления нового раздела к базе данных, а также вывода ее в интрефейс в виде кнопки
def add_section(entry, current_table):
    global root, section_frame
    section_title = entry.get().strip().upper()
    if section_title != "":
        entry.delete(0, 'end')
        # if not section_title in existing_sections:
    if add_section_to_db(section_title, current_table):
        add_table_to_tbls_list(Data_base_file, section_title, current_table)
        new_section_btn = SectionBtn(section_frame, section_title, open_section, current_table)
        new_section_btn.create_inner_table_add_to_the_row(current_table)
        # else:
        #     messagebox.showinfo("Ошибка", "Такая запись уже существует")
    else:
        pass


# функция добавления нового раздела к базе данных
def add_section_to_db(section_name, current_table):
    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    q = 'INSERT INTO "{}" (section_name) values(?)'
    try:
        cur.execute(q.format(current_table), (section_name,))
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        messagebox.showinfo("Ошибка", "Такой раздел уже существует")
        conn.close()
        return False


def add_table_to_tbls_list(file_name, name, parent_table):
    conn = sqlite3.connect(file_name)
    cur = conn.cursor()
    q = f'''INSERT into "tbls_list" (existing_section,
                                    parent_table, 
                                    created_time,
                                    last_edit_time) 
                            values ("{name}",
                                    "{parent_table}",
                                    "{get_time()}",
                                    "{get_time()}")
                                                                    '''
    cur.execute(q)
    conn.commit()


def layout_frames():
    global buttons_frame, section_frame, section_inner_lvl_frame, notebook_frame, back_btn, current_section_indicator

    for widget in main_frame.winfo_children():
        widget.destroy()

    buttons_frame = ttk.Frame(main_frame, style="Mainframe.TFrame")
    buttons_frame.grid(row=0, column=0, columnspan=3, sticky=W)
    current_section_indicator = Label(buttons_frame, textvariable=current_section_var, background="#FEF5E7",
                                      font="BOLD")

    sections_raw_frame = ttk.Frame(main_frame, style="Mainframe.TFrame")
    sections_raw_frame.grid(row=1, column=0, sticky=NS)
    sections_canvas = Canvas(sections_raw_frame, background="#FEF5E7")
    sections_scr_bar = ttk.Scrollbar(sections_raw_frame,
                                     orient="vertical",
                                     command=sections_canvas.yview)
    section_frame = ttk.Frame(sections_raw_frame, style="Mainframe.TFrame")
    section_frame.bind("<Configure>",
                       lambda e: sections_canvas.configure(
                           scrollregion=sections_canvas.bbox("all")
                       ))
    sections_canvas.create_window((0, 0), window=section_frame, anchor="nw")
    sections_canvas.configure(yscrollcommand=sections_scr_bar.set)

    sections_canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
    sections_scr_bar.pack(side=RIGHT, fill=Y)

    section_inner_lvl_frame = ttk.Frame(main_frame, width=300, style="Mainframe.TFrame")
    section_inner_lvl_frame.grid(row=1, column=1, sticky=NSEW, padx=0)

    notebook_frame = ttk.Frame(main_frame, style="Mainframe.TFrame")
    notebook_frame.grid(row=1, column=2)

    back_btn = ttk.Button(buttons_frame, text="Назад", command=None)


# Вернуться к предыдущему разделу, спросить о сохранении, в некоторых случаях text_widget=None
def go_to_previous_section(current_table, text_widget):
    try:
        current_note = text_widget.get(1.0, "end").strip()
        if current_note != text_widget.descr_from_base:
            if messagebox.askokcancel("Сохранение",
                                      f"Сохранить изменения в записи {text_widget.table}?"):
                add_description(text_widget, text_widget.table)

    except AttributeError:
        print(AttributeError)

    conn = sqlite3.connect(Data_base_file)
    cur = conn.cursor()
    cur.execute(f"""SELECT parent_table
                      FROM tbls_list
                     WHERE existing_section='{current_table}'""")
    sections_tuple = cur.fetchall()
    conn.close()

    try:
        layout_frames()
        open_section(sections_tuple[0][0], current_table)
    except IndexError:
        layout_frames()
        open_section(None, "main")


# функция для удаления текущего раздела
def ask_delete_section(parent_table, table_name):
    try:
        if messagebox.askokcancel(f'Delete "{table_name}?"',
                                  f'Are you sure you want to delete "{table_name}"'):
            delete_section(table_name)

    except IndexError:
        pass


# Удаление раздела из базы данных и возврат к предыдущему разделу
def delete_section(table_name):
    try:

        conn = sqlite3.connect(Data_base_file)
        cur = conn.cursor()

        #  find parent table
        cur.execute(f"""SELECT parent_table FROM tbls_list
                         WHERE existing_section='{table_name}'""")
        parent_table = cur.fetchall()[0][0]

        #  delete the row from parent table
        cur.execute(f"DELETE FROM '{parent_table}' WHERE section_name='{table_name}'")

        #   delete the table
        cur.execute(f"DROP TABLE '{table_name}'")

        #  delete the row from tbls_list table
        cur.execute(f"DELETE FROM tbls_list WHERE existing_section='{table_name}'")
        conn.commit()
        go_to_previous_section(parent_table, None)
    except sqlite3.OperationalError:
        messagebox.showinfo("Ошибка", "Нельзя удалить основной раздел")


# вызов класса move section interface
def call_move_section(table_name):
    try:
        MoveSectionInterface(table_name)


    except sqlite3.OperationalError:
        print(sqlite3.OperationalError)


# Открытие раздела базы данных в интерфейсе (current table - то, где сейчас
# inner table - то, что открываем


def open_section(current_table, inner_table):
    #  удаляем все кнопки с секциями из фрейма-кнопок для заполнения его новыми кнопками

    for widget in section_frame.winfo_children():
        widget.destroy()
    section_frame.update()
    #  отправляем команду на создание нового фрейма, нового Энтри  для добавления разделов внутрь открываемого
    NewSectionEntry(section_frame, inner_table)
    # удаляем все кнопки с секциями из фрейма-энтри для заполнения его новыми кнопками
    for widget in notebook_frame.winfo_children():
        widget.destroy()
    notebook_frame.update()
    # выкладываем имеющиеся разделы

    layout_section_btns(inner_table)
    for widget in buttons_frame.winfo_children():
        widget.pack_forget()
    buttons_frame.update()

    description_text_widget = DescriptionText(notebook_frame, inner_table)

    back_btn.configure(command=lambda: go_to_previous_section(current_table, description_text_widget))
    back_btn.update()
    back_btn.pack(side=LEFT)

    move_btn = ttk.Button(buttons_frame, text="Переместить текущий раздел",
                          command=lambda: call_move_section(inner_table))
    move_btn.pack(side=LEFT)

    delete_section_btn = ttk.Button(buttons_frame, text="Удалить текущий раздел",
                                    command=lambda: ask_delete_section(current_table,
                                                                       inner_table))
    delete_section_btn.pack(side=LEFT)

    search_btn = ttk.Button(buttons_frame, text="Поиск",
                            command=lambda: layout_search_interface(notebook_frame))
    search_btn.pack(side=RIGHT, pady=(5,0), padx=(10,0))

    current_section_var.set(f"../{current_table}/{inner_table}")
    current_section_indicator.pack()


#  this function returns string YYYY-MM-DD HH:MM:SS
def get_time():
    return str(datetime.now())[:-7]


def time_to_sec(str_time):
    date = str_time.split(" ")[0]
    date_split = date.split("-")
    print(date)
    days = int(date_split[0]) * 365 * 0.25 + int(date_split[1]) * 30.45 + int(date_split[2])

    time = str_time.split(" ")[1]
    time_split = time.split(":")
    seconds = int(time_split[0]) * 3600 + int(time_split[1]) * 60 + int(time_split[2])
    total_seconds = days * 86400 + seconds
    return total_seconds


if __name__ == "__main__":
    global app
    app = App()