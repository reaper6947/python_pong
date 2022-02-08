# Pre-Poke Framework
# Implements a general game template for games with animation
# You must use this template for all your graphical lab assignments
# and you are only allowed to inlclude additional modules that are part of
# the Python Standard Library; no other modules are allowed

import pygame


# User-defined functions
HEIGHT = 700
WIDTH = 1000
PADDLE_GAP = 100
PADDLE_VELOCITY = 5
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((WIDTH, HEIGHT))
   # set the title of the display window
   pygame.display.set_caption('Pong')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      self.score = [0,0]
      # === game specific objects
      self.ball = Ball('white', 10, [50, 50], [2, 4], self.surface)
      self.l_paddle  =  Paddle('white', PADDLE_GAP, HEIGHT/2-(PADDLE_HEIGHT/2), PADDLE_WIDTH, self.surface, PADDLE_HEIGHT)
      self.r_paddle  = Paddle('white', WIDTH-PADDLE_GAP, HEIGHT/2-(PADDLE_HEIGHT/2), PADDLE_WIDTH, self.surface, PADDLE_HEIGHT)
   

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True


   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.ball.draw()
      self.l_paddle.draw()
      self.r_paddle.draw()
      self.draw_score()
      pygame.display.update() # make the updated surface appear on the display

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      keys_Pressed = pygame.key.get_pressed()
      if keys_Pressed[pygame.K_q]:
         self.l_paddle.velocity = -PADDLE_VELOCITY
      if keys_Pressed[pygame.K_a]:
         self.l_paddle.velocity = PADDLE_VELOCITY
      if keys_Pressed[pygame.K_p]:
         self.r_paddle.velocity = -PADDLE_VELOCITY
      if keys_Pressed[pygame.K_l]:
         self.r_paddle.velocity = PADDLE_VELOCITY
 

      
      if self.l_paddle.shape.y +self.l_paddle.velocity >= 0 and self.l_paddle.shape.y+ self.l_paddle.shape.height +self.l_paddle.velocity <=HEIGHT:
         self.l_paddle.shape.y+=self.l_paddle.velocity
      if self.r_paddle.shape.y +self.r_paddle.velocity >= 0 and self.r_paddle.shape.y+ self.r_paddle.shape.height +self.r_paddle.velocity <=HEIGHT:
         self.r_paddle.shape.y+=self.r_paddle.velocity
      #if self.ball.center[0]+self.ball.radius >= PADDLE_GAP+self.l_paddle.shape.width/2:
        # pass
  
      if self.ball.center[0]+self.ball.radius >= WIDTH:
         self.score[0]+=1
      if self.ball.center[0] - self.ball.radius == 0:
         self.score[1]+=1
 
      
      if self.l_paddle.shape.collidepoint(self.ball.center) or self.r_paddle.shape.collidepoint(self.ball.center):
         self.ball.velocity[0] = -self.ball.velocity[0]
         #self.ball.velocity[1] = -self.ball.velocity[1]

      self.ball.move()

   def draw_score(self):
        # Draw the score
        left_score =  str(self.score[0])
        right_score = str(self.score[1])
        font_size = 70
        font_name = 'Times New Roman'
        fg_color = pygame.Color('white')
        bg_color = None
        font = pygame.font.SysFont(font_name, font_size)
        left_box = font.render(left_score, True, fg_color, bg_color)
        left_location = (0, 0)
        self.surface.blit(left_box, left_location)
        right_box = font.render(right_score, True, fg_color, bg_color)
        right_location = (WIDTH -100,0)
        self.surface.blit(right_box, right_location)
        
class Ball:
   # An object in this class represents a Dot that moves 
   
   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
      # Initialize a Dot.
      # - self is the Dot to initialize
      # - color is the pygame.Color of the dot
      # - center is a list containing the x and y int
      #   coords of the center of the dot
      # - radius is the int pixel radius of the dot
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object

      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.surface = surface
      
   def move(self):
      # Change the location of the Dot by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # - self is the Dot
      size = self.surface.get_size() # size is a tuple (width, height)
      for i in range(0,2): # 0, 1
         self.center[i] = (self.center[i] + self.velocity[i])
            # left edge is similar to the top edge
            # right edge is similar to the bottom edge
         if self.center[i] <= self.radius or self.center[i] + self.radius >= size[i]:
            self.velocity[i] = -self.velocity[i]
            

   def draw(self):
      # Draw the dot on the surface
      # - self is the Dot
      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)

class Paddle:
   # An object in this class represents a Dot that moves 
   def __init__(self,paddle_color,paddle_x,paddle_y,paddle_width, surface, paddle_height,paddle_velocity =0):

      # Initialize a Dot.
      # - self is the Dot to initialize
      # - color is the pygame.Color of the paddle
      # - surface is the window's pygame.Surface object

      self.shape  = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
      self.color = pygame.Color(paddle_color)
      self.velocity = paddle_velocity
      self.surface = surface
      
   def draw(self):
      # Draw the dot on the surface
      # - self is the Dot
      pygame.draw.rect(self.surface, self.color, self.shape)

main()
