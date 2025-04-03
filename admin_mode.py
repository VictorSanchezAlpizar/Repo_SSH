from code_lists import *
from sensors_list import *

NO_ERR    =  8
ERR       = -1
IDLE      =  0
REG_USR   =  1
REG_SNR   =  2
MOD_SNR   =  3
REG_TEL   =  4
EXIT      =  5

REG_USR_2 =  10


current_state = IDLE
active = False

Users_list = {
    "User_1" : {"ID": "1", "PWD": "1234"},
    "User_2" : {"ID": "2", "PWD": "2341"},
    "User_3" : {"ID": "3", "PWD": "3412"},
    "User_4" : {"ID": "4", "PWD": "4123"},
    "User_5" : {"ID": "5", "PWD": "5555"},
}

def admin_mode_sm(cmd):
    global current_state, active
    status = 0
    print("Admin mode")
    print(current_state)
    #Estado actual de la maquina de estados
    try:
        cmd = int(cmd)
        if (current_state == IDLE and int(cmd) <= 5):
            current_state = cmd
            status = NO_ERR
        elif (current_state != IDLE):
            status = NO_ERR
        else:
            status = ERR
            print("Invalid entry.")
    except ValueError:
        status = ERR
        print("Invalid entry.")
    
    
    #Continuar con operaciones
    if (current_state == REG_USR):
        if (active == False):
            active = True
            status = REG_USR
        else:
            active = False


    elif (current_state == REG_SNR):
        if (active == False):
            active = True
            status = REG_USR
        else:
            active = False

    elif (current_state == MOD_SNR):
        if (active == False):
            active = True
            status = REG_USR
        else:
            active = False

    elif (current_state == REG_TEL):
        if (active == False):
            active = True
            status = REG_USR
        else:
            active = False

    elif (current_state == EXIT):
        status = ERR
    else:
        print("Invalid.")
        status = ERR
    return status

def actualizar_User(code_name, value):
    valid_config = False
    if code_name in Codes_list:
        Codes_list[code_name] = value
        valid_config = True
        return valid_config
    else:
        print("Configuracion no disponible")
        return valid_config

def save_Users_list():
    with open("users.txt", "w") as file:
        json.dump(Codes_list, file, indent=2)
    print("Lista de usuarios almacenada en memoria")

def read_Users_list():
    global Codes_list
    with open("users.txt", "r") as file:
        Codes_list = json.load(file)
    print("Lista de usuarios actualizada:", Codes_list)