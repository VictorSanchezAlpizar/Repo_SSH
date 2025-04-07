from code_lists import *
from sensors_list import *
from utils import *

NO_ERR      =  8
ERR         = -1
IDLE        =  0
REG_USR     =  1
REG_SNR     =  2
MOD_SNR     =  9
REG_TEL     =  4
EXIT        =  5

REG_USR_2   =  10
REG_SNR_2   =  11
MOD_SNR_2   =  12
REG_TEL_2   =  13
MOD_CODE    =  14
MODE_CODE_2 =  15
MODE_REST   =  16

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

utils_SSH = {
    "Agencia_Seguridad" : "+50612345678"
}

# SW-Req: [SW-ID-91]
def rest_system():
    Sensors_list = Sensors_list_copy
    utils_SSH = utils_SSH_copy
    Users_list = Users_list_copy

# SW-Req: [SW-ID-21]
# SW-Req: [SW-ID-87]
def admin_mode_sm(cmd):
    global current_state, active, Sensors_list, Users_list, tmp_1, tmp_2, utils_SSH
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
                if (cmd == MODE_REST):
                    rest_system()
                    current_state = IDLE
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
    # SW-Req: [SW-ID-23]
    # SW-Req: [SW-ID-48]
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
    # SW-Req: [SW-ID-24]
    elif (current_state == REG_SNR or current_state == REG_SNR_2):
        if (current_state == REG_SNR):
            if (active == False):
                active = True
                status = REG_SNR
                print("HERE 1")
            else:
                # SW-Req: [SW-ID-17]
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
                # SW-Req: [SW-ID-28]
                # SW-Req: [SW-ID-32]
                if (cmd == 0 or cmd == 1):
                    # SW-Req: [SW-ID-31]
                    if (cmd == 1 and tmp_2 == 1):
                        status = IDLE
                        print("Invalid entry. Sensor 0 cannot be Zone 1")
                        status = IDLE
                        current_state = IDLE
                    else:
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
    # SW-Req: [SW-ID-30]
    elif (current_state == MOD_SNR or current_state == MOD_SNR_2):
        if (current_state == MOD_SNR):
            if (active == False):
                active = True
                status = MOD_SNR
                print("HERE 1")
            else:
                # SW-Req: [SW-ID-17]
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
                # SW-Req: [SW-ID-28]
                # SW-Req: [SW-ID-32]
                if (cmd == 0 or cmd == 1):
                    # SW-Req: [SW-ID-31]
                    if (cmd == 1 and tmp_2 == 1):
                        status = IDLE
                        print("Invalid entry. Sensor 0 cannot be Zone 1")
                        status = IDLE
                        current_state = IDLE
                    else:
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
    # SW-Req: [SW-ID-25]
    # SW-Req: [SW-ID-54]
    elif (current_state == REG_TEL or current_state == REG_TEL_2):
        if (current_state == REG_TEL):
            if (active == False):
                active = True
                status = REG_TEL
                print("HERE 1")
            else:
                active = False
                tmp_1 = "#"+cmd
                if (len(tmp_1) == 4): #Extension len
                    tmp_2 = snr
                    status = REG_TEL_2
                    current_state = REG_TEL_2
                    utils_SSH["Agencia_Seguridad"] = tmp_1
                    print("HERE 2")
                        
                if (current_state != REG_TEL_2):
                    status = IDLE
                    print("Invalid entry.")
                    status = IDLE
                    current_state = IDLE


        elif (current_state == REG_TEL_2):
            try:
                cmd = int(cmd)
                if (len(cmd) == 8):
                    utils_SSH["Agencia_Seguridad"] += cmd
                    save_utils_list()
                    print("HERE 3")
                else:
                    status = IDLE
                    print("Invalid entry.")
                    utils_SSH["Agencia_Seguridad"] = "+50612345678"
                    print("Setting default invalid phone number")
                    status = IDLE
                    current_state = IDLE
            except ValueError:
                status = ERR
                print("Invalid entry.")
            status = IDLE
            current_state = IDLE

    #--------------------------------------------------------------
    #--------------------------------------------------------------
    #MODIFY CODE
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    # SW-Req: [SW-ID-30]
    elif (current_state == MOD_SNR or current_state == MOD_SNR_2):
        if (current_state == MOD_SNR):
            if (active == False):
                active = True
                status = MOD_SNR
                print("HERE 1")
            else:
                # SW-Req: [SW-ID-17]
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
                # SW-Req: [SW-ID-28]
                # SW-Req: [SW-ID-32]
                if (cmd == 0 or cmd == 1):
                    # SW-Req: [SW-ID-31]
                    if (cmd == 1 and tmp_2 == 1):
                        status = IDLE
                        print("Invalid entry. Sensor 0 cannot be Zone 1")
                        status = IDLE
                        current_state = IDLE
                    else:
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

#--------------------------------------------------------------------------------
#END ADMIN MODE
#--------------------------------------------------------------------------------

def actualizar_User(usr_name, value):
    valid_config = False
    if usr_name in Users_list:
        Users_list[usr_name] = value
        valid_config = True
        return valid_config
    else:
        # SW-Req: [SW-ID-51]
        print("Configuracion no disponible")
        return valid_config

# SW-Req: [SW-ID-26]
def save_Users_list():
    try:
        with open("users.txt", "w") as file:
            json.dump(Users_list, file, indent=2)
        print("Lista de usuarios almacenada en memoria")
    # SW-Req: [SW-ID-52]
    except (IOError, OSError) as file_error:
        print(f"Error al guardar el archivo: {file_error}")
    except TypeError as type_error:
        print(f"Error al convertir los datos a JSON: {type_error}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# SW-Req: [SW-ID-26]
# SW-Req: [SW-ID-89]
def read_Users_list():
    global Users_list
    try:
        with open("users.txt", "r") as file:
            Users_list = json.load(file)
        print("Lista de usuarios actualizada:", Users_list)
    # SW-Req: [SW-ID-52]
    except FileNotFoundError:
        print("El archivo 'users.txt' no fue encontrado.")
    except json.JSONDecodeError as decode_error:
        print(f"Error de formato en el archivo JSON: {decode_error}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# SW-Req: [SW-ID-26]
def save_utils_list():
    try:
        with open("utils.txt", "w") as file:
            json.dump(utils_SSH, file, indent=1)
        print("Lista de utilidades almacenada en memoria")
    # SW-Req: [SW-ID-52]
    except (IOError, OSError) as file_error:
        print(f"Error al guardar el archivo: {file_error}")
    except TypeError as type_error:
        print(f"Error al convertir los datos a JSON: {type_error}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# SW-Req: [SW-ID-26]
# SW-Req: [SW-ID-89]
def read_utils_list():
    global utils_SSH
    try:
        with open("utils.txt", "r") as file:
            utils_SSH = json.load(file)
        print("Lista de utilidades actualizada:", utils_SSH)
    # SW-Req: [SW-ID-52]
    except FileNotFoundError:
        print("El archivo 'utils.txt' no fue encontrado.")
    except json.JSONDecodeError as decode_error:
        print(f"Error de formato en el archivo JSON: {decode_error}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

save_Users_list()
read_Users_list()
save_utils_list()
read_utils_list()