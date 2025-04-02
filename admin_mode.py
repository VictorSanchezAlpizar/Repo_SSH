import tkinter as tk
NO_ERR  = 8
ERR     = -1
IDLE    = 0
REG_USR = 1
REG_SNR = 2
MOD_SNR = 3
REG_TEL = 4
EXIT    = 5

current_state = IDLE
active = False

Users_list = {
    "User_1" : "1111",
    "User_2" : "2222",
    "User_3" : "3333",
    "User_4" : "4444",
    "User_5" : "5555"
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

