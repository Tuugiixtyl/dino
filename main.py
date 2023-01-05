import pygame
import os
import random
pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.transform.scale(pygame.image.load(os.path.join("assets/witch", "w_run_1.png")), (54, 88)),
            pygame.transform.scale(pygame.image.load(os.path.join("assets/witch", "w_run_2.png")), (54, 88)),
            pygame.transform.scale(pygame.image.load(os.path.join("assets/witch", "w_run_3.png")), (54, 88)),
            pygame.transform.scale(pygame.image.load(os.path.join("assets/witch", "w_run_4.png")), (54, 88)),
            pygame.transform.scale(pygame.image.load(os.path.join("assets/witch", "w_run_5.png")), (54, 88)),
            pygame.transform.scale(pygame.image.load(os.path.join("assets/witch", "w_run_6.png")), (54, 88)),
            pygame.transform.scale(pygame.image.load(os.path.join("assets/witch", "w_run_7.png")), (54, 88)),]

JUMPING = pygame.transform.scale(pygame.image.load(os.path.join("assets/witch", "w_jump.png")), (54, 69))
DUCKING = [pygame.transform.scale(pygame.image.load(os.path.join("assets/witch", "w_duck_1.png")), (46, 46)),
           pygame.transform.scale(pygame.image.load(os.path.join("assets/witch", "w_duck_2.png")), (46, 46)),]

TOMBSTONE = [pygame.transform.scale(pygame.image.load(os.path.join("assets/obstacle", "tombstone.png")), (54, 84))]

ZOMBO = [pygame.transform.scale(pygame.image.load(os.path.join("assets/obstacle", "o_zombo_1.png")), (66, 84)),
         pygame.transform.scale(pygame.image.load(os.path.join("assets/obstacle", "o_zombo_2.png")), (66, 84)),]

BAT = [pygame.transform.scale(pygame.image.load(os.path.join("assets/obstacle", "o_bat_1.png")), (54, 36)),
       pygame.transform.scale(pygame.image.load(os.path.join("assets/obstacle", "o_bat_2.png")), (54, 36)),]

BG = pygame.image.load(os.path.join("assets/other", "Track.png"))

