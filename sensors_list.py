import json

#Zone Disponibles
ZONE_0 = 0
ZONE_1 = 1

#Status Disponibles
ACTIVE = 1
INACTIVE = 0

#Install Estatus
OFF_MODE    = 2
INSTALL     = 1
NOT_INSTALL = 0

# SW-Req: [SW-ID-27]
# SW-Req: [SW-ID-16]
Sensors_list = {
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

# SW-Req: [SW-ID-88]
# SW-Req: [SW-ID-92]
def actualizar_sensor(sensor_name, key, value):
    valid_config = False
    if sensor_name in Sensors_list and key in Sensors_list[sensor_name]:
        Sensors_list[sensor_name][key] = value
        valid_config = True
        return valid_config
    else:
        print("Configuracion no disponible")
        return valid_config

# SW-Req: [SW-ID-29]
# SW-Req: [SW-ID-15]
def save_sensors_list():
    with open("sensors.txt", "w") as file:
        json.dump(Sensors_list, file, indent=4)
    print("Lista de sensores almacenada en memoria")

# SW-Req: [SW-ID-29]
# SW-Req: [SW-ID-15]
def read_sensors_list():
    global Sensors_list
    with open("sensors.txt", "r") as file:
        Sensors_list = json.load(file)
    print("Lista de sensores actualizada:", Sensors_list)

#read_sensors_list()

"""
HOWTO: Guardar y leer de "memoria" la lista de sensores

print(f'Sensor ID: {Sensors_list["S1"]["ID"]}')
print(f'Sensor Install Status: {Sensors_list["S1"]["Install"]}')

x = actualizar_sensor("S1", "Install", INSTALL)

print(f'Sensor ID: {Sensors_list["S1"]["ID"]}')
print(f'Sensor Install Status: {Sensors_list["S1"]["Install"]}')
print(f'Was config valid: {x}')

save_sensors_list()
read_sensors_list()

print(f'Sensor ID: {Sensors_list["S1"]["ID"]}')
print(f'Sensor Install Status: {Sensors_list["S1"]["Install"]}')
"""

"""
HOWTO: Acceder lista de sensores

print(f'Sensor ID: {Sensors_list["S1"]["ID"]}')
print(f'Sensor Install Status: {Sensors_list["S1"]["Install"]}')

x = actualizar_sensor("S1", "Install", INSTALL)
print(f'Sensor ID: {Sensors_list["S1"]["ID"]}')
print(f'Sensor Install Status: {Sensors_list["S1"]["Install"]}')
print(f'Was config valid: {x}')

x = actualizar_sensor("S1", "Installed", INSTALL)
print(f'Sensor ID: {Sensors_list["S1"]["ID"]}')
print(f'Sensor Install Status: {Sensors_list["S1"]["Install"]}')
print(f'Was config valid: {x}')
"""
