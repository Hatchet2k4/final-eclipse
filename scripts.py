import ika
import engine
from const import *
import inventory


#make part of engine soon...
flags = { 
"door1opened": False
}
##medsci
def OpenDoor1():
    
    if type(engine.engine.inv.grabbeditem) == inventory.BlueKey:    
        engine.engine.sound.Play("click.wav")
    
    
        if flags["door1opened"]:
            ika.Map.SetTile(8, 3, 5, 82) #change to green
            ika.Map.SetTile(8, 3, 3, 80) #close door
            flags["door1opened"]=False
        else:
            flags["door1opened"]=True
            ika.Map.SetTile(8, 3, 5, 81) #change to red
            ika.Map.SetTile(8, 3, 3, 0) #open door
    else:
        engine.engine.sound.Play("beep1.wav")
        engine.engine.messages.AddMessage("Blue keycard required.", 600)
            