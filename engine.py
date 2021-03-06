import ika
from inventory import *
import intro
from const import *
import entity
import sound
import pda
import credits
import scripts 

import wrapper #encapsulate ika functions for easy porting if needed

ika.SetCaption(ika.GetCaption() + " - Final Eclipse")
engine = None
#intro.Start()
#credits.Start()

class Engine(object):
    def __init__(self):        
    
        self.debug=True #debug mode
    
        self.tinyfont = ika.Font('fonts/log_white.fnt')
        self.itemfont = ika.Font('fonts/item_white.fnt')
        self.itemfontgrey = ika.Font('fonts/item_grey.fnt')
        self.gunfont = ika.Font('fonts/font_gun.fnt')
        self.medfont = ika.Font('fonts/medfont.fnt')
        self.greyfont = ika.Font('fonts/log_grey.fnt')
        self.whitefont = ika.Font('fonts/log_white.fnt')
        
        ### basic loading splash screen..
        ika.Video.DrawRect(0,0,320,240, ika.RGB(0,0,0), 1)
        self.whitefont.Print(140,116, "Loading...")
        ika.Video.ShowPage()

        self.pda = pda.PDA()
        self.messages = Messages()
        self.fullscreen = False

        self.sound = sound.Sound()

        self.hudmain = ika.Image("img/ui/hudmain.png")
        self.hudcolor = ika.Image("img/ui/hudcolor.png")
        self.spectrum = ika.Canvas("img/ui/hudspectrum.png")
        self.hudhealth = ika.Image("img/ui/hudhealth.png")

        self.pointer = ika.Image("img/ui/pointer.png")
        self.ptr = self.pointer

        self.left=8 #top left of main window
        self.top=5

		#self.texturetest=ika.Image("Img/Walls/texturetest.png")
        self.deck = "" #name of current deck        
        
        #todo - make deck aware
        self.switches = [] #list of switch objects
        
        self.things = [] #list of things - additional objects that can update gamestate over time. usually spawned by a switch. will get despawned if deck changes
        
        self.backgrounds = {} #dict of images per deck
        self.wallimages = [] #list of dicts for wall images. access as self.wallimages[tile number]['flat1left'] to get the image "
        self.objectimages = [] #list of dicts of object images
        self.decalimages = [] #list of dicts for decal images
        
        
        
        self.objnum = 20 #objects currently start at tile 20 in the map editor        
        self.decalnum = 80 #decals currently start at tile 20 in the map editor
        
        self.arrows = [] #images of arrows for automap
                
        self.layer_visibility= [1]*4 #for debug of row layers
        
        for i in range(4):
            self.arrows.append(ika.Image("Img/minimap/Pointer"+str(i)+".png"))

        self.tiles=[ika.Image("Img/minimap/space.png"),
                    ika.Image("Img/minimap/wall.png"),
                    ika.Image("Img/minimap/enemy.png"),
                    ika.Image("Img/minimap/enemy_d.png")] #needs to be updated!

        self.backflip = 0
        self.moved = False

        
        self.NewGame() #setup initial settings for enemies, items, switches, etc.
        self.LoadAssets()
        
        self.LoadDeck("medsci", 3, 5, EAST)        


        self.color = ika.RGB(0,0,0)
        self.offtable = [(0,-1), (1, 0), (0, 1), (-1,0)]
        self.offtable_l = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        self.offtable_r = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        ### Dicts to determine decal facing. Key is player facing, and returns the side on which the decal should be visible from that direction.
        self.facetable = { NORTH: SOUTH, EAST: WEST, SOUTH: NORTH, WEST: EAST } #front
        self.facetable_l = { NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH } #left perspective
        self.facetable_r = { NORTH: WEST, EAST: NORTH, SOUTH: EAST, WEST: SOUTH } #right perspective
        

        #assets = [self.handframes, self.pipeframes, self.pistolframes, self.shotgunframes, self.rifleframes, self. tiles, self.backgrounds, self.wallimages, self.decalimages, self.objectimages]
        #imgusage = sys.getsizeof(assets)
        #ika.Log("Estimated image memory usage: " + str(imgusage/1024) +"KB")

    def LoadDeck(self, deck, x, y, facing):
        
        #save state before switching decks! may not be needed as the are already referring to global..
        #self.global_entities[self.deck] = self.entities
        #self.global_items[self.deck] = self.items
        #self.global_switches[self.deck] = self.switches
        
        #load new deck
        self.deck = deck
        
        self.plrx=x
        self.plry=y
        self.facing=facing
        
        
        ika.Map.Switch(deck+'.ika-map')        
        self.back = self.backgrounds[deck]
        
        self.entities = self.global_entities[deck]
        self.items = self.global_items[deck]
        self.switches = self.global_switches[deck]
        
        self.things = self.global_things[deck]
        
        self.music = ika.Music("music/"+deck+".ogg") #change per deck
        self.music.loop = True
        self.music.Play()
        
    def LoadAssets(self):       #combine all into one LoadAssets call
       decklist = ["medsci", "office", "operations", "barracks", "final"]
       for d in decklist:     
           self.backgrounds[d] = [ika.Image("img/backgrounds/"+d+"1.png"), ika.Image("img/backgrounds/"+d+"2.png")]

       #Lists of all resources for walls, decals and objects. The order is important, as it's based on the order in tileset. 
       walllist = ["med1", "med2", "med1win", "med1door", "med2door", "military", "militarydoor", "bed", "final", "finalspace"]    

       
       decallist = ["door", "dcode_g", "dcode_r", "dkey_r", "dkey_g", "blood_sm", "blood_big", "switch1", "switch2"]
       
       objlist = ["table", "medtable", "blood_floor1", "blood_floor2", "crate"] 
       
       imglist = ["flat1left", "flat1mid", "flat1right", "per1left", "per1right", "flat2left", "flat2mid", "flat2right", 
                  "per2left", "per2right",  "flat3left",  "flat3mid", "flat3right", "per3left", "per3right",
                  "per4farleft", "per4left",  "per4right",  "per4farright"] 
          
       for path in walllist:                  
           wall = { }
           for img in imglist: 
               wall[img] = ika.Image("img/walls/"+path+"/"+img+".png")
         
           self.wallimages.append(wall)                     

                  
       for path in decallist:    
            d = {}
            for img in imglist: 
                d[img] = ika.Image("img/decals/"+path+"/"+img+".png")

            self.decalimages.append(d)         

       self.decalimages.append(self.wallimages[0])
       self.decalimages.append(self.wallimages[1])
       self.decalimages.append(self.wallimages[2])
       self.decalimages.append(self.wallimages[4])       
       self.decalimages.append(self.wallimages[5])       
       self.decalimages.append(self.wallimages[6])       

       
       imglist = ["1left", "1mid","1right",
                   "2left", "2mid","2right",
                   "3left", "3mid","3right"]

       for path in objlist:
          obj = { }
          for img in imglist:
             obj[img] = ika.Image("img/objects/"+path+"/"+img+".png")
          self.objectimages.append(obj)

       #load images for the first person weapon views
       self.handframes = [ika.Image("Img/weapons/fp_handr.png"),
                           ika.Image("Img/weapons/fp_handr_punch1.png"),
                           ika.Image("Img/weapons/fp_handr_punch2.png")]

       self.pipeframes = [ika.Image("Img/weapons/fp_pipe.png"),
                           ika.Image("Img/weapons/fp_pipe_hit1.png"),
                           ika.Image("Img/weapons/fp_pipe_hit2.png")]

       self.pistolframes = [ika.Image("Img/weapons/fp_pistol.png"),
                             ika.Image("Img/weapons/fp_pistol_firing.png")]

       self.shotgunframes = [ika.Image("Img/weapons/fp_shotgun.png"),
                              ika.Image("Img/weapons/fp_shotgun_firing.png"),
                              ika.Image("Img/weapons/fp_shotgun_cock.png")]

       self.rifleframes = [ika.Image("Img/weapons/fp_rifle.png"),
                            ika.Image("Img/weapons/fp_rifle_firing.png")]
                            
    
    
    def NewGame(self):
        self.inv = Inventory()
        self.equip = Equip()
        
        self.global_things = { 
        
        "medsci": [Zone(9, 11, scripts.Elevator1)], 
        "office": [],
        "operations": [],
        "barracks": [],
        "final": []              
        }
        
        self.global_entities = { "medsci": [
                       entity.Vagimon(11,17, ika.Random(0, 4)),
                       entity.Vagimon(15,7, ika.Random(0, 4)),
                       entity.Vagimon(11,10, ika.Random(0, 4)),
                       entity.Vagimon(13,12, ika.Random(0, 4)),
                       entity.Vagimon(5,9, ika.Random(0, 4)),
                       entity.Vagimon(12,20, ika.Random(0, 4)),
                       entity.Vagimon(15,19, ika.Random(0, 4)),
                       entity.Vagimon(22,16, ika.Random(0, 4)),
                       entity.Vagimon(22,21, ika.Random(0, 4)),
                       entity.Vagimon(19,20, ika.Random(0, 4)),
                       entity.Vagimon(21,22, ika.Random(0, 4)),
                       entity.Vagimon(19,14, ika.Random(0, 4)),
                       entity.Vagimon(26,14, ika.Random(0, 4)),
                       entity.Vagimon(29,12, ika.Random(0, 4)),

                       entity.Walker(19,4, ika.Random(0, 4)),
                       entity.Walker(19,7, ika.Random(0, 4)),
                       entity.Walker(23,3, ika.Random(0, 4)),
                       entity.Walker(18,11, ika.Random(0, 4)),
                       entity.Walker(11,11, ika.Random(0, 4)),
                       entity.Walker(6,20, ika.Random(0, 4)),
                       entity.Walker(4,22, ika.Random(0, 4)),
                       entity.Walker(14,19, ika.Random(0, 4)),
                       entity.Walker(14,22, ika.Random(0, 4)),
                       entity.Walker(15,15, ika.Random(0, 4)),
                       entity.Walker(23,14, ika.Random(0, 4)),
                       entity.Walker(25,19, ika.Random(0, 4)),
                       entity.Walker(28,20, ika.Random(0, 4)),
                       entity.Walker(27,7, ika.Random(0, 4)),
                       entity.Walker(26,3, ika.Random(0, 4)),
                       entity.Walker(29,3, ika.Random(0, 4)),
                       entity.Walker(26,5, ika.Random(0, 4))
                       ], 
                       "office": [],
                       "operations": [],
                       "barracks": [entity.Vagimon(5,9, ika.Random(0, 4))],
                       "final": []                       
                       }
                       
        

        self.global_items = { "medsci": {
                       (4, 6) : [Pipe(), Pistol(16)],
                       (3, 6) : [BlueKey()],
                       (9,5) : [Armor1()],
                       (9,5) : [Hypo(2)],
                       (4,8) : [Pistol(7)],
                       (3,12) : [Clip()],
                       (13,5) : [Clip()],
                       (9,7) : [Shotgun(2)],
                       (23,3) : [Shells()],
                       (23,4) : [Shells()],
                       (23,5) : [Shells()],
                       (22,9) : [Armor2()],
                       (11,9) : [Clip()],
                       (7,14) : [Rifle(60)],
                       (7,15) : [Clip(48)],
                       (3,14) : [Clip(48)],
                       (3,15) : [Hypo()],
                       (18,9) : [Shells()],
                       (19,9) : [Shells()],
                       (15,12) : [Armor3()],
                       (22,11) : [Shells()],
                       (23,11) : [Shells()],
                       (23,12) : [Shells()],
                       (27,21) : [Pistol(16)],
                       (29,21) : [Rifle(60)],
                       (5, 6) : [Recorder(0)],
                       (12,7) : [Recorder(1)],
                       (10,7) : [Hypo(2)],
                       (10,7) : [Recorder(2)],
                       (21,6) : [Recorder(3)],
                       (11,9) : [Recorder(4)],
                       (17,11) : [Recorder(5)],
                       (29,21) : [Recorder(6)]
                     },
                        "office": {},
                       "operations": {},
                       "barracks": {},
                       "final": {}   
                     }
                    #x, y, facing, action, clickable=False, clickarea=(0,0,0,0)):
        self.global_switches = { 
                    "medsci": { (8, 3): [Switch(8, 3, WEST, scripts.OpenDoor1, True, (148, 56, 12, 17))], 
                                (8, 11): [Switch(8, 11, WEST, scripts.OpenDoor2, True, (148, 56, 12, 17))]
                              },
                        "office": {},
                       "operations": {},
                       "barracks": {},
                       "final": {}   
                     }


        self.health = 70
        self.max_health = 100

        self.immunity = 80
        self.max_immunity = 100

        self.attack = 0
        self.defense = 0

        self.plrx = 0
        self.plry = 0
        self.facing = EAST

        self.backflip = 0
        self.moved = False

        self.curframe = 0
        self.attacking = False
        self.reloading = False
        self.animtimer = 0

        self.tinteffect = False

        self.moveanim = False #currently in movement animation
        self.movetimer = 0
        self.slideimg= [None, None] #needs refactoring, HACK
        self.slidedir=None
        
        

    def Run(self):

        time = ika.GetTime()
        done = False
        color = 0



        while not done:
            if self.plrx == 27 and self.plry == 2: #HACK
               self.End()

            t = ika.GetTime()
            while t > time:
               time += 1
               self.AnimUpdate()
               self.messages.Update()
               for e in self.entities:
                  e.Update()

            time = ika.GetTime()

            self.color = self.spectrum.GetPixel(self.health, 0)

            ika.Input.Update()

            ###process input ###

            self.DoInput()
            self.UpdateStats()            
            self.Move() #todo. don't move player or grab walls here yet, but return new position and facing to use as input for AnimWalls
            
            if self.moveanim:
                self.AnimWalls()
            
            
            for thing in self.things:
                thing.Update()
            
            #done processing, input, start main hud drawing            
            
            ika.Video.Blit(self.hudmain, 0, 0)
            ika.Video.TintBlit(self.hudcolor, 0, 0, self.color)
            ika.Video.TintDistortBlit(self.hudhealth,
                                  (249, 144, self.color),
                                  (249 + (50 * self.health / self.max_health), 144, self.color),
                                  (249 + (50 * self.health / self.max_health), 150, self.color),
                                  (249, 150, self.color))
            #draw in main window
            ika.Video.ClipScreen(self.left, self.top, self.left+224, self.top+128) ##prevent from drawing outside the main window                        
            self.DrawWalls()
            
            
            if ika.Input.keyboard['F12'].Pressed():
                 img = ika.Video.GrabCanvas(self.left, self.top, self.left+224, self.top+128)
                 img.Save("testwallsx"+str(self.plrx) +"y"+str(self.plry)+"f"+str(self.facing)+".png")  #hack to screenshot just the walls drawn so far
            
            
            self.DrawFrames() #draws equipped weapon in its current state
            ika.Video.ClipScreen() #stop clipping now.
            
            #draw rest of ui
            self.inv.Draw()
            self.equip.Draw()

            self.pda.Draw()
            self.messages.Draw()

            #effects
            #if self.tinteffect:
            #    ika.Video.DrawRect(self.left,self.top,self.left+224,self.top+128, ika.RGB(127,0,0, 127))

            if self.fullscreen:
               ### Fake fullscreen mode! But currently no mouse. May hack in a fullscreen mode mouse for fun..
               scr = ika.Video.GrabImage(self.left,self.top, self.left + 224, self.top+128)
               ika.Video.DrawRect(0,0,320,240, ika.RGB(0,0,0), 1)
               w = int(224*1.5)
               h = int(128*1.5)
               topleftx = 160 - (w/2)
               toplefty = 120 - (h/2)
               ika.Video.ScaleBlit(scr, topleftx,toplefty, w, h)

            self.tinyfont.Print(0,0, str(ika.GetFrameRate()))
            #self.tinyfont.Print(0,10, str(self.animtimer))
            self.DoMouse()
            if ika.Input.keyboard['ESCAPE'].Pressed(): #pause
               #scr = ika.Video.GrabImage(0,0, 320, 240)
               ika.Video.DrawRect(0,0,320,240, ika.RGB(0,0,0,128), 1) #darken screen while paused
               ika.Video.ShowPage()
               while not ika.Input.keyboard['ESCAPE'].Pressed(): 
                   #ika.Video.Blit(scr, 0,0)

                   ika.Input.Update()
                   #ika.Video.ShowPage()

               ika.Input.Unpress()
               time = ika.GetTime()


            ika.Video.ShowPage()
                    




    def DoInput(self):
    
 
    
        if ika.Input.keyboard['RCTRL'].Position() or ika.Input.keyboard['LCTRL'].Position() or self.MouseM():
           self.Attack()

        if ika.Input.keyboard['R'].Pressed():
           self.Reload()

        if ika.Input.keyboard['F'].Pressed():
           if self.equip.lefthand:
              self.equip.lefthand.Use()
              if isinstance(self.equip.lefthand, Stackable) and self.equip.lefthand.count == 0:
                 self.equip.lefthand = None

        if ika.Input.keyboard['M'].Pressed() or ika.Input.keyboard['1'].Pressed():
           self.pda.SetMode(0)
           self.sound.Play("click.wav")
        if ika.Input.keyboard['T'].Pressed() or ika.Input.keyboard['2'].Pressed():
           self.pda.SetMode(1)
           self.sound.Play("click.wav")
        if ika.Input.keyboard['O'].Pressed() or ika.Input.keyboard['3'].Pressed():
           self.pda.SetMode(2)
           self.sound.Play("click.wav")
        if ika.Input.keyboard['L'].Pressed() or ika.Input.keyboard['4'].Pressed():
           self.pda.SetMode(3)
           self.sound.Play("click.wav")

        if ika.Input.keyboard['TAB'].Pressed():
            self.fullscreen = not self.fullscreen
        
        if self.debug: #debug mode for layer visibility toggling
            for i in range(4):                        
                if ika.Input.keyboard['F'+str(i+1)].Pressed():    
                    self.layer_visibility[i] = int(not self.layer_visibility[i]) #swap 0/1
            

    # MOUSE #############################################################################################

    def MouseX(self):
        return ika.Input.mouse.x.Position()
    def MouseY(self):
        return ika.Input.mouse.y.Position()
    def MouseL(self):
        return ika.Input.mouse.left.Position()
    def MouseR(self):
        return ika.Input.mouse.right.Position()
    def MouseM(self):
        return ika.Input.mouse.middle.Position()
    def MouseW(self):
        #mousewheel doesn't currently work, returns 0 or false for position/pressed. Goal - recompile ika and finish mousewheel support! 
        return ika.Input.mouse.wheel.Position() 

    def MouseClicked(self):
        return ika.Input.mouse.left.Pressed() or ika.Input.mouse.right.Pressed()

    def DoMouse(self):

       if self.inv.grabbeditem is None:
          ika.Video.TintBlit(self.ptr, int(self.MouseX()), int(self.MouseY()), self.color)
       else:
          self.inv.grabbeditem.Draw(int(self.MouseX())-8, int(self.MouseY())-8)
          #self.inv.grabbeditem.Draw(int(self.MouseX()), int(self.MouseY()))

       if self.MouseClicked(): #click!       
       
          ### Main Window Click ###############################################################################
          
          if self.MouseX() > self.left and self.MouseX() < self.left + 224 \
          and self.MouseY() > self.top and self.MouseY() < self.top + 128: #clicked in main window
              offx, offy = self.offtable[self.facing]
              #translate to window coordinates
              mx=self.MouseX()-self.left
              my=self.MouseY()-self.top
              
              triggered=False
              
              if self.switches.has_key((self.plrx+offx, self.plry+offy)): #switch exists here, priority over items
                 for s in  self.switches[(self.plrx+offx, self.plry+offy)]:
                    sx, sy, sw, sh=s.clickarea
                    #not currently checking facing, will add after
                    if mx>=sx and mx<=sx+sw and my>=sy and my<=sy+sh: #clicked in area 
                        s.Activate()                 
                        triggered = True
              
              
              #need to check if specific area for items is clicked, just uses anywhere in window for now
              if not triggered: #only try to place stuff if wasn't triggered
                  if self.inv.grabbeditem is None: #not holding an item, try to grab one
                     #todo: code pressing buttons
                     # if facing a wall directly ahead and wall contains a pressable item, find the clickable area and compare to activate
                    if not wrapper.GetTile(self.plrx+offx, self.plry+offy, 0): #don't try to grab from tiles that have walls. Bug if items are placed in a doorway..

                        if self.items.has_key((self.plrx+offx, self.plry+offy)): #item exists here
                            self.inv.grabbeditem = self.items[(self.plrx+offx, self.plry+offy)].pop() #grabs only the first item out of the list
                            self.messages.AddMessage(self.inv.grabbeditem.name)
                            if len(self.items[(self.plrx+offx, self.plry+offy)]) == 0:
                               del self.items[(self.plrx+offx, self.plry+offy)] #delete out of dict if it's empty
                  else: #holding an item, try to place it                        
                     if not wrapper.GetTile(self.plrx+offx, self.plry+offy, 0): #don't try to place onto a wall. Does not work for doors..
                         if self.items.has_key((self.plrx+offx, self.plry+offy)):
                            self.items[(self.plrx+offx, self.plry+offy)].append(self.inv.grabbeditem)
                         else:
                            self.items[(self.plrx+offx, self.plry+offy)] = [self.inv.grabbeditem]
                         self.inv.grabbeditem = None

          #### Inventory System ###############################################################################

          if self.MouseX() > self.inv.left and self.MouseX() < self.inv.left + 64 \
          and self.MouseY() > self.inv.top and self.MouseY() < self.inv.top + 128: #clicked in inventory
             if self.MouseL():
                 if self.inv.grabbeditem is None: #not holding an item, grab one
                    self.inv.GrabItem(self.MouseX(), self.MouseY())
                 else: #holding an item, place it
                    self.inv.PlaceItem(self.MouseX(), self.MouseY())


             elif self.MouseR(): #use the item!
                 self.inv.UseItem(self.MouseX(), self.MouseY())

          #### Equip System ###################################################################################

          if self.MouseX() > 253 and self.MouseX() < 253+16 \
          and self.MouseY() > 178 and self.MouseY() < 178+32: #Right hand

              if self.MouseL():
                 if self.inv.grabbeditem is None:
                    self.inv.grabbeditem = self.equip.TakeItem(0)
                 else:
                    self.equip.AddItem(self.inv.grabbeditem, 0)
              elif self.MouseR():
                 self.equip.UseItem(0)

          if self.MouseX() > 253 and self.MouseX() < 253+16 \
          and self.MouseY() > 210 and self.MouseY() < 210+16: #Left hand
              if self.MouseL():
                 if self.inv.grabbeditem is None:
                    self.inv.grabbeditem = self.equip.TakeItem(1)
                 else:
                    self.equip.AddItem(self.inv.grabbeditem, 1)
              elif self.MouseR():
                 self.equip.UseItem(1)

          if self.MouseX() > 272 and self.MouseX() < 272+32 \
          and self.MouseY() > 178 and self.MouseY() < 178+32: #Armor
              if self.MouseL():
                 if self.inv.grabbeditem is None:
                    self.inv.grabbeditem = self.equip.TakeItem(2)
                 else:
                    self.equip.AddItem(self.inv.grabbeditem, 2)
              elif self.MouseR():
                 self.equip.UseItem(2)

          if self.MouseX() > 272 and self.MouseX() < 272+32 \
          and self.MouseY() > 210 and self.MouseY() < 210+16: #Belt
              if self.MouseL():
                 if self.inv.grabbeditem is None:
                    self.inv.grabbeditem = self.equip.TakeItem(3)
                 else:
                    self.equip.AddItem(self.inv.grabbeditem, 3)
              elif self.MouseR():
                 self.equip.UseItem(3)

          #### PDA system #####################################################################################

          if self.MouseX() > 9 and self.MouseX() < 231 \
          and self.MouseY() > 170 and self.MouseY() < 235:
             self.pda.Click(int(self.MouseX()), int(self.MouseY()))


    def Reload(self, ammotype=None):
       if self.attacking: return
       required = 0

       #todo: right click on ammo to reload

        #if ammotype:
       if isinstance(self.equip.righthand, Pistol) and self.equip.righthand.count < 16:
          required = 16 - self.equip.righthand.count
          s = "reload_pistol.wav"
          ammo = Clip
       elif isinstance(self.equip.righthand, Rifle) and self.equip.righthand.count < 60:
          required = 60 - self.equip.righthand.count
          s = "reload_rifle.wav"
          ammo = Clip
       elif isinstance(self.equip.righthand, Shotgun) and self.equip.righthand.count < 8:
          required = 8 - self.equip.righthand.count
          s = "reload_shotgun.wav"

          ammo = Shells

       if required == 0: return

       self.reloading = True
       self.animtimer = 0
       played = False

       for i in self.inv.items:
          if isinstance(i, ammo):
             if i.count > required: #more ammo in the clip than needed
                self.equip.righthand.count += required
                i.count -= required
                required = 0
             else: #need more ammo than the clip has
                self.equip.righthand.count += i.count
                required -= i.count
                self.inv.DeleteItem(i)

             if played == False:
                self.sound.Play(s)
                played = True

             if required == 0: return #keep going if we still need more ammo, otherwise return

    def UpdateStats(self):
      attack = 1
      if self.equip.righthand is not None:
         attack = self.equip.righthand.attack
      self.attack = attack

      defense = 0
      if self.equip.armor is not None:
         defense += self.equip.armor.defense
      if self.equip.belt is not None:
         defense += self.equip.belt.defense

      self.defense = defense

    def Attack(self):
       hurt = False
       distance = 3

       if self.equip.righthand is None:
          if (ika.Input.keyboard['RCTRL'].Pressed() or ika.Input.keyboard['LCTRL'].Pressed() \
          or ika.Input.mouse.middle.Pressed()) and not self.attacking and not self.reloading:
             self.attacking = True
             self.curframe = 1
             hurt = True
             distance = 1

       elif isinstance(self.equip.righthand, Pipe):
          if (ika.Input.keyboard['RCTRL'].Pressed() or ika.Input.keyboard['LCTRL'].Pressed() \
          or ika.Input.mouse.middle.Pressed()) and not self.attacking and not self.reloading:
             self.attacking = True
             self.curframe = 1
             hurt = True
             distance = 1

       elif isinstance(self.equip.righthand, Pistol):
          if (ika.Input.keyboard['RCTRL'].Pressed() or ika.Input.keyboard['LCTRL'].Pressed() \
          or ika.Input.mouse.middle.Pressed()) and not self.attacking and not self.reloading:
            if self.equip.righthand.count > 0:
               self.attacking = True
               self.curframe = 1
               self.equip.righthand.count -= 1
               self.sound.Play("fire_pistol.wav")
               hurt = True
               offx, offy = self.offtable[self.facing]
               #self.entities.append(entity.Projectile(self.plrx+offx,self.plry+offy, self.facing)) 
               
               
            else:
               self.sound.Play("Empty.wav")

       elif isinstance(self.equip.righthand, Shotgun):
          if (ika.Input.keyboard['RCTRL'].Pressed() or ika.Input.keyboard['LCTRL'].Pressed() \
          or ika.Input.mouse.middle.Pressed()) and not self.attacking and not self.reloading:
            if self.equip.righthand.count > 0:
               self.attacking = True
               self.curframe = 1
               self.equip.righthand.count -= 1
               self.sound.Play("fire_shotgun.wav", 0.75)
               hurt = True
            else:
               self.sound.Play("Empty.wav")

       elif isinstance(self.equip.righthand, Rifle):
          if not self.attacking and not self.reloading:
            if self.equip.righthand.count > 0:
               self.attacking = True
               self.curframe = 1
               self.equip.righthand.count -= 1
               self.sound.Play("fire_rifle.wav")
               hurt = True
            else:
               if ika.Input.keyboard['RCTRL'].Pressed() or ika.Input.keyboard['LCTRL'].Pressed() or ika.Input.mouse['MOUSEM'].Pressed():
                  self.sound.Play("Empty.wav")

       #Ensure these buttons are unpressed
       ika.Input.mouse.middle.Pressed()
       ika.Input.keyboard['RCTRL'].Pressed()
       ika.Input.keyboard['LCTRL'].Pressed()

       if hurt: #we can hurt someone :D
          offx, offy = self.offtable[self.facing]
          for i in range(1, distance+1):
             o=ika.Map.GetObs(self.plrx+i*offx, self.plry+i*offy, 0) #check for walls first
             if o: return #end if we hit an obstruction first
             
             ents = self.GetEnts(self.plrx+i*offx, self.plry+i*offy)
             for e in ents:
                if e and isinstance(e, entity.Enemy) and not e.dead:
                   e.Hurt(self.attack)
                   if not self.equip.righthand:
                      self.sound.Play("punch_hit.wav")
                   elif isinstance(self.equip.righthand, Pipe):
                      self.sound.Play("punch_hit.wav")
                   return

    def AnimUpdate(self):
       if self.attacking == True:
          if self.equip.righthand is None:
             if self.animtimer < 6:
                self.curframe = 1
             elif self.animtimer < 12:
                self.curframe = 2
             elif self.animtimer < 20:
                self.curframe = 1

             self.animtimer += 1
             if self.animtimer > 20:
                self.attacking = False
                self.animtimer = 0
                self.curframe = 0

          elif isinstance(self.equip.righthand, Pipe):
             if self.animtimer < 10:
                self.curframe = 1
             elif self.animtimer < 20:
                self.curframe = 2
             elif self.animtimer < 30:
                self.curframe = 1

             self.animtimer += 1
             if self.animtimer > 30:
                self.attacking = False
                self.animtimer = 0
                self.curframe = 0

          if isinstance(self.equip.righthand, Pistol):
             self.curframe = 1
             self.animtimer += 1
             if self.animtimer > 8:
                self.attacking = False
                self.animtimer = 0
                self.curframe = 0

          if isinstance(self.equip.righthand, Rifle):
             if self.animtimer < 7: self.curframe = 1
             else: self.curframe = 0
             self.animtimer += 1
             if self.animtimer > 10:
                self.attacking = False
                self.animtimer = 0
                self.curframe = 0

          if isinstance(self.equip.righthand, Shotgun):
             if self.animtimer < 8:
                self.curframe = 1
             elif self.animtimer < 25:
                self.curframe = 0
             elif self.animtimer < 45:
                self.curframe = 2
             elif self.animtimer < 75:
                self.curframe = 0

             self.animtimer += 1
             if self.animtimer >= 75:
                self.attacking = False
                self.animtimer = 0
                self.curframe = 0

       if self.reloading == True:
          self.animtimer += 1
          if self.animtimer > self.equip.righthand.reloadtime:
             self.reloading = False
             self.animtimer = 0

    def DrawFrames(self):
      if self.equip.righthand is None:
         ika.Video.Blit(self.handframes[self.curframe], 125-5*self.curframe, 74)

      if isinstance(self.equip.righthand, Pipe):
         ika.Video.Blit(self.pipeframes[self.curframe], 125-5*self.curframe, 45)

      elif isinstance(self.equip.righthand, Pistol):
         ika.Video.Blit(self.pistolframes[self.curframe], 128, 82+2*self.curframe)
         if self.equip.righthand.count > 9: s = str(self.equip.righthand.count)
         else: s = "0"+str(self.equip.righthand.count)
         self.gunfont.Print(164,120+2*self.curframe,s)

      elif isinstance(self.equip.righthand, Shotgun):
         if self.curframe == 1: #firing, move it down slightly for recoil
            ika.Video.Blit(self.shotgunframes[1], 120, 78)
         else:
            ika.Video.Blit(self.shotgunframes[self.curframe], 120, 75)

      elif isinstance(self.equip.righthand, Rifle):
         ika.Video.Blit(self.rifleframes[self.curframe], 120, 75+2*self.curframe)
         if self.equip.righthand.count > 9: s = str(self.equip.righthand.count)
         else: s = "0"+str(self.equip.righthand.count)
         self.gunfont.Print(175,122+2*self.curframe,s)

    #OTHER ###################################################################################################

    def Move(self):
        if self.attacking or self.moveanim: return #bad, no move for you!

        offx, offy = self.offtable[self.facing]
        self.moved = False

        if ika.Input.keyboard['UP'].Pressed() or ika.Input.keyboard['W'].Pressed():
            if not self.GetObs(self.plrx+offx, self.plry+offy):
                self.plrx += offx; self.plry += offy
                self.moved = True

        elif ika.Input.keyboard['DOWN'].Pressed() or ika.Input.keyboard['S'].Pressed():
            offx *= -1; offy *= -1
            if not self.GetObs(self.plrx+offx, self.plry+offy):
                self.plrx += offx; self.plry += offy
                self.moved = True

        elif ika.Input.keyboard['LEFT'].Pressed() or ika.Input.keyboard['Q'].Pressed():
            if ika.Input.keyboard['RSHIFT'].Position() or ika.Input.keyboard['LSHIFT'].Position():
               offx, offy = self.offtable_l[self.facing]
               if not self.GetObs(self.plrx+offx, self.plry+offy):
                  self.plrx += offx; self.plry += offy
                  self.moved = True
            else:
               self.facing -= 1
               if self.facing < 0: self.facing = 3
               self.moved = True

        elif ika.Input.keyboard['RIGHT'].Pressed() or ika.Input.keyboard['E'].Pressed():
            if ika.Input.keyboard['RSHIFT'].Position() or ika.Input.keyboard['LSHIFT'].Position():
               offx, offy = self.offtable_r[self.facing]
               if not self.GetObs(self.plrx+offx, self.plry+offy):
                  self.plrx += offx; self.plry += offy
                  self.moved = True
            else:
               self.facing += 1
               if self.facing > 3: self.facing = 0
               self.moved = True

        elif ika.Input.keyboard['A'].Pressed():
           offx, offy = self.offtable_l[self.facing]
           if not self.GetObs(self.plrx+offx, self.plry+offy): 
              
              #HACK
              self.slideimg[0] = self.GrabWalls(self.plrx, self.plry, self.facing) #get current position still
              
              
              
              self.moved = True
              self.moveanim = True
              
              self.slideimg[1] = self.GrabWalls(self.plrx+offx, self.plry+offy, self.facing)
              
              self.plrx += offx; self.plry += offy
              

        elif ika.Input.keyboard['D'].Pressed():
            offx, offy = self.offtable_r[self.facing]
            if not self.GetObs(self.plrx+offx, self.plry+offy):
               self.plrx += offx; self.plry += offy
               self.moved = True

    def GetObs(self, x, y):
       if not ika.Map.GetObs(x,y,0):
          for e in self.entities:
             if e.x == x and e.y == y and not e.dead and isinstance(e, entity.Enemy):
                return True #enemy found, blocked
          return False
       return True #obstruction found
       
       
    def GrabWalls(self, dx, dy, facing): #returns an image of the walls drawn in a specific direction        
        ika.Video.ClipScreen(self.left, self.top, self.left+224, self.top+128)
        self.DrawWalls(dx, dy, facing)    
        ika.Video.ClipScreen()
        
        #img = ika.Video.GrabCanvas(self.left, self.top, self.left+224, self.top+128)
        #img.Save("testWalls.png")        
        
        return ika.Video.GrabImage(self.left, self.top, self.left+224, self.top+128)
    




    def DrawWalls(self, dx=None, dy=None, facing=None):
    
        if dx==None: dx=self.plrx
        if dy==None: dy=self.plry
        if facing==None: facing=self.facing
        
   
        if(self.moved): #We just took a step. Flip the background image, to make the movement look more realistic.
            self.backflip += 1
            if(self.backflip > 1): self.backflip = 0

        ents = [None]*25
        f_items = [None]*25

        item_offset = [0]*25
        
        b_obj = [False] * 25
        obj = [0]*25
        
        b_walls = [False] * 25
        walls = [0]*25
        
        b_decals = [[False] * 25,  [False] * 25]
        decals = [[0]*25, [0]*25] #currently two decal layers        
        decalf = [[0]*25, [0]*25] #decal facing
        decal_layers = [3, 5] #current decal layer indexes

        x = 0
        y = 0
        t = 0 #flat index, 0 - 25
        
        
        
        self.back[self.backflip].Blit(self.left, self.top) #Draw the background
        
	    ### This section generates 4 rows of data, to fill in the 25 item list as above. These are laid out in the following cell format, with cell 1 being the player's position:
        """
        [16][17][18][19][20][21][22][23][24][25]
            [ 8][ 9][10][11][12][13][14][15]
                [ 3][ 4][ 5][ 6][ 7]
                    [ 0][ 1][ 2]
        """
        ### These cells are dependent on the player's current facing, but makes it much easier to determine what must be drawn later. 
        ### Some cells are unused. This algorithm could (and possibly should) be modified to have a better line of sight to reduce unused cells.
        
        
        #this table is used to draw items at various heights if they are on top of specific objects as below
        offsettable = { OBJECT_TABLE: [16, 16, 12, 8], 
                        OBJECT_MEDTABLE: [16, 16, 12, 8],
                        OBJECT_CRATE: [40, 40, 36, 32]
                        } 
        
        for i in range(4): #4 rows, gathers data from player row outwards   
            j = -i-1 #starts at -1, ends -4 
            while(j < i+2): 
                #determine how cells that will be filled 
                if facing == 0: x = j; y = -i
                if facing == 1: x = i; y = j
                if facing == 2: x = -j; y = i
                if facing == 3: x = -i; y = -j                
                
                
                
                walls[t] = wrapper.GetTile(int(dx+x), int(dy+y), 0) #Wall layer
                if walls[t] > 0 and walls[t] < self.objnum:
                    walls[t]-=1 #walls are 0 based, so subtract 1 to get the correct index for the image
                    b_walls[t]=True #wall exists here
                
                ### HACK! Draw a facing view when in Obj mode of PDA ###
                ### Eventually will use this to test line of sight view to update the automap correctly ###
                if self.pda.mode == 2: 
                    if t==1: self.tiles[2].Blit(100+8*x, 199+8*y)
                    
                    elif walls[t]>0: 
                        self.tiles[1].Blit(100+8*x, 199+8*y)
                    else: self.tiles[0].Blit(100+8*x, 199+8*y)
                ### END HACK ###
                
                ents[t] = self.GetEnts(int(dx+x), int(dy+y))
                
                for l in range(len(decal_layers)):
                    d = wrapper.GetTile(int(dx+x), int(dy+y), decal_layers[l])
                    if d>=self.decalnum and d<100: #within decal range, currently tiles 40+
                        d-=self.decalnum
                        b_decals[l][t]=True
                        
                        decals[l][t] = d #get the decal tile number
                        
                        f = wrapper.GetTile(int(dx+x), int(dy+y), decal_layers[l] + 1) #facing layer is one layer higher than current decal layer
                        decalf[l][t] = f % 4 #get the facing number. Hack, modding by 4 lets us use any tile if we wanted to, and lets us put colors to help identify different decal layer facings

                
                o = wrapper.GetTile(int(dx+x), int(dy+y), 1) #Object layer
                
                if o>=self.objnum and o<self.decalnum: #within object range, currently tiles 20-40                  
                    b_obj[t] = True
                  #try: 
                    obj[t] = o - self.objnum # reduce bu objnumber in order to reference image arrays correctly
                  #except IndexError: 
                  #    #sometimes get very odd results for o when reading outside map bounds..
                  #    ika.Log("t:" + str(t))
                  #    ika.Log("o:" + str(o))
                  #    ika.Log("objnum:" + str(self.objnum))
                  #    ika.Log("x:"+str(int(dx+x)))
                  #    ika.Log("y:"+str(int(dy+y)))

                
                if self.items.has_key((int(dx+x), int(dy+y))):
                   f_items[t] = self.items[(int(dx+x), int(dy+y))]
                   
                   if o in [OBJECT_TABLE, OBJECT_MEDTABLE]: #hack to draw items at proper height on tables, object numbers 0 and 1
                      item_offset[t] = [48, 11, 9,0][i]
                   elif o+self.objnum == [OBJECT_CRATE]: #crate 
                      item_offset[t] = 32/(i+1) + 24

                j += 1
                t += 1




        ##### Drawing logic. Draws from back to front. #########################################                        
        
        
        
        #side walls
        pwalldicts = [ { 17: "per4farleft", 18: "per4left", 20: "per4right", 21: "per4farright"},
                       { 10: "per3left" , 12: "per3right" },
                       { 4: "per2left", 6: "per2right"},
                       { 0: "per1left", 2: "per1right"} ]
                                             
        #flat walls    
        fwalldicts = [ { }, #empty dict here as flat walls do not have a 4th row
                       {18: "flat3left", 19: "flat3mid", 20: "flat3right" },
                       {10: "flat2left", 11: "flat2mid", 12: "flat2right" },
                       {4: "flat1left", 5: "flat1mid", 6: "flat1right" }
        ]
        
        objdicts = [ { }, #empty dict here as objects do not have a 4th row                    
                     { 18: "3left", 19: "3mid", 20: "3right" },
                     { 10: "2left", 11: "2mid", 12: "2right" },  
                     { 4: "1left", 5: "1mid", 6: "1right"}  ]
        
        #locations for items
        base_itemy = [0, 64, 75, 100] #furthest to closest. index 0 is unused
        base_itemx = [[0,0,0], [25, 116, 185], [15, 116, 205], [10, 116, 210] ] # [row] [left, mid, right]
        scale = [0, 0.4, 0.75, 1]
        
        #locations for entities
        base_entityy = [0, 36, 32, 30] #furthest to closest. index 0 is unused
        base_entityx = [[0,0,0], [50, 101, 152], [7, 89, 170], [-58, 73, 198] ] # [row] [left, mid, right]        
        entrow = [3,2,1,0] #reverses the row index since the facing is stored closest to furthest
        
        
        for row in range(4): 
            if self.layer_visibility[row]:
                #using objects dict to draw objects, items and 
                for key, val in objdicts[row].items():                   
                   #objects are refreshingly simple to draw currently...
                   if b_obj[key]: self.objectimages[obj[key]][val].Blit(self.left, self.top)
     
                   if row>0:
                        draw = True
                        side=0     
                        
                        if "left" in val: side=0
                        elif "mid" in val: side=1
                        elif "right" in val: side=2
                        
                        if row==3 and side in (0, 2):
                            draw = False #Hack! Don't draw item if in last row and on either side. 
                        
                        if f_items[key] and draw:
                            for i, item in enumerate(f_items[key]):                                 
                                w = int( (item.w*16) * (scale[row]) / 2) #divide by 2 so can use half to +- from the base
                                h = int( (item.h*12) * (scale[row]) ) #using 12 instead of 16 to give a squished perspective view
                                yoffset = (item.h-1) * 6 # hack! move up 6 pixels for every extra tile of item height                                
                                #add (i*2) to move down 2 pixels for each stack. May need to put a max number of items in a stack to prevent weirdness..
                                topleft  = (base_itemx[row][side] - w  + (i*2), base_itemy[row] - item_offset[key] - yoffset + (i*2))
                                topright = (base_itemx[row][side] + w  + (i*2), base_itemy[row] - item_offset[key] - yoffset + (i*2)) 
                                botright = (base_itemx[row][side] + w  + (i*2), base_itemy[row] + h - item_offset[key] - yoffset + (i*2)) 
                                botleft  = (base_itemx[row][side] - w  + (i*2), base_itemy[row] + h - item_offset[key] - yoffset + (i*2))                                 
                                ika.Video.DistortBlit(item.img, topleft, topright, botright, botleft)                                

                        if(ents[key]): #enemies and entities next!
                           for e in ents[key]: 
                               if isinstance(e, entity.Enemy): ika.Video.Blit(e.GetFrame(facing, entrow[row]), base_entityx[row][side], base_entityy[row])
                               #elif isinstance(e, entity.Projectile):  ika.Video.Blit(e.GetFrame(facing, 2), 50+12, 36+12)                               
    
                #front facing walls and decals
                for key, val in fwalldicts[row].items():              
                      if b_walls[key]: self.wallimages[walls[key]][val].Blit(self.left, self.top)              
                      for l in range(len(decal_layers)):
                          if b_decals[l][key]:  
                            if self.facetable[facing] == decalf[l][key]:
                                try:
                                    self.decalimages[decals[l][key]][val].Blit(self.left, self.top)
                                except:
                                    ika.Log("key: "+str(key))
                                    ika.Log("val: "+str(val))
                                    ika.Log("decals[l][key]: "+str(decals[l][key]))
                                    ika.Log("key: "+str(key))                                    
                #perspective walls and decals
                for key, val in pwalldicts[row].items():
                      if b_walls[key]: self.wallimages[walls[key]][val].Blit(self.left, self.top)
                      for l in range(len(decal_layers)):
                          if b_decals[l][key]:  #and facing is correct
                            if ("left" in val and self.facetable_l[facing] == decalf[l][key]) or \
                               ("right" in val and self.facetable_r[facing] == decalf[l][key]): 
                                 try:
                                    self.decalimages[decals[l][key]][val].Blit(self.left, self.top)
                                 except:
                                    ika.Log("key: "+str(key))
                                    ika.Log("val: "+str(val))
                                    ika.Log("decals[l][key]: "+str(decals[l][key]))
                                    ika.Log("key: "+str(key))
                                    


        
        ##### Drawing done! #####	
        

        
    def AnimWalls(self):
        #currently kills all user input to draw animated walls instead
        time = ika.GetTime()        
        animlength = 14 #how many ticks to draw        
        animtimer = 1 #starts at 1 until > animlength
        done = False                        
        
        offsetx = 224/animlength

        while not done:
            t = ika.GetTime()
            while t > time:
               time += 1
               
               
            ika.Input.Update()
            time = ika.GetTime()
        
        
        
            ika.Video.Blit(self.hudmain, 0, 0)
            ika.Video.TintBlit(self.hudcolor, 0, 0, self.color)
            ika.Video.TintDistortBlit(self.hudhealth,
                                  (249, 144, self.color),
                                  (249 + (50 * self.health / self.max_health), 144, self.color),
                                  (249 + (50 * self.health / self.max_health), 150, self.color),
                                  (249, 150, self.color))
        
            ika.Video.ClipScreen(self.left, self.top, self.left+224, self.top+128)
            
            
            ika.Video.Blit(self.slideimg[0], self.left + int(offsetx * animtimer), self.top, ika.Opaque)
            ika.Video.Blit(self.slideimg[1], self.left + int(offsetx * animtimer) - 224, self.top, ika.Opaque)
            
            self.DrawFrames() #draws equipped weapon in its current state
            
            ika.Video.ClipScreen()
            
            self.inv.Draw()
            self.equip.Draw()

            self.pda.Draw()
            self.messages.Draw()
            
            ika.Video.ShowPage()
            
            animtimer +=1
            if animtimer > animlength: done = True
                
        self.moveanim=False    

    def GetEnts(self, x, y):
       dead_ents = []
       ents = []
       for e in self.entities:
          if e.x == x and e.y == y:
             if not e.dead: ents.append(e)
             else: dead_ents.append(e)
       return dead_ents + ents #makes sure dead entities are first


    def DrawAutoMap(self):
        for x in range(-11, 12):
            for y in range(-3, 4):
                if wrapper.GetTile(int(self.plrx+x), int(self.plry+y), 0) > 0 \
                and wrapper.GetTile(int(self.plrx+x), int(self.plry+y), 0) !=4: #haaaack

                   self.tiles[1].Blit(100+8*x, 199+8*y)
                ents = self.GetEnts(self.plrx+x, self.plry+y)
                for e in ents:
                   if e.dead:
                      self.tiles[3].Blit(100+8*x, 199+8*y)
                   else:
                      self.tiles[2].Blit(100+8*x, 199+8*y)

        ika.Video.TintBlit(self.arrows[self.facing], 100, 199, self.color)

    def Heal(self, amount):
       self.health += amount
       if self.health > self.max_health:
          self.health = self.max_health

    def Hurt(self, amount):
       
       hurtamt = (amount - self.defense)
       if hurtamt < 1: hurtamt=1
       self.health -= hurtamt

       if self.health > 75: self.sound.Play("pain100.wav")
       elif self.health > 50: self.sound.Play("pain75.wav")
       elif self.health > 25: self.sound.Play("pain50.wav")
       elif self.health > 0: self.sound.Play("pain25.wav")
       else: #dead!
          self.health = 0
          self.sound.Play("death.wav")
          self.Die()

    def Die(self):
       time = ika.GetTime()
       t = 0
       scr = ika.Video.GrabImage(0,0, 320, 240)
       while t < 128:
          ika.Video.Blit(scr, 0,0)
          ika.Video.DrawRect(0,0,320,240, ika.RGB(t,0,0,t), 1)
          ika.Input.Update()
          ika.Video.ShowPage()
          t = ika.GetTime() - time

       time = ika.GetTime()
       t = 0

       while t < 128:
          ika.Video.Blit(scr, 0,0)
          ika.Video.DrawRect(0,0,320,240, ika.RGB(128-t,0,0,128+t), 1)
          ika.Input.Update()
          ika.Video.ShowPage()
          t = ika.GetTime() - time
          self.music.volume = (128-t)/128.0

       self.music.Pause()
       intro.Start()

    def End(self):
       time = ika.GetTime()
       t = 0
       scr = ika.Video.GrabImage(0,0, 320, 240)

       while t < 255:
          ika.Video.Blit(scr, 0,0)
          ika.Video.DrawRect(0,0,320,240, ika.RGB(0,0,0,t), 1)
          ika.Input.Update()
          ika.Video.ShowPage()
          t = ika.GetTime() - time
          self.music.volume = (255-t)/255.0

       self.music.Pause()
       credits.Start()

