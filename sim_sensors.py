import tkinter as tk
from sensors_list import *

class SimSensors:
    def __init__(self, root):
        self.root = root
        self.sensor_window = None
        self.default_bg_color = "#f0f0f0"
        self.active_bg_color = "red"
        self.sensor_buttons = {}
        self.sensor_states = {}  # Diccionario para guardar estados localmente

    def open_sim_sensor_falla(self):
        """Abre la ventana de simulación de fallas en sensores"""
        if self.sensor_window and self.sensor_window.winfo_exists():
            self.sensor_window.lift()
            return
            
        self.sensor_window = tk.Toplevel(self.root)
        self.sensor_window.title("Simulador de Fallas en Sensores")
        self.sensor_window.config(padx=10, pady=10)
        
        frame = tk.Frame(self.sensor_window)
        frame.pack()
        
        # Inicializar estados desde Sensors_list
        self._init_sensor_states()
        
        # Crear matriz 4x4 de botones
        for i in range(4):
            for j in range(4):
                sensor_num = i * 4 + j + 1
                sensor_name = f"S{sensor_num}"
                btn = tk.Button(
                    frame,
                    text=f"S{sensor_num}",
                    width=5,
                    height=2,
                    bg=self.active_bg_color if self.sensor_states[sensor_name] else self.default_bg_color,
                    command=lambda num=sensor_num: self.toggle_sensor_state(num))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.sensor_buttons[sensor_num] = btn
        
        # Botón para cerrar
        tk.Button(
            self.sensor_window,
            text="Cerrar",
            command=self.sensor_window.destroy
        ).pack(pady=10)

    def _init_sensor_states(self):
        """Inicializa los estados de los sensores desde Sensors_list"""
        self.sensor_states = {
            f"S{i}": bool(Sensors_list[f"S{i}"]["Status"])
            for i in range(1, 17)
        }

    def toggle_sensor_state(self, sensor_num):
        """Alterna el estado del sensor de manera robusta"""
        sensor_name = f"S{sensor_num}"
        
        # Obtener estado actual desde el diccionario local
        current_state = self.sensor_states.get(sensor_name, False)
        new_state = not current_state
        
        # Actualizar estado local
        self.sensor_states[sensor_name] = new_state
        
        # Actualizar interfaz
        btn = self.sensor_buttons.get(sensor_num)
        if btn:
            btn.config(bg=self.active_bg_color if new_state else self.default_bg_color)
        
        # Actualizar Sensors_list y guardar
        if actualizar_sensor(sensor_name, "Status", ACTIVE if new_state else INACTIVE):
            status_text = "ACTIVADO" if new_state else "DESACTIVADO"
            print(f"Sensor {sensor_name} {status_text}")
            save_sensors_list()