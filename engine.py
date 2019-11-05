import ika
from inventory import *
import intro
from const import *
import entity
import sound
import pda
import credits


ika.SetCaption(ika.GetCaption() + " - Final Eclipse")
engine = None
#intro.Start()
#credits.Start()

class Engine(object):
    def __init__(self):

        self.tinyfont = ika.Font('fonts/log_white.fnt')
        self.itemfont = ika.Font('fonts/item_white.fnt')
        self.itemfontgrey = ika.Font('fonts/item_grey.fnt')
        self.gunfont = ika.Font('fonts/font_gun.fnt')

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

        self.left=8
        self.top=5

        self.lw0=[]
        self.cw0=[]
        self.rw0=[]
        self.lp0=[]
        self.rp0=[]

        self.lw1=[]
        self.cw1=[]
        self.rw1=[]
        self.lp1=[]
        self.rp1=[]

        self.lw2=[]
        self.cw2=[]
        self.rw2=[]
        self.lp2=[]
        self.rp2=[]

        self.flp3=[]
        self.lp3=[]
        self.rp3=[]
        self.frp3=[]

		#self.texturetest=ika.Image("Img/Walls/texturetest.png")\
        self.deck = ""
        self.backgrounds = {}
        self.objects = []
        self.decals = []
        self.objnum = 20 #objects start at 20 in the map
        self.decalnum = 40
        self.arrows = []
        for i in range(4):
            self.arrows.append(ika.Image("Img/minimap/Pointer"+str(i)+".png"))

        self.tiles=[ika.Image("Img/minimap/space.png"),
                    ika.Image("Img/minimap/wall.png"),
                    ika.Image("Img/minimap/enemy.png"),
                    ika.Image("Img/minimap/enemy_d.png")]

        self.backflip = 0
        self.moved = False


        #self.LoadWalls("medsci")
        self.LoadWalls()
        self.LoadDecals()
        self.LoadObjects()
        
        self.LoadDeck("final")
        

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


        self.color = ika.RGB(0,0,0)
        self.offtable = [(0,-1), (1, 0), (0, 1), (-1,0)]
        self.offtable_l = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        self.offtable_r = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def LoadDeck(self, deck):
        self.deck = deck
        self.back = self.backgrounds[deck]

    def LoadWalls(self):
       
       decklist = ["medsci", "office", "operations", "barracks", "final"]
       for d in decklist:     
           self.backgrounds[d] = [ika.Image("img/backgrounds/"+d+"1.png"), ika.Image("img/backgrounds/"+d+"2.png")]
       
       
       
       #if deck == "medsci":
       walllist = ["med1", "med2", "med1win", "med1door", "med2door", "military", "militarydoor", "bed", "final", "finalspace"]          
       
       
          
       for path in walllist:

         self.lw0.append(ika.Image("img/walls/"+path+"/flat1left.png"))
         self.cw0.append(ika.Image("img/walls/"+path+"/flat1mid.png"))
         self.rw0.append(ika.Image("img/walls/"+path+"/flat1right.png"))

         self.lp0.append(ika.Image("img/walls/"+path+"/per1left.png"))
         self.rp0.append(ika.Image("img/walls/"+path+"/per1right.png"))

         self.lw1.append(ika.Image("img/walls/"+path+"/flat2left.png"))
         self.cw1.append(ika.Image("img/walls/"+path+"/flat2mid.png"))
         self.rw1.append(ika.Image("img/walls/"+path+"/flat2right.png"))

         self.lp1.append(ika.Image("img/walls/"+path+"/per2left.png"))
         self.rp1.append(ika.Image("img/walls/"+path+"/per2right.png"))

         self.lw2.append(ika.Image("img/walls/"+path+"/flat3left.png"))
         self.cw2.append(ika.Image("img/walls/"+path+"/flat3mid.png"))
         self.rw2.append(ika.Image("img/walls/"+path+"/flat3right.png"))

         self.lp2.append(ika.Image("img/walls/"+path+"/per3left.png"))
         self.rp2.append(ika.Image("img/walls/"+path+"/per3right.png"))

         self.flp3.append(ika.Image("img/walls/"+path+"/per4farleft.png"))
         self.lp3.append(ika.Image("img/walls/"+path+"/per4left.png"))
         self.rp3.append(ika.Image("img/walls/"+path+"/per4right.png"))
         self.frp3.append(ika.Image("img/walls/"+path+"/per4farright.png"))

    def LoadObjects(self):
       objlist = ["table", "medtable", "blood_floor1", "blood_floor2", "crate"]
       filelist = ["1left.png", "1mid.png","1right.png",
                   "2left.png", "2mid.png","2right.png",
                   "3left.png", "3mid.png","3right.png"]

       for path in objlist:
          obj = []
          for img in filelist:
             obj.append(ika.Image("img/objects/"+path+"/"+img))
          self.objects.append(obj)

    def LoadDecals(self):
        decallist = ["door", "dcode_r", "dcode_g", "dkey_r", "dkey_g", "blood_sm", "blood_big", "switch1", "switch2"] #order is important, based on order in tileset. /4 for each direction
        filelist = ["flat1left.png", "flat1mid.png","flat1right.png", "per1left.png", "per1right.png",
               "flat2left.png", "flat2mid.png","flat2right.png", "per2left.png", "per2right.png",
               "flat3left.png", "flat3mid.png","flat3right.png", "per3left.png", "per3right.png",
               "per4left.png", "per4right.png", "per4left.png", "per4farleft, per4farright.png"]
        
        for path in decallist:      
            d=Decal()
            d.lw0 = ika.Image("img/decals/"+path+"/flat1left.png")
            d.cw0 = ika.Image("img/decals/"+path+"/flat1mid.png")
            d.rw0 = ika.Image("img/decals/"+path+"/flat1right.png")

            d.lp0 = ika.Image("img/decals/"+path+"/per1left.png")
            d.rp0 = ika.Image("img/decals/"+path+"/per1right.png")

            d.lw1 = ika.Image("img/decals/"+path+"/flat2left.png")
            d.cw1 = ika.Image("img/decals/"+path+"/flat2mid.png")
            d.rw1 = ika.Image("img/decals/"+path+"/flat2right.png")

            d.lp1 = ika.Image("img/decals/"+path+"/per2left.png")
            d.rp1 = ika.Image("img/decals/"+path+"/per2right.png")

            d.lw2 = ika.Image("img/decals/"+path+"/flat3left.png")
            d.cw2 = ika.Image("img/decals/"+path+"/flat3mid.png")
            d.rw2 = ika.Image("img/decals/"+path+"/flat3right.png")

            d.lp2 = ika.Image("img/decals/"+path+"/per3left.png")
            d.rp2 = ika.Image("img/decals/"+path+"/per3right.png")

            d.flp3 = ika.Image("img/decals/"+path+"/per4farleft.png")
            d.lp3 = ika.Image("img/decals/"+path+"/per4left.png")
            d.rp3 = ika.Image("img/decals/"+path+"/per4right.png")
            d.frp3 = ika.Image("img/decals/"+path+"/per4farright.png")
            self.decals.append(d) 

    def NewGame(self):
        self.inv = Inventory()
        self.equip = Equip()
        self.entities=[
                       #entity.Vagimon(10,3, ika.Random(0, 4)),
                       #entity.Vagimon(5,8, ika.Random(0, 4)),
                       #entity.Vagimon(7,11, ika.Random(0, 4)),
                       #entity.Vagimon(3,11, ika.Random(0, 4)),
                       entity.Vagimon(11,17, ika.Random(0, 4)),
                       entity.Vagimon(15,7, ika.Random(0, 4)),
                       entity.Vagimon(11,10, ika.Random(0, 4)),
                       entity.Vagimon(13,12, ika.Random(0, 4)),
                       entity.Vagimon(6,15, ika.Random(0, 4)),
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
                       entity.Walker(9,11, ika.Random(0, 4)),
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
                       ]

        self.items = {
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
                     }

        self.health = 70
        self.max_health = 100

        self.immunity = 80
        self.max_immunity = 100

        self.attack = 0
        self.defense = 0

        self.plrx = 3
        self.plry = 5
        self.facing = EAST

        self.backflip = 0
        self.moved = False

        self.curframe = 0
        self.attacking = False
        self.reloading = False
        self.animtimer = 0

        self.music = ika.Music("music/medsci.ogg")
        self.music.loop = True
        self.music.Play()

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

            self.UpdateStats()
            self.Move()
            self.DrawWalls()
            self.DrawFrames() #draws equipped weapon in its current state

            #main hud drawing
            ika.Video.Blit(self.hudmain, 0, 0)
            ika.Video.TintBlit(self.hudcolor, 0, 0, self.color)
            ika.Video.TintDistortBlit(self.hudhealth,
                                  (249, 144, self.color),
                                  (249 + (50 * self.health / self.max_health), 144, self.color),
                                  (249 + (50 * self.health / self.max_health), 150, self.color),
                                  (249, 150, self.color))

            self.inv.Draw()
            self.equip.Draw()

            self.pda.Draw()
            self.messages.Draw()

            if not self.fullscreen:
               self.DoMouse()
            else: #no mouse in fullscreen mode :P
               scr = ika.Video.GrabImage(8,5, 224, 133)
               ika.Video.DrawRect(0,0,320,240, ika.RGB(0,0,0), 1)
               ika.Video.ScaleBlit(scr, 0, 28, 320, 184)

            #self.tinyfont.Print(0,0, str(ika.GetFrameRate()))
            #self.tinyfont.Print(0,10, str(self.animtimer))

            if ika.Input.keyboard['ESCAPE'].Pressed():
               #scr = ika.Video.GrabImage(0,0, 320, 240)
               ika.Video.DrawRect(0,0,320,240, ika.RGB(0,0,0,128), 1)
               ika.Video.ShowPage()
               while not ika.Input.keyboard['ESCAPE'].Pressed():
                   #ika.Video.Blit(scr, 0,0)

                   ika.Input.Update()
                   #ika.Video.ShowPage()

               ika.Input.Unpress()
               time = ika.GetTime()

            ika.Video.ShowPage()

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
          and self.MouseY() > self.top + 8 and self.MouseY() < self.top + 128: #clicked in bottom of main window
              offx, offy = self.offtable[self.facing]
              if self.inv.grabbeditem is None: #not holding an item, try to grab one
                 #todo: code pressing buttons
                 # if facing a wall directly ahead and wall contains a pressable item, find the clickable area and compare to activate


                 if self.items.has_key((self.plrx+offx, self.plry+offy)): #item exists here
                    self.inv.grabbeditem = self.items[(self.plrx+offx, self.plry+offy)].pop() #grabs only the first item out of the list
                    self.messages.AddMessage(self.inv.grabbeditem.name)
                    if len(self.items[(self.plrx+offx, self.plry+offy)]) == 0:
                       del self.items[(self.plrx+offx, self.plry+offy)] #delete out of dict if it's empty
              else: #holding an item, place it
              		#todo: add in code for using keys on buttons, etc

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
               self.entities.append(entity.Projectile(self.plrx+offx,self.plry+offy, self.facing))
               
               
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
        if self.attacking: return #bad, no move for you!

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
              self.plrx += offx; self.plry += offy
              self.moved = True

        elif ika.Input.keyboard['D'].Pressed():
            offx, offy = self.offtable_r[self.facing]
            if not self.GetObs(self.plrx+offx, self.plry+offy):
               self.plrx += offx; self.plry += offy
               self.moved = True

    def GetObs(self, x, y):
       if not ika.Map.GetObs(x,y,0):
          for e in self.entities:
             if e.x == x and e.y == y and not e.dead:
                return True #entity found
          return False
       return True #obsutrction found

    def DrawWalls(self):

        if(self.moved): #Took a step. Flip the background image, to make the movement look more realistic..
            self.backflip += 1
            if(self.backflip > 1): self.backflip = 0

        ents = [None]*25
        f_items = [None]*25

        item_offset = [0]*25

        obj = [None]*25
        walls = [1]*25
        decals = [None]*25

        x = 0
        y = 0
        t = 0 #flat index to walls
        
        #background
        self.back[self.backflip].Blit(self.left, self.top)
        
	
        for i in range(4): #4 rows
            j = -i-1 #starts -1, ends -4 
            while(j < i+2):
                if self.facing == 0: x = j; y = -i
                if self.facing == 1: x = i; y = j
                if self.facing == 2: x = -j; y = i
                if self.facing == 3: x = -i; y = -j

                walls[t] = ika.Map.GetTile(int(self.plrx+x), int(self.plry+y), 0) #Wall layer
                ents[t] = self.GetEnts(int(self.plrx+x), int(self.plry+y))
                
                d = ika.Map.GetTile(int(self.plrx+x), int(self.plry+y), 3) #Decal layer
                if d>=self.decalnum and d<100: #within decal range, currently tiles 40+
                    d-=self.decalnum
                    try: 
                       dec = int(d /4) #get the decal tile number
                       facing = d % 4 #get the facing number
                       #decals[t] = self.decals[dec]
                       decals[t] = dec
                    except IndexError: 
                        ika.Log("d:" + str(d))
                
                o = ika.Map.GetTile(int(self.plrx+x), int(self.plry+y), 1) #get from Object layer
                
                if o>=self.objnum and o<self.decalnum: #within object range, currently tiles 20-40
                  o-=self.objnum
                  try: 
                     obj[t] = self.objects[o]
                  except IndexError: 
                      #sometimes get very odd results for o when reading outside map bounds..
                      ika.Log("t:" + str(t))
                      ika.Log("o:" + str(o))
                      ika.Log("objnum:" + str(self.objnum))
                      ika.Log("x:"+str(int(self.plrx+x)))
                      ika.Log("y:"+str(int(self.plry+y)))
                      
                      
                      
                  
                  

                
                if self.items.has_key((int(self.plrx+x), int(self.plry+y))):
                   f_items[t] = self.items[(int(self.plrx+x), int(self.plry+y))]
                   if o<2: #hack to draw items at proper height on tables, object numbers 0 and 1
                      item_offset[t] = 32/(i+1)
                   elif o-self.objnum==4: #crate 
                      item_offset[t] = 32/(i+1) + 24

                j += 1
                t += 1





        ##### Row 3 ############################################################################
        if(walls[17]): self.flp3[walls[17]-1].Blit(self.left, self.top)
        if(walls[18]): self.lp3[walls[18]-1].Blit(self.left, self.top)
        if(walls[20]): self.rp3[walls[20]-1].Blit(self.left, self.top)
        if(walls[21]): self.frp3[walls[21]-1].Blit(self.left, self.top)
        """
        if(decals[17]): decals[17].flp3.Blit(self.left, self.top)
        if(decals[18]): decals[18].lp3.Blit(self.left, self.top)
        if(decals[20]): decals[20].rp3.Blit(self.left, self.top)
        if(decals[21]): decals[21].frp3.Blit(self.left, self.top)
        """
        ##### Row 2 ############################################################################

        if(obj[18]): obj[18][6].Blit(self.left, self.top)
        if(obj[19]): obj[19][7].Blit(self.left, self.top)
        if(obj[20]): obj[20][8].Blit(self.left, self.top)

        if f_items[18]:
           for i in f_items[18]: ika.Video.DistortBlit(i.img,
                                  (25, 66-item_offset[18]), (25+8*i.w, 66-item_offset[18]),
                                  (25+8*i.w,66+6*i.h-item_offset[18]), (25, 66+6*i.h-item_offset[18]))
        if f_items[19]:
           for i in f_items[19]: ika.Video.DistortBlit(i.img,
                                  (110, 66-item_offset[19]), (110+8*i.w, 66-item_offset[19]),
                                  (110+8*i.w,66+6*i.h-item_offset[19]), (110, 66+6*i.h-item_offset[19]))
        if f_items[20]:
           for i in f_items[20]: ika.Video.DistortBlit(i.img,
                                  (185, 66-item_offset[20]), (185+8*i.w, 66-item_offset[20]),
                                  (185+8*i.w,66+6*i.h-item_offset[20]), (185, 66+6*i.h-item_offset[20]))
        if(ents[18]):
           for e in ents[18]: 
               if isinstance(e, entity.Enemy): ika.Video.Blit(e.GetFrame(self.facing, 2), 50, 36)
               elif isinstance(e, entity.Projectile):  ika.Video.Blit(e.GetFrame(self.facing, 2), 50+12, 36+12)                               
        if(ents[19]):
           for e in ents[19]: 
               if isinstance(e, entity.Enemy): ika.Video.Blit(e.GetFrame(self.facing, 2), 101, 36)
               elif isinstance(e, entity.Projectile):  ika.Video.Blit(e.GetFrame(self.facing, 2), 101+12, 36+12)
        if(ents[20]):
           for e in ents[20]: 
               if isinstance(e, entity.Enemy): ika.Video.Blit(e.GetFrame(self.facing, 2), 152, 36)
               elif isinstance(e, entity.Projectile):  ika.Video.Blit(e.GetFrame(self.facing, 2), 152+12, 36+12)

        if(walls[18]): self.lw2[walls[18]-1].Blit(self.left, self.top)
        if(walls[19]): self.cw2[walls[19]-1].Blit(self.left, self.top)
        if(walls[20]): self.rw2[walls[20]-1].Blit(self.left, self.top)

        if(walls[10]): self.lp2[walls[10]-1].Blit(self.left, self.top)
        if(walls[12]): self.rp2[walls[12]-1].Blit(self.left, self.top)
        
        if(decals[18]): self.decals[decals[18]-1].lw2.Blit(self.left, self.top)
        if(decals[19]): self.decals[decals[19]-1].cw2.Blit(self.left, self.top)
        if(decals[20]): self.decals[decals[20]-1].rw2.Blit(self.left, self.top)
        if(decals[10]): self.decals[decals[10]-1].lp2.Blit(self.left, self.top)
        if(decals[12]): self.decals[decals[12]-1].rp2.Blit(self.left, self.top)

        ##### Row 1 ############################################################################

        if(obj[10]): obj[10][3].Blit(self.left, self.top)
        if(obj[11]): obj[11][4].Blit(self.left, self.top)
        if(obj[12]): obj[12][5].Blit(self.left, self.top)

        if f_items[10]:
           for i in f_items[10]: ika.Video.DistortBlit(i.img,
                                  (15, 75-item_offset[10]), (15+12*i.w, 75-item_offset[10]),
                                  (15+12*i.w,75+(10-i.h)*i.h-item_offset[10]), (15, 75+(10-i.h)*i.h-item_offset[10]))
        if f_items[11]:
           for i in f_items[11]: ika.Video.DistortBlit(i.img,
                                  (110, 75-item_offset[11]), (110+12*i.w, 75-item_offset[11]),
                                  (110+12*i.w,75+(10-i.h)*i.h-item_offset[11]), (110, 75+(10-i.h)*i.h-item_offset[11]))
        if f_items[12]:
           for i in f_items[12]: ika.Video.DistortBlit(i.img,
                                  (205, 75-item_offset[12]), (205+12*i.w, 75-item_offset[12]),
                                  (205+12*i.w,75+(10-i.h)*i.h-item_offset[12]), (205, 75+(10-i.h)*i.h-item_offset[12]))

        if(ents[10]):
           for e in ents[10]: #ika.Video.Blit(e.GetFrame(self.facing, 1), 7, 32)
               if isinstance(e, entity.Enemy): ika.Video.Blit(e.GetFrame(self.facing, 1), 7, 32)
               elif isinstance(e, entity.Projectile):  ika.Video.TintBlit(e.GetFrame(self.facing, 1), 50+8, 32+8, e.color)   
        if(ents[11]):
           for e in ents[11]: #ika.Video.Blit(e.GetFrame(self.facing, 1), 89, 32)
               if isinstance(e, entity.Enemy): ika.Video.Blit(e.GetFrame(self.facing, 1), 89, 32)
               elif isinstance(e, entity.Projectile):  ika.Video.TintBlit(e.GetFrame(self.facing, 1), 50+8, 32+8, e.color)   
        if(ents[12]):
           for e in ents[12]: #ika.Video.Blit(e.GetFrame(self.facing, 1), 170, 32)
               if isinstance(e, entity.Enemy): ika.Video.Blit(e.GetFrame(self.facing, 1), 170, 32)
               elif isinstance(e, entity.Projectile):  ika.Video.TintBlit(e.GetFrame(self.facing, 1), 50+8, 32+8, e.color)   


        if(walls[10]): self.lw1[walls[10]-1].Blit(self.left, self.top)
        if(walls[11]): self.cw1[walls[11]-1].Blit(self.left, self.top)
        if(walls[12]): self.rw1[walls[12]-1].Blit(self.left, self.top)

        if(walls[4]): self.lp1[walls[4]-1].Blit(self.left, self.top)
        if(walls[6]): self.rp1[walls[6]-1].Blit(self.left, self.top)

        #do facing..
        """
        if(decals[10]): decals[10].lw1.Blit(self.left, self.top)
        if(decals[11]): decals[11].cw1.Blit(self.left, self.top)
        if(decals[12]): decals[12].rw1.Blit(self.left, self.top)
        if(decals[4]): decals[4].lp1.Blit(self.left, self.top)
        if(decals[6]): decals[6].rp1.Blit(self.left, self.top)
        """
        ##### Row 0 ############################################################################

        if(obj[4]): obj[4][0].Blit(self.left, self.top)
        if(obj[5]): obj[5][1].Blit(self.left, self.top)
        if(obj[6]): obj[6][2].Blit(self.left, self.top)

        if f_items[4]:
           for i in f_items[4]: ika.Video.DistortBlit(i.img,
                                          (10, 96-i.h-item_offset[4]), (10+16*i.w, 96-i.h-item_offset[4]),
                                          (10+16*i.w,96+(14-i.h*2)*i.h-item_offset[4]), (10, 96+(14-i.h*2)*i.h-item_offset[4]))
        if f_items[5]:
           for i in f_items[5]: ika.Video.DistortBlit(i.img,
                                          (107, 96-i.h-item_offset[5]), (107+16*i.w, 96-i.h-item_offset[5]),
                                          (107+16*i.w,96+(14-i.h*2)*i.h-item_offset[5]), (107, 96+(14-i.h*2)*i.h-item_offset[5]))
        if f_items[6]:
           for i in f_items[6]: ika.Video.DistortBlit(i.img,
                                          (210, 96-i.h-item_offset[6]), (210+16*i.w, 96-i.h-item_offset[6]),
                                          (210+16*i.w,96+(14-i.h*2)*i.h-item_offset[6]), (210, 96+(14-i.h*2)*i.h-item_offset[6]))

        if(ents[4]):
           for e in ents[4]: #ika.Video.Blit(e.GetFrame(self.facing, 0), -58, 30)
               if isinstance(e, entity.Enemy): ika.Video.Blit(e.GetFrame(self.facing, 0), -58, 30)
               elif isinstance(e, entity.Projectile):  ika.Video.TintBlit(e.GetFrame(self.facing, 0), -58+32, 30+32, e.color)   
        if(ents[5]):
           for e in ents[5]: #ika.Video.Blit(e.GetFrame(self.facing, 0), 73, 30)
               if isinstance(e, entity.Enemy): ika.Video.Blit(e.GetFrame(self.facing, 0), 73, 30)
               elif isinstance(e, entity.Projectile):  ika.Video.TintBlit(e.GetFrame(self.facing, 0), 73+32, 30+8, e.color)   
        if(ents[6]):
           for e in ents[6]: #ika.Video.Blit(e.GetFrame(self.facing, 0), 198, 30)
               if isinstance(e, entity.Enemy): ika.Video.Blit(e.GetFrame(self.facing, 0), 198, 30)
               elif isinstance(e, entity.Projectile):  ika.Video.TintBlit(e.GetFrame(self.facing, 0), 198+32, 30+32, e.color)   

        if(walls[4]): self.lw0[walls[4]-1].Blit(self.left, self.top)
        if(walls[5]): self.cw0[walls[5]-1].Blit(self.left, self.top)
        if(walls[6]): self.rw0[walls[6]-1].Blit(self.left, self.top)

        #do facing..
        if(decals[4]): self.decals[decals[4]-1].lw0.Blit(self.left, self.top)
        if(decals[5]): self.decals[decals[5]-1].cw0.Blit(self.left, self.top)
        if(decals[6]): self.decals[decals[6]-1].rw0.Blit(self.left, self.top)


        #if f_items[1]:
        #   for i in f_items[1]: ika.Video.Blit(i.img, 110, 110)

        # diagonal walls row 0
        if(walls[0]): self.lp0[walls[0]-1].Blit(self.left, self.top)
        if(walls[2]): self.rp0[walls[2]-1].Blit(self.left, self.top)
        
        if(decals[0]): self.decals[decals[0]-1].lp0.Blit(self.left, self.top)
        if(decals[2]): self.decals[decals[2]-1].rp0.Blit(self.left, self.top)

	#self.cw1[0].Blit(self.left, self.top)
	#self.texturetest.Blit(self.left+15, self.top+6)
	
	#uncomment for fun texture distortion :D 
	#self.texturetest.DistortBlit((self.left+15, self.top+6),
	#			     (self.left+53, self.top+20),
	#			     (self.left+53, self.top+89),
	#			     (self.left+15, self.top+117)    	
	
	#)
	


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
                if ika.Map.GetTile(int(self.plrx+x), int(self.plry+y), 0) > 0 \
                and ika.Map.GetTile(int(self.plrx+x), int(self.plry+y), 0) !=4:

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

class Decal(object): 
    def __init__(self):
        self.lw0=None
        self.cw0=None
        self.rw0=None
        self.lp0=None
        self.rp0=None
                 
        self.lw1=None
        self.cw1=None
        self.rw1=None
        self.lp1=None
        self.rp1=None
                 
        self.lw2=None
        self.cw2=None
        self.rw2=None
        self.lp2=None
        self.rp2=None

        self.flp3=None
        self.lp3=None
        self.rp3=None
        self.frp3=None

class Messages(object): #two message lines under the dungeon window
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

   def Pop(self): #pops bottom message up one level
        self.SetMessage(self.msg[1], self.time[1], self.maxtime[1], 0)
        self.SetMessage("", 0, 0, 1)

   def Draw(self):
      for i, m in enumerate(self.msg):
         engine.tinyfont.Print(10, 144+10*i, m)

ika.Map.Switch('medsci.ika-map')

engine = Engine()
engine.NewGame()
engine.Run()

