import ika

#Put all the ika functions into wrapper functions, for ease of porting later should we need it...

def Font(filename):
    return ika.Font(filename)

def DrawRect(x1,y1,x2,y2,color,filled=0,blendmode=0):
    ika.Video.DrawRect(x1,y1,x2,y2,color,filled,blendmode)

def Image(filename):
    return ika.Image(filename)

def RGB(r, g, b, a=255):
    return ika.RGB(r,g,b,a)

def ShowPage():
    ika.Video.ShowPage()

def Switch(map):
    ika.Map.Switch(map)

def Log(message):
    ika.Log(message)

def Random(i):
    return ika.Random(i)
    
def GetTime():
    return ika.GetTime()

def GetTile(x, y, layer):
    if x>=0 and y>=0:
        return ika.Map.GetTile(x, y, layer)
    return 0 #return 0 if out of bounds
    
#may need to do more than this eventually..
Input = ika.Input 

    
    
    
    
    
    