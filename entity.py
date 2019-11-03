import ika
import engine
from const import *


class Entity(object):
    def __init__(self, x, y, f):        
      self.x = x
      self.y = y

      self.startx = x #keep a record of original spawn location
      self.starty = y

      self.facing = f
      self.curframe = 0
      self.time = 0

      #access as [player facing][entity facing]
      self.dirtable = [[0, 1, 2, 3], #player facing north
                       [3, 0, 1, 2], #east
                       [2, 3, 0, 1], #south
                       [1, 2, 3, 0]] #west

      self.offtable = [(0,-1), (1, 0), (0, 1), (-1,0)]

    def Update(self):
       pass
       
class Projectile(Entity):
    sprites=[ika.Image("Img/effects/circle32.png"),
            ika.Image("Img/effects/circle24.png"),
            ika.Image("Img/effects/circle16.png")]    

    def __init__(self, x, y, f):        
        super(type(self), self).__init__(x, y, f)
        self.numframes = 1
        self.distance=0
        self.max_distance = 5
        self.dead=False
        
    def Update(self):
        if not self.dead:
            self.time += 1
            if self.time>=20:
                self.time=0
                self.distance+=1
                if self.distance>self.max_distance:
                    self.dead=True
                else:
                    self.Move(self.facing)
                    
    def Move(self, d):
      offx, offy = self.offtable[d]
      if not engine.engine.GetObs(self.x+offx, self.y+offy):
         self.x += offx
         self.y += offy
      else:
         self.dead=True
       
        
    def GetFrame(self, face, row):
        return Projectile.sprites[self.numframes*row]

#### Generic enemy class #######################################################

class Enemy(Entity):
   def __init__(self, x, y, f):
      super(Enemy, self).__init__(x, y, f)      

      self.attacking = False
      self.dead = False
      self.dying = False
      self.hurt = False

      self.hp = 0
      self.numframes = 15


      self.attacking = False
      self.walkanim = 1

   def Update(self):
      pass

   def Hurt(self, dmg):
      if self.dead: return
      self.hp -= dmg
      if self.hp <= 0:
         self.hp = 0
         if not self.dying:
            self.dying = True
            self.time = 0
      else:
         if not self.attacking:
            self.hurt = True
            self.hurttime = 0

   def Distance(self, x, y):
      return abs(self.startx-x) + abs(self.starty-y)

def LoadMonsterFrames(f):
   sprites = []
   for s in ['96', '64', '40']:
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_b1.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_b2.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_r1.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_r2.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_f1.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_f2.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_l1.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_l2.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_atk1.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_atk2.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_atk3.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_atk4.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_die1.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_die2.png"))
      sprites.append(ika.Image("Img/enemies/"+f+s+"/"+f+"_dead.png"))
   return sprites


#### Specific enemy classes ############################################################################

class Vagimon(Enemy):
   sprites = LoadMonsterFrames("vagimon")

   def __init__(self, x, y, f):
      super(type(self), self).__init__(x, y, f)
      self.hp = 20
      self.time = ika.Random(0, 100)
      self.hurttime = 0
   def GetFrame(self, face, row):
      if self.dead:
         return Vagimon.sprites[14 + self.numframes*row]
      elif self.dying:
         return Vagimon.sprites[12 + self.numframes*row + self.time / 40]
      elif self.hurt:
         return Vagimon.sprites[12 + self.numframes*row]
      elif not self.attacking:
         return Vagimon.sprites[(self.dirtable[face][self.facing])*2 + (self.numframes*row)+self.walkanim]
      elif self.attacking:
         return Vagimon.sprites[8 + self.time/10 + self.numframes*row]

   def Move(self, d):
      offx, offy = self.offtable[d]
      if not engine.engine.GetObs(self.x+offx, self.y+offy) and self.Distance(self.x+offx, self.y+offy)<10:
         self.x += offx
         self.y += offy
         self.facing = d

   def Update(self):
      if self.dead: return

      self.time += 1

      if self.attacking and self.time == 30:
         offx, offy = self.offtable[self.facing]
         if engine.engine.plrx == self.x + offx and engine.engine.plry == self.y + offy:
            engine.engine.Hurt(6) #make sure the player is still in front of the enemy before hurting him :P

      elif self.attacking and self.time >= 40:
         self.attacking = False
         self.time = 0

      if self.hurt:
         self.hurttime += 1
         if self.hurttime > 10:
            self.hurt = False
            self.hurttime = 0

      if self.dying and self.time >= 80:
         self.dying = False
         self.dead = True
         self.time = 0

      if self.time > 200: #time to move
         randmove = True
         self.time = 0
         for d in range(4):
            offx, offy = self.offtable[d]
            for i in range(1, 4):
               if engine.engine.plrx == self.x + offx*i and engine.engine.plry == self.y + offy*i:
                  randmove = False

                  if i == 1: #player within range!
                     self.attacking = True
                     self.facing = d
                     self.time = 0
                     engine.engine.sound.Play("vagimon_attack.wav", 1)
                  else:
                     self.Move(d)

         if randmove:
            #won't move any more than 4 squares from its start location
               self.Move(ika.Random(0, 4))


      if self.time % 200 < 100:
         self.walkanim = 0
      else:
         self.walkanim = 1

class Walker(Enemy):
   sprites = LoadMonsterFrames("walker")

   def __init__(self, x, y, f):
      super(type(self), self).__init__(x, y, f)
      self.hp = 32
      self.time = ika.Random(0, 100)

   def GetFrame(self, face, row):
      if self.dead:
         return Walker.sprites[14 + self.numframes*row]
      elif self.dying:
         return Walker.sprites[12 + self.numframes*row + self.time / 40]
      elif self.hurt:
         return Walker.sprites[12 + self.numframes*row]
      if not self.attacking:
         return Walker.sprites[(self.dirtable[face][self.facing])*2+(self.numframes*row)+self.walkanim]
      elif self.attacking:
         return Walker.sprites[8 + self.time/10 + self.numframes*row]

   def Move(self, d):
      offx, offy = self.offtable[d]
      if not engine.engine.GetObs(self.x+offx, self.y+offy) and self.Distance(self.x+offx, self.y+offy) < 10:
         self.x += offx
         self.y += offy
         self.facing = d

   def Update(self):
      if self.dead: return

      self.time += 1

      if self.attacking and self.time == 30:
         offx, offy = self.offtable[self.facing]
         if engine.engine.plrx == self.x + offx and engine.engine.plry == self.y + offy:
            engine.engine.Hurt(10) #make sure the player is still in front of the enemy before hurting him :P

      elif self.attacking and self.time >= 40:
         self.attacking = False
         self.time = 0

      if self.hurt:
         self.hurttime += 1
         if self.hurttime > 10:
            self.hurt = False
            self.hurttime = 0

      if self.dying and self.time >= 80:
         self.dying = False
         self.dead = True
         self.time = 0

      if self.time > 200: #time to move
         randmove = True
         self.time = 0
         for d in range(4):
            offx, offy = self.offtable[d]
            for i in range(1, 4):
               if engine.engine.plrx == self.x + offx*i and engine.engine.plry == self.y + offy*i:
                  randmove = False

                  if i == 1: #player within range!
                     self.attacking = True
                     self.facing = d
                     self.time = 0
                     engine.engine.sound.Play("vagimon_attack.wav", 1)
                  else:
                     self.Move(d)

         if randmove:
             self.Move(ika.Random(0, 4))


      if self.time % 200 < 100:
         self.walkanim = 0
      else:
         self.walkanim = 1






