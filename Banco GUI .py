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
def reitengro(cuenta,title):
    image = "logo.jpg"
    msg = "Selecciona una accion: \n"
    choices = ["Retirar","Salir"]
    choice = easygui.buttonbox(msg, image=image, choices=choices, title=title)
    if (choice == "Retirar"): 
        retiro = easygui.multenterbox("Ingresa la cantidad:",title, ["Cantidad"])
        if retiro is not None:
            try:
                retiro = int(retiro[0])
            except:
                retiro = cuenta["saldo"] * 2
                
        else: 
            sys.exit()
        if (retiro < cuenta["saldo"]):
            easygui.msgbox('Tu transaccion fue exitosa', title, 'Next', image="logo.jpg")
            cuenta["saldo"] = cuenta["saldo"] - retiro
        else: 
            easygui.msgbox('No cuentas con suficiente saldo o la cantidad no es valida', title, 'Next', image="logo.jpg")
    elif(choice == "Salir"):
        sys.exit()
def main():
    title = 'BANCO AA'
    easygui.msgbox('Bienvenido al BANCO AA', title, 'Next', image="logo.jpg")
    numero_cuenta = easygui.multenterbox("Ingresa tu numero de cuenta:",title, ["Numero de cuenta"])
    if numero_cuenta is not None:
        try:
            numero_cuenta = int(numero_cuenta[0])
        except:
            numero_cuenta = "NA"
    else:
        sys.exit()
    if(numero_cuenta == Cuentas.cuenta1["numero_cuenta"]):
        easygui.msgbox('Tu numero de cuenta es: \n\n' + str(Cuentas.cuenta1["numero_cuenta"])
         +"\n\n" +  "Tu saldo es: \n\n$" + str(Cuentas.cuenta1["saldo"]) + "\n\n" + "Tu interes es: \n\n"
         + str(Cuentas.cuenta1["interes"]) +"%"  , title, 'Next', image="logo.jpg")
        reitengro(cuenta= Cuentas.cuenta1, title=title)
    elif (numero_cuenta == Cuentas.cuenta2["numero_cuenta"]):
        easygui.msgbox('Tu numero de cuenta es: \n\n' + str(Cuentas.cuenta2["numero_cuenta"])
         +"\n\n" +  "Tu saldo es: \n\n$" + str(Cuentas.cuenta2["saldo"]) + "\n\n" + "Tu interes es: \n\n"
         + str(Cuentas.cuenta2["interes"]) +"%"  , title, 'Next', image="logo.jpg")
        reitengro(cuenta= Cuentas.cuenta2, title=title)
    else:
        easygui.msgbox("Cuenta no disponible", title, 'Next', image="triste.jpg")
 

while True: 
    main()
