# Copyright Per-Simon Saal & Sascha Schade
# MIT License

# Use this template to start your VectorOS program:

import vectoros
import asyncio
import keyleds
import keyboardcb
import timer
from vos_state import vos_state

#user code
from machine import Pin,I2C
import ADXL345
import time
import math
from machine import Pin, ADC, PWM
#user code end

#task_name="hello"  # use this name in vos_launch.py, too
task_name="game"
_run_every_ms=20   # how often to loop

_freeze=False
_exit=False
_menu_key=None

#user code
i2c = I2C(1,scl=Pin(15),sda=Pin(14), freq=10000)
adx = ADXL345.ADXL345(i2c)
#user code end

# Outsiders can call this to exit you
def exit(key=None):
    global _exit,task_name, _menu_key
    _exit=True
    vectoros.remove_task(task_name)
    _menu_key.detach()
    vos_state.show_menu=True
# do any cleanup (keyboard, timers) you need here
# or consider a "finally" in the main loop


# Outsiders can call this to pause you
def freeze(state=True):
    global _freeze
    _freeze=state

#Listen für Sensorwerte
sensor_values_x = [0] * 10
sensor_values_y = [0] * 10
#Startposition
pos_x = 6.
pos_y = 125.
#Liste aller Rechtecke (Hindernisse)
rects=[[60, 90, 180, 10],[0, 150, 180, 10]]
#Liste vom Ziel
goal=[105, 210, 30, 30]
#Spielergebnis
game_over = False
in_goal = False
#Tonausgabe
#beep = PWM(Pin(28))

#Supermario Melodie
async def playit():
    await tone(660,100);
    await asyncio.sleep_ms(150);
    await tone(660,100);
    await asyncio.sleep_ms(300);
    await tone(660,100);
    await asyncio.sleep_ms(300);
    await tone(510,100);
    await asyncio.sleep_ms(100);
    await tone(660,100);
    await asyncio.sleep_ms(300);
    await tone(770,100);
    await asyncio.sleep_ms(550);
    await tone(380,100);
    await asyncio.sleep_ms(575);

    await tone(510,100);
    await asyncio.sleep_ms(450);
    await tone(380,100);
    await asyncio.sleep_ms(400);
    await tone(320,100);
    await asyncio.sleep_ms(500);
    await tone(440,100);
    await asyncio.sleep_ms(300);
    await tone(480,80);
    await asyncio.sleep_ms(330);
    await tone(450,100);
    await asyncio.sleep_ms(150);
    await tone(430,100);
    await asyncio.sleep_ms(300);
    await tone(380,100);
    await asyncio.sleep_ms(200);
    await tone(660,80);
    await asyncio.sleep_ms(200);
    await tone(760,50);
    await asyncio.sleep_ms(150);
    await tone(860,100);
    await asyncio.sleep_ms(300);
    await tone(700,80);
    await asyncio.sleep_ms(150);
    await tone(760,50);
    await asyncio.sleep_ms(350);
    await tone(660,80);
    await asyncio.sleep_ms(300);
    await tone(520,80);
    await asyncio.sleep_ms(150);
    await tone(580,80);
    await asyncio.sleep_ms(150);
    await tone(480,80);
    await asyncio.sleep_ms(500);

    await tone(510,100);
    await asyncio.sleep_ms(450);
    await tone(380,100);
    await asyncio.sleep_ms(400);
    await tone(320,100);
    await asyncio.sleep_ms(500);
    await tone(440,100);
    await asyncio.sleep_ms(300);
    await tone(480,80);
    await asyncio.sleep_ms(330);
    await tone(450,100);
    await asyncio.sleep_ms(150);
    await tone(430,100);
    await asyncio.sleep_ms(300);
    await tone(380,100);
    await asyncio.sleep_ms(200);
    await tone(660,80);
    await asyncio.sleep_ms(200);
    await tone(760,50);
    await asyncio.sleep_ms(150);
    await tone(860,100);
    await asyncio.sleep_ms(300);
    await tone(700,80);
    await asyncio.sleep_ms(150);
    await tone(760,50);
    await asyncio.sleep_ms(350);
    await tone(660,80);
    await asyncio.sleep_ms(300);
    await tone(520,80);
    await asyncio.sleep_ms(150);
    await tone(580,80);
    await asyncio.sleep_ms(150);
    await tone(480,80);
    await asyncio.sleep_ms(500);
    
#user code
#Mittelwertbildung der Sensorwerte
def avg():
    global sensor_values_x, sensor_values_y
    x=adx.xValue#/256.
    y=adx.yValue#/256.
    
    #Begrenzen der Sensorwerte
    x=min(x, 239)    
    y=min(y, 239)
    #Laufender Mittelwert
    sensor_values_x = sensor_values_x[1:] + [x]
    sensor_values_y = sensor_values_y[1:] + [y]
    
    #Rückgabe der Mittelwerte
    return sum(sensor_values_x) / len(sensor_values_x), sum(sensor_values_y) / len(sensor_values_y)
    
