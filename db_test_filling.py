import sqlite3
from main_raw import *
global Data_base_file
Data_base_file = "sections.db"

conn = sqlite3.connect("sections.db")
cur = conn.cursor()

# try:
#     for i in range(1000):
#         add_table_to_tbls_list("sections.db", i, "main")
# except:
#     pass
#
#
# cur.execute(f"SELECT existing_section from tbls_list")
# tables_list_scripty = cur.fetchall()
# tables_list = []
# print(tables_list)
#
# for i in tables_list_scripty:
#     tables_list.append(i[0])
#
# for i in tables_list:
#     create_table(cur, conn, i)
#
# for i in tables_list:
#     for k in range(20):
#         cur.execute(f'INSERT INTO "{i}" (section_name) values(f"{str(i)}+{str(k)}")')
#
# conn = sqlite3.connect()
# cur = conn.cursor()
# for i in tables_list:
#     cur.execute(f'''UPDATE "tbls_list" SET description = "{str(i)*int(i)}"
#             WHERE existing_section = "{i}"''')

# cur.execute("SELECT existing_section from tbls_list")
# tables_list_scripty = cur.fetchall()
# tables_list = []
#
# for i in tables_list_scripty:
#     tables_list.append(i[0])
#
# for i in tables_list:
#     try:
#         cur.execute(f'INSERT into main (section_name) values({str(i)})')
#     except:
#         pass

# print(tables_list)

# for i in tables_list_scripty:
#     tables_list.append(i[0])
# cur.execute(f"")
# print_crnt_tbl("1")

