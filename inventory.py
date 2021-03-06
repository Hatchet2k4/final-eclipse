import ika
import engine

#### Inventory System ############################################################################################

class Inventory(object):
   def __init__(self):

      #None = empty
      #DummyItem = filled box, points to the item object that fills it
      #Item object = obvious :P


      self.items = [None] * 32
      self.left = 247
      self.top = 6


      self.AddItem(1, 1, Shells(16))
      self.AddItem(0, 1, Shells(10))
      self.AddItem(0, 0, Medkit(1))
      self.AddItem(0, 2, Food(2))

      #self.AddItem(3, 0, Shotgun(6) )
      #self.AddItem(0, 5, Armor1())
      self.AddItem(2, 6, Clip(40))
      self.AddItem(2, 7, Clip(60))
      self.AddItem(3, 7, Clip())
      self.AddItem(1, 7, Clip(42))

      self.block = ika.Image("Img/ui/block.png")
      self.grabbeditem = None


   def Draw(self):
      for i, item in enumerate(self.items):
         if item is not None:
            if isinstance(item, Item):
               #for w in range(item.w):
               #   for h in range(item.h):
                     #ika.Video.TintBlit(self.block, int(self.left+16*(i%4)+16*w), int(self.top+16*(i/4)+16*h),
                     #                     ika.RGB(0,0,128,100))
               #ika.Video.DrawRect(int(self.left+16*(i%4) - 1), int(self.top+16*(i/4) - 1),
               #                   int(self.left+16*(i%4)+16*item.w - 1), int(self.top+16*(i/4)+16*item.h - 1),
                                  #ika.RGB(0,0,255,128))
               #                   engine.engine.color)
               item.Draw(int(self.left+16*(i%4)), int(self.top+16*(i/4)))

   #tries to add an item to the inventory. Returns true if an item is grabbed as a result of this, false if not
   def AddItem(self, x, y, item): 
      
      if x+item.w>4 or y+item.h>8: return False #can't place an item if doing so would put it ouf of bounds

      g_item=None
      grab = False
      itemlist = self.CheckItems(x, y, item.w, item.h)

      if len(itemlist) < 2: #only try to place the item if there is one or no items underneath it

         if len(itemlist) == 1: #only one item, try to grab it

            g_item=self.TakeItem(itemlist[0][0], itemlist[0][1]) #Takes the item at the x / y location of first (only) item in the itemlist

            if isinstance(g_item, Stackable) and item.countable == True and type(g_item) == type(item) : #same type of item, try to stack them
               needed = item.max_count - item.count
               if needed >= g_item.count: #has room for the entire grabbed item to stack into it
                   item.count += g_item.count
                   g_item = None
               elif needed > 0: #only set to the maximum amount allowed by the item, rest is reduced from original item
                    item.count = item.max_count
                    g_item.count -= needed
            else: #normal item, so grab it instead of stacking it
               grab = True
         if (item.h > 1 or item.w > 1): #item < 1 tile in some direction, so place dummy items first
             d = DummyItem(x,y) #dummy items that point to the real item (only used for items larger than 1x1)
             for h in range(item.h):
                for w in range(item.w):
                   self.items[self.GetIndex(x+w,y+h)] = d
         self.items[self.GetIndex(x, y)] = item #place the real item at the top left location
         
         self.grabbeditem=g_item 
      else: grab = False #too many items underneath

      return grab

   #returns a list of x, y locations
   def CheckItems(self, x, y, w, h):
      itemList = []
      for a in range(w):
         for b in range(h):
            i = self.items[self.GetIndex(x+a,y+b)]
            if isinstance(i, Item):
               itemList.append((x+a, y+b))
            elif isinstance(i, DummyItem):
               if not (i.x, i.y) in itemList: #add original item, not the dummy
                  itemList.append((i.x, i.y))

      return itemList

   def TakeItem(self, x, y): #picks up an item from inventory and returns it
      item = self.items[self.GetIndex(x,y)]
      if isinstance(item, Item):
         self.RemoveItem(x,y, item.w, item.h)
      elif isinstance(item, DummyItem):
         i = self.items[self.GetIndex(item.x, item.y)] #find the original index pointed to by the dummy
         self.RemoveItem(item.x, item.y, i.w, i.h)
         item = i
      else: return None

      return item

   def DeleteItem(self, item):
      x, y = self.GetXY(self.items.index(item))
      self.RemoveItem(x, y, item.w, item.h)

   def RemoveItem(self, x, y, w, h):
      for i in range(h):
         for j in range(w):
            self.items[self.GetIndex(x+j,y+i)] = None

   def GetIndex(self, x, y): #square coordinates
      return int((y*4)+x)

   def GetXY(self, index):
      return index%4, index/4

   #### Public functions (The only ones the mouse system should access :P) ########################################
   #### x and y are mouse positions for these functions
   def UseItem(self, x, y):
      
      x -= self.left
      y -= self.top

      item = self.items[self.GetIndex(int(x/16),int(y/16))]

      if isinstance(item, Item): #make doubly sure it's an item before trying to use it..
         item.Use()
         if isinstance(item, Stackable) and item.count == 0:
            self.RemoveItem(int(x/16), int(y/16), item.w, item.h)

   def PlaceItem(self, x, y):
      x -= self.left
      y -= self.top

      if isinstance(self.AddItem(int(x/16), int(y/16), self.grabbeditem), Item):
         engine.engine.messages.AddMessage(self.grabbeditem.name)

   def GrabItem(self, x, y): #picks up an item from inventory and assigns it to be the item in your hand
      x -= self.left
      y -= self.top

      item = self.TakeItem(int(x/16), int(y/16))
      if item is not None:
         self.grabbeditem = item
         engine.engine.messages.AddMessage(self.grabbeditem.name)

