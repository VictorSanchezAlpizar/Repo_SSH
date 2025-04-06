import tkinter as tk
from code_lists import *
from sensors_list import *
from admin_mode import *
from utils import * # type: ignore
from sim_sensors import SimSensors
from modo_0_monitor import Modo0Monitor
from modo_1_monitor import Modo1Monitor
from modo_ahorro_monitor import ModoAhorroMonitor

#Parameters --------------------------------------------------------------------------------------
# Crear la interfaz principal
root = tk.Tk()
root.title("Interfaz Principal")
sim_sensors = SimSensors(root)

# MODO 0
# SW-Req: [SW-ID-1]
# SW-Req: [SW-ID-14]
# SW-Req: [SW-ID-34]
def handle_sensor_alert(triggered_sensors):
    print(f"¡ALERTA! Sensores activados: {', '.join(triggered_sensors)}")
    label_alerta.config(bg="red", text=f"Alerta: {triggered_sensors[0]}")
    # SW-Req: [SW-ID-72]
    format_alert_message(utils_SSH["Agencia_Seguridad"], active_user, CODE_SENSOR, triggered_sensors[0])


modo0_monitor           = Modo0Monitor(root, handle_sensor_alert)
modo1_monitor           = Modo1Monitor(root, handle_sensor_alert)
modo_ahorro_monitor     = ModoAhorroMonitor(root, handle_sensor_alert)
menu_to_be_displayed    = tk.StringVar(value="MODE INIT")
usr_to_be_displayed     = tk.StringVar(value="USR NS")
ps_to_be_displayed      = tk.StringVar(value="Power Supply")
bat_lvl_to_be_displayed = tk.StringVar(value="Batery Level")
save_sensors_list()

#Utils ---------------------------------------------------------------------------------------------
# SW-Req: [SW-ID-72]
def format_alert_message(num_tel, usr, alert_type, alert_snr = 0):
    global alert_message_GSM

    alert_message_GSM["num_tel_Agencia"] = num_tel
    alert_message_GSM["usr_Active"] = usr
    alert_message_GSM["Alert_Type"] = alert_type
    alert_message_GSM["Alerted_snr"] = alert_snr
    
    if (alert_message_GSM["Alert_Type"] == CODE_INCENDIO or 
        alert_message_GSM["Alert_Type"] == CODE_PANICO):
        data_to_save = {k: v for k, v in alert_message_GSM.items() if k != "Alerted_snr"}
    else:
        data_to_save = alert_message_GSM

    with open("gsm_alerts.txt", "w") as file:
        json.dump(data_to_save, file, indent=4)
    
    print("Mensaje preparado:", data_to_save)

def init_menu():
    menu_to_be_displayed.set(f"Modo Activo: {menu_label}")
    bat_lvl_to_be_displayed.set(f"Nivel Bateria: {nivel_bateria.get()}%")
    ps_to_be_displayed.set(f"Fuente Alimentación: {current_PS}")

def verify_PS(*args):
    global current_PS, ps_to_be_displayed, usr_Bat_limit, current_PS
    """Función se ejecuta cada vez que el nivel de voltaje cambia"""
    bat_lvl_to_be_displayed.set(f"Nivel Bateria: {nivel_bateria.get()}%")
    ps_to_be_displayed.set(f"Fuente Alimentación: {current_PS}")
    
    # SW-Req: [SW-ID-2]
    if (nivel_bateria.get() < usr_Bat_limit and current_PS == CODE_BATERIA):
        label_bateria.config(bg="green", text="Batería")
    else:
        label_bateria.config(bg="white", text="Batería")

#Variables required to track the Batery level
nivel_bateria = tk.IntVar(value=50)
nivel_bateria.trace_add("write", verify_PS)

