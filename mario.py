# Use this template to start your VectorOS program:

import vectoros
import asyncio
import keyleds
import keyboardcb
import timer
from vos_state import vos_state
from machine import Pin, ADC, PWM


task_name="mario"  # use this name in vos_launch.py, too
_run_every_ms=500   # how often to loop


_freeze=False
_exit=False
_menu_key=None

# Outsiders can call this to exit you
def exit(key=None):
    global _exit,task_name, _menu_key
    _exit=True
    vectoros.remove_task(task_name)
    _menu_key.detach()
    vos_state.show_menu=True
# do any cleanup (keyboard, timers) you need here
# or consider a "finally" in the main loop

beep = PWM(Pin(28))

# Outsiders can call this to pause you
def freeze(state=True):
    global _freeze
    _freeze=state

async def tone(freq=0, duration=0):
    beep.freq(freq)
    beep.duty_u16(32768)
    await asyncio.sleep_ms(duration)
    beep.duty_u16(0)
    

async def vos_main():
    global _freeze, _exit, _run_every_ms, task_name, _menu_key
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
# your code will mostly go here            
            print("Do something here")
            await playit()
        await asyncio.sleep_ms(_run_every_ms)   
    _exit=False  # reset for next time
    vectoros.remove_task(task_name)   # make sure we are removed (also does this in exit)

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