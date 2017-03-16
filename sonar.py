# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class Infra():
        def __init__(self,sortie):

            self.sortie = sortie
            GPIO.setup(self.sortie,GPIO.IN)

        def is_near_obstacle(self) :
            if GPIO.input(IN)==1 : #si il y'a un objet à proximité détecté
                return True
            else :
                return False




class Sonar():
    def __init__(self, trig, echo):
        """
        Sonar(trig, echo)
        """
        self.TRIG = trig
        self.ECHO = echo
        GPIO.setup(self.TRIG,GPIO.OUT) 
        GPIO.setup(self.ECHO,GPIO.IN) 

    def avg_mesure(self):
        somme = 0
        compteur = 0
        for a in range(0,5):
                somme += self.mesure()
                compteur += 1
        return round(somme/compteur,2) 
        """on arrondit la moyenne à 2 décimales après la virgule"""

    def mesure(self):

        GPIO.output(self.TRIG, False) 
        """on met la broche trig initialement à un potentiel nul"""
        print ("Waiting For Sensor To Settle")
        time.sleep(2) # laisse 2s au capteur pour s'initialiser

        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)
        """on a activé le capteur pendant 10 micro-secondes qui émet donc un train d'ultrasons 
        (8 séries à 40 Hz) la broche écho d'entrée du rapi va rester à 3,3V tout le temps 
        que met le signal pour partir du capteur, se réfléchir sur un objet et revenir """

        while GPIO.input(self.ECHO)==0:
            pulse_start = time.time()
            
"""Calcul du basculement à l'état haut : on démarre un timer à l'instant où le capteur 
à finis d'émettre un train d'impulsion """

        while GPIO.input(self.ECHO)==1:
            pulse_end = time.time()
            
"""Calcul du basculement à l'état bas : on arrête le timer dès que le capteur 
reçoit les ultrasons réfléchis """

        pulse_duration = pulse_end - pulse_start
        temps_émission = pulse_duration/2 
        
""" on fait la moyenne du temps de parcours aller-retour
 pour avoir le temps que met l'onde pour aller de l'éméteur à l'obstacle """
 
         vitesse_ref = 34300 
 """ valeur de référence vitesse du son dans l'air au niveau de la mer """
         distance = vitesse_ref * temps_émission 
         distance = round(distance, 2) # affiche la distance
         
        return distance


def test():
    sonar1 = Sonar(23, 24)
    
    while 1:   #Boucle infinie
            try:
                    distance = sonar1.avg_mesure()
                    print "Distance:", distance ,"cm"
            except:
                    print("my job here is done")
                    break
    
    GPIO.cleanup() #remet à zéro les broches du GPIO (réinitialise)
    
###########################################################################################
#                                                                                         #
# TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING #
# TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING #
#                                                                                         #
###########################################################################################

# Uncomment to test :
#test()



