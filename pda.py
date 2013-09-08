import ika
import engine
class PDA(object):
   def __init__(self):
      self.mode = 0
      self.buttons = [ika.Image("Img/ui/hudbmap.png"),
                      ika.Image("Img/ui/hudbstat.png"),
                      ika.Image("Img/ui/hudbobj.png"),
                      ika.Image("Img/ui/hudblog.png")]

      self.bhighlight = -1

      self.scroll_up = ika.Image("Img/ui/scroll_up.png")
      self.scroll_down = ika.Image("Img/ui/scroll_down.png")
      self.scroll_bar = ika.Image("Img/ui/scroll_bar.png")
      self.scroll_block = ika.Image("Img/ui/scroll_block.png")

      self.closebox = ika.Image("Img/ui/closebox.png")

      self.scroll = 0
      self.page = 0 #0 = list, 1 = message
      self.highlight = -1

      self.fulllogs = self.LoadLogs()
      self.logs = self.ReduceLogs()

      self.font = ika.Font('fonts/log_grey.fnt')
      self.hlfont = ika.Font('fonts/log_white.fnt')

   def Draw(self):


      x = engine.engine.MouseX()
      y = engine.engine.MouseY()
      bhl = False



      for i in range(4): #pda mode button highlight
         if self.mode != i and x > 199 and x < 199+33 and y > 171+16*i and y < 171+16*(i+1):
            r,g,b,a = ika.GetRGB(engine.engine.color)
            ika.Video.TintBlit(self.buttons[i], 199, 171+16*i, ika.RGB(r,g,b,192))

            if self.bhighlight != i:
               engine.engine.sound.Play("highlight.wav")

            self.bhighlight = i
            bhl = True

      if bhl == False: self.bhighlight = -1

      ika.Video.TintBlit(self.buttons[self.mode], 199, 171+16*self.mode, engine.engine.color)

      if self.mode == 0: # Map
         engine.engine.DrawAutoMap()

      if self.mode == 1: # Stats
         self.font.Print(13,174, "Health:   "+str(engine.engine.health)+"/"+str(engine.engine.max_health))
         self.font.Print(13,184, "Immunity: "+str(engine.engine.immunity)+"/"+str(engine.engine.max_immunity))
         self.font.Print(13,194, "Attack:   "+str(engine.engine.attack))
         self.font.Print(13,204, "Defense:  "+str(engine.engine.defense))

      if self.mode == 3: #Logs :D
         num = 0

         if self.page == 0: #Log List
            highlighted = False
            for i in range(min(6, len(self.logs))):
               if x > 13 and x <13 + self.font.StringWidth(self.logs[i][1]) and y > 174+10*i and y < 174+10*(i+1):
                  if i != self.highlight:
                     engine.engine.sound.Play("highlight.wav")

                  self.highlight = i
                  highlighted = True

            if highlighted == False: self.highlight = -1

            if len(self.logs)>0:
               for i in range(self.scroll, len(self.logs)):
                  show, title, message = self.logs[i]
                  if num < 6:
                     if self.highlight == num:
                        self.hlfont.Print(13, 174+10*num, title)
                     else: self.font.Print(13, 174+10*num, title)
                     num += 1


         else: #View the message
            for i in range(self.scroll, len(self.message)):
               if num < 6:
                  self.font.Print(13, 174+10*num, self.message[i])
                  num += 1

            ika.Video.TintBlit(self.closebox, 178, 173, engine.engine.color)


         #Scroll bar stuff
         ika.Video.TintDistortBlit(self.scroll_bar,
                                    (188, 181, engine.engine.color),(196, 181, engine.engine.color),
                                    (196, 224, engine.engine.color),(188, 224, engine.engine.color))

         if self.page == 0:
            scroll_range = len(self.logs) - 6
         else: scroll_range = len(self.message) - 6

         size = 43
         ypos = 181
         if scroll_range > 0:
            if scroll_range == 1: #special case that looks nice
               size = 35
            else: size = 42 / scroll_range + 1
            ypos = 181+((self.scroll * (43-size)) / scroll_range)
            #ika.Video.TintBlit(self.scroll_block, 188, int(ypos), engine.engine.color)


         ika.Video.TintDistortBlit(self.scroll_block,
                              (188, int(ypos), engine.engine.color),(196, int(ypos), engine.engine.color),
                              (196, int(ypos+size), engine.engine.color),(188, int(ypos+size), engine.engine.color))


         ika.Video.TintBlit(self.scroll_up, 188, 173, engine.engine.color)
         ika.Video.TintBlit(self.scroll_down, 188, 224, engine.engine.color)

         #ika.Video.TintDistortBlit(self.scroll_block,
         #                     (188, int(ypos), engine.engine.color),(196, int(ypos), engine.engine.color),
         #                     (196, int(ypos+size), engine.engine.color),(188, int(ypos+size), engine.engine.color))

         #ika.Video.DrawRect(188, int(ypos), 196, int(ypos+size), ika.RGB(0, 0, 0, 0), 1)

         #self.font.Print(10,0, str(self.scroll))
         #self.font.Print(10,10, str(ypos))
         #self.font.Print(10,20, str(size))
         #self.font.Print(10,40, str(scroll_range))


   def SetMode(self, m):
      self.mode = m
      self.page = 0
      self.scroll = 0

   def Click(self, x, y):

      for i in range(4): #pda mode button click
         if x > 199 and x < 199+33 and y > 171+16*i and y < 171+16*(i+1):
            self.SetMode(i)
            engine.engine.sound.Play("click.wav")

      if self.mode == 3:
         if self.page == 1:
            if x >= 178 and x <= 178+8 and y >= 173 and y <= 173+8: #close log
               self.page = 0
               self.scroll = 0
               engine.engine.sound.Play("click.wav")

         if x >= 188 and x <= 188+8 and y >= 173 and y <= 173+8: #scroll up
            if self.scroll > 0:
               self.scroll -= 1
            engine.engine.sound.Play("click.wav")

         if x >= 188 and x <= 188+8 and y >= 224 and y <= 224+8: #scroll down
            if self.page == 0:
               if self.scroll < len(self.logs)-6:
                  self.scroll += 1
            else:
               if self.scroll < len(self.message)-6:
                  self.scroll += 1
            engine.engine.sound.Play("click.wav")

         if x > 188 and x < 188+8 and y > 181 and y < 224: #clicked inside the scroll bar (not done yet)
            if self.page == 0:
               scroll_range = len(self.logs) - 6
            else: scroll_range = len(self.message) - 6

            if scroll_range > 0:
               pass

         if self.page == 0 and x > 13 and x <180:
            for i in range(min(6, len(self.logs))):
               if y > 174+10*i and y < 174+10*(i+1): #clicked on a message
                  self.page = 1
                  self.message = self.logs[i+self.scroll][2]
                  self.scroll = 0
                  engine.engine.sound.Play("click.wav")


   def LoadLogs(self):
      f = file("logs.dat")
      linelist = f.readlines()
      f.close()
      logs = []
      message = []
      title = ""
      for l in linelist:
         if title == "": title = l
         else:
            if l[0] != "#": #loop until a # character is reached
               message.append(l)
            else:
               logs.append((False, title, message))
               message = []
               title = ""

         ika.Input.Update()

      return logs

   def ReadLog(self, num):
      read, title, message = self.fulllogs[num]
      self.fulllogs[num] = (True, title, message)
      self.logs = self.ReduceLogs()

   def ReduceLogs(self):
      l = []
      for i in self.fulllogs:
         if i[0] is True:
            l.append(i)
      return l