#Kollisionsprüfung
def is_in_rect(rect, pos):
    x=rect[0]
    y=rect[1]
    lx=rect[2]
    ly=rect[3]
    px=pos[0]
    py=pos[1]
    
    #Prüfen ob Kollision besteht
    if (x <= px <= (x + lx)) and (y <= py <= (y + ly)):
        return True
    #Keine Kollision Rückgabe
    return False
    
#Tonausgabe
async def tone(freq=0, duration=0):
    beep.freq(freq)
    beep.duty_u16(32768)
    await asyncio.sleep_ms(duration)
    beep.duty_u16(0)

#"main.py"
def game():
    global pos_x, pos_y, game_over, in_goal
    #delta der Sensorwerte für Beschleunigung des Rechtecks
    dx,dy=avg()
    #Berechnen der neuen Rechteckposition mit dem Delta
    #Spielschwierigkeit
    pos_x+=(dy/5.)
    pos_y+=(dx/5.)

    #Berechnen des Radius in Pixel vom Display
    r=math.sqrt(pos_x**2+pos_y**2)
    #Berechnen des Winkels der aktuellen Position
    phi=math.atan2(pos_y,pos_x)
    #Begrenzen des Radius auf 120 Pixel
    r=min(r, 120)
    #Berechnen der Position auf dem Radius
    pos_x=r*math.cos(phi)
    pos_y=r*math.sin(phi)
    
    #Verbotene Variable, Konditionieren der Position aufgrund der
    #Einbaulage des Sensors und verschieben, damit die negativen
    #Sensorwerte angezeigt werden können
    pp = [int(-pos_x)+126, int(-pos_y)+126]
    #Gameover prüfen (Kollision)
    for rect in rects:
        game_over = is_in_rect(rect, pp) or game_over
    #Ziel prüfen (Kollision)   
    in_goal = is_in_rect(goal, pp) or in_goal
    #Display leeren
    screen=vectoros.get_screen()
    screen.clear(0)
    
    #print('x, y:%.3f,%.3f'%(x,y))
    #screen.text(40,98, f"X={x:.3f}")
    #screen.text(40,130, f"Y={y:.3f}")
    #screen.pixel(x+120,y+120,1234)
    #screen.ellipse(0,0,120,120,65535)
    #screen.tft.vline(120,80, 80, 7843)
    #screen.tft.hline(80, 120, 80, 7843)
    
    #Ende des Spiels
    if game_over:
        screen.text(40,98, "Game Over!")
    elif in_goal:
        screen.text(40,98, "You Won!")
        #Melodie beim gewinnen abspielen
        #await playit()
    #Neue Position des Rechtecks anzeigen    
    else:
        y=min(-int(pos_y)+120,234)
        y=max(y,6)
        x=min(-int(pos_x)+120,234)
        x=max(x,6)
    
        #boundaries zeichnen
        for rect in rects:
            screen.tft.fill_rect(rect[0], rect[1], rect[2], rect[3], 63488)
        #goal zeichnen
        screen.tft.fill_rect(goal[0], goal[1], goal[2], goal[3], 2016)
        #moving square zeichnen
        screen.tft.fill_rect(x-6,y-6,11,11,65504)    
# user code end

async def vos_main():
    global _freeze, _exit, _run_every_ms, task_name, _menu_key
    global in_goal, game_over, pos_x, pos_y
    _freeze=False
    _exit=False
# exit on Menu
    _menu_key=keyboardcb.KeyboardCB({keyleds.KEY_MENU: exit})
# if you want to control keyboard and LED without running the whole OS
    if vectoros.vectoros_active()==False:
        keyboardcb.KeyboardCB.run(250)
        timer.Timer.run()
    while _exit==False:
        if _freeze==False:
# your code will mostly go here  ##############################################################          
            #print("Do something here")
            #hello()
            game()
        await asyncio.sleep_ms(_run_every_ms)   
    _exit=False  # reset for next time
    game_over = False
    in_goal = False
    pos_x = 6.
    pos_y = 125.
    vectoros.remove_task(task_name)   # make sure we are removed (also does this in exit)

def main():
    asyncio.run(vos_main())
# code here will never, ever run under VectorOS

# if you want the possibility to run directly without VectorOS
#if __name__=="__main__":
#    main()

# if you want to configure to run in vos_launch but still run this file
# add the main function to to vos_launch.py and use this:
if __name__=="__main__":
    vectoros.run()

