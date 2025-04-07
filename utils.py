import tkinter as tk
from sensors_list import *

#States
START_MENU           = 0
MAIN_MENU            = 1
USER_MODE_MENU       = 2
MODO_0_MENU          = 3
MODO_1_MENU          = 4
MODO_DESARMADO_MENU  = 5
MODO_AHORRO          = 6

USR_INACTIVE         = 0
USR_PROGRESS         = 1
USR_END              = 2
USR_ACTIVE           = 3

#ERROR_CODES
ERROR_MODE           = -1
EXIT_MODE            =  0
EXIT_USR             =  3

#PS CODES
CODE_BATERIA         = "Bateria"
CODE_PRINCIPAL       = "Principal"
CODE_PANICO          = "Panico"
CODE_INCENDIO        = "Incendio"
CODE_SENSOR          = "Alarma Sensor"

row_custom           = 0
col_custom           = 0
current_State        = 0
current_Usr_State    = 0
usr_ID               = "NA"
sequence             = []
main_menu_labels     = []
admin_menu_labels    = []

menu_label           = "DESARMADO"
active_user          = "0"
current_PS           = "Principal"
usr_Bat_limit        = -1

# Crear y colocar los botones en la interfaz principal
buttons = [
    '1', '2', '3', 'Esc',
    '4', '5', '6', 'Enter',
    '7', '8', '9', 'Pánico',
    '*', '0', '#', 'Bomberos',
]

alert_message_GSM = {
    "num_tel_Agencia" : "+50612345678",
    "usr_Active"      : 0,
    "Alert_Type"      : 0,
    "Alerted_snr"     : 0
}

Sensors_list_copy = {
    "S1": {"ID": 1, "Zone": 0, "Status": INACTIVE, "Install": INSTALL},
    "S2": {"ID": 2, "Zone": 0, "Status": INACTIVE, "Install": INSTALL},
    "S3": {"ID": 3, "Zone": 1, "Status": INACTIVE, "Install": INSTALL},
    "S4": {"ID": 4, "Zone": 0, "Status": INACTIVE, "Install": NOT_INSTALL},
    "S5": {"ID": 5, "Zone": 1, "Status": INACTIVE, "Install": INSTALL},
    "S6": {"ID": 6, "Zone": 0, "Status": INACTIVE, "Install": NOT_INSTALL},
    "S7": {"ID": 7, "Zone": 0, "Status": INACTIVE, "Install": INSTALL},
    "S8": {"ID": 8, "Zone": 0, "Status": INACTIVE, "Install": NOT_INSTALL},
    "S9": {"ID": 9, "Zone": 0, "Status": INACTIVE, "Install": NOT_INSTALL},
    "S10": {"ID": 10, "Zone": 0, "Status": INACTIVE, "Install": NOT_INSTALL},
    "S11": {"ID": 11, "Zone": 0, "Status": INACTIVE, "Install": NOT_INSTALL},
    "S12": {"ID": 12, "Zone": 0, "Status": INACTIVE, "Install": NOT_INSTALL},
    "S13": {"ID": 13, "Zone": 0, "Status": INACTIVE, "Install": NOT_INSTALL},
    "S14": {"ID": 14, "Zone": 0, "Status": INACTIVE, "Install": NOT_INSTALL},
    "S15": {"ID": 15, "Zone": 0, "Status": INACTIVE, "Install": NOT_INSTALL},
    "S16": {"ID": 16, "Zone": 0, "Status": INACTIVE, "Install": NOT_INSTALL},
}

Users_list_copy = {
    "User_1" : {"ID": "1", "PWD": "1234"},
    "User_2" : {"ID": "2", "PWD": "2341"},
    "User_3" : {"ID": "3", "PWD": "3412"},
    "User_4" : {"ID": "4", "PWD": "4123"},
    "User_5" : {"ID": "5", "PWD": "5555"},
}

utils_SSH_copy = {
    "Agencia_Seguridad" : "+50612345678"
}