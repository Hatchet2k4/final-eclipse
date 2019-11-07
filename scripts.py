import ika
import engine
from const import *
import inventory


#make part of engine soon...
flags = { 
"door1opened": False
}

##medsci
##todo, pass args
def OpenDoor1():
    
    if type(engine.engine.inv.grabbeditem) == inventory.BlueKey:    
        engine.engine.sound.Play("click.wav")
    
        #TODO: changes to the map need to persist. Create engine functions to set the tiles, and these changes are stored as keys in another global dict. 
        
        if flags["door1opened"]:
            ika.Map.SetTile(8, 3, 5, DECAL_DKEY_G) #change to green
            ika.Map.SetTile(8, 3, 3, 80) #close door
            ika.Map.SetObs(8,3, 0, 1) #set obstruction
            flags["door1opened"]=False
        else:            
            ika.Map.SetTile(8, 3, 5, DECAL_DKEY_R) #change to red
            ika.Map.SetTile(8, 3, 3, 0) #open door
            ika.Map.SetObs(8,3, 0, 0) #remove obstruction
            flags["door1opened"]=True
    else:
        engine.engine.sound.Play("beep1.wav")
        engine.engine.messages.AddMessage("Blue keycard required.", 600)
            