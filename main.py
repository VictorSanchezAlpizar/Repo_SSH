import tkinter as tk
from code_lists import *
from sensors_list import *
from admin_mode import *

#Parameters --------------------------------------------------------------------------------------
# Crear la interfaz principal
root = tk.Tk()
root.title("Interfaz Principal")

# Crear y colocar los botones en la interfaz principal
buttons = [
    '1', '2', '3', 'Esc',
    '4', '5', '6', 'Enter',
    '7', '8', '9', 'Pánico',
    '*', '0', '#', 'Bomberos'
]

row_custom    = 0
col_custom    = 0
current_State = 0

sequence = []
additional_text_labels = []

#States
START_MENU          = 0
MAIN_MENU           = 1
USER_MODE_MENU      = 2
MODO_0_MENU         = 3
MODO_1_MENU         = 4
MODO_DESARMADO_MENU = 5
MODO_AHORRO         = 6

#ERROR_CODES
ERROR_MODE = -1
EXIT_MODE  =  0

#Utils ---------------------------------------------------------------------------------------------

def update_label():
    """Actualiza el label_ID según el estado actual."""
    if current_State == START_MENU:
        label_ID.config(text="User ID: ")
        hide_all()
    elif current_State == MAIN_MENU:
        label_ID.config(text="Opciones: ")
        hide_all()
        show_main_menu()

def hide_all():
    hide_main_menu()

def show_main_menu():
    """Muestra las líneas de texto adicionales en la pantalla principal."""
    for label in additional_text_labels:
        label.grid()

def hide_main_menu():
    """Oculta las líneas de texto adicionales en la pantalla principal."""
    for label in additional_text_labels:
        label.grid_remove()

#MAIN APP
#USR INTERACTS WITH SSH

def on_button_click(value):
    global current_State, sequence

    if value == "Pánico" or value == "Bomberos":
        # Cambiar el color del indicador L1 a verde cuando se presiona "Batería"
        label_alerta.config(bg="red")

    elif value == "Esc":
        # Limpiar el cuadro de texto si se presiona "Esc"
        entry_ID.delete(0, tk.END)
        sequence.clear()  # Limpiar la secuencia

    elif value == "Enter":
        if (current_State == START_MENU and sequence == ["1"]):
            current_State = MAIN_MENU  # Cambiar al menú principal
            update_label()  # Actualizar el label
        elif (current_State == START_MENU):
            update_label()  # Actualizar el label
        elif current_State == MODO_0_MENU:
            1
        elif current_State == MODO_1_MENU:
            1
        elif current_State == MODO_DESARMADO_MENU:
            1
        elif current_State == USER_MODE_MENU:
            current_command = get_string(sequence)
            status = admin_mode(current_command)
            if (status == ERROR_MODE or status == EXIT_MODE):
                current_State = START_MENU  # Volver al estado inicial
                update_label()  # Actualizar el label
        elif current_State == MODO_AHORRO:
            1
        else:
            if (sequence[0]=='#' and sequence[-1]=='*'):
                current_Code = get_code(sequence)
                if (current_Code == Codes_list["Code_Modo_0"]):
                    current_State = MODO_0_MENU

                elif (current_Code == Codes_list["Code_Modo_1"]):
                    current_State = MODO_1_MENU

                elif (current_Code == Codes_list["Code_Desarmado"]):
                    current_State = MODO_DESARMADO_MENU

                elif (current_Code == Codes_list["Code_Admin"]):
                    current_State = USER_MODE_MENU

                elif (current_Code == Codes_list["Code_Ahorro"]):
                    current_State = MODO_AHORRO

                else:
                    print("Invalid command. Returning to START MENU")
                    current_State = START_MENU  # Volver al estado inicial

            update_label()  # Actualizar el label
        entry_ID.delete(0, tk.END)
        sequence.clear()  # Limpiar la secuencia

    else:
        # Añadir el valor del botón al cuadro de texto
        entry_ID.insert(tk.END, value)
        sequence.append(value)  # Añadir el valor a la secuencia

    print(f"Button {value} clicked")

def turn_on_main_button(value):
    if value == "Sim falla electrica ON":
        # Cambiar el estado del botón en la interfaz principal
        label_bateria.config(bg="green", text="Batería")
    if value == "Sim falla electrica OFF":
        # Cambiar el estado del botón en la interfaz principal
        label_bateria.config(bg="white", text="Batería")
    if value == "Sim Bomberos PASS":
        # Cambiar el estado del botón en la interfaz principal
        label_alerta.config(bg="white", text="Alerta")

def open_secondary_interface():
    secondary_window = tk.Toplevel(root)
    secondary_window.minsize(width=25, height=25)
    secondary_window.config(padx=5, pady=5)
    secondary_window.title("Interfaz Secundaria")

    # Botón en la interfaz secundaria para encender el botón en la principal
    tk.Button(secondary_window, text="Sim falla electrica ON", command=lambda b="Sim falla electrica ON": turn_on_main_button(b)).pack(pady=5)
    tk.Button(secondary_window, text="Sim falla electrica OFF", command=lambda b="Sim falla electrica OFF": turn_on_main_button(b)).pack(pady=10)
    tk.Button(secondary_window, text="Sim Sensor falla", command=lambda b="Sim Sensor falla": turn_on_main_button(b)).pack(pady=15)
    tk.Button(secondary_window, text="Sim Bomberos PASS", command=lambda b="Sim Bomberos PASS": turn_on_main_button(b)).pack(pady=20)
    
#Main interface ---------------------------------------------------------------------------------------

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
additional_text_labels = [
    tk.Label(root, text="1. Ver perfil", font=("Arial", 12)),
    tk.Label(root, text="2. Cambiar contraseña", font=("Arial", 12)),
    tk.Label(root, text="3. Cerrar sesión", font=("Arial", 12))
]

row_custom = 1

# Colocar las líneas de texto adicionales en la interfaz (inicialmente ocultas)
for i, label in enumerate(additional_text_labels):
    label.grid(row=row_custom+i, column=0, columnspan=4, sticky="w")
    label.grid_remove()  # Ocultar inicialmente

row_custom+=len(additional_text_labels)

label_bateria = tk.Label(root, text="Batería", bg="white", width=10, height=2)
label_bateria.grid(row=row_custom+1, column=0, columnspan=1)

label_alerta = tk.Label(root, text="Alerta", bg="white", width=10, height=2)
label_alerta.grid(row=row_custom+1, column=1, columnspan=2)

# Etiquetas adicionales en la interfaz principal
tk.Label(root, text="S E S", font=('Arial', 14)).grid(row=row_custom+2, column=0, columnspan=1)
tk.Label(root, text="SSH-101", font=('Arial', 14)).grid(row=row_custom+2, column=1, columnspan=2)

# Botón para abrir la interfaz secundaria
tk.Button(root, text="Abrir Interfaz Sim", command=open_secondary_interface).grid(row=row_custom+4, column=0, columnspan=4)

root.mainloop()