from tkinter import *
import json
import os
import pickle


def open_section(section_name, new_window):
    print("Open_section is done")
    global Help_base
    global Directory

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
    print("add_existing_sections_as_btns is done")
    global Help_base
    # global Directory
    #
    # Directory = Directory + '/' + current_section
    # sections_tree = []
    # sections_tree = Directory.split('/')
    # sections_tree.pop(0)
    inner_sections = []
    if Help_base.get(current_section, '') is '':
        pass
    else:
        inner_sections.append(Help_base.get(current_section, ''))
    print(inner_sections, " inner sections")

    # create btns corresponding to existing sections
    for key in inner_sections:
        btn_name = Button(current_window, text=key, command=lambda key=key : open_section(key, key))
        btn_name.pack()


def add_section(new_section, current_section, current_window):
    print("add_section is done")
    global Directory
    global Help_base

    Directory = Directory + '/' + current_section
    sections_tree = []
    sections_tree = Directory.split('/')
    sections_tree.pop(0)
    help_base_temp = dict()

    # duplicate Hlp_base to a temporary dictionary
    for key in Help_base:
        help_base_temp[key] = Help_base.get(key)
    print(help_base_temp, "<=help_base_temp before")

    # go inside help_base_temp
    for key in sections_tree:
        value = help_base_temp.get(key, '***')
        if value != '***':
            value = help_base_temp.get(value, '***')   # надо переназначать временный словарь на внутренний
            if current_section is in value:

        else:
            help_base_temp[current_section] = new_section
            print(help_base_temp, "<=help_base_temp after")

    for key in help_base_temp:
        Help_base[key] = help_base_temp.get(key)

    current_section_btn = Button(current_window, text=new_section, textvariable=current_section,
                                 command=lambda : open_section(new_section, new_section,))
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