import threading
import time
from sensors_list import *

class ModoAhorroMonitor:
    def __init__(self, root, alert_callback, main_sensors=["S1"], timeout=5):
        self.root = root
        self.alert_callback = alert_callback
        self.main_sensors = main_sensors  # Sensores principales (siempre activos)
        self.timeout = timeout  # Tiempo para desactivar secundarios (ej. 300s = 5min)
        self.running = False
        self.thread = None
        self.check_interval = 0.5  # Igual que en Modo0
        self.last_activity_time = None
        self.secondary_sensors = self._get_secondary_sensors()

    def _get_secondary_sensors(self):
        """Lista de sensores secundarios (instalados y no principales)"""
        return [
            name for name, data in Sensors_list.items()
            if data["Install"] == INSTALL and name not in self.main_sensors
        ]

    def start_monitoring(self):
        """Inicia el modo ahorro: desactiva secundarios y monitorea principales"""
        if not self.running:
            self._set_secondary_sensors_install(OFF_MODE)  # Desactiva secundarios
            self.running = True
            self.last_activity_time = time.time()
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()
            print(f"[MODO AHORRO] Iniciado. Timeout: {self.timeout}s")

    def _monitor_loop(self):
        """Bucle principal idéntico en estructura a Modo0"""
        while self.running:
            if self._check_main_sensors_activated():
                self._handle_activity()
            self._check_inactivity()
            time.sleep(self.check_interval)

    def _check_main_sensors_activated(self):
        """Misma lógica que Modo0 pero solo para main_sensors"""
        return any(
            Sensors_list[name]["Status"] == ACTIVE
            for name in self.main_sensors
            if name in Sensors_list and Sensors_list[name]["Install"] == INSTALL
        )

    def _handle_activity(self):
        """Al detectar actividad en sensores principales"""
        if self._are_secondaries_disabled():
            self._reactivate_secondaries()
        self.last_activity_time = time.time()  # Reinicia contador

    def _check_inactivity(self):
        """Desactiva secundarios si pasa el timeout sin actividad"""
        if (time.time() - self.last_activity_time > self.timeout 
            and not self._are_secondaries_disabled()):
            self._deactivate_secondaries()

    def _are_secondaries_disabled(self):
        """Verifica si los secundarios están OFF_MODE"""
        return all(
            Sensors_list[name]["Install"] == OFF_MODE 
            for name in self.secondary_sensors 
            if name in Sensors_list
        )

    def _reactivate_secondaries(self):
        """Reactiva sensores secundarios (Install=INSTALL)"""
        self._set_secondary_sensors_install(INSTALL)
        print("[MODO AHORRO] Sensores secundarios reactivados")

    def _deactivate_secondaries(self):
        """Desactiva sensores secundarios (Install=OFF_MODE)"""
        self._set_secondary_sensors_install(OFF_MODE)
        print(f"[MODO AHORRO] Sensores secundarios desactivados por inactividad")

    def _set_secondary_sensors_install(self, mode):
        """Cambia Install de los secundarios (INSTALL/OFF_MODE)"""
        for name in self.secondary_sensors:
            if name in Sensors_list:
                Sensors_list[name]["Install"] = mode
        save_sensors_list()

    def stop_monitoring(self):
        """Detiene el modo idéntico a Modo0"""
        if self.running:
            self.running = False
            self._reactivate_secondaries()  # Reactiva todo al salir
            if self.thread:
                self.thread.join()
            print("[MODO AHORRO] Monitor detenido")

    def check_desarmado_during_operation(self):
        """Para cancelar operaciones pendientes al desarmar"""
        if self.running:
            print("[MODO AHORRO] Desarmado manual detectado")