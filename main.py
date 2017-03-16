# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from robotcontrol import Robot, Motor
from sonar import Sonar

GPIO.setmode(GPIO.BCM)

SPEED = 60

robot = Robot()
robot.set_speed(SPEED)

prev_angle = 0

while 1:  # Boucle infinie
    try:
        sonar1 = Sonar(23, 24)
"""
        sonar2 = Sonar(22,10)
        sonar3 = Sonar(9,11)
        sonar4 = Sonar(8,7)
        infra1 = Infra(2)
        infra2 = Infra(3)
"""


        distance1 = sonar1.avg_mesure()
     """distance2 = sonar2.avg_mesure()
        distance3 = sonar3.avg_mesure()
        distance4 = sonar4.avg_mesure()"""

        print(distance1,"distance2,distance3,distance4")

        proxy1 = infra1.proxy()
        proxy2 = infra2.proxy()

        if proxy1 == 1 
            angle = 0
            robot.set_speed(-SPEED)
        if proxy2 == 1
            angle = 0
            robot.set_speed(-SPEED)

""" Car les capteurs infrarouges sont derrieres donc 
si ils détectent un objet c'est qu'on recule sur quelque chose, il faut alors réavancer
        
"""
        # set angle
        if distance >= 70 :
            angle = 0 #pas d'obstacle à proximité, on ne tourne pas 
            robot.set_speed(SPEED)
            
            print("Tout droit")    
        elif distance >= 20:
            # Distance : entre 20 et 70. 
            d = 1- ((distance - 20) * 2 / 100)
            # Distance : entre 0 et 1 . (Unités arbitraires!)
            angle = d * 100 # cela permet d'appliquer un pourcentage de rotation
            robot.set_speed(SPEED)
            
            print("je tourne de "+str(angle))
        else :
            # La distance est de moins de 5 cm
            angle = 0
            robot.set_speed(-SPEED)
            
            print("Je recule !")
        
        # On change l'angle seulement si il est != du précédent, ça évite de faire travailler les lib pour rien. 
        #if angle != prev_angle : 
        #    robot.set_angle(angle) # Change la direction du robot
        """aucune idée si ca sert de mettre ca"""  
      
        robot.set_angle(angle) # Change la direction du robot
        robot.compute_and_go()
        
        prev_angle = angle

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("[QUIT] Arrêt en cours ... ")

GPIO.cleanup()
print("--- Fin du programme ---")