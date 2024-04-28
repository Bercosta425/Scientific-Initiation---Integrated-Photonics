import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
import serial as ser
import time
import Model
import numpy as np
from threading import Thread
# import camera_chinesa

#A relação microstep/mm é: 14474219/15mm
#Altura máxima do parafuso é de 15 mm
#Home atual: 8600408
#Posição máxima: 22084627

FormUI, WindowUI = uic.loadUiType("qtdesign.ui")
ser = ser.Serial('COM14',  baudrate=19200, bytesize=8, xonxoff=True, timeout=0.1)
a = ser.readlines()


command = '1TP?\n\r'
ser.write(command.encode())             
received_data = ser.readlines()[0]
decoded_string = received_data.decode("utf-8")

class Window(FormUI, WindowUI):
    t2 = None

    def __init__(self):
        super(Window, self).__init__()
        
        self.setupUi(self)
        
        self.stopmotion.clicked.connect(self.StopMotion)
        self.home.clicked.connect(self.Home)
        self.up_PR.clicked.connect(self.Move_PR_up)
        self.down_PR.clicked.connect(self.Move_PR_down)
        self.move_PA.clicked.connect(self.MovePa)
        self.up_free.pressed.connect(self.Move_up)
        self.up_free.released.connect(self.StopMotion)
        self.down_free.pressed.connect(self.Move_down)
        self.down_free.released.connect(self.StopMotion)
        self.pushButton.clicked.connect(lambda: self.set_v(self.angle.value()))
        
        self.position_update()
        
        self.show()

        # self.start_camera()

    # def closeEvent(self, event):
    #     camera_chinesa.run = False
    #     # self.t2.join()

    #     while camera_chinesa.cam.isOpened():
    #         time.sleep(0.1)
    #     event.accept() # let the window close

    # def start_camera(self):
    #     self.t2 = Thread(target=camera_chinesa.open_camera_red)
    #     self.t2.start()

    def real_position(self, position):
       real_position = "%.2f" % ((int(position[5:]) - (8600408)) * 15/15027738)
       return str(real_position)
    
    def position_update(self):
        time.sleep(0.1)
        command = '1TP?\n\r'
        ser.write(command.encode())      
        received_data = ser.readlines()[0]
        decoded_string = received_data.decode("utf-8")
        print(decoded_string)

        self.current_position.setText(self.real_position(decoded_string) + " mm")

    
    def set_v(self, angle):
        self.velocity_value.setValue(float(Model.v(angle, Model.R0, Model.tau)))
        return self.required_velocity.setText(Model.v(angle, Model.R0, Model.tau) + " *10^-6 m/s")
        
    
    def StopMotion(self):
        ser.write(b'1ST\n\r')   
        self.position_update()
        print("Motion stopped")
        print(' ')

    def Home(self):
        command = '1TP?\n\r'
        ser.write(command.encode())             
        received_data = ser.readlines()[0]
        decoded_string = received_data.decode("utf-8")
        if int(decoded_string[5:]) <= 8600408:
            print("Home reached")
        else:
            print("Search Home")
        #Define a velocidade:
            velocity = self.velocity_value.value()      #Velocidade digitada pelo usuário em um
            new_velocity = velocity*(15635*1.66)/1500          #Conversão para full-steps
            command = '1VA'+str(new_velocity)+'\n\r'    #Comando que será enviado para o motor
            ser.write(command.encode())                #Envia o comando
            time.sleep(0.1)

            command = '1VA?\n\r'
            ser.write(command.encode())             #Pergunta a velocidade atual
            received_data = ser.readlines()[0]
            decoded_string = received_data.decode("utf-8")
            print(decoded_string)
            check_velocity = float(decoded_string[5:])
            check_velocity = check_velocity*1500/(15635*1.66)
            print(f"Velocity = {check_velocity} um/s")
            
            time.sleep(0.1)
            
            #Define a aceleração:
            acceleration = self.acceleration_value.value()      #Aceleração digitada pelo usuário em um
            new_acceleration = acceleration*(15635*1.66)/1500          #Conversão para full-steps
            command = '1AC'+str(new_acceleration)+'\n\r'    #Comando que será enviado para o motor
            ser.write(command.encode())                #Envia o comando
            time.sleep(0.1)

            command = '1AC?\n\r'
            ser.write(command.encode())             #Pergunta a aceleração atual
            received_data = ser.readlines()[0]
            decoded_string = received_data.decode("utf-8")
            print(decoded_string)
            check_acceleration = float(decoded_string[5:])
            check_acceleration = check_acceleration*1500/(15635*1.66)
            print(f"Acceleration = {check_acceleration} um/s")        
            time.sleep(0.1)

            ser.write(b'1PA8600408\n\r')
            self.position_update()

            print(' ')

    def Move_down(self):
        command = '1TP?\n\r'
        ser.write(command.encode())             
        received_data = ser.readlines()[0]
        decoded_string = received_data.decode("utf-8")
        if int(decoded_string[5:]) <= 8600408:
            print("Home reached")
        else:
            print("Becker going down")
        #Define a velocidade:
        velocity = self.velocity_value.value()      #Velocidade digitada pelo usuário em um
        new_velocity = velocity*(15635*1.66)/1500         #Conversão para full-steps
        command = '1VA'+str(new_velocity)+'\n\r'    #Comando que será enviado para o motor
        ser.write(command.encode())                #Envia o comando
        time.sleep(0.1)

        command = '1VA?\n\r'
        ser.write(command.encode())             #Pergunta a velocidade atual
        received_data = ser.readlines()[0]
        decoded_string = received_data.decode("utf-8")
        
        check_velocity = float(decoded_string[5:])
        check_velocity = check_velocity*1500/(15635*1.66)
        print(f"Velocity = {check_velocity} um/s")
        
        time.sleep(0.1)
        
        #Define a aceleração:
        acceleration = self.acceleration_value.value()      #Aceleração digitada pelo usuário em um
        new_acceleration = acceleration*(15635*1.66)/1500          #Conversão para full-steps
        command = '1AC'+str(new_acceleration)+'\n\r'    #Comando que será enviado para o motor
        ser.write(command.encode())                #Envia o comando
        time.sleep(0.1)

        command = '1AC?\n\r'
        ser.write(command.encode())             #Pergunta a aceleração atual
        received_data = ser.readlines()[0]
        decoded_string = received_data.decode("utf-8")
        check_acceleration = float(decoded_string[5:])
        check_acceleration = check_acceleration*1500/(15635*1.66)
        print(f"Acceleration = {check_acceleration} um/s")        
        time.sleep(0.1)

        ser.write(b'1PA8600408\n\r')
        self.position_update()

        print(' ')

    def Move_up(self):
        command = '1TP?\n\r'
        ser.write(command.encode())             
        received_data = ser.readlines()[0]
        decoded_string = received_data.decode("utf-8")
        if int(decoded_string[5:]) >= 220846270:
            print("Maximum length reached")
        else:
            print("Becker going up")
    	#Define a velocidade:
            command = '1VA?\n\r'
            ser.write(command.encode())             #Pergunta a posição atual
            received_data = ser.readlines()[0]
            decoded_string = received_data.decode("utf-8")
            print(decoded_string)
            
            velocity = self.velocity_value.value()      #Velocidade digitada pelo usuário em um
            new_velocity = velocity*(15635*1.66)/1500          #Conversão para full-steps
            command = '1VA'+str(new_velocity)+'\n\r'    #Comando que será enviado para o motor
            ser.write(command.encode())                #Envia o comando
            time.sleep(0.1)

            command = '1VA?\n\r'
            ser.write(command.encode())             #Pergunta a velocidade atual
            received_data = ser.readlines()[0]
            decoded_string = received_data.decode("utf-8")
            
            check_velocity = float(decoded_string[5:])
            check_velocity = check_velocity*1500/(15635*1.66)
            print(f"Velocity = {check_velocity} um/s")
            
            time.sleep(0.1)
            
            #Define a aceleração:
            acceleration = self.acceleration_value.value()      #Aceleração digitada pelo usuário em um
            new_acceleration = acceleration*(15635*1.66)/1500          #Conversão para full-steps
            command = '1AC'+str(new_acceleration)+'\n\r'    #Comando que será enviado para o motor
            ser.write(command.encode())                #Envia o comando
            time.sleep(0.1)

            command = '1AC?\n\r'
            ser.write(command.encode())             #Pergunta a aceleração atual
            received_data = ser.readlines()[0]
            decoded_string = received_data.decode("utf-8")
            check_acceleration = float(decoded_string[5:])
            check_acceleration = check_acceleration*1500/(15635*1.66)
            print(f"Acceleration = {check_acceleration} um/s")        
            time.sleep(0.1)

            ser.write(b'1PA22084627\n\r')
            self.position_update()

            print(' ')

    def Move_PR_up(self):
        commando = '1TP?\n\r'
        ser.write(commando.encode())             #Pergunta a posição atual
        received_data = ser.readlines()[0]
        
        decoded_string = received_data.decode("utf-8")
        
        real_position = int(decoded_string[5:])
        print(real_position)

        if real_position > 22084627 :
            print("Limite máximo")
        elif real_position - 7190041/15 > 22084627 :
             ser.write(b'1PA9000000 \n\r')
        else:
        #Define a velocidade:
            velocity = self.velocity_value.value()      #Velocidade digitada pelo usuário
            new_velocity = velocity*(15635*1.66)/1500
            print(velocity)          #Conversão para full-steps
            command = '1VA'+str(new_velocity)+'\n\r'    #Comando que será enviado para o motor
            ser.write(command.encode())                #Envia o comando
            time.sleep(0.1)

            command = '1VA?\n\r'
            ser.write(command.encode())             #Pergunta a velocidade atual
            received_data = ser.readlines()[0]
            decoded_string = received_data.decode("utf-8")
            print(decoded_string)
            check_velocity = float(decoded_string[5:])
            check_velocity = check_velocity*1500/(15635*1.66)
            print(f"Velocity = {check_velocity} um/s")
            
            time.sleep(0.1)
            
            #Define a aceleração:
            acceleration = self.acceleration_value.value()      #Aceleração digitada pelo usuário em um
            new_acceleration = acceleration*(15635*1.66)/1500          #Conversão para full-steps
            command = '1AC'+str(new_acceleration)+'\n\r'    #Comando que será enviado para o motor
            ser.write(command.encode())                #Envia o comando
            time.sleep(0.1)

            command = '1AC?\n\r'
            ser.write(command.encode())             #Pergunta a aceleração atual
            received_data = ser.readlines()[0]
            decoded_string = received_data.decode("utf-8")
            check_acceleration = float(decoded_string[5:])
            check_acceleration = check_acceleration*1500/(15635*1.66)
            print(f"Acceleration = {check_acceleration} um/s")        
            time.sleep(0.1)

            
            command = '1PR'+str(7190041/15)+'\n\r'
            ser.write(command.encode())  
            print('Moved up 0,5 mm')
            self.position_update()
            print(' ')

    def Move_PR_down(self):

        commando = '1TP?\n\r'
        ser.write(commando.encode())             #Pergunta a velocidade atual
        received_data = ser.readlines()[0]
        decoded_string = received_data.decode("utf-8")
        print(decoded_string)

        real_position = float(decoded_string[5:])

        if real_position < 8600408:
            print("Limite máximo")
        elif real_position - 7190041/15 < 8600408:
            self.Home()
        else:
        #Define a velocidade:
            velocity = self.velocity_value.value()      #Velocidade digitada pelo usuário em um
            new_velocity = velocity*(15635*1.66)/1500          #Conversão para full-steps
            command = '1VA'+str(new_velocity)+'\n\r'    #Comando que será enviado para o motor
            ser.write(command.encode())                #Envia o comando
            time.sleep(0.1)

            command = '1VA?\n\r'
            ser.write(command.encode())             #Pergunta a velocidade atual
            received_data = ser.readlines()[0]
            decoded_string = received_data.decode("utf-8")
            
            check_velocity = float(decoded_string[5:])
            check_velocity = check_velocity*1500/(15635*1.66)
            print(f"Velocity = {check_velocity} um/s")
            
            time.sleep(0.1)
            
            #Define a aceleração:
            acceleration = self.acceleration_value.value()      #Aceleração digitada pelo usuário em um
            new_acceleration = acceleration*(15635*1.66)/1500          #Conversão para full-steps
            command = '1AC'+str(new_acceleration)+'\n\r'    #Comando que será enviado para o motor
            ser.write(command.encode())                #Envia o comando
            time.sleep(0.1)

            command = '1AC?\n\r'
            ser.write(command.encode())             #Pergunta a aceleração atual
            received_data = ser.readlines()[0]
            decoded_string = received_data.decode("utf-8")
            check_acceleration = float(decoded_string[5:])
            check_acceleration = check_acceleration*1500/(15635*1.66)
            print(f"Acceleration = {check_acceleration} um/s")        
            time.sleep(0.1)
            
            command = '1PR-'+str(7190041/15)+'\n\r'
            ser.write(command.encode())  
            print('Moved down 0,5 mm')
            self.position_update()
            print(' ')

    def MovePa(self):
        #Define a velocidade:
        velocity = self.velocity_value.value()      #Velocidade digitada pelo usuário em um
        new_velocity = velocity*(15635*1.66)/1500
        command = '1VA'+str(new_velocity)+'\n\r'    #Comando que será enviado para o motor
        ser.write(command.encode())                #Envia o comando
        time.sleep(0.1)

        command = '1VA?\n\r'
        ser.write(command.encode())             #Pergunta a velocidade atual
        received_data = ser.readlines()[0]
        decoded_string = received_data.decode("utf-8")
        
        check_velocity = float(decoded_string[5:])
        check_velocity = check_velocity*1500/(15635*1.66)
        print(f"Velocity = {check_velocity} um/s")
        
        time.sleep(0.1)
        
        #Define a aceleração:
        acceleration = self.acceleration_value.value()      #Aceleração digitada pelo usuário em um
        new_acceleration = acceleration*(15635*1.66)/1500          #Conversão para full-steps
        command = '1AC'+str(new_acceleration)+'\n\r'    #Comando que será enviado para o motor
        ser.write(command.encode())                #Envia o comando
        time.sleep(0.1)

        command = '1AC?\n\r'
        ser.write(command.encode())             #Pergunta a aceleração atual
        received_data = ser.readlines()[0]
        decoded_string = received_data.decode("utf-8")
        check_acceleration = float(decoded_string[5:])
        check_acceleration = check_acceleration*1500/(15635*1.66)
        print(f"Acceleration = {check_acceleration} um/s")        
        time.sleep(0.1)

        absolute_position = self.absolute_position.value()

        new_absolute_position = absolute_position*15027738/15 + (8600408)
        command = '1PA'+str(new_absolute_position)+'\n\r'    #Comando que será enviado para o motor
        ser.write(command.encode())
        self.position_update() 

        print("Moved")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    
    janela = Window()
    
    # Run application
    app.exec()

    # Exit when done
    sys.exit()