#### Equipment System ##############################################################################################

class Equip(object):
   def __init__(self):
      self.righthand = Rifle(60)
      self.lefthand = None
      self.armor = Armor2()
      self.belt = Belt2()
      
      #self.righthand = None
      #self.lefthand = None
      #self.armor = Clothing()
      #self.belt = None

   def Draw(self):
      if self.righthand: self.righthand.Draw(253, 178)
      if self.lefthand: self.lefthand.Draw(253, 210)
      if self.armor: self.armor.Draw(272, 178)
      if self.belt: self.belt.Draw(272, 210)

   def AddItem(self, item, slot):
      if engine.engine.attacking or engine.engine.reloading: return #BAD! :P

      g_item = None
      if slot == 0: #right hand
         if isinstance(item, Weapon):
            if item.h == 2: #only takes one slot, do as normal
               g_item = self.righthand
               self.righthand = item
               if g_item:
                  engine.engine.messages.AddMessage(g_item.name)
            else: #two handed weapon
               if self.righthand and self.lefthand: return #both slots full

               if self.righthand: #only right hand full
                  g_item = self.righthand
                  engine.engine.messages.AddMessage(g_item.name)
                  self.righthand = None
                  self.righthand = item
               elif self.lefthand: #only left hand full
                  g_item = self.lefthand
                  engine.engine.messages.AddMessage(g_item.name)
                  self.lefthand = None
                  self.righthand = item
               else: #no hands full
                  self.righthand = item
         else: return

      elif slot == 1: #left hand
         if item.w == 1 and item.h == 1:
            if self.righthand and self.righthand.h == 3: #two handed weapon already equipped
               g_item = self.righthand
               engine.engine.messages.AddMessage(g_item.name)
               self.righthand = None
               self.lefthand = item
            else: #just a simple place
               g_item = self.lefthand
               self.lefthand = item
         else: return

      elif slot == 2: #armor
         if isinstance(item, Armor):
            g_item = self.armor
            if g_item: engine.engine.messages.AddMessage(g_item.name)
            self.armor = item
         else: return

      elif slot == 3: #belt
         if isinstance(item, Belt):
            g_item = self.belt
            if g_item: engine.engine.messages.AddMessage(g_item.name)
            self.belt = item
         else: return

      engine.engine.inv.grabbeditem = g_item

   def TakeItem(self, slot):
      r = None
      if slot == 0:
          r = self.righthand
          self.righthand = None
      elif slot == 1:
          r = self.lefthand
          self.lefthand = None
      elif slot == 2:
          r = self.armor
          self.armor = None
      elif slot == 3:
          r = self.belt
          self.belt = None
      if r: engine.engine.messages.AddMessage(r.name)

      return r

   def UseItem(self, slot):
      item = None
      if slot == 0: item = self.righthand
      elif slot == 1: item = self.lefthand
      elif slot == 2: item = self.armor
      elif slot == 3: item = self.belt

      if isinstance(item, Item):
         item.Use()
         if isinstance(item, Stackable) and item.count == 0:
            self.TakeItem(slot)

