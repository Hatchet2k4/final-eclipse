import ika
import engine
from const import *

#make part of engine soon...
flags = { 
"door1opened": False
}
##medsci
def OpenDoor1():
    
    engine.engine.sound.Play("click.wav")
    if flags["door1opened"]:
        ika.Map.SetTile(8, 3, 5, 82) #change to green
        ika.Map.SetTile(8, 3, 3, 80) #close door
        flags["door1opened"]=False
    else:
        flags["door1opened"]=True
        ika.Map.SetTile(8, 3, 5, 81) #change to red
        ika.Map.SetTile(8, 3, 3, 0) #open door