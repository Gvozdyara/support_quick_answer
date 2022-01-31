from tkinter import *

import json

# create buttons corresponding to the existing sections in data.txt
def add_existing_section_as_btn():

    with open('data.json', 'r') as file: # read support data
        help_data = json.load(file)

        k = 0 # var for row for buttons to enter to existing sections
        for i in help_data:
            i_btn = Button(root, text=i, width=20, command=lambda i=i: open_section(i))

            i_btn.grid(column=2, row=k)

            k += 1


## define a function to add a title

def add_section(window, section_name):
    with open('data.json', 'r') as file: # read support data
        help_data = json.load(file)

    new_section = section.get()
    help_data[new_section] = []
    help_data[new_section].append(None) # main sections of the support data such as sensors' names
    with open('data.json', 'w') as outfile:
        json.dump(help_data, outfile)
    n = len(help_data)
    new_name_btn = new_section + str(n)
    new_name_btn= Button(root, text=new_section, width=20,
                         command=lambda new_section=new_section:
                         open_section(new_section))
    new_name_btn.grid(column=2, row=n+1)

    return


##open new window to go into a section
def open_section(section_name):


    window_name = str(section_name) + "_window"
    window_name = Tk()
    window_name.title(section_name)

    add_existing_section_as_btn()

    section = Entry(window_name)
    section.grid(column=0, row=0)

    record_section_btn = Button(window_name, text="Add new section",
                                command=lambda window_name=window_name: add_section(window_name, section.get()))
    record_section_btn.grid(column=1, row=0)

    with open('data.json', 'r') as file: # read support data
        help_data = json.load(file)
    inner_sections =  help_data.get(section_name)
    print(len(inner_sections))
    k = 0  # var for row for buttons to enter to existing sections
    for i in inner_sections:
        i_btn = Button(window_name, text=i, width=20, command=lambda i=i: open_section(i))

        i_btn.grid(column=2, row=k)

        k += 1
    window_name.mainloop()
    return




root = Tk()

add_existing_section_as_btn()



section = Entry(root)
section.grid(column=0, row=0)

record_section_btn = Button(root, text="Add new section", command=lambda: add_section(root, section.get()))
record_section_btn.grid(column=1, row=0)



root.mainloop()
