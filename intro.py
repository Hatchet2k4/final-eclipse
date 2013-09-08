import ika
import engine

def Start():
   ika.Video.DrawRect(0,0,320,240,ika.RGB(0,0,0), 1)
   ika.Video.ShowPage()

   music = ika.Music("music/intro.ogg")
   music.loop = True
   music.Play()

   img = ika.Image("Img/logo/ika_work.png")


   fridge=[]
   for i in range(1, 10):
      fridge.append(ika.Image("Img/logo/bitchfridge"+str(i)+".png"))

   team=ika.Image("Img/logo/team.png")
   presents=ika.Image("Img/logo/presents.png")

   ika.Delay(100)


   time = ika.GetTime()
   t = 0

   while t<255:
      ika.Input.Update()
      ika.Video.DrawRect(0,0,320,240,ika.RGB(0,0,0), 1)
      ika.Video.TintBlit(img, 0, 0, ika.RGB(255, 255, 255, t))
      ika.Video.ShowPage()
      t=ika.GetTime()-time

   while t<355:
      ika.Input.Update()
      t=ika.GetTime()-time

   while t<610:
      ika.Input.Update()
      ika.Video.DrawRect(0,0,320,240,ika.RGB(0,0,0), 1)
      ika.Video.TintBlit(img, 0, 0, ika.RGB(255, 255, 255, 610-t))
      ika.Video.ShowPage()
      t=ika.GetTime()-time

   while t<680:
      ika.Input.Update()
      t=ika.GetTime()-time

   time = ika.GetTime()
   t=0

   while t<128:
      ika.Input.Update()
      ika.Video.DrawRect(0,0,320,240,ika.RGB(t*2,t*2,t*2), 1)
      ika.Video.TintBlit(fridge[0], 0, 0, ika.RGB(255,255,255, t*2))
      ika.Video.ShowPage()
      t=ika.GetTime()-time

   time = ika.GetTime()
   t=0
   while t<578:
      ika.Input.Update()

      ika.Video.DrawRect(0,0,320,240,ika.RGB(255,255,255), 1)

      if t<128:
         ika.Video.Blit(fridge[0], 0, 0)
         ika.Video.TintBlit(team, 124, 10, ika.RGB(255, 255, 255, t*2))

      if t>=128 and t<180:
         ika.Video.Blit(fridge[0], 0, 0)
         ika.Video.Blit(team, 124, 10)

      if t>=180 and t<250:
         ika.Video.Blit(team, 124, 10)
         ika.Video.Blit(fridge[int((t-180)/10)], 0, 0)

      if t>=250 and t<350:
         ika.Video.Blit(fridge[8], 0, 0)
         ika.Video.Blit(team, 124, 10)

      if t>=350 and t<478:
         ika.Video.Blit(fridge[8], 0, 0)
         ika.Video.Blit(team, 124, 10)
         ika.Video.TintBlit(presents, 88, 210, ika.RGB(255, 255, 255, (t-350)*2))

      if t>=478 and t<578:
         ika.Video.Blit(fridge[8], 0, 0)
         ika.Video.Blit(team, 124, 10)
         ika.Video.Blit(presents, 88, 210)

      ika.Video.ShowPage()
      t=ika.GetTime()-time

   time = ika.GetTime()
   t=0

   while t<128:
      ika.Input.Update()
      ika.Video.DrawRect(0,0,320,240,ika.RGB(255-t*2,255-t*2,255-t*2), 1)
      ika.Video.TintBlit(fridge[8], 0, 0, ika.RGB(255,255,255, 255-t*2))
      ika.Video.TintBlit(team, 124, 10, ika.RGB(255,255,255, 255-t*2))
      ika.Video.TintBlit(presents, 88, 210, ika.RGB(255,255,255, 255-t*2))

      ika.Video.ShowPage()
      t=ika.GetTime()-time

   #Title

   planet = ika.Image("Img/title/planet.png")
   background = ika.Image("Img/title/background.png")
   title = ika.Image("Img/title/finaleclipse.png")
   titleglow = ika.Image("Img/title/finaleclipse_glow.png")
   opts = ika.Image("Img/title/new_load_quit.png")
   sunglow = ika.Image("Img/title/sunglow.png")

   optsg = ika.Image("Img/title/new_load_quit_glow.png")
   optsglow = [ika.Image("Img/title/new_load_quit_glow1.png"),
               ika.Image("Img/title/new_load_quit_glow2.png"),
               ika.Image("Img/title/new_load_quit_glow3.png")]

   time = ika.GetTime()
   t = 0

   glow = 0
   glow2 = 0
   #while t<1280:
   done=False

   selected = 0
   glowvalue = [255, 0, 0]
   glowincrement = [0, 0, 0]
   counted = False
   while not done:
      ika.Input.Update()

      ika.Video.Blit(background, 0, 0)


      if t>=500:
         s=t-500
         if s%400<200:
            glow = int(255 - (s%400)/4)
         else: glow = int(155 + (s%400)/4)

      if t>=755:
         s=t-755
         if s%600<300:
            glow2 = (s%600)/4
         else: glow2= 150-(s%600)/4

      if t<500:
         ika.Video.DrawRect(0,0,320,240,ika.RGB(0,0,0, 255-t/2), 1)

         glow = (t/2)+5

         ika.Video.TintBlit(sunglow, 0, 0, ika.RGB(255, 255, int(255-glow/2), glow))
         ika.Video.Blit(planet, 139-t/16, 48+t/50)

      if t>=500 and t<755:
         ika.Video.TintBlit(sunglow, 0, 0, ika.RGB(255, glow, 128, glow))
         ika.Video.Blit(planet, 108, 58)

         ika.Video.TintBlit(titleglow, 0, 0, ika.RGB(int(t-250), 0, 0, int(t-500)))
         ika.Video.TintBlit(title, 0, 0, ika.RGB(255, 255, 255, t-500))

      if t>=755 and t<1010:
         ika.Video.TintBlit(sunglow, 0, 0, ika.RGB(255, glow, 128, glow))
         ika.Video.Blit(planet, 108, 58)
         ika.Video.TintBlit(titleglow, 0, 0, ika.RGB(int(255-glow2/2), 0, 0, int(255-glow2)))
         ika.Video.Blit(title, 0, 0)

         ika.Video.TintBlit(optsg, 190, 130, ika.RGB(164, 164, 255, int((t-755)/2)) )
         ika.Video.TintBlit(optsglow[0], 190, 130, ika.RGB(164, 164, 255, t-755))

         ika.Video.TintBlit(opts, 190, 130, ika.RGB(255, 255, 255, t-755))



      if t>=1010:
         if counted == False: #cheap attempt at getting a good speed for the crossfades
            if ika.GetFrameRate < 100:
               inc = 300 / ika.GetFrameRate()
            else: inc = 3
            counted = True

         ika.Video.TintBlit(sunglow, 0, 0, ika.RGB(255, glow, 128, glow))
         ika.Video.Blit(planet, 108, 58)
         ika.Video.TintBlit(titleglow, 0, 0, ika.RGB(int(255-glow2/2), 0, 0, int(255-glow2)))
         ika.Video.Blit(title, 0, 0)

         ika.Video.TintBlit(optsg, 190, 130, ika.RGB(164, 164, 255, 128))

         for i in range(3):
            if glowincrement[i] != 0:
               glowvalue[i] += glowincrement[i]
               if glowvalue[i] > 255: glowvalue[i] = 255
               if glowvalue[i] < 0: glowvalue[i] = 0

            ika.Video.TintBlit(optsglow[i], 190, 130, ika.RGB(164, 164, 255, int(glowvalue[i])))

         ika.Video.Blit(opts, 190, 130)

         if ika.Input.keyboard['UP'].Pressed():
            glowincrement[selected] = -inc
            selected -= 1
            if selected < 0: selected = 2
            glowincrement[selected] = inc

         if ika.Input.keyboard['DOWN'].Pressed():
            glowincrement[selected] = -inc
            selected += 1
            if selected > 2: selected = 0
            glowincrement[selected] = inc

      if t>1000 and ika.Input.keyboard['RETURN'].Pressed():
         done=True
         scr=ika.Video.GrabImage(0,0,320,240)
      #font.Print(0,0,str(t))

      #font.Print(0,20,str(glowincrement))
      #font.Print(0,30,str(glowvalue))

      ika.Video.ShowPage()
      t=ika.GetTime()-time



   time = ika.GetTime()
   t = 0
   while t<128:
      music.volume = (128-t)/128.0
      ika.Video.Blit(scr, 0,0)
      ika.Video.DrawRect(0,0,320,240,ika.RGB(0,0,0, t*2), 1)
      ika.Video.ShowPage()
      ika.Input.Update()
      t=ika.GetTime()-time


   if selected == 2: ika.Exit("")

   if engine.engine: engine.engine.NewGame()