def update_label():
    global current_State, current_Usr_State, active_user, menu_label, menu_to_be_displayed, usr_to_be_displayed
    """Actualiza el label_ID según el estado actual."""

    # SW-Req: [SW-ID-2]
    # SW-Req: [SW-ID-57]
    # SW-Req: [SW-ID-61]
    menu_to_be_displayed.set(f"Modo Activo: {menu_label}")
    usr_to_be_displayed.set(f"Usuario: {active_user}")
    
    if (current_Usr_State == USR_INACTIVE):
        label_ID.config(text="User ID: ")
        hide_all()
        show_start_menu()
    elif (current_Usr_State == USR_PROGRESS):
        label_ID.config(text="Password: ")
        hide_all()
        show_start_menu()
    elif (current_Usr_State == USR_END):
        label_ID.config(text="Batery LVL (1-100): ")
        hide_all()
        show_start_menu()
    elif (current_Usr_State == USR_ACTIVE):
        if current_State == START_MENU:
            label_ID.config(text="User ID: ")
            hide_all()
            show_start_menu()
        elif current_State == MAIN_MENU:
            label_ID.config(text="Opciones: ")
            hide_all()
            show_main_menu()
        elif current_State == USER_MODE_MENU:
            label_ID.config(text="Opciones: ")
            hide_all()
            show_admin_menu()
        elif current_State == MODO_0_MENU:
            menu_label = "ARMADO. MODO 0"
            label_ID.config(text="Opciones: ")
            hide_all()
            show_main_menu()
        elif current_State == MODO_1_MENU:
            menu_label = "ARMADO. MODO 1"
            label_ID.config(text="Opciones: ")
            hide_all()
            show_main_menu()
        elif current_State == MODO_AHORRO:
            menu_label = "ARMADO. AHORRO"
            label_ID.config(text="Opciones: ")
            hide_all()
            show_main_menu()
        elif current_State == MODO_DESARMADO_MENU:
            menu_label = "DESARMADO"
            label_ID.config(text="Opciones: ")
            hide_all()
            show_main_menu()
    else:
        label_ID.config(text="User ID: ")
        hide_all()

def hide_all():
    hide_start_menu()
    hide_main_menu()
    hide_admin_menu()

def show_start_menu():
    for label in start_menu_labels:
        label.grid()

def show_main_menu():
    """Muestra las líneas de texto adicionales en la pantalla principal."""
    for label in main_menu_labels:
        label.grid()

def show_admin_menu():
    """Muestra Menu modo Admin."""
    for label in admin_menu_labels:
        label.grid()

def hide_start_menu():
    """Oculta las líneas de texto adicionales en la pantalla principal."""
    for label in start_menu_labels:
        label.grid_remove()

def hide_main_menu():
    """Oculta las líneas de texto adicionales en la pantalla principal."""
    for label in main_menu_labels:
        label.grid_remove()

def hide_admin_menu():
    """Oculta las líneas de texto adicionales en la pantalla principal."""
    for label in admin_menu_labels:
        label.grid_remove()

#-----------------------------------------------------------------------------------------
#MAIN APP
#USR INTERACTS WITH SSH
#-----------------------------------------------------------------------------------------

