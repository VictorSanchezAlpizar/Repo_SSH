import json

Codes_list = {
    "Code_Modo_0"   : "123456",
    "Code_Modo_1"   : "234567",
    "Code_Desarmado": "345678",
    "Code_Admin"    : "456781",
    "Code_Ahorro"   : "567812"
}

def actualizar_Code(code_name, value):
    valid_config = False
    if code_name in Codes_list:
        Codes_list[code_name] = value
        valid_config = True
        return valid_config
    else:
        print("Configuracion no disponible")
        return valid_config

def save_Codes_list():
    with open("codes.txt", "w") as file:
        json.dump(Codes_list, file, indent=1)
    print("Lista de sensores almacenada en memoria")

def read_Codes_list():
    global Codes_list
    with open("codes.txt", "r") as file:
        Codes_list = json.load(file)
    print("Lista de codigos actualizada:", Codes_list)

def get_code(seq):
    code = ''
    for i in seq[1:-1]:
        code += i
    return code

def get_string(seq):
    code = ''
    for i in seq:
        code += i
    return code

#TESTS
#print(Codes_list["Code_Admin"])
#save_Codes_list()
#read_Codes_list()