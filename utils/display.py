from os import system, name
import pandas as pd


def clear_screen():
    system("cls" if name == "nt" else "clear")


def display_list(of):
    objs = of.find()
    output = pd.DataFrame()
    for obj in objs:
        obj = dict(obj.__dict__)
        del obj['_sa_instance_state']
        output = output.append(obj, ignore_index=True)
    print(output)


def crud_menu(of):
    clear_screen()
    print(f"1. Create a {of}")
    plural = of if of[-1] != "y" else of[:-1] + "ie"
    print(f"2. List all {plural}s")
    print(f"3. Delete a {of}")
    selection = int(input("Selection: "))
    while selection < 1 or selection > 3:
        selection = int(input("Selection: "))

    return selection
