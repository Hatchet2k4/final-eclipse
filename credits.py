import ika
import engine


def Start():

   planet = ika.Image("Img/title/planet.png")
   background = ika.Image("Img/title/background.png")
   title = ika.Image("Img/title/finaleclipse.png")
   titleglow = ika.Image("Img/title/finaleclipse_glow.png")
   sunglow = ika.Image("Img/title/sunglow.png")

   fridge = ika.Image("Img/logo/bitchfridge9.png")

   music = ika.Music("music/office.ogg")
   music.Play()
   ika.Delay(100)

   time = ika.GetTime()
   t = 0
   glow = 0
   glow2 = 0
   done = False

   font = ika.Font("fonts/tinyfont.fnt")

   while t<6255:

      if t%400<200:
         glow = int(255 - (t%400)/4)
      else: glow = int(155 + (t%400)/4)

      if t%600<300:
         glow2 = (t%600)/4
      else: glow2= 150-(t%600)/4

      ika.Video.Blit(background, 0, 0)
      ika.Video.TintBlit(sunglow, 0, 0, ika.RGB(255, glow, 128, glow))
      ika.Video.Blit(planet, 108, 58)

      if t<255:
         ika.Video.DrawRect(-1,-1,320,240, ika.RGB(0,0,0,255-t), 1)
      elif t<6000:
         ika.Video.TintBlit(titleglow, 0, 300-(t/4), ika.RGB(int(255-glow2/2), 0, 0, int(255-glow2)))
         ika.Video.Blit(title, 0, 300-(t/4))
         ika.Video.Blit(fridge, 0, 600-(t/4))

         Center(font, 850-(t/4), "-= Team Bitchfridge =-")

         Center(font, 930-(t/4), "Code:")
         Center(font, 950-(t/4), "Hatchet - @Boy are my fingers tired@")

         Center(font, 1030-(t/4), "Art:")
         Center(font, 1050-(t/4), "corey - @I like to make pretty pictures@")

         Center(font, 1130-(t/4), "Music:")
         Center(font, 1150-(t/4), "infey - @I am a cool guy and I like girls@")

         Center(font, 1230-(t/4), "Special Thanks:")
         Center(font, 1250-(t/4), "andy - For making ika and fixing bugs")
         Center(font, 1270-(t/4), "IRC testers - Your feedback was appreciated")

         Center(font, 1400-(t/4), "Thank you for playing!")
         Center(font, 1410-(t/4), "Full version coming soon!")

      else:
         ika.Video.DrawRect(-1,-1,320,240, ika.RGB(0,0,0,t-6000), 1)
         music.volume = (6255-t) / 255.0

      t=ika.GetTime()-time

      ika.Video.ShowPage()
      ika.Input.Update()

   ika.Exit("")

def Center(font, y, txt):
   font.Print(160-font.StringWidth(txt)/2, y, txt)
