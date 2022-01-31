from tkinter import *

import json

# create buttons corresponding to the existing sections in data.txt
def add_existing_section_as_btn():

    with open('data.txt', 'r') as file: # read support data
        help_data = json.load(file)

        k = 0 # var for row for buttons to enter to existing sections
        for i in help_data:
            existing_section_btn = i
            label_name = i + '_label'

            i_bnt = i

            i_btn = Button(root, text=i, width=20, command=lambda: print(i_btn.cget("text")))

            i_btn.grid(column=2, row=k)

            label_name = Label(root, text=label_name) # label that shows that algorithm of giving names is right
            label_name.grid(column=3, row=k)

            k += 1


## define a function to add a title

def add_section():
    with open('data.txt', 'r') as file: # read support data
        help_data = json.load(file)

    new_section = section.get()
    help_data[new_section] = []
    help_data[new_section].append(None) # main sections of the support data such as sensors' names
    with open('data.txt', 'w') as outfile:
        json.dump(help_data, outfile)
    n = len(help_data)
    new_name_btn = new_section + str(n)
    new_name_btn= Button(root, text=new_section, width=20, command=lambda: open_section(Button.cget("text")))
    new_name_btn.grid(column=2, row=n+1)

    return


##open new window to go into a section
def open_section(section_name):
    window_name = str(section_name) + "_window"
    window_name = Tk()
    window_name.title(section_name)

    return




root = Tk()

add_existing_section_as_btn()



section = Entry(root)
section.grid(column=0, row=0)

record_section_btn = Button(root, text="Add new section", command=lambda: add_section())
record_section_btn.grid(column=1, row=0)













root.mainloop()