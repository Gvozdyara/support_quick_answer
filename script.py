import sqlite3
from main import get_time
from main import print_crnt_tbl

with open("string.txt", "r", encoding="utf8") as f:
    string1 = f.read()
exceptions = ["'", '"', '\\', "{", "}", ";"]
for i in string1:
    if i in exceptions:
        i = "'" + i + "'"
        print(i)
descr_list = list()
ind=int(0)
while ind in range(len(string1)):
    descr_list.append(string1[ind:ind+500])
    ind+=500
print("string splitted")



conn = sqlite3.connect("sections.db")
cur = conn.cursor()

cur.execute(f"""
                SELECT existing_section
                  FROM tbls_list""")
main_list_raw = cur.fetchall()
main_list = []
for i in main_list_raw:
    main_list.append(i[0])


ind=0
for i in main_list:
    try:
        cur.execute(f'''CREATE TABLE IF NOT EXISTS "{str(i)}" (
                                                                section_name TEXT UNIQUE
                                                                )''')
        print(f"{i} table is created")
        try:
            for j in range(30):
                try:
                    name = f'{str(j)}_{str(i)}'
                    cur.execute(f"""CREATE TABLE IF NOT EXISTS '{name}' (
                                                            section_name TEXT UNIQUE,
                                                            inner_table_sqlobject TEXT UNIQUE
                                                            )""")
                    print(f'{name} is created')
                    cur.execute(f'''INSERT into "tbls_list" (existing_section,
                                                            description,
                                                            parent_table,
                                                            created_time,
                                                            last_edit_time)
                                                    values (?,?,?,?,?)''',
                                                           (name,
                                                            string1[ind:ind+555],
                                                            i,
                                                            get_time(),
                                                            get_time()))
                    ind+=555
                    print(f'{name} is added to tbls_list')

                    cur.execute(f"""INSERT INTO '{i}' (section_name)
                                            VALUES('{name}')""")
                    print(f'{name} is added to {i}')
                except sqlite3.IntegrityError:
                    print("error adding new line to a table", j)
                    continue
        except sqlite3.IntegrityError:
            print("exception adding to tbls_list", f'{str(j)}+{str(i)}')
            continue
    except sqlite3.IntegrityError:
        print("exception creating new table")
        continue


conn.commit()





# print_crnt_tbl("34")