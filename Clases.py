import sys    #importamos la libreria del sistema que nos permite abortar el codigo
import easygui
class Contador(): #Creamos la clase Contador
    def __init__(self): #Creamos el constructor de la clase, el cual la incializa
        self.N = None   #Declaramos la variable como Global y le asignamos un valor nulo
    def SetContador(self, n): #Creamos el metodo (funcion) SetContador al que le ponemos un parametro de entrada "n"
        self.N = n #Asignamos la variable global N a dicho parametro
    def Incrementar(self): #Creamos el metodo Incrementar
        self.N += 1 #Incrementamos en 1 y guardamos en la misma variable
    def GetCont(self): #Creamos el metodo GetCont
        return self.N  #El cual unicamente retorna el valor de N para ser accedido en el codigo e impreso en la consola
title = "Clases"
C1 = Contador() #Creamos una instancia C1 de la clase Contador
C2 = Contador() #Creamos una instancia C2 de la clase Contador
numero1 = easygui.multenterbox("Ingresa la cantidad 1:",title, ["Cantidad 1"]) #Creamos la interfaz que solicita el dato 1
numero1 = int(numero1[0]) #Convertimos el dato 1 a entero para hacer la operacion
C1.SetContador(numero1) #De la instancia C1 llamamos al metodo SetContador antes definido y le damos el parametro de entrada igual a 0
C1.Incrementar()  #De la instancia C1 llamamos al metodo Incrementar
ans = str(C1.GetCont()) #Convertimos el resultado de GetCont de la instancia C1 a string para colocarlo en la interfaz
easygui.msgbox('El resultado 1 es: ' + ans, title, 'Next', image="logo2.jpg") #Creamos la interfaz
#Imprimimos el resultado del metodo GetCont de la instancia C1
numero2 = easygui.multenterbox("Ingresa la cantidad 2:",title, ["Cantidad 2"]) # #creamos la interfaz que solicita el dato 2
numero2 = int(numero2[0])  #Convertimos el dato 2 a entero para hacer la operacion
C2.SetContador(numero2) #De la instancia C2 llamamos al metodo SetContador antes definido y le damos el parametro de entrada igual a 0
C2.Incrementar()  #De la instancia C2 llamamos al metodo Incrementar, aqui N pasa a ser 1
C2.Incrementar()  #De la instancia C2 llamamos al metodo Incrementar, aqui N pasa a ser 2
C2.Incrementar()  #De la instancia C2 llamamos al metodo Incrementar, aqui N pasa a ser 3
ans2 = str(C2.GetCont()) #Imprimimos el resultado del metodo GetCont de la instancia C2
easygui.msgbox('El resultado 2 es: ' + ans2, title, 'Next', image="logo2.jpg") #Creamos la interfaz
easygui.msgbox('C1: ' + ans + '\n' + 'C2: ' + ans2, title, 'Next', image="logo2.jpg") #Creamos la interfaz que imprime los 2 resultados
sys.exit() #Abortamos la ejecucion 



