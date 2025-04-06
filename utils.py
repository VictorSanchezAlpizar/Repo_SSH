import tkinter as tk

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
    '*', '0', '#', 'Bomberos'
]

alert_message_GSM = {
    "num_tel_Agencia" : "+50612345678",
    "usr_Active"      : 0,
    "Alert_Type"      : 0,
    "Alerted_snr"     : 0
}