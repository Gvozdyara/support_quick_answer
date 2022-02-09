from tkinter import *
import json
import os
import pickle


def open_section(section_name, new_window, directory):
    global Help_base

    new_window = Tk()
    new_window.title(section_name)



    new_section_entry = Entry(new_window)
    new_section_entry.pack()

    add_section_btn = Button(new_window, text="Add section",
                             command=lambda: add_section(new_section_entry.get(), section_name, new_window))
    add_section_btn.pack()

    add_existing_sections_as_btns(section_name, new_window)



    return


def add_existing_sections_as_btns(current_section, current_window):
    global Help_base


    inner_sections = list(Help_base.get(current_section, ''))

    # create btns corresponding to existing sections
    for key in inner_sections:
        btn_name = str(key) + "_btn"
        btn_name = Button(current_window, text=key, command=lambda key=key : open_section(key, key))
        btn_name.pack()

    print(Help_base)
    return

def add_section(new_section, current_section, current_window):
    print(new_section)
    global Directory
    global Help_base

    Directory = Directory + '/' + current_section
    sections_tree = []
    sections_tree = "/".split(Directory)
    help_base_temp = Help_base
    for item in sections_tree:
        ''.join(item)
        inner_item = help_base_temp.get(item, '***')
        if inner_item != '***':
            help_base_temp = dict(help_base_temp.get(item))
        else:
            help_base_temp[current_section] = new_section

    inner_sections = list(Help_base.get(current_section, "")) #need to fix this to open inner key-value pairs
    inner_sections.append(new_section)
    Help_base[current_section] = inner_sections
    current_section_btn = Button(current_window, text=new_section, textvariable=current_section,
                                 command=lambda new_section=new_section : open_section(new_section, new_section, Directory))
    current_section_btn.pack()
    with open("data.txt", "wb", ) as file:
        pickle.dump(Help_base, file)



    # Help_base.get(current_section).append(new_section)
    print(Help_base)
    return Help_base

try:
    with open("data.txt", "rb") as file:
        Help_base = pickle.load(file)
except:
    print("empty dict")
    Help_base = dict()

root = Tk()
root.title("Quick answer")
add_existing_sections_as_btns("root", root)

# is used to keep track of the keys in Help_base
Directory = ""

new_section_entry = Entry(root)
new_section_entry.pack()

add_section_btn = Button(root, text="Add section", command=lambda: add_section(new_section_entry.get(), "root", root))
add_section_btn.pack()




root.mainloop()