REG_USR = 1
REG_SNR = 2
MOD_SNR = 3
REG_TEL = 4
EXIT    = 5

def admin_mode(cmd):
    status = 0
    print("Admin mode")
    if (cmd == REG_USR):
        1
    elif (cmd == REG_SNR):
        2
    elif (cmd == MOD_SNR):
        3
    elif (cmd == REG_TEL):
        4
    elif (cmd == EXIT):
        5
    else:
        print("Invalid.")
        status = 3
    return status