### For activatable objects in the main view. Can also activate other, non clickable objects in the world, such as doors! 
### Switches are invisible, but are paired with decals.
### Each can be given a custom function to run, making them very flexible. :) 
class Switch(object): 
    def __init__(self, x, y, facing, action, clickable=False, clickarea=(0,0,0,0)):
        
        self.x=x #map x/y location of the switch.. may not be needed
        self.y=y
        self.action=action #reference to a function to run when switch is activated.
        self.facing=facing #direction of the switch
        self.clickarea = clickarea #tuple of form (x,y,w,h). are in main view coordinates, so 0,0 would be the top left of the world.
        
        
    def Activate(self):
        self.action()
        
        
class Messages(object): #for the two message lines under the main view
   def __init__(self):
      self.msg = ["", ""]
      self.time = [0, 0]
      self.maxtime = [0, 0]

   def Update(self):
      for i in range(2): 
          if self.maxtime[i] > 0: 
            self.time[i] +=1
            
      if self.time[0] >= self.maxtime[0]: #only pops one message per update
          self.Pop()         
         
   def AddMessage(self, msg, maxtime=500):
      if self.msg[0] == "":
         self.SetMessage(msg, 0, maxtime, 0)         
      elif self.msg[1] == "":
         self.SetMessage(msg, 0, maxtime, 1)
      else:
         self.Pop()
         self.SetMessage(msg, 0, maxtime, 1)

   def SetMessage(self, msg, time, maxtime, slot):
        self.msg[slot] = msg
        self.time[slot] = time
        self.maxtime[slot] = maxtime

   def Pop(self): #pops bottom message up one level and discards the top message
        self.SetMessage(self.msg[1], self.time[1], self.maxtime[1], 0)
        self.SetMessage("", 0, 0, 1)

   def Draw(self):
      for i, m in enumerate(self.msg):
         engine.tinyfont.Print(10, 144+10*i, m)


#generic thing, can update every frame to detect or react to changes
#class Thing(object):
#    def __init__(self, x, y, script):
#        self.x=x
#        self.y=y 
#        self.script=script
#
#    def update()

#type of thing that watches for player position

class Zone(object):
    def __init__(self, x, y, script):
        self.x=x
        self.y=y 
        self.script=script
        self.triggered=False

    def Update(self):
        self.script(self)




engine = Engine()
engine.Run()



    