from tkinter import *

import json

# create buttons corresponding to the existing sections in data.json
def add_existing_section_as_btn(current_window):
    with open('data.json', 'r') as file: # read support data
        help_data = json.load(file)
    print(current_window)
    k = 0 # var for row for buttons to enter to existing sections
    for key in help_data.keys():
        key_btn = Button(current_window, text=key, width=20, command=lambda key=key: open_section(key))
        key_btn.grid(column=2, row=k)

        k += 1


## Add section  as buttons to the current section to the current window
def add_section(window_name, section_name, entered_section_name):
    # global Current_directory
    # with open('data.json', 'r') as file: # read support data
    #     help_data = json.load(file)
    #
    # #remember the current path
    # new_directory = Current_directory + section_name + "/"
    # Current_directory = new_directory
    # sections = Current_directory.split("/")
    # sections.pop(-1)
    #
    # for i in sections:
    #     dict = {}
    #     count = 0
    #     if help_data.get(i, 'default') is not None:
    #         dict[i] = help_data.get(i)

    #add new element to the current section


    # add section(entry) value as a section to the data.json.load

     # main sections of the support data such as sensors' names

    #add the new section to the file data.json
    # with open('data.json', 'w') as outfile:
    #     json.dump(help_data, outfile, indent=4)
    #
    # n = len(inner_list)
    # new_name_btn = entered_section_name + str(n)
    # new_name_btn = Button(window_name, text=entered_section_name, width=20,
    #                      command=lambda entered_section_name=entered_section_name:
    #                      open_section(entered_section_name))
    # new_name_btn.grid(column=2, row=n)
    with open('data.json', 'r') as file:  # read support data
        help_data_base = json.load(file)
    print(window_name)

    return


##create a new window to go into a section
def open_section(section_name):

    window_name = str(section_name) + "_window"
    window_name = Tk()
    window_name.title(section_name)


    #Place section-named buttons on the window
    #lambda window_name=window_name: add_existing_section_as_btn(window_name)

    section = Entry(window_name)
    section.grid(column=0, row=0)

    record_section_btn = Button(window_name, text="Add new section",
                                command=lambda: add_section(window_name, section_name, section.get()))
    record_section_btn.grid(column=1, row=0)




root = Tk()
root.title("root")


add_existing_section_as_btn(root)

global Current_directory
Current_directory = ""


root.mainloop()
