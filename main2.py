from tkinter import *
import json
import os
import pickle

def add_existing_sections_as_btns(current_window):
    return

def add_section(new_section, current_section, current_window):

    global Help_base
    inner_sections = list(Help_base.get(current_section, ""))
    inner_sections.append(new_section)
    Help_base[current_section] = inner_sections
    current_section_btn = Button(current_window, text=new_section, textvariable=current_section)
    current_section_btn.pack()
    with open("data.txt", "wb", ) as file:
        pickle.dump(Help_base, file)



    # Help_base.get(current_section).append(new_section)
    print(Help_base)
    return Help_base


with open("data.txt", "rb") as file:
    Help_base = pickle.load(file)


root = Tk()
root.title("Quick answer")

new_section_entry = Entry(root)
new_section_entry.pack()

add_section_btn = Button(root, text="Add section", command=lambda: add_section(new_section_entry.get(), "root", root))
add_section_btn.pack()




root.mainloop()