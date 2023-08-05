"""Main module."""
import os
import subprocess
import json 
from pathlib import Path
import sys
import shutil
from getpass import getpass

def create_config(): 
    path = Path(get_config_path())
    if not path.parent.exists(): 
        path.parent.mkdir(exist_ok=True, parents=True)
        print("Created folder for quickzoom config: {}".format(str(path.parent)))
    if not path.exists(): 
        valid_input = ["y", "n"]
        while True:
            user_input = input("Quickzoom did not detect a config file yet. Do you want to create it at: {}? (y/n)".format(str(path)))
            if user_input.lower() in valid_input: 
                if user_input == "n": 
                    print("Aborted creating config file")
                    quit_application()
                else:
                    try:
                        with open(str(path), "w") as f: 
                            json.dump({}, f)
                    except:
                        raise RuntimeError("Could not create config file: {}".format(str(path)))
                    print("Created empty config file: {}".format(str(path)))
                    break
            else:
                continue

def quit_application(): 
    print("Application was terminated.")
    sys.exit(0)

def exception_handler(func): 
    def func_wrapper(*args, **kwargs): 
        try: 
            return func(*args, **kwargs)

        except ValueError as error:
            print(
                "# Oops. Seems like you gave some wrong input!"
                f"\n# Error: {error}"
                "\n# Apllication will be terminated."
            ) 
            quit_application() 

        except RuntimeError as error: 
            print(
                "# Oops. Something went wrong!"
                f"\n# Error: {error}"
                "\n# Apllication will be terminated."
            )
            quit_application()

    return func_wrapper

def get_config_path(): 
    path = Path.home().joinpath(".quickzoom/rooms.json")
    return str(path) 

def get_zoom_exe(): 
    if sys.platform == "win32":
        path = Path(os.getenv('APPDATA')).joinpath("Zoom/bin/Zoom.exe")
    if sys.platform == "linux":
        raise RuntimeError("Linux is not implemented yet!")
    if sys.platform == "darwin":
        raise RuntimeError("MacOs is not implemented yet!")

    return str(path)

def connect_to_meeting(meeting_id, pw): 
    zoom_exe = get_zoom_exe() 
    connect_flag = "--url=zoommtg://zoom.us/join?action=join"
    cmd_str = f'{zoom_exe} "{connect_flag}&confno={meeting_id}&pwd={pw}"'

    print("Connecting to meeting: {}...".format(meeting_id))
    subprocess.call(cmd_str, shell=True)
    
def get_room_info(room_name):
    json_obj = load_json_dic()

    if room_name in json_obj: 
        return convert_room_info(json_obj[room_name])
    else:
        raise ValueError("The room {} is not specified in the config: {}".format(room_name, get_config_path()))

def load_json_dic():
    json_room_path = get_config_path()
    try:
        with open(json_room_path, "r") as f: 
            json_obj = json.load(f)
    except: 
        raise RuntimeError("Couldn't load room config at: {}".format(json_room_path))

    return json_obj

def save_json_dic(dic):
    json_room_path = get_config_path()
    try:
        with open(json_room_path, "w") as f: 
            json.dump(dic, f, indent=4)
    except: 
        raise RuntimeError("Couldn't save room config at: {}".format(json_room_path))
    
def validate_zoom_exe(): 
    if Path(get_zoom_exe()).exists(): 
        return True
    else:
        return False 

def validate_config_exists(): 
    path = Path(get_config_path())
    if path.exists(): 
        print("Found config file: {}".format(str(path)))
        return True
    else:
        return False  

def is_config_empty():
    json_obj = load_json_dic() 
    if len(json_obj) == 0: 
        return True
    else:
        return False 

def print_room_info(room_label): 
    room_info = get_room_info(room_label)
    print("Meeting ID: {}".format(room_info["id"]))

def convert_room_info(room_info_dic): 
    room_info_dic["id"] = room_info_dic["id"].replace("-", "")
    return room_info_dic

def create_room(): 
    print("Create a new room")
    dic = load_json_dic() 
    input_room_label = input("Room Label: ")
    if input_room_label in dic: 
        while True:
            user_input = input("The room: {} was already created. Do you want to override? (y/n)".format(input_room_label))
            if user_input.lower() == "y":
                break
            elif user_input.lower() == "n": 
                sys.exit("Aborted room creation.")
            else:
                continue

    input_room_id = input("Zoom Metting-Id: ")
    input_room_pwd  = input("Room Password: ")

    dic[input_room_label] = {"id": input_room_id, "pw": input_room_pwd}
    save_json_dic(dic)
    print("Succesfully created new room! Type: 'quickzoom {}' in your terminal to connect to it!".format(input_room_label))

def prompt_first_room(): 
    valid_input = ["y", "n"]
    while True: 
        user_input = input("Seems like you have no rooms in your config. Do you want to create your first one? (y/n)")
        if user_input.lower() in valid_input: 
            if user_input == "n": 
                quit_application()
            else:
                create_room()
                break
        else:
            continue

@exception_handler
def run(args): 

    newroom = args.newroom
    roomlabel = args.roomlabel

    #first check if config exists if not create it no matter if any flags are provided
    if not validate_config_exists(): 
        create_config()

    #check if config has any rooms, if not ask for first room
    if is_config_empty():
        prompt_first_room()
        return 

    #if the newroom flag is specified create new room and exit
    if newroom: 
        create_room()
        return 

    #if newroom flag was not specified check if roomlabel is not None
    if not roomlabel:
        print("Please provide a roomlabel that you want zoom to connect to.")
        return 

    if not validate_zoom_exe(): 
        raise RuntimeError("Zoom.exe does not exist at: {}".format(get_zoom_exe()))

    room_info = get_room_info(roomlabel) 
    print_room_info(roomlabel)
    connect_to_meeting(room_info["id"], room_info["pw"])
    