def on_button_click(value):
    global utils_SSH, current_State, current_Usr_State, usr_ID, usr_Bat_limit, sequence, start_menu_label, active_user
    tmp_usr    = "NA"
    tmp_pwd    = "NA"
    tmp_lvl    = 0
    is_match   = 0

    # SW-Req: [SW-ID-1]
    # SW-Req: [SW-ID-9]
    # SW-Req: [SW-ID-10]
    if value == "Pánico" or value == "Bomberos":
        # Cambiar el color del indicador L1 a verde cuando se presiona "Batería"
        label_alerta.config(bg="red")
        # SW-Req: [SW-ID-82]
        # SW-Req: [SW-ID-83]
        # SW-Req: [SW-ID-85]
        # SW-Req: [SW-ID-86]
        if value == "Pánico":
            format_alert_message(utils_SSH["Agencia_Seguridad"], active_user, CODE_PANICO)
        else:
            format_alert_message(utils_SSH["Agencia_Seguridad"], active_user, CODE_INCENDIO)

    elif value == "Esc":
        # Limpiar el cuadro de texto si se presiona "Esc"
        entry_ID.delete(0, tk.END)
        sequence.clear()  # Limpiar la secuencia

    # SW-Req: [SW-ID-38]
    elif value == "Enter":
        if (current_State == START_MENU and (sequence[0] != "#" and sequence[0] != "*")):
            
            if (current_Usr_State == USR_INACTIVE):
                tmp_usr = get_string(sequence)
                for user, data in Users_list.items():
                    if data["ID"] == tmp_usr:
                        is_match = True
                        usr_ID = user
                
                if (is_match == True):
                    active_user = tmp_usr
                    current_Usr_State = USR_PROGRESS
                    is_match = False
                    update_label()  # Actualizar el label

                else:
                    print("Invalid USR")
                    current_State = START_MENU
                    update_label()  # Actualizar el label

            elif (current_Usr_State == USR_PROGRESS):
                tmp_pwd = get_string(sequence)
                if (Users_list[usr_ID]["PWD"] == tmp_pwd):
                    if (usr_Bat_limit != -1):
                        current_Usr_State = USR_ACTIVE
                        current_State = MAIN_MENU  # Cambiar al menú principal
                        menu_label = "USER MENU"
                        usr_ID = "NA"
                        update_label()  # Actualizar el label
                    else:
                        current_Usr_State = USR_END
                        update_label()  # Actualizar el label        

                else:
                    print("Invalid PWD")
                    current_State = START_MENU
                    current_Usr_State = USR_INACTIVE
                    update_label()  # Actualizar el label

            elif (current_Usr_State == USR_END):
                try:
                    tmp_lvl = int(get_string(sequence))
                    if (tmp_lvl >=1 and tmp_lvl < 100):
                        usr_Bat_limit = tmp_lvl
                        current_Usr_State = USR_ACTIVE
                        current_State = MAIN_MENU  # Cambiar al menú principal
                        menu_label = "USER MENU"
                        usr_ID = "NA"
                        update_label()  # Actualizar el label
                    else:
                        print("Invalid LVL")
                        menu_label = "START MENU"
                        current_State = START_MENU
                        current_Usr_State = USR_INACTIVE
                        update_label()  # Actualizar el label
                except ValueError:
                    print("Invalid LVL")
                    menu_label = "START MENU"
                    current_State == START_MENU
                    current_Usr_State = USR_INACTIVE
                    update_label()  # Actualizar el label
        
        elif (current_State == MAIN_MENU and get_string(sequence) == str(EXIT_USR)):
            current_State = START_MENU  # Cambiar al menú start
            menu_label = "START MENU"
            current_Usr_State = USR_INACTIVE
            update_label()  # Actualizar el label

        # SW-Req: [SW-ID-21]
        elif current_State == USER_MODE_MENU:
            menu_label = "MODO ADMIN"
            current_command = get_string(sequence)
            status = admin_mode_sm(current_command)

            #---------------------------------------
            #MAIN ADMIN
            #---------------------------------------

            if (status == IDLE):
                label_ID.config(text="Opciones: ")
            
            #---------------------------------------
            #REGISTER / MODIFY USER
            #---------------------------------------

            if (status == REG_USR):
                label_ID.config(text="Nuevo USR: ")
            elif (status == REG_USR_2):
                label_ID.config(text="Nueva PWD: ")
            
            #---------------------------------------
            #REGISTER SENSOR
            #---------------------------------------

            elif (status == REG_SNR):
                label_ID.config(text="Nuevo SNR (1-16): ")
            elif (status == REG_SNR_2):
                label_ID.config(text="Zona (0-1): ")

            #---------------------------------------
            #MODIFY SENSOR
            #---------------------------------------

            elif (status == MOD_SNR):
                label_ID.config(text="Modificar SNR (1-16): ")
            elif (status == MOD_SNR_2):
                label_ID.config(text="Zona (0-1,2:N_INST): ")

            #---------------------------------------
            #MODIFY TEL
            #---------------------------------------

            elif (status == REG_TEL):
                label_ID.config(text="Extensión (#XYZ): ")
            elif (status == REG_TEL_2):
                label_ID.config(text="Numero Agencia Seguridad: ")

            #---------------------------------------
            #ERROR IN PROGRESS
            #---------------------------------------

            if (status == ERROR_MODE or status == EXIT_USR):
                menu_label = "START MENU"
                current_Usr_State = USR_INACTIVE
                current_State = START_MENU  # Volver al estado inicial
                update_label()  # Actualizar el label

        else:
            # SW-Req: [SW-ID-42]
            # SW-Req: [SW-ID-45]
            if (sequence[0]=='#' and sequence[-1]=='*'):
                current_Code = get_code(sequence)
                # SW-Req: [SW-ID-21]
                # SW-Req: [SW-ID-55]
                # SW-Req: [SW-ID-56]
                if (current_Code == Codes_list["Code_Modo_0"]):
                    # Chequeo inicial solo para Modo 0
                    sensores_activos = modo0_monitor._check_activated_sensors()  # Usamos tu método existente
            
                    if sensores_activos:
                        print(f"[MODO 0] ¡No se puede armar! Sensores activos: {sensores_activos}")
                        label_alerta.config(bg="yellow", text= f"{sensores_activos[0]} Activo")
                        current_State = MODO_DESARMADO_MENU  # Volvemos a desarmado
                    else:
                        current_State = MODO_0_MENU
                        label_alerta.config(bg="white", text="Alerta") 
                        modo0_monitor.start_monitoring()
                    
                    update_label()  # Actualizamos la interfaz una sola vez
                # SW-Req: [SW-ID-21]
                # SW-Req: [SW-ID-59]
                # SW-Req: [SW-ID-60]
                elif (current_Code == Codes_list["Code_Modo_1"]):
                    sensores_activos = modo1_monitor._check_activated_sensors()  # Usamos tu método existente
            
                    if sensores_activos:
                        print(f"[MODO 1] ¡No se puede armar! Sensores activos: {sensores_activos}")
                        label_alerta.config(bg="yellow", text= f"{sensores_activos[0]} Activo")
                        current_State = MODO_DESARMADO_MENU  # Volvemos a desarmado
                    else:
                        current_State = MODO_1_MENU
                        label_alerta.config(bg="white", text="Alerta") 
                        modo1_monitor.start_monitoring()
                    
                    update_label()  # Actualizamos la interfaz una sola vez               
                # SW-Req: [SW-ID-21]
                elif (current_Code == Codes_list["Code_Desarmado"]):
                    current_State = MODO_DESARMADO_MENU
                    update_label()
                    modo0_monitor.stop_monitoring()  # Detener monitoreo
                    modo1_monitor.stop_monitoring()
                    modo_ahorro_monitor.stop_monitoring()
                    print("[INFO] Estado DESARMADO")
                    label_alerta.config(bg="white", text="Alerta") 
                # SW-Req: [SW-ID-21]
                elif (current_Code == Codes_list["Code_Admin"]):
                    current_State = USER_MODE_MENU
                    menu_label = "MODO ADMIN"
                # SW-Req: [SW-ID-21]
                elif (current_Code == Codes_list["Code_Ahorro"]):
                    current_State = MODO_AHORRO
                    label_alerta.config(bg="white", text="Alerta") 
                    modo_ahorro_monitor.start_monitoring()

                    update_label()  # Actualizamos la interfaz una sola vez 
                else:
                    print("Invalid command. Returning to START MENU")
                    current_State = START_MENU  # Volver al estado inicial
                    current_Usr_State == USR_INACTIVE
                    menu_label = "START MENU"
                    update_label()

            update_label()  # Actualizar el label
        entry_ID.delete(0, tk.END)
        sequence.clear()  # Limpiar la secuencia

    else:
        # Añadir el valor del botón al cuadro de texto
        entry_ID.insert(tk.END, value)
        sequence.append(value)  # Añadir el valor a la secuencia

