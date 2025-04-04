from code_lists import *
from sensors_list import *

NO_ERR    =  8
ERR       = -1
IDLE      =  0
REG_USR   =  1
REG_SNR   =  2
MOD_SNR   =  9
REG_TEL   =  4
EXIT      =  5

REG_USR_2 =  10
REG_SNR_2 =  11
MOD_SNR_2 =  12
REG_TEL_2 =  13


current_state = IDLE
active = False
tmp_1 = "NA"
tmp_2 = "NA"


Users_list = {
    "User_1" : {"ID": "1", "PWD": "1234"},
    "User_2" : {"ID": "2", "PWD": "2341"},
    "User_3" : {"ID": "3", "PWD": "3412"},
    "User_4" : {"ID": "4", "PWD": "4123"},
    "User_5" : {"ID": "5", "PWD": "5555"},
}

Phone_number = ""

def admin_mode_sm(cmd):
    global current_state, active, Sensors_list, Users_list, tmp_1, tmp_2
    status = 0
    #Actualizar datos con Usuarios almacenados en memoria
    save_Users_list()
    read_Users_list()
    print("Admin mode")
    print(current_state)

    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #INIT ADMIN MODE
    #--------------------------------------------------------------
    #--------------------------------------------------------------

    if (current_state == IDLE):
        try:
            cmd = int(cmd)
            if (current_state == IDLE):
                current_state = cmd
                status = NO_ERR
                if (cmd == 3):
                    current_state = MOD_SNR
            elif (current_state != IDLE):
                status = NO_ERR
            else:
                status = ERR
                print("Invalid entry.")
        except ValueError:
            status = ERR
            print("Invalid entry.")

    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #NEW USER / MODIFY USER
    #--------------------------------------------------------------
    #--------------------------------------------------------------

    if (current_state == REG_USR or current_state == REG_USR_2):
        if (current_state == REG_USR):
            if (active == False):
                active = True
                status = REG_USR
            else:
                active = False
                tmp_1 = str(cmd)
                for user, data in Users_list.items():
                    if data["ID"] == tmp_1:
                        tmp_2 = user
                        status = REG_USR_2
                        current_state = REG_USR_2


        elif (current_state == REG_USR_2):
            try:
                cmd = str(cmd)
                Users_list[tmp_2]["PWD"] = cmd
                save_Users_list()
            except ValueError:
                status = ERR
                print("Invalid entry.")
            status = IDLE
            current_state = IDLE

    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #NEW SNR
    #--------------------------------------------------------------
    #--------------------------------------------------------------

    elif (current_state == REG_SNR or current_state == REG_SNR_2):
        if (current_state == REG_SNR):
            if (active == False):
                active = True
                status = REG_SNR
                print("HERE 1")
            else:
                active = False
                tmp_1 = int(cmd)
                for snr, data in Sensors_list.items():
                    if data["ID"] == tmp_1:
                        if data["Install"] == 0:
                            tmp_2 = snr
                            status = REG_SNR_2
                            current_state = REG_SNR_2
                            print("HERE 2")
                        
                if (current_state != REG_SNR_2):
                    status = IDLE
                    print("Invalid entry.")
                    status = IDLE
                    current_state = IDLE


        elif (current_state == REG_SNR_2):
            try:
                cmd = int(cmd)
                if (cmd == 0 or cmd == 1):
                    Sensors_list[tmp_2]["Zone"] = cmd
                    Sensors_list[tmp_2]["Install"] = INSTALL
                    save_sensors_list()
                    print("HERE 3")
                else:
                    status = IDLE
                    print("Invalid entry.")
                    status = IDLE
                    current_state = IDLE
            except ValueError:
                status = ERR
                print("Invalid entry.")
            status = IDLE
            current_state = IDLE

    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #MODIFY SNR
    #--------------------------------------------------------------
    #--------------------------------------------------------------

    elif (current_state == MOD_SNR or current_state == MOD_SNR_2):
        if (current_state == MOD_SNR):
            if (active == False):
                active = True
                status = MOD_SNR
                print("HERE 1")
            else:
                active = False
                tmp_1 = int(cmd)
                for snr, data in Sensors_list.items():
                    if data["ID"] == tmp_1:
                        if data["Install"] == 1:
                            tmp_2 = snr
                            status = MOD_SNR_2
                            current_state = MOD_SNR_2
                            print("HERE 2")
                        
                if (current_state != MOD_SNR_2):
                    status = IDLE
                    print("Invalid entry.")
                    status = IDLE
                    current_state = IDLE


        elif (current_state == MOD_SNR_2):
            try:
                cmd = int(cmd)
                if (cmd == 0 or cmd == 1):
                    Sensors_list[tmp_2]["Zone"] = cmd
                    Sensors_list[tmp_2]["Install"] = INSTALL
                    save_sensors_list()
                    print("HERE 3")
                elif (cmd == 2):
                    Sensors_list[tmp_2]["Zone"] = 0
                    Sensors_list[tmp_2]["Install"] = NOT_INSTALL
                    save_sensors_list()
                    print("HERE 4")
                else:
                    status = IDLE
                    print("Invalid entry.")
                    status = IDLE
                    current_state = IDLE
            except ValueError:
                status = ERR
                print("Invalid entry.")
            status = IDLE
            current_state = IDLE

    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #ADD/MODIFY TEL
    #--------------------------------------------------------------
    #--------------------------------------------------------------

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

# IMPLEMENTS: SW-ID-XX
def actualizar_User(usr_name, value):
    valid_config = False
    if usr_name in Users_list:
        Users_list[usr_name] = value
        valid_config = True
        return valid_config
    else:
        print("Configuracion no disponible")
        return valid_config

def save_Users_list():
    with open("users.txt", "w") as file:
        json.dump(Users_list, file, indent=2)
    print("Lista de usuarios almacenada en memoria")

def read_Users_list():
    global Users_list
    with open("users.txt", "r") as file:
        Users_list = json.load(file)
    print("Lista de usuarios actualizada:", Users_list)

save_Users_list()
read_Users_list()