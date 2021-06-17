import json
import os
import sys

def load_config():

    config = {
    	"dir_path" : "/home/jiri/todo",
    	"date_format" : "%Y-%m-%d",
    	"print_after_change" : False,
    	"show_date" : True,
    	"cl_header" : 72,
    	"cl_checkbox" :125,
    	"cl_tag" : 125,
    	"cl_deadline" : 108,
    	"cl_message" : 253,
    	"cl_id" : 78,
    	"cl_sepparator" : 166
    }

    config_path = os.path.join(os.path.dirname(__file__),"config.json")
    
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print("There is no config file in the folder. The file will be created at " + config_path )
        with open(config_path, "w") as config_file:
            json.dump(config, config_file, indent = 4)
    
    return(config)