def turn_on_main_button(value):
    global current_PS
    if value == "Sim falla electrica ON":
        # Cambiar el estado del botón en la interfaz principal
        current_PS = CODE_BATERIA
        #label_bateria.config(bg="green", text="Batería")
    if value == "Sim falla electrica OFF":
        # Cambiar el estado del botón en la interfaz principal
        current_PS = CODE_PRINCIPAL
        #label_bateria.config(bg="white", text="Batería")
    if value == "Sim Bomberos PASS":
        # Cambiar el estado del botón en la interfaz principal
        label_alerta.config(bg="white", text="Alerta")
    if value == "Sim Sensor falla":
        sim_sensors.open_sim_sensor_falla()  # Usamos la clase

def open_secondary_interface():
    global nivel_bateria
    secondary_window = tk.Toplevel(root)
    secondary_window.minsize(width=25, height=25)
    secondary_window.config(padx=5, pady=5)
    secondary_window.title("Interfaz Secundaria")

    # Botón en la interfaz secundaria para encender el botón en la principal
    tk.Button(secondary_window, text="Sim falla PS Principal ON", command=lambda b="Sim falla electrica ON": turn_on_main_button(b)).pack(pady=5)
    tk.Button(secondary_window, text="Sim falla PS Principal OFF", command=lambda b="Sim falla electrica OFF": turn_on_main_button(b)).pack(pady=10)
    tk.Button(secondary_window, text="Sim Sensor falla", command=lambda b="Sim Sensor falla": turn_on_main_button(b)).pack(pady=15)
    tk.Button(secondary_window, text="Sim Alert PASS", command=lambda b="Sim Bomberos PASS": turn_on_main_button(b)).pack(pady=20)

    # Barra deslizante
    scale = tk.Scale(secondary_window, from_=0, to=100, orient="horizontal", variable=nivel_bateria, label="Nivel")
    scale.pack(pady=10)

    # Mostrar el valor actual de la barra
    label = tk.Label(secondary_window)
    label.pack()

#------------------------------------------------------------------------------------------------------   
# Main interface
# MENUS Setup
#------------------------------------------------------------------------------------------------------

label_ID = tk.Label(text="User ID: ", font=("Arial", 14))
label_ID.grid(column=0, row=0)

