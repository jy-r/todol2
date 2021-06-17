import click
import os
import sys
import json
import re
import logging
import readline
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
date_format = "%Y-%m-%d"

today = date.today().strftime(date_format)
today_file_path = os.path.join(dir_path, today) + ".json"


def load_todo_all():
    files_to_check = os.listdir(dir_path)
    todo_all_dic = {}

    for f in files_to_check:
        with open(os.path.join(dir_path, f),"r") as f_read:
            todo_all_dic[f] = json.load(f_read)
    return(todo_all_dic)


def input_prefill(prompt, text):
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    result = input(prompt)
    readline.set_pre_input_hook()
    return result


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
                print_output.append(("(" + cl_id +i+ cl_reset + ")") + \
                    ("  " if len(i) < 2 else " ") + \
                    (" " if len(i) < 3 else "") + \
                    ("[" + cl_checkbox + checkbox + cl_reset + "] " if print_all else "")+ \
                     (("[" + cl_tag + v["tag"] + cl_reset + "] ") if v["tag"] != "" else "") + \
                     (("[" + cl_deadline + v["deadline"] + cl_reset + "] ") if
                         v["deadline"] != "" else "") + \
                     cl_message + v["message"] + cl_reset)
        if print_flag:
            print(cl_header + re.sub("\.json","", td) + cl_reset)
            for i in print_output:
                print(i)

def find_filename_by_id(td_id):
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
    return filename, file_count


def mark_todo(td_id, action="done"):
    filename, file_count = find_filename_by_id(td_id)
    if file_count > 1:
        print("There is multiple files with this id")
        if action=="done":
            print("Task in " + filename + " will be marked")
        elif action=="deleted":
            print("Task in " + filename + " will be deleted")
    if filename == "": 
        print("There is no todo with id " + str(td_id))
        return()
    
    logging.debug("Marking " + action + str(td_id) + " in file " + filename)
    if action=="done":
        print("Marked " + str(td_id) + " in file " + filename)
    elif action=="deleted":
        print("Deleted " + str(td_id) + " in file " + filename)

    with open(os.path.join(dir_path, filename), "r") as file:
        file_data = json.load(file)

    with open(os.path.join(dir_path, filename), "w") as file:
        if action == "done":
            file_data[str(td_id)]["done"] = True
        elif action == "deleted":
            file_data.pop(str(td_id))
        json.dump(file_data, file, indent = 4)


def edit_todo(td_id):
    filename, file_count = find_filename_by_id(td_id)
    if file_count > 1:
        print("There is multiple files with this id. Delete duplicates and try again")
        return()
    if filename == "": 
        print("There is no todo with id " + str(td_id))
        return()
   
    logging.debug("Editing" + str(td_id) + " in file " + filename)
    print("Editing " + str(td_id) + " in file " + filename)

    with open(os.path.join(dir_path, filename), "r") as file:
        edited_todo = json.load(file)[td_id]

    logging.debug(edited_todo)

    edited_todo["deadline"] = input_prefill("Edit deadline: ",edited_todo["deadline"]) 
    edited_todo["tag"] = input_prefill("Edit tag: ",edited_todo["tag"]) 
    edited_todo["message"] = input_prefill("Edit message: ",edited_todo["message"]) 

    logging.debug(edited_todo)

    write_todo(edited_todo, today_file_path)

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
        file_data[new_todo["id"]] = new_todo
        json.dump(file_data, file, indent = 4)
        logging.debug("New todo: writing - "+filename)


def print_todo_load(print_all=False):
   todo_all_dic = load_todo_all()
   print_todo_all(todo_all_dic, print_all)


@click.group()
def main():
    """
    TO DO List manager
    """

@main.command()
@click.option("--all", "print_all", is_flag=True,
        help="Print all todos, even unfinished once")
def p(print_all):
   """Print todos"""
   print_todo_load(print_all)


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
    print_todo_load(False)

@main.command()
@click.argument("td_id", required=True)
def delete(td_id):
   """Delete ID"""
   mark_todo(td_id, action="deleted")
   print_todo_load(False)

@main.command()
@click.argument("td_id", required=True)
def done(td_id):
   """Mark ID as done"""
   mark_todo(td_id, action="done")
   print_todo_load(False)

@main.command()
@click.argument("td_id", required=True)
def edit(td_id):
   """Edit ID"""
   edit_todo(td_id)
   print_todo_load(False)

@main.command()
@click.option("--all", "print_all", is_flag=True,
        help="Print all todos, even unfinished once")
@click.option("--deadline", "deadline", is_flag=True,
        help="Print all todos, even unfinished once")
@click.option("--tag", default="",
        help="Print all todos with this tag")
@click.option("--word", default="", 
        help="Print all todos, that contain this word")
def search(print_all, word, tag, deadline):
   todo_all_dic = load_todo_all()
   todo_selected_dic = {} 
   if tag != "": 
        for f, td in todo_all_dic.items():
            td_tmp = {} 
            for i, v in td.items():
                if v["tag"] == tag:
                   td_tmp[i] = v
            todo_selected_dic[f] = td_tmp
    
   if word != "": 
       if len(todo_selected_dic) > 0:
           todo_all_dic = todo_selected_dic
       for f, td in todo_all_dic.items():
           td_tmp = {} 
           for i, v in td.items():
               if bool(re.search(word, v["message"])):
                  td_tmp[i] = v
           todo_selected_dic[f] = td_tmp

   if deadline: 
       if len(todo_selected_dic) > 0:
           todo_all_dic = todo_selected_dic
       for f, td in todo_all_dic.items():
           td_tmp = {} 
           for i, v in td.items():
               if v["deadline"] != "":
                  td_tmp[i] = v
           todo_selected_dic[f] = td_tmp

   """Print todos"""
   print_todo_all(todo_selected_dic, print_all)


if __name__ == "__main__":
    main()
