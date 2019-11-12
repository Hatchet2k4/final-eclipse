import ika
import engine
from const import *
import inventory


#make part of engine soon...
flags = { 
"door1opened": False,
"door2opened": False
}

##medsci
##todo, pass args
#todo, make a template for this type of door code

def KeyDoorTemplate(x, y, flag, flagval=False, btn="button",key=None):
    if not flags.has_key(flag): #set up the flag dict with default value if doesn't exist  yet
        flags[flag]=flagval
    
    if key==None or type(engine.engine.inv.grabbeditem) == type(key): #no key required, or holding the required key    
        if flags[flag]:
            if not engine.engine.GetEnts(x, y):
                engine.engine.sound.Play("click.wav")
                ika.Map.SetTile(x, y, 5, DECAL_DCODE_G) #change to green
                ika.Map.SetTile(x, y, 3, 80) #close door
                ika.Map.SetObs(x,y, 0, 1) #set obstruction
                flags[flag]=False
            else: #entity in the way
                engine.engine.sound.Play("beep1.wav")
                engine.engine.messages.AddMessage("Door blocked.", 600)                
        else:            
            engine.engine.sound.Play("click.wav")
            ika.Map.SetTile(x, y, 5, DECAL_DCODE_R) #change to red
            ika.Map.SetTile(x, y, 3, 0) #open door
            ika.Map.SetObs(x, y, 0, 0) #remove obstruction
            flags[flag]=True
    else: #doesn't have key 
        engine.engine.sound.Play("beep1.wav")
        engine.engine.messages.AddMessage("key required.", 600) #todo: get generic keyname from class

def OpenDoor1():    
    if type(engine.engine.inv.grabbeditem) == inventory.BlueKey:                
        #TODO: changes to the map need to persist. Create engine functions to set the tiles, and these changes are stored as keys in another global dict. 
        
        if flags["door1opened"]: #door is open, try to close it
            if not engine.engine.GetEnts(8, 3):
                engine.engine.sound.Play("click.wav")
                ika.Map.SetTile(8, 3, 5, DECAL_DKEY_G) #change to green
                ika.Map.SetTile(8, 3, 3, 80) #close door
                ika.Map.SetObs(8,3, 0, 1) #set obstruction
                flags["door1opened"]=False
            else: 
                engine.engine.sound.Play("beep1.wav")
                engine.engine.messages.AddMessage("Door blocked.", 600)
        else:            
            engine.engine.sound.Play("click.wav")
            ika.Map.SetTile(8, 3, 5, DECAL_DKEY_R) #change to red
            ika.Map.SetTile(8, 3, 3, 0) #open door
            ika.Map.SetObs(8,3, 0, 0) #remove obstruction
            flags["door1opened"]=True
    else:
        engine.engine.sound.Play("beep1.wav")
        engine.engine.messages.AddMessage("Blue keycard required.", 600)
        
def OpenDoor2():            
        if flags["door2opened"]:
            if not engine.engine.GetEnts(8, 11):
                engine.engine.sound.Play("click.wav")
                ika.Map.SetTile(8, 11, 5, DECAL_DCODE_G) #change to green
                ika.Map.SetTile(8, 11, 3, 80) #close door
                ika.Map.SetObs(8,11, 0, 1) #set obstruction
                flags["door2opened"]=False
            else: 
                engine.engine.sound.Play("beep1.wav")
                engine.engine.messages.AddMessage("Door blocked.", 600)                
        else:            
            engine.engine.sound.Play("click.wav")
            ika.Map.SetTile(8, 11, 5, DECAL_DCODE_R) #change to red
            ika.Map.SetTile(8, 11, 3, 0) #open door
            ika.Map.SetObs(8, 11, 0, 0) #remove obstruction
            flags["door2opened"]=True
   
   
   
   
   
   
            