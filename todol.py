import click
import os
import sys
import json
import re
import logging
from datetime import date
from colored import fg, attr

cl_header = fg(72)
cl_checkbox = fg(125)
cl_tag = fg(125)
cl_deadline = fg(108)
cl_message = fg(253)
cl_id = fg(78)
cl_sepparator = fg(166)
cl_reset = attr('reset')

logging.basicConfig(filename='./app.log', filemode='w',
        format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

dir_path = "./todo"
todo_dic = {
        "id": "",
        "date": "",
        "deadline": "",
        "done": False,
        "tag": "",
        "message": ""
        }

today = date.today().strftime("%Y-%m-%d")
today_file_path = os.path.join(dir_path, today) + ".json"

files_to_check = os.listdir(dir_path)
todo_all_dic = {}

for f in files_to_check:
        with open(os.path.join(dir_path, f),"r") as f_read:
            todo_all_dic[f] = json.load(f_read)


def print_todo(todo, print_all=False):
    if print_all:
        for i, v in todo.items():
            print(("("+i+")").rjust(5," ") + " [%s] %s"%(v["done"], v["message"]))
    else:
        for i, v in todo.items():
            if not v["done"]:
                print(("("+i+")").rjust(5," ") + " [%s] %s"%(v["done"], v["message"]))


def print_todo_all(todo_all_dic, print_all=False):
    todo_all_dic_keys = sorted([*todo_all_dic.keys()], reverse = True)
    for td in todo_all_dic_keys:
        print_output = []
        print_flag = False
        for i, v in todo_all_dic[td].items():
            if not v["done"] or print_all:
                print_flag = True
                checkbox = "x" if v["done"] else " "
                print_output.append(("(" + cl_id +i+ cl_reset + ") ").rjust(5," ") + \
                    "[" + cl_checkbox + checkbox + cl_reset + "] " + \
                     (("[" + cl_tag + v["tag"] + cl_reset + "] ") if v["tag"] != "" else "") + \
                     (("[" + cl_deadline + v["deadline"] + cl_reset + "] ") if
                         v["deadline"] != "" else "") + \
                     cl_message + v["message"] + cl_reset)
        if print_flag:
            print(cl_header + re.sub("\.json","", td) + cl_reset)
            for i in print_output:
                print(i)

def mark_as_done(td_id):
    files_to_check = os.listdir(dir_path)
    ids = {} 
    filename = ""
    file_count = 0
    for f in files_to_check:
        with open(os.path.join(dir_path, f),"r") as f_read:
            ids[f] = [*json.load(f_read).keys()]
    for i, v in ids.items():
        for j in v:
            if j == str(td_id):
                filename = i
                file_count += 1
                break
    if file_count > 1:
        print("There is multiple files with this id")
        print("Task in " + filename + " will be marked")
    if filename == "": 
        print("There is no todo with id " + str(td_id))
    else:
        print(filename)
    logging.debug("Marking " + str(td_id) + " in file " + filename)
    print("Marked " + str(td_id) + " in file " + filename)

    with open(os.path.join(dir_path, filename), "r") as file:
        file_data = json.load(file)

    with open(os.path.join(dir_path, filename), "w") as file:
        file_data[str(td_id)]["done"] = True
        json.dump(file_data, file, indent = 4)

def get_last_id():
    files_to_check = os.listdir(dir_path)
    ids = []
    for f in files_to_check:
        with open(os.path.join(dir_path, f),"r") as f_read:
            ids = ids + ([*json.load(f_read).keys()])
    ids = [int(ele) for ele in ids]
    logging.debug("Last id: " + str(max(ids)) + " from " + str(ids))
    return(int(max(ids)))


def write_todo(new_todo, filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            file_data = json.load(file)
            logging.debug("New todo: loading - "+filename)
    else:
        logging.debug("File not found " + filename)
        file_data = {}
        print("File " + filename + " created")
    with open(filename, "w") as file:
        file_data.setdefault(new_todo["id"], new_todo)
        json.dump(file_data, file, indent = 4)
        logging.debug("New todo: writing - "+filename)

@click.group()
def main():
    """
    TO DO List manager
    """

@main.command()
@click.option("--dir_path", type=click.Path(),
        default=".", 
        help="Deadline till the taks should be done (YYYY-MM-DD)")
def init(dir_path):
    pass


@main.command()
# @click.option("--message", "-m", multiple=True, 
#         help="input message")
@click.option("--full_mode", "--f", is_flag=True, 
        help="Use full add mode")
@click.option("--deadline", default="",
        help="Deadline till the taks should be done (YYYY-MM-DD)")
@click.option("--tag", default="",
        help="tag")
@click.argument("message", required=False, default="")
def add(deadline, message, tag, full_mode):
    """Add todo"""
    if full_mode:
        message = input("Write message:")
        tag = input("Tag:")
        if deadline == "":
            deadline = input("Deadline (YYYY-MM-DD):")
        click.echo(message)
    else:
        click.echo(message)
    new_todo = todo_dic
    new_todo["date"] = today 
    new_todo["deadline"] = deadline 
    new_todo["tag"] = tag 
    new_todo["message"] = message
    new_todo["id"] = str(get_last_id() + 1)

    logging.debug(new_todo)

    write_todo(new_todo, today_file_path)



@main.command()
@click.argument("td_id", required=True)
def done(td_id):
   """Mark ID as done"""
   mark_as_done(td_id)

@main.command()
@click.option("--all", "print_all", is_flag=True,
        help="Print all todos, even unfinished once")
def p(print_all):
   """Print todos"""
   print_todo_all(todo_all_dic, print_all)

if __name__ == "__main__":
    main()