#### Generic Item Objects ###########################################################################################

class Item(object):
   def __init__(self, img, w, h, name, count=1, countable=False, imgused=None):
      self.img = img
      self.w = w
      self.h = h
      self.count = count
      self.countable = countable
      self.name = name
      if imgused is not None:
        self.imgused = imgused

   def Draw(self, x, y):
      ika.Video.Blit(self.img, x, y)
      if self.countable:
         if self.count > 0: #print in white if at least 1 left. Works up to 99, no ammo/stacks higher than this
            engine.engine.itemfont.Print(x + 16*self.w - 6*len(str(self.count))+1, y + 16*self.h - 7, str(self.count))
         else: engine.engine.itemfontgrey.Print(x + 16*self.w - 6, y + 16*self.h - 7, "0")

   def Use(self): #specific items must override this if they are to be used
      pass

class DummyItem(object):
   def __init__(self, x, y):
      self.x = x
      self.y = y

#### Specific Item Objects #########################################################################################

#Weapons
class Weapon(Item):
   def __init__(self, img, w, h, name, count=1, countable=False):
      super(Weapon, self).__init__(img, w, h, name, count, countable)
      self.attack = 0 #attack power
      self.reloadtime = 0 #ticks per reload

class Pipe(Weapon):
   img = ika.Image("Img/items/pipe.png")
   def __init__(self, count=0):
      super(type(self), self).__init__(type(self).img, 1, 2, "Lead Pipe")
      self.attack = 4
      self.reloadtime = 35

class Pistol(Weapon):
   img = ika.Image("Img/items/pistol.png")
   def __init__(self, count=0):
      super(type(self), self).__init__(type(self).img, 1, 2, "Pistol", count, True)
      self.attack = 3
      self.reloadtime = 35

class Shotgun(Weapon):
   img = ika.Image("Img/items/shotgun.png")
   def __init__(self, count=0):
      super(type(self), self).__init__(type(self).img, 1, 3, "Shotgun", count, True)
      self.attack = 10
      self.reloadtime = 70

class Rifle(Weapon):
   img = ika.Image("Img/items/rifle.png")
   def __init__(self, count=0):
      super(type(self), self).__init__(type(self).img, 1, 3, "Assault Rifle", count, True)
      self.attack = 2
      self.reloadtime = 200
#Armor
class Armor(Item):
   def __init__(self, img, w, h, name, count=1, countable=False):
      super(Armor, self).__init__(img, w, h, name, count, countable)

class Clothing(Armor):
   img = ika.Image("Img/items/clothing1.png")
   def __init__(self):
      super(type(self), self).__init__(type(self).img, 2, 2, "Clothes")
      self.defense = 1

class Armor1(Armor):
   img = ika.Image("Img/items/armor1.png")
   def __init__(self):
      super(type(self), self).__init__(type(self).img, 2, 2, "Light Armor")
      self.defense = 2

class Armor2(Armor):
   img = ika.Image("Img/items/armor2.png")
   def __init__(self):
      super(type(self), self).__init__(type(self).img, 2, 2, "Medium Armor")
      self.defense = 3

class Armor3(Armor):
   img = ika.Image("Img/items/armor3.png")
   def __init__(self):
      super(type(self), self).__init__(type(self).img, 2, 2, "Heavy Armor")
      self.defense = 4