entry_ID = tk.Entry(width=10, font=("Arial", 14))
entry_ID.grid(column=1, row=0)

col_custom+=2

for button in buttons:
    if button == 'Esc':
        tk.Button(root, text=button, command=lambda b=button: on_button_click(b), bg='white').grid(row=row_custom, column=col_custom, padx=5, pady=5, sticky="nsew")
    elif button == 'Enter':
        tk.Button(root, text=button, command=lambda b=button: on_button_click(b), bg='white').grid(row=row_custom, column=col_custom, padx=5, pady=5, sticky="nsew")
    elif button == 'Pánico':
        tk.Button(root, text=button, command=lambda b=button: on_button_click(b), bg='yellow').grid(row=row_custom, column=col_custom, padx=5, pady=5, sticky="nsew")
    elif button == 'Bomberos':
        tk.Button(root, text=button, command=lambda b=button: on_button_click(b), bg='red').grid(row=row_custom, column=col_custom, padx=5, pady=5, sticky="nsew")
    else:
        tk.Button(root, text=button, command=lambda b=button: on_button_click(b)).grid(row=row_custom, column=col_custom, padx=5, pady=5, sticky="nsew")
    
    col_custom += 1
    if col_custom > 5:
        col_custom = 2
        row_custom += 1

# Crear las líneas de texto adicionales (inicialmente ocultas)
start_menu_labels = [
    tk.Label(root, textvariable=ps_to_be_displayed, font=("Arial", 10)),
    tk.Label(root, textvariable=bat_lvl_to_be_displayed, font=("Arial", 10)),
    tk.Label(root, textvariable=menu_to_be_displayed, font=("Arial", 10))
]


main_menu_labels = [
    tk.Label(root, textvariable=usr_to_be_displayed, font=("Arial", 10)),
    tk.Label(root, textvariable=menu_to_be_displayed, font=("Arial", 10)),
    tk.Label(root, textvariable=ps_to_be_displayed, font=("Arial", 10)),
    tk.Label(root, textvariable=bat_lvl_to_be_displayed, font=("Arial", 10)),
    tk.Label(root, text="3. Cerrar sesión", font=("Arial", 10))
]

admin_menu_labels = [
    tk.Label(root, textvariable=menu_to_be_displayed, font=("Arial", 10)),
    tk.Label(root, textvariable=ps_to_be_displayed, font=("Arial", 10)),
    tk.Label(root, textvariable=bat_lvl_to_be_displayed, font=("Arial", 10)),
    tk.Label(root, text="1. Registro de Usuarios", font=("Arial", 10)),
    tk.Label(root, text="2. Registro de Sensores", font=("Arial", 10)),
    tk.Label(root, text="3. Modificar Sensor", font=("Arial", 10)),
    tk.Label(root, text="4. Registro Num. Telefonico", font=("Arial", 10)),
    tk.Label(root, text="5. Salir Modo Admin", font=("Arial", 10))
]


# Colocar las líneas de texto adicionales en la interfaz (inicialmente ocultas)
row_custom = 1
for i, label in enumerate(start_menu_labels):
    label.grid(row=row_custom+i, column=0, columnspan=4, sticky="w")
    #label.grid_remove()  # Ocultar inicialmente

for i, label in enumerate(main_menu_labels):
    label.grid(row=row_custom+i, column=0, columnspan=4, sticky="w")
    label.grid_remove()  # Ocultar inicialmente

row_custom = 1
for i, label in enumerate(admin_menu_labels):
    label.grid(row=row_custom+i, column=0, columnspan=4, sticky="w")
    label.grid_remove()  # Ocultar inicialmente

row_custom+=len(admin_menu_labels)

label_bateria = tk.Label(root, text="Batería", bg="white", width=10, height=2)
label_bateria.grid(row=row_custom+1, column=0, columnspan=1)

label_alerta = tk.Label(root, text="Alerta", bg="white", width=10, height=2)
label_alerta.grid(row=row_custom+1, column=1, columnspan=2)

# Etiquetas adicionales en la interfaz principal
tk.Label(root, text="S E S", font=('Arial', 14)).grid(row=row_custom+2, column=0, columnspan=1)
tk.Label(root, text="SSH-101", font=('Arial', 14)).grid(row=row_custom+2, column=1, columnspan=2)

# Botón para abrir la interfaz secundaria
tk.Button(root, text="Abrir Interfaz Sim", command=open_secondary_interface).grid(row=row_custom+4, column=0, columnspan=4)

init_menu()
root.mainloop()