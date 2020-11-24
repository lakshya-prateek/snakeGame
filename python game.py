#program to make a snake game....

import random,pygame,sys,time
from pygame.locals import*


#assigning screen display
class python:
   # naming variables  
   fps=9
   window_width = 1260
   window_height = 720
   cell_size=30
   assert window_width%cell_size == 0
   assert window_height%cell_size == 0
   cell_width=int(window_width/cell_size)
   cell_height=int(window_height/cell_size)
   #              r   g   b
   white    =   (255,255,255)
   black    =   (0  , 0 , 0 )
   red      =   (255, 0 , 0 )
   green    =   ( 0 ,255, 0 )
   darkgreen=   ( 0 ,127, 0 )
   darkgray =   (40 , 40, 40)
   yellow   =   (255,255, 0 )
   blue     =   ( 0 ,255,255)
   BGcolour = black
   UP="up"
   DOWN="down"
   LEFT="left"
   RIGHT="right"

   head = 0



   def main(self):
      global fpsclock,display,basicfont,pickupsound
      pygame.init()
      fpsclock=pygame.time.Clock()
      display=pygame.display.set_mode((self.window_width,self.window_height))
      basicfont=pygame.font.Font('freesansbold.ttf',20)
      pygame.display.set_caption('Python')
    
      

      while True:
          pygame.mixer.music.load('the man.mp3')
          pygame.mixer.music.play(-1 ,0.0) 
          self.showstartscreen()
         
          self.rungame()
          self.showGameOverScreen()
          self.highscore(len(self.snakecoords) - 3)
        
        

   def rungame(self):
      self.x=random.randint(5,self.cell_width-20)
      self.y=random.randint(5,self.cell_height-10)
      self.snakecoords=[{'x':self.x,'y':self.y},
                       {'x':self.x-1,'y':self.y},
                       {'x':self.x-2,'y':self.y}]

      self.direction=self.RIGHT


      self.frog=self.getRandomLocation()
      while True:
         for event in pygame.event.get():
            if event.type == QUIT:
               self.terminate()

            elif event.type == KEYDOWN:

               if event.key == K_LEFT:
                  self.direction=self.LEFT
               elif event.key == K_RIGHT:
                  self.direction=self.RIGHT
               elif event.key == K_UP:
                  self.direction=self.UP
               elif event.key == K_DOWN:
                  self.direction=self.DOWN
               elif event.key == K_ESCAPE:
                  self.terminate()
               elif event.key == ord('p'):
                    # Pausing the game
                    pygame.mixer.music.stop()
                    self.showtextpause() # pause until a key press
                    pygame.mixer.music.play(-1, 0.0)
               elif event.key == ord('m'):
                  #pausing sound
                   pygame.mixer.music.stop()

                   
                    
         #check weather snake has hit itself        
         if self.snakecoords[self.head]['x'] == -1 or self.snakecoords[self.head]['x'] == self.cell_width or self.snakecoords[self.head]['y'] == self.cell_height or self.snakecoords[self.head]['y'] == -1 :
               return #game over
         for snakeBody in self.snakecoords[1:]:
            if snakeBody['x'] == self.snakecoords[self.head]['x'] and snakeBody['y'] == self.snakecoords[self.head]['y']:
               return # game over
       
        


         #check weather snake has eaten frog
         if self.snakecoords[self.head]['x'] == self.frog['xx'] and self.snakecoords[self.head]['y'] == self.frog['yy']:
                pygame.mixer.music.load('sound.mp3')
                pygame.mixer.music.play(1,0.0)
                self.frog = self.getRandomLocation()#set new apple
                
                  
                
         else:
              del self.snakecoords[-1]#remove snake tail

              


         
         #move the snake
         if self.direction == self.UP:
              self.newhead={'x':self.snakecoords[self.head]['x'],'y':self.snakecoords[self.head]['y']-1}
         elif self.direction == self.DOWN:
              self.newhead={'x':self.snakecoords[self.head]['x'],'y':self.snakecoords[self.head]['y']+1}    
         elif self.direction == self.LEFT:
              self.newhead={'x':self.snakecoords[self.head]['x']-1,'y':self.snakecoords[self.head]['y']}    
         elif self.direction == self.RIGHT:
              self.newhead={'x':self.snakecoords[self.head]['x']+1,'y':self.snakecoords[self.head]['y']}        
         self.snakecoords.insert(0,self.newhead)


         display.fill(self.BGcolour)
         self.drawgrass()
         self.drawsnake(self.snakecoords)
         self.drawfrog(self.frog)
         self.drawScore(len(self.snakecoords) - 3)
         pygame.display.update()
         fpsclock.tick(self.fps)


   def drawPressKeyMsg(self):
        presskeysurf = basicfont.render('Press enter to play.', True , self.darkgray)
        presskeyRect = presskeysurf.get_rect()
        presskeyRect.topleft = (self.window_width - 203, self.window_height - 30)
        display.blit(presskeysurf, presskeyRect)
    

   def checkForKeyPress(self):
    
       if len(pygame.event.get(QUIT)) > 0:   #check for quit events
           self.terminate()
       keyUpEvents = pygame.event.get(KEYUP)
       if len(keyUpEvents) == 0:      #check for keyup events
           return None
       if keyUpEvents[0].key == K_ESCAPE:
           self.terminate()
       return keyUpEvents[0].key
   
    
   def showstartscreen(self):
        titlefont=pygame.font.Font('freesansbold.ttf',100)
        titlesurf1=titlefont.render('PYTHON!',True,self.white,self.darkgreen)
        titlesurf2=titlefont.render('PYTHON!',True,self.green)

        degree1=0
        degree2=0
        while True:
            
            display.fill(self.BGcolour)
            rotatedSurf1 = pygame.transform.rotate(titlesurf1, degree1)
            rotatedRect1 = rotatedSurf1.get_rect()
            rotatedRect1.center = (self.window_width / 2, self.window_height / 2)
            display.blit(rotatedSurf1, rotatedRect1)

            rotatedSurf2 = pygame.transform.rotate(titlesurf2, degree2)
            rotatedRect2 = rotatedSurf2.get_rect()
            rotatedRect2.center = (self.window_width / 2,self.window_height / 2)
            display.blit(rotatedSurf2, rotatedRect2)
           
            self.drawPressKeyMsg()

            if self.checkForKeyPress():
                pygame.event.get() # clear event 
                return
            pygame.display.update()
            fpsclock.tick(self.fps)
            degree1 += 3 # rotate by 3 degrees each frame
            degree2 += 5 # rotate by 5 degrees each frame
            

   def terminate(self):
       pygame.quit()
       sys.exit()


   def getRandomLocation(self):
        return {'xx': random.randint(1, self.cell_width - 10), 'yy': random.randint(1, self.cell_height- 10)}


   def showGameOverScreen(self):
        gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
        gamesurf = gameOverFont.render('Game', True, self.blue)
        oversurf = gameOverFont.render('Over', True, self.blue)
        gamerect = gamesurf.get_rect()
        overrect = oversurf.get_rect()
        gamerect.midtop = (self.window_width / 2, 10)
        overrect.midtop = (self.window_width / 2, gamerect.height)

        display.blit(gamesurf, gamerect)
        display.blit(oversurf, overrect)
        self.drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)
        pygame.mixer.music.stop()
        pygame.mixer.music.load('GameOversound.mp3')
        pygame.mixer.music.play(1,0.0) 
        
        self.checkForKeyPress() # clear out any key presses in the event 

        while True:
            if self.checkForKeyPress():
                pygame.event.get()#clear event 
                return


   def drawScore(self,score):
       scoreSurf = basicfont.render('Score: %s' % (score), True, self.white)
       scoreRect = scoreSurf.get_rect()
       scoreRect.topleft = (self.window_width - 120, 10)
       display.blit(scoreSurf, scoreRect)
    

   def drawsnake(self,snakeCoords):
       for self.coord in snakeCoords:
           self.x = self.coord['x'] * self.cell_size
           self.y = self.coord['y'] * self.cell_size
           pygame.draw.ellipse(display, self.red ,(self.x,self.y, self.cell_size+5, self.cell_size),12)
           pygame.draw.ellipse(display, self.yellow ,(self.x+4, self.y+4 , self.cell_size-3, self.cell_size-8),8)


   def drawfrog(self,coord):
       self.x = coord['xx'] * self.cell_size
       self.y = coord['yy'] * self.cell_size
       frog = pygame.image.load("frog3.png")
       frogRect = pygame.Rect(self.x, self.y, self.cell_size, self.cell_size)
       display.blit(frog, frogRect)


   
   def showtextpause(self):
        pausefont = pygame.font.Font('freesansbold.ttf', 50)
        pausesurf = pausefont.render('Game Pause',True,self.blue)
        pauserect = pausesurf.get_rect()
        pauserect.midtop = (self.window_width / 2, 100)
        display.blit(pausesurf, pauserect)
        self.drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)
        self.checkForKeyPress()
        while True :               #check for key press to continue
            if self.checkForKeyPress(): 
                pygame.event.get()
                return

   def drawgrass(self):
    
       grass = pygame.image.load("image.jpeg")
       grassrect=pygame.draw.ellipse(display, self.BGcolour ,(0, 0, self.cell_size, self.cell_size),1)
       display.blit(grass,grassrect)

   def highscore(self,score):
        highscorefont = pygame.font.Font('freesansbold.ttf', 80)
        highscoresurf = highscorefont.render('Your Score: %s' % (score),True,self.blue)
        highscorerect = highscoresurf.get_rect()
        highscorerect.midbottom  = (self.window_width / 2, 600)
        display.blit(highscoresurf, highscorerect)
        self.drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)
        self.checkForKeyPress()
        while True :               #check for key press to continue
            if self.checkForKeyPress(): 
                pygame.event.get()
                return
 

a=python()
a.main()
    