#Belts
class Belt(Item):
   def __init__(self, img, w, h, name, count=1, countable=False):
      super(Belt, self).__init__(img, w, h, name, count, countable)

class Belt1(Belt):
   img = ika.Image("Img/items/belt1.png")
   def __init__(self):
      super(type(self), self).__init__(type(self).img, 2, 1, "Belt #1")
      self.defense = 2

class Belt2(Belt):
   img = ika.Image("Img/items/belt2.png")
   def __init__(self):
      super(type(self), self).__init__(type(self).img, 2, 1, "Belt #2")
      self.defense = 5

#Keys
class Key(Item):
   def __init__(self, img, w, h, name, count=1, countable=False):
      super(Key, self).__init__(img, w, h, name, count, countable)    

class BlueKey(Key):
    img = ika.Image("Img/items/key_blue.png")
    def __init__(self):
       super(type(self), self).__init__(type(self).img, 1, 1, "Blue Keycard")
       self.access = 1

class GreenKey(Key):
    img = ika.Image("Img/items/key_green.png")
    def __init__(self):
       super(type(self), self).__init__(type(self).img, 1, 1, "Green Keycard")
       self.access = 2     

class RedKey(Key):
    img = ika.Image("Img/items/key_red.png")
    def __init__(self):
       super(type(self), self).__init__(type(self).img, 1, 1, "Red Keycard")
       self.access = 3


#General Items
class Recorder(Item):
   img = ika.Image("Img/items/recorder.png")
   imgused = ika.Image("Img/items/recorder_used.png")
   def __init__(self, lognumber):
      super(type(self), self).__init__(type(self).img, 1, 1, "Log Recorder", type(self).imgused)
      self.lognumber = lognumber
      self.used = False
   def Use(self):
      if not self.used:
         engine.engine.pda.ReadLog(self.lognumber)
         engine.engine.messages.AddMessage("Log Uploaded to PDA")
         engine.engine.sound.Play("beep1.wav")
         self.used = True
         self.img = self.imgused

#Stackable Items 
class Stackable(Item):
   def __init__(self, img, w, h, name, count=1, countable=True):
      super(Stackable, self).__init__(img, w, h, name, count, countable)
      self.max_count = 0 #override per item  

#Ammo
class Clip(Stackable):
   img = ika.Image("Img/items/clip.png")
   def __init__(self, count=16):
      super(type(self), self).__init__(type(self).img, 1, 1, "Clip", count, True)
      self.max_count = 60
   def Use(self):
      pass
      #engine.engine.Reload(Clip)

class Shells(Stackable):
   img = ika.Image("Img/items/shells.png")
   def __init__(self, count=12):
      super(type(self), self).__init__(type(self).img, 1, 1, "Shells", count, True)
      self.max_count = 24
   def Use(self):
      pass
      #engine.engine.Reload(Shells)

class Cells(Stackable):
   img = ika.Image("Img/items/powercell.png")
   def __init__(self, count=30):
      super(type(self), self).__init__(type(self).img, 1, 1, "Power Cells", count, True)
      self.max_count = 90
   def Use(self):
      pass

#Healing items
class Hypo(Stackable):
   img = ika.Image("Img/items/hypo.png")
   def __init__(self, count=1):
      super(type(self), self).__init__(type(self).img, 1, 1, "Health hypo", count, True)
      self.max_count=5
   def Use(self):
      engine.engine.Heal(20)
      self.count -= 1

class Medkit(Stackable):
   img = ika.Image("Img/items/medkit.png")
   def __init__(self, count=1):
      super(type(self), self).__init__(type(self).img, 1, 1, "Medical kit", count, True)
      self.max_count=5
   def Use(self):
      engine.engine.Heal(50)
      self.count -= 1
      
class Food(Stackable):
   img = ika.Image("Img/items/foodcan.png")
   
   def __init__(self, count=1):
      super(type(self), self).__init__(type(self).img, 1, 1, "Canned food", count, True)
      self.max_count=5
   def Use(self):
      engine.engine.Heal(10)
      self.count -= 1
      
      