class Witch:
  X_POS = 80
  Y_POS = 310
  Y_POS_DUCK = 360
  JUMP_VEL = 8.5

  def __init__(self):
      self.duck_img = DUCKING
      self.run_img = RUNNING
      self.jump_img = JUMPING

      self.w_duck = False
      self.w_run = True
      self.w_jump = False

      self.step_index = 0
      self.jump_vel = self.JUMP_VEL
      self.image = self.run_img[0]
      self.w_rect = self.image.get_rect()
      self.w_rect.x = self.X_POS
      self.w_rect.y = self.Y_POS

  def update(self, userInput):
      if self.w_duck:
          self.duck()
      if self.w_run:
          self.run()
      if self.w_jump:
          self.jump()

      if self.step_index >= 10:
          self.step_index = 0

      if userInput[pygame.K_UP] and not self.w_jump:
          self.w_duck = False
          self.w_run = False
          self.w_jump = True
      elif userInput[pygame.K_DOWN] and not self.w_jump:
          self.w_duck = True
          self.w_run = False
          self.w_jump = False
      elif not (self.w_jump or userInput[pygame.K_DOWN]):
          self.w_duck = False
          self.w_run = True
          self.w_jump = False

  def duck(self):
      self.image = self.duck_img[self.step_index // 5]
      self.w_rect = self.image.get_rect()
      self.w_rect.x = self.X_POS
      self.w_rect.y = self.Y_POS_DUCK
      self.step_index += 1

  def run(self):
      self.image = self.run_img[self.step_index // 2]
      self.w_rect = self.image.get_rect()
      self.w_rect.x = self.X_POS
      self.w_rect.y = self.Y_POS
      self.step_index += 1

  def jump(self):
      self.image = self.jump_img
      if self.w_jump:
          self.w_rect.y -= self.jump_vel * 4
          self.jump_vel -= 0.8
      if self.jump_vel < - self.JUMP_VEL:
          self.w_jump = False
          self.jump_vel = self.JUMP_VEL

  def draw(self, SCREEN):
      SCREEN.blit(self.image, (self.w_rect.x, self.w_rect.y))

class Obstacle:
  def __init__(self, image, type):
    self.image = image
    self.type = type
    self.rect = self.image[self.type].get_rect()
    self.rect.x = SCREEN_WIDTH

  def update(self):
    self.rect.x -= game_speed
    if self.rect.x < -self.rect.width:
        obstacles.pop()

  def draw(self, SCREEN):
    SCREEN.blit(self.image[self.type], self.rect)

class Tombstone(Obstacle):
  def __init__(self, image):
      self.type = random.randint(0, 0)
      super().__init__(image, self.type)
      self.rect.y = 325

class Bats(Obstacle):
  def __init__(self, image):
      self.type = 0
      super().__init__(image, self.type)
      self.rect.y = 290
      self.index = 0

  def draw(self, SCREEN):
      if self.index >= 9:
          self.index = 0
      SCREEN.blit(self.image[self.index//5], self.rect)
      self.index += 1

class Zombo(Obstacle):
  def __init__(self, image):
      self.type = 0
      super().__init__(image, self.type)
      self.rect.y = 325
      self.index = 0

  def draw(self, SCREEN):
      if self.index >= 9:
          self.index = 0
      SCREEN.blit(self.image[self.index//5], self.rect)
      self.index += 1

def main():
  global game_speed, x_pos_bg, y_pos_bg, points, obstacles
  run = True
  clock = pygame.time.Clock()
  player = Witch()
  game_speed = 20
  x_pos_bg = 0
  y_pos_bg = 380
  points = 0
  font = pygame.font.Font('freesansbold.ttf', 20)
  obstacles = []
  death_count = 0

  def background():
    global x_pos_bg, y_pos_bg
    image_width = BG.get_width()
    SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    if x_pos_bg <= -image_width:
      SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
      x_pos_bg = 0
    x_pos_bg -= game_speed

  def score():
    global points, game_speed
    points += 1
    if points % 100 == 0:
      game_speed += 1

    text = font.render("Points: " + str(points), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (1000, 40)
    SCREEN.blit(text, textRect)

  while run:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = True

    SCREEN.fill((255, 255, 255))
    userInput = pygame.key.get_pressed()

    player.draw(SCREEN)
    player.update(userInput)

    if len(obstacles) == 0:
      if random.randint(0, 2) == 0:
          obstacles.append(Tombstone(TOMBSTONE))
      elif random.randint(0, 2) == 1:
          obstacles.append(Bats(BAT))
      elif random.randint(0, 2) == 2:
          obstacles.append(Zombo(ZOMBO))

    for obstacle in obstacles:
      obstacle.draw(SCREEN)
      obstacle.update()
      if player.w_rect.colliderect(obstacle.rect):
        death_count += 1
        pygame.time.delay(350)
        menu(death_count)

    background()

    score()

    clock.tick(30)
    pygame.display.update()

def menu(death_count):
  global points
  run = True
  while run:
    SCREEN.fill((255, 255, 255))
    font = pygame.font.Font('freesansbold.ttf', 30)

    if death_count == 0:
        text = font.render("Press any Key to Start", True, (0, 0, 0))
    elif death_count > 0:
        text = font.render("Press any Key to Restart", True, (0, 0, 0))
        score = font.render("Your Score: " + str(points), True, (0, 0, 0))
        scoreRect = score.get_rect()
        scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        SCREEN.blit(score, scoreRect)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    SCREEN.blit(text, textRect)
    SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = True
        if event.type == pygame.KEYDOWN:
            main()

menu(death_count=0)