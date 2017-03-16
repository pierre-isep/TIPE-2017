# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

class Motor():
        """
        Définit un moteur
        """
        def __init__(self, a, b, freq):
                """
                Instancier et configurer le moteur
                """
                GPIO.setup(a, GPIO.OUT) #pin a configuré en sortie 
                GPIO.setup(b, GPIO.OUT) # pin b configuré en sortie
                self.frontpin = GPIO.PWM(a, freq) # on démarre l'instance PWM
                self.rearpin  = GPIO.PWM(b, freq) # idem
                self.frontpin.start(0) # démarre le duty cycle à 0%
                self.rearpin.start(0) # idem
                
        
        def set_speed(self, speed):  # Méthode d'instance
                """
                Prend les valeurs de speed entre -100 et 100 (AR / AV) , à 0 : on ne bouge pas 
                """
                print("[.] Motor.set_speed : got speed = " + str(speed))
                if speed > 0:
                        self.frontpin.ChangeDutyCycle(speed) # Si speed>0 on souhaite avancer 
                        self.rearpin.ChangeDutyCycle(0)
                elif speed < 0:
                        self.frontpin.ChangeDutyCycle(0)    # on souhaite reculer
                        self.rearpin.ChangeDutyCycle(-speed) # -speed car duty cycle doit etre positif
                elif speed == 0:
                        self.frontpin.ChangeDutyCycle(0) # si speed nul on ne souhaite pas bouger
                        self.rearpin.ChangeDutyCycle(0)
                        

class Robot():
        """
        Classe définissant un robot
        """
        def __init__ (self):
                """
                But : Instancier un robot et le configurer
                """
                self.angle = 0
                self.vitesse = 0
                
                # Config GPIO
                GPIO.setmode(GPIO.BCM) # Mapping des pins (en BCM pas en board)
                self.PWM_FREQ = 50    
                """ Fréquence de modulation PWM durant une période de 20ms  (fréquence : 50Hz)
                (envoie des signaux numériques durant cette période suivant le rapport cyclique (dc) en %)"""
                
                # Instanciation des moteurs
                self.moteur_gauche = Motor(14, 15 , self.PWM_FREQ) # moteur gauche va correspondre aux pins 14 et 15 (14 pour l'avant et 15 pour l'arrière) 
                self.moteur_droit = Motor(17, 18, self.PWM_FREQ) #même chose pour le moteur droit

        def set_angle(self, angle):
                """
                Définir la courbure à prendre
                Valeur de angle :

                Gauche                  Droite
                <---------------------------->
                -100    -50    0    50     100

                """
                if angle > 100:
                        print("[!] RobotControl : Valeur de angle supérieure à 100.\n[.] Remplacé par 100.")
                        angle = 100
                self.angle = angle

        def set_speed(self, vitesse):
                """
                Définir la vitesse du robot
                Valeur de vitesse :

                Arrière      Arrêt       Avant
                <---------------------------->
                -100    -50    0    50     100
                FULL         NONE         FULL
                """
                self.vitesse = vitesse
        
        def compute_wheelSpeeds(self):
            """
            Robot.compute_wheelSpeeds()
            Calculer la valeur de la vitesse théorique à appliquer à chaque moteur en fonction de la vitesse et de l'angle. 
            """
            left_motor = self.vitesse + self.angle
            right_motor = self.vitesse - self.angle
            
            # Scale factor defaults to 1 (échelle, facteur de proportionnalité)
            scale_factor = 1
            
            # Calculate scale factor
            if abs(left_motor) > 100 or abs(right_motor) > 100:
                # Find highest of the 2 values, since both could be above 100
                x = max(abs(left_motor), abs(right_motor))
            
                # Calculate scale factor
                scale_factor = 100.0 / x # revient entre 0 et 1
            
            # Use scale factor, and turn values back into integers
            left_motor = int(left_motor * scale_factor)
            right_motor = int(right_motor * scale_factor)
            self.left = left_motor
            self.right = right_motor
            print("[.] -- GAUCHE : " +str(self.left)+ " DROITE : " +str(self.right))
            
        def compute_and_go(self):
                """
                Compute motor values, then apply them
                """
                self.compute_wheelSpeeds()
                self.go()
        
        def go(self):
            """
            Appliquer les valeurs
            """
            try :
                self.moteur_gauche.set_speed(self.left)
                self.moteur_droit.set_speed(self.right)
                print("[.] -- GAUCHE : " +str(self.left)+ " DROITE : " +str(self.right))
            except :
                print("[!] Robot.go() : Les valeurs des vitesses n'ont pas encore été configurées. Ignorez cette erreur si elle ne réapparait pas. ")
        
        
        def stop(self):
            """
            Un arrêt pur et simple. Pratique, n'efface pas les valeurs de vitesse et d'angle.
            """
            self.moteur_gauche.set_speed(0)
            self.moteur_droit.set_speed(0)
                        