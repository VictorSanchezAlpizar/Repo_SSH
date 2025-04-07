import threading
import time
from sensors_list import *

OFF_MODE    = 2

class ModoAhorroMonitor:
    def __init__(self, root, alert_callback):
        self.root = root
        self.alert_callback = alert_callback
        self.main_sensors = ["S1", "S7"]  # Sensores principales
        self.timeout = 5                   # 5s para desactivar secundarios
        self.evaluation_time = 7           # 7s para evaluar secundarios
        self.running = False
        self.alert_active = False
        self.secondary_sensors = []
        self.timers = {}
        self.evaluation_active = False  # Nuevo flag para controlar evaluación

    def _get_secondary_sensors(self):
        """Obtiene lista actualizada de sensores secundarios"""
        return [name for name, data in Sensors_list.items()
                if data["Install"] == INSTALL and name not in self.main_sensors]

    def start_monitoring(self):
        """Inicia el modo ahorro de energía"""
        if not self.running:
            self.running = True
            self.alert_active = False
            self.evaluation_active = False
            self.secondary_sensors = self._get_secondary_sensors()
            print(f"[MODO AHORRO] Iniciado")
            
            self._deactivate_secondaries()

            # 2. Mensaje y timer para empezar monitoreo
            print(f"[MODO AHORRO] Tienes {self.timeout}s para salir")
            self.timer = threading.Timer(self.timeout, self._start_monitoring_real)
            self.timer.start()

    def _start_monitoring_real(self):
        """Inicia el monitoreo después del tiempo de salida"""
        print("[MODO AHORRO] Monitoreo activado")
        threading.Thread(target=self._monitor_loop, daemon=True).start()

    def _monitor_loop(self):
        """Bucle principal de monitoreo"""
        while self.running:
            active_main_sensors = self._get_active_main_sensors()
            
            if active_main_sensors and not self.alert_active and not self.evaluation_active:
                print(f"[MODO AHORRO] Sensores principales activados: {active_main_sensors}")
                self._reactivate_secondaries()
                self._evaluate_secondaries(active_main_sensors)
            
            time.sleep(0.1)

    # SW-Req: [SW-ID-39]
    # SW-Req: [SW-ID-40]
    def _evaluate_secondaries(self, active_main_sensors):
        """Evalúa sensores secundarios durante 7 segundos"""
        self.evaluation_active = True
        evaluation_end = time.time() + self.evaluation_time
        alerted = False
        print(f"[MODO AHORRO] Evaluando sensores secundarios en {self.evaluation_time}s")
        
        while (time.time() < evaluation_end and 
               not alerted and 
               self.running and 
               self.evaluation_active):  # Ahora verifica evaluation_active
            
            active_secondaries = self._get_active_secondary_sensors()
            if active_secondaries:
                print(f"[MODO AHORRO] Alertando sensores secundarios: {active_secondaries}")
                self.alert_active = True
                self.evaluation_active = False
                self.alert_callback(active_secondaries)
                alerted = True
                break
                
            time.sleep(0.1)
        
        if not alerted and self.evaluation_active:  # Solo si la evaluación no fue cancelada
            print("[MODO AHORRO] Evaluación completada sin actividad en secundarios")
            if self._get_active_main_sensors():
                print(f"[MODO AHORRO] Sensores principales aún activos: {active_main_sensors}")
                self.alert_active = True
                self.evaluation_active = False
                self.alert_callback(active_main_sensors)
            else:
                self._deactivate_secondaries()
        
        self.evaluation_active = False

    # SW-Req: [SW-ID-40]
    def _get_active_main_sensors(self):
        """Devuelve lista de sensores principales activos"""
        return [name for name in self.main_sensors
                if self._is_sensor_active(name)]

    def _get_active_secondary_sensors(self):
        """Devuelve lista de sensores secundarios activos"""
        return [name for name in self.secondary_sensors
                if (name in Sensors_list and
                    Sensors_list[name]["Status"] == ACTIVE and
                    Sensors_list[name]["Install"] == INSTALL)]

    def _is_sensor_active(self, sensor_name):
        """Verifica si un sensor específico está activo"""
        return (sensor_name in Sensors_list and
                Sensors_list[sensor_name]["Status"] == ACTIVE and
                Sensors_list[sensor_name]["Install"] in [INSTALL, OFF_MODE])

    # SW-Req: [SW-ID-41]
    def _deactivate_secondaries(self):
        """Desactiva sensores secundarios"""
        if not self.running or self.alert_active:
            return

        for name in self.secondary_sensors:
            if name in Sensors_list:
                Sensors_list[name]["Install"] = OFF_MODE

        save_sensors_list()
        print("[MODO AHORRO] Sensores secundarios desactivados")

    
    def _reactivate_secondaries(self):
        """Reactiva todos los sensores secundarios"""
        self._cancel_timer('inactivity')
        for name in self.secondary_sensors:
            if name in Sensors_list:
                Sensors_list[name]["Install"] = INSTALL

        save_sensors_list()
        print("[MODO AHORRO] Todos los sensores reactivados")

    def _start_timer(self, name, interval, callback):
        """Inicia un timer con nombre"""
        self._cancel_timer(name)
        self.timers[name] = threading.Timer(interval, callback)
        self.timers[name].start()

    def _cancel_timer(self, name):
        """Cancela un timer específico"""
        if name in self.timers and self.timers[name].is_alive():
            self.timers[name].cancel()

    def stop_monitoring(self):
        """Detiene completamente el modo ahorro"""
        self.running = False
        self.alert_active = False
        self.evaluation_active = False
        for timer in self.timers.values():
            timer.cancel()
        print("[MODO AHORRO] Monitoreo detenido")

    def handle_disarm(self):
        """Maneja el desarme del sistema"""
        self.alert_active = False
        self.evaluation_active = False  # Esto cancela la evaluación en curso
        print("[MODO AHORRO] Sistema desarmado")
        # Volver a monitorear
        if self.running:
            self._deactivate_secondaries()