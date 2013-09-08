import ika

class Sound(object):
   def __init__(self, maxsize=24):
      self.sounds = []
      self.maxsize = maxsize

   def Play(self, filename, volume=0.5):
      s = ika.Sound("sfx/"+filename)
      s.volume = volume
      s.Play()
      self.sounds.append(s)
      if len(self.sounds) > self.maxsize: #cut the list in half when it gets too big
         self.sounds = self.sounds[int(self.maxsize/2):]