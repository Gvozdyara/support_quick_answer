from tkinter import *

import json

# create buttons corresponding to the existing sections in data.json
def add_existing_section_as_btn(current_window):
    with open('data.json', 'r') as file: # read support data
        help_data = json.load(file)

        for key in help_data:
            if
        k = 0 # var for row for buttons to enter to existing sections
        for i in help_data:
            i_btn = Button(current_window, text=i, width=20, command=lambda i=i: open_section(i))

            i_btn.grid(column=2, row=k)

            k += 1


## Add section  as buttons to the current section to the current window
def add_section(window_name, section_name, entered_section_name):
    with open('data.json', 'r') as file: # read support data
        help_data = json.load(file)
    # add section(entry) value as a section to the data.json.load
    current_section_dict = help_data[section_name]
    current_section_dict = dict()
    current_section_dict[entered_section_name] = "null" # main sections of the support data such as sensors' names

    #add the new section to the file data.json
    with open('data.json', 'w') as outfile:
        json.dump(current_section_dict, outfile, indent=4)

    n = len(current_section_dict)
    new_name_btn = entered_section_name + str(n)
    new_name_btn = Button(window_name, text=entered_section_name, width=20,
                         command=lambda entered_section_name=entered_section_name:
                         open_section(entered_section_name))
    new_name_btn.grid(column=2, row=n)

    return


##create a new window to go into a section
def open_section(section_name):

    window_name = str(section_name) + "_window"
    window_name = Tk()
    window_name.title(section_name)

    #Place section-named buttons on the window
    lambda window_name=window_name: add_existing_section_as_btn(window_name)

    section = Entry(window_name)
    section.grid(column=0, row=0)

    record_section_btn = Button(window_name, text="Add new section",
                                command=lambda window_name=window_name: add_section(window_name, section_name, section.get()))
    record_section_btn.grid(column=1, row=0)


root = Tk()

add_existing_section_as_btn(root)







root.mainloop()
