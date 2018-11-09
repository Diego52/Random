import input_data
import sys
import easygui
class Cuentas():
    cuenta1 = {
        'numero_cuenta':24,
        'saldo':15000,
        'interes': 2
        }
    cuenta2 = {
        'numero_cuenta':25,
        'saldo':8000,
        'interes': 5
        }
def reitengro(cuenta):
    print("Selecciona una accion: \n")
    print("1- Retirar")
    print("2- Salir")
    choice = input_data.get_value()
    if (choice == "1"): 
        print("ingrese una cantidad: \n")
        retiro = input_data.get_value()
        retiro = int(retiro)
        if (retiro < cuenta["saldo"]):
            print("Tu transaccion fue exitosa")
            cuenta["saldo"] = cuenta["saldo"] - retiro
        else: 
            print("No tienes saldo suficiente")
    elif(choice == "2"):
        sys.exit()
def main():
    title = 'BANCO AA'
    easygui.msgbox('Bienvenido al BANCO AA', title, 'Next', image="logo.jpg")
    print("\nBienvenido al BANCO AA\n")
    fieldValues = easygui.multenterbox("Ingresa tu numero de cuenta:",title, ["Numero de cuenta"])
    print("Ingresa tu numero de cuenta:\n")
    numero_cuenta = int(input_data.get_value()) 
    if(numero_cuenta == Cuentas.cuenta1["numero_cuenta"]):
        print("Tu numero de cuenta es: ")
        print(Cuentas.cuenta1["numero_cuenta"],"\n")
        print("Tu saldo es: ")
        print("$",Cuentas.cuenta1["saldo"],"\n")
        print("Tu interes es: ")
        print(Cuentas.cuenta1["interes"],"%\n")
        reitengro(cuenta= Cuentas.cuenta1)
    elif (numero_cuenta == Cuentas.cuenta2["numero_cuenta"]):
        print("Tu numero de cuenta es: ")
        print(Cuentas.cuenta2["numero_cuenta"],"\n")
        print("Tu saldo es: ")
        print("$",Cuentas.cuenta2["saldo"],"\n")
        print("Tu interes es: ")
        print(Cuentas.cuenta2["interes"],"%\n")
        reitengro(cuenta= Cuentas.cuenta2)
    else:
        print("Cuenta no disponible")   

while True: 
    main()
