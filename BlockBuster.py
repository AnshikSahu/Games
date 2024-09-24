import pygame
import random
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Hello World!')
score=0
time=60
level=1
font = pygame.font.Font(None, 36)
class Ball:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx=vx
        self.vy=vy
        self.moving=False
        self.tunnel=0

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 10, 0)

    def move(self):
        self.x += self.vx
        self.y += self.vy

        if self.x <= 10 or self.x >= 630:
            self.vx = -self.vx
        if self.y <= 10:
            self.vy = -self.vy
        if self.y >= 467:
            if(self.check_collision_with_board(board)):
                self.vy = -self.vy
                self.vx=1.05*abs(self.vy)*(ball.x-board.x-board.size/2)/(board.size/2)
            else:
                pygame.time.delay(1000)
                lost_game()

    def update(self):
        self.move()
        if(ball.tunnel>0):
            ball.tunnel-=0.1
        self.vx=self.vx*1.0001
        self.vy=self.vy*1.0001

    def check_collision_with_board(self, board):
        if self.x >= board.x-4 and self.x <= board.x + 4+board.size and self.y >= 467 and self.y <= 480:
            return True
        return False
    
class Board:
    def __init__(self, x):
        self.x = x
        self.size=75
        self.bullets_left=0

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, 465, self.size, 15), 0)
        if(self.bullets_left>0):
            pygame.draw.rect(screen, (0, 225, 225), (self.x, 460,5,5), 0)
            pygame.draw.rect(screen, (0, 225, 225), (self.x+self.size-5, 460,5,5), 0)

    def move(self, x):
        self.x += x

        if self.x <= 0:
            self.x = 0
        elif self.x >= 640-board.size:
            self.x = 640-board.size

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self,colour):
        if(colour==1):
            pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, 50, 20), 0)
        elif(colour==2):
            pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, 50, 20), 0)

    def check_collision_with_ball(self, ball):
        if ball.x >= self.x-4 and ball.x <= self.x + 54 and ball.y >= self.y-4 and ball.y <= self.y + 24:
            if(ball.tunnel==0):    
                if(ball.y<self.y or ball.y>self.y+20):
                    ball.vy=-ball.vy
                else:
                    ball.vx=-ball.vx
            if(blocks.remaining[blocks.blocks.index(self)]==1):
                r=random.randint(0,34)
                if(r==0):
                    drops.add_drop(self.x+25, self.y+10, 1)
                elif(r==5):
                    drops.add_drop(self.x+25, self.y+10, 2)
                elif(r==10):
                    drops.add_drop(self.x+25, self.y+10, 3)
                elif(r==15):
                    drops.add_drop(self.x+25, self.y+10, 4)
                elif(r==20):
                    drops.add_drop(self.x+25, self.y+10, 5)
                elif(r==25):
                    drops.add_drop(self.x+25, self.y+10, 6)
                elif(r==30):
                    drops.add_drop(self.x+25, self.y+10, 7)
            return True
        return False
    def check_collision_with_bullet(self):
        for bullet in bullets.bullets:
            if bullet.x >= self.x and bullet.x <= self.x + 50 and bullet.y >= self.y and bullet.y <= self.y + 20:
                bullets.remove_bullet(bullet)
                return True
        return False
    
class Blocks:
    def __init__(self):
        self.blocks=[]
        self.remaining=[]
        if(level==1):
            for i in range(0, 30):
                self.remaining.append(1)
                self.blocks.append(Block(20+60*(i%10), 60+30*(i//10)))
        elif(level==2):
            for i in range(0, 30):
                self.remaining.append(2)
                self.blocks.append(Block(20+60*(i%10), 60+30*(i//10)))
        else:
            win()

    def draw(self):
        for block in self.blocks:
            if self.remaining[self.blocks.index(block)]>0:
                block.draw(self.remaining[self.blocks.index(block)])

    def update(self, ball):
        global score
        for(i, block) in enumerate(self.blocks):
            if self.remaining[i]>0 and (block.check_collision_with_ball(ball) or block.check_collision_with_bullet()):
                score+=1
                self.remaining[i]-=1

    def all_blocks_destroyed(self):
        for i in self.remaining:
            if i>0:
                return False
        return True

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy=-2*abs(ball.vy)

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 2, 0)

    def move(self):
        self.y += self.vy

class Bullets:
    def __init__(self):
        self.bullets=[]

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()

    def update(self):
        for bullet in self.bullets:
            bullet.move()
            if(bullet.y<0):
                self.remove_bullet(bullet)

    def add_bullet(self, x, y):
        self.bullets.append(Bullet(x, y))

    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)

class Drop:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.vy=3

    def draw(self):
        if(self.type==1):
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 5, 0)
        elif(self.type==2):
            pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 5, 0)
        elif(self.type==3):
            pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 5, 0)
        elif(self.type==4):
            pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 5, 0)
        elif(self.type==5):
            pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 5, 0)
        elif(self.type==6):
            pygame.draw.circle(screen, (255, 0, 255), (self.x, self.y), 5, 0)
        elif(self.type==7):
            pygame.draw.circle(screen, (0, 255, 255), (self.x, self.y), 5, 0)

    def move(self):
        self.y += self.vy

    def check_collision_with_board(self, board):
        if self.x >= board.x-4 and self.x <= board.x + 4+board.size and self.y >= 467 and self.y <= 480:
            return True
        return False

    def effect(self):
        if(self.type==1):
            board.bullets_left+=5
        if(self.type==2):
            global time
            time+=5
        if(self.type==3):
            ball.tunnel=10
        if(self.type==4):
            board.size+=10
        if(self.type==5):
            board.size-=10
        if(self.type==6):
            lost_game()
        if(self.type==7):
            global score
            score+=10

class Drops:
    def __init__(self):
        self.drops=[]

    def draw(self):
        for drop in self.drops:
            drop.draw()

    def update(self):
        for drop in self.drops:
            drop.move()
            if(drop.check_collision_with_board(board)):
                drop.effect()
                self.remove_drop(drop)
            elif(drop.y>480):
                self.remove_drop(drop)

    def add_drop(self, x, y, type):
        self.drops.append(Drop(x, y, type))

    def remove_drop(self, drop):
        self.drops.remove(drop)

ball=Ball(357.5, 465, 5, 5)
board=Board(320)
blocks=Blocks()
bullets=Bullets()
drops=Drops()

def win():
    score+=time
    screen.fill((255, 255, 255))
    text = font.render("You win!", 1, (10, 10, 10))
    text2 = font.render("Your score is "+str(score), 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = 20
    screen.blit(text, textpos)
    screen.blit(text2, (textpos.centerx, textpos.centery+20))
    pygame.display.flip()
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()
    exit()

def time_up():
    screen.fill((255, 255, 255))
    text = font.render("Time's up!", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = 20
    screen.blit(text, textpos)
    pygame.display.flip()
    pygame.display.update()
    pygame.time.delay(2000)

def draw():
    screen.fill((255, 255, 255))
    ball.draw()
    board.draw()
    blocks.draw()
    bullets.draw()
    drops.draw()
    text = font.render("Score: "+str(score), 1, (10, 10, 10))
    text2 = font.render("Time: "+str(time), 1, (10, 10, 10))
    text3=font.render("Bullet: "+str(board.bullets_left), 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = 20
    text2pos = text2.get_rect()
    text2pos.centerx = screen.get_rect().centerx
    text2pos.centery = 40
    text3pos = text3.get_rect()
    text3pos.centerx = 60
    text3pos.centery = 20
    screen.blit(text, textpos)
    screen.blit(text2, text2pos)
    screen.blit(text3, text3pos)
    pygame.display.flip()
    pygame.display.update()

def level_up():
    global level
    global time
    global score
    global ball
    global board
    global blocks
    global bullets
    screen.fill((255, 255, 255))
    text = font.render("Level up!", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = 20
    screen.blit(text, textpos)
    pygame.display.flip()
    pygame.display.update()
    pygame.time.delay(2000)
    level+=1
    time=60
    score+=100
    ball=Ball(357.5, 465, 5, 5)
    board=Board(320)
    blocks=Blocks()
    bullets=Bullets()

def main():
    global score
    global time
    global ball
    global board
    global blocks
    iterations=0
    cool_down=0
    while time>0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            board.move(-10)
            if(not ball.moving):
                ball.x-=10
        elif keys[pygame.K_RIGHT]:
            board.move(10)
            if(not ball.moving):
                ball.x+=10
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()
        elif keys[pygame.K_SPACE] and cool_down==0:
            if(ball.moving and board.bullets_left>0):
                bullets.add_bullet(board.x, 465)
                bullets.add_bullet(board.x+board.size, 465)
                board.bullets_left-=1
            else:
                ball.moving=True
            cool_down=30
        if(ball.moving):
            ball.update()
        else:
            ball.x=ball.x+ball.vx
            if(ball.x<=board.x or ball.x>=board.x+board.size):
                ball.vx=-ball.vx
        blocks.update(ball)
        bullets.update()
        drops.update()
        if(blocks.all_blocks_destroyed()):
            level_up()
        if ball.check_collision_with_board(board):
            score+=1
        draw()
        pygame.time.delay(15)
        iterations+=1
        if cool_down>0:
            cool_down-=1
        if iterations%50==0:
            time-=1
    time_up()
    lost_game()

def reset():
    global score
    global time
    global ball
    global board
    global blocks
    global level
    global bullets
    global drops

    score=0
    time=60
    level=1
    ball=Ball(357.5, 465, 5, 5)
    board=Board(320)
    blocks=Blocks()
    drops=Drops()
    bullets=Bullets()
    draw()
    main()

def lost_game():
    screen.fill((255, 255, 255))
    #Game Over
    text = font.render("Game Over", 1, (10, 10, 10))
    text2 = font.render("Score: "+str(score), 1, (10, 10, 10))
    text3=font.render("Press Space to Restart", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    textpos.centery = 20
    text2pos = text2.get_rect()
    text2pos.centerx = screen.get_rect().centerx
    text2pos.centery = 40
    text3pos = text3.get_rect()
    text3pos.centerx = screen.get_rect().centerx
    text3pos.centery = 60
    screen.blit(text, textpos)
    screen.blit(text2, text2pos)
    screen.blit(text3, text3pos)
    pygame.display.flip()
    t=0
    while t<1000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            keys=pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                exit()
            elif keys[pygame.K_SPACE]:
                    reset()
        pygame.time.delay(10)
        t+=1
    exit()
        
main()

# pygame.init()

# screen = pygame.display.set_mode((640, 480))
# pygame.display.set_caption('Hello World!')
# screen.fill((255, 255, 255))
# pygame.display.flip()

# blocks=[True]*30
# blocks_x=[20+i*60 for i in range(10)]+[20+i*60 for i in range(10)]+[20+i*60 for i in range(10)]
# blocks_y=[50]*10+[80]*10+[110]*10
# for i in range(30):
#     pygame.draw.rect(screen, (0, 0, 0), (blocks_x[i], blocks_y[i], 50, 20), 0)

# x=320
# time=30
# iterations=0
# y=240
# vx=5
# vy=5
# bullet=False
# bullet_x=0
# bullet_y=0
# speed=5
# board_x=320
# score=0
# pygame.draw.rect(screen, (255, 0, 0), (board_x, 465,5,5), 0)
# pygame.draw.rect(screen, (255, 0, 0), (board_x+70, 465,5,5), 0)
# pygame.draw.circle(screen, (0, 0, 255), (x, y), 10, 0)
# pygame.draw.rect(screen, (0, 0, 255), (board_x, 470, 75, 10), 0)
# font = pygame.font.Font(None, 36)
# text = font.render("Score: "+str(score), 1, (10, 10, 10))
# text2=font.render("Time: "+str(time), 1, (10, 10, 10))
# textpos = text.get_rect()
# textpos.centerx = screen.get_rect().centerx
# textpos.centery = 20
# text2pos = text2.get_rect()
# text2pos.centerx = screen.get_rect().centerx
# text2pos.centery = 40
# screen.blit(text, textpos)
# pygame.display.update()
# while True:
#     iterations=iterations+1
#     if(time==0):
#         screen.fill((255, 255, 255))
#         #Game Over
#         text = font.render("Game Over", 1, (10, 10, 10))
#         text2 = font.render("Score: "+str(score), 1, (10, 10, 10))
#         text3=font.render("Press Space to Restart", 1, (10, 10, 10))
#         textpos = text.get_rect()
#         textpos2 = text2.get_rect()
#         textpos3 = text3.get_rect()
#         textpos.centerx = screen.get_rect().centerx
#         textpos.centery = screen.get_rect().centery
#         textpos2.centerx = screen.get_rect().centerx
#         textpos2.centery = screen.get_rect().centery+50
#         textpos3.centerx = screen.get_rect().centerx
#         textpos3.centery = screen.get_rect().centery+100
#         screen.blit(text, textpos)
#         screen.blit(text2, textpos2)
#         screen.blit(text3, textpos3)
#         pygame.display.update()
#         restart=False
#         for i in range(100):
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     exit()
#                 keys = pygame.key.get_pressed()
#                 if keys[pygame.K_SPACE]:
#                     restart=True
#                     break
#             if restart:
#                 break
#             pygame.time.delay(20)
#         if restart:
#             x=320
#             y=240
#             vx=3
#             vy=3
#             time=15
#             board_x=320
#             score=0
#             for i in range(30):
#                 blocks[i]=True
#             pygame.draw.circle(screen, (0, 0, 255), (x, y), 10, 0)
#             pygame.draw.rect(screen, (0, 0, 255), (board_x, 470, 75, 10), 0)
#             text = font.render("Score: "+str(score), 1, (10, 10, 10))
#             textpos = text.get_rect()
#             textpos.centerx = screen.get_rect().centerx
#             textpos.centery = 20
#             screen.blit(text, textpos)
#             pygame.display.update()
#             continue
#         break
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT]:
#         board_x=board_x-10
#         if board_x<0:
#             board_x=0
#     elif keys[pygame.K_RIGHT]:
#         board_x=board_x+10
#         if board_x>565:
#             board_x=565
#     elif keys[pygame.K_ESCAPE]:
#         pygame.quit()
#         exit()
#     elif keys[pygame.K_SPACE]:
#         if not bullet:
#             bullet=True
#             bullet_x=board_x+ 2.5
#             bullet_y=465
#     x=x+vx
#     y=y+vy
#     win=True
#     for i in range(30):
#         if blocks[i]:
#             win=False
#             break
#     if win:
#         screen.fill((255, 255, 255))
#         #Game Over
#         text = font.render("You Win", 1, (10, 10, 10))
#         text2 = font.render("Score: "+str(score), 1, (10, 10, 10))
#         text3=font.render("Press Space to Restart", 1, (10, 10, 10))
#         textpos = text.get_rect()
#         textpos2 = text2.get_rect()
#         textpos3 = text3.get_rect()
#         textpos.centerx = screen.get_rect().centerx
#         textpos.centery = screen.get_rect().centery
#         textpos2.centerx = screen.get_rect().centerx
#         textpos2.centery = screen.get_rect().centery+50
#         textpos3.centerx = screen.get_rect().centerx
#         textpos3.centery = screen.get_rect().centery+100
#         screen.blit(text, textpos)
#         screen.blit(text2, textpos2)
#         screen.blit(text3, textpos3)
#         pygame.display.update()
#         restart=False
#         for i in range(100):
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     exit()
#                 keys = pygame.key.get_pressed()
#                 if keys[pygame.K_SPACE]:
#                     restart=True
#                     break
#             if restart:
#                 break
#             pygame.time.delay(20)
#         if restart:
#             x=320
#             y=240
#             vx=3
#             vy=3
#             time=15
#             board_x=320
#             score=0
#             for i in range(30):
#                 blocks[i]=True
#             pygame.draw.circle(screen, (0, 0, 255), (x, y), 10, 0)
#             pygame.draw.rect(screen, (0, 0, 255), (board_x, 470, 75, 10), 0)
#             text = font.render("Score: "+str(score), 1, (10, 10, 10))
#             textpos = text.get_rect()
#             textpos.centerx = screen.get_rect().centerx
#             textpos.centery = 20
#             screen.blit(text, textpos)
#             pygame.display.update()
#             continue
#         break
#     if x>640:
#         vx=-1*vx
#         x=640
#     elif x<0:
#         vx=-1*vx
#         x=0
#     if y>465:
#         if x>board_x-4 and x<board_x+75+4:
#             score=score+1
#             # r=abs(x-(board_x+37.5))/37.5
#             # vy=-1*2*speed * (1-r)
#             # if(vx>0):
#             #     vx=2*speed * r
#             # else:
#             #     vx=-2*speed * r
#             vy=-1*vy
#             vx=speed*(x-(board_x+37.5))/37.5
#             y=465
#         else:
#             screen.fill((255, 255, 255))
#             #Game Over
#             text = font.render("Game Over", 1, (10, 10, 10))
#             text2 = font.render("Score: "+str(score), 1, (10, 10, 10))
#             text3=font.render("Press Space to Restart", 1, (10, 10, 10))
#             textpos = text.get_rect()
#             textpos2 = text2.get_rect()
#             textpos3 = text3.get_rect()
#             textpos.centerx = screen.get_rect().centerx
#             textpos.centery = screen.get_rect().centery
#             textpos2.centerx = screen.get_rect().centerx
#             textpos2.centery = screen.get_rect().centery+50
#             textpos3.centerx = screen.get_rect().centerx
#             textpos3.centery = screen.get_rect().centery+100
#             screen.blit(text, textpos)
#             screen.blit(text2, textpos2)
#             screen.blit(text3, textpos3)
#             pygame.display.update()
#             restart=False
#             for i in range(100):
#                 for event in pygame.event.get():
#                     if event.type == pygame.QUIT:
#                         pygame.quit()
#                         exit()
#                     keys = pygame.key.get_pressed()
#                     if keys[pygame.K_SPACE]:
#                         restart=True
#                         break
#                 if restart:
#                     break
#                 pygame.time.delay(20)
#             if restart:
#                 x=320
#                 y=240
#                 vx=3
#                 vy=3
#                 time=15
#                 board_x=320
#                 score=0
#                 for i in range(30):
#                     blocks[i]=True
#                 pygame.draw.circle(screen, (0, 0, 255), (x, y), 10, 0)
#                 pygame.draw.rect(screen, (0, 0, 255), (board_x, 470, 75, 10), 0)
#                 text = font.render("Score: "+str(score), 1, (10, 10, 10))
#                 textpos = text.get_rect()
#                 textpos.centerx = screen.get_rect().centerx
#                 textpos.centery = 20
#                 screen.blit(text, textpos)
#                 pygame.display.update()
#                 continue
#             break
#     elif y<0:
#         vy=-1*vy
#         y=0
#     for i in range(30):
#         if blocks[i]:
#             if x>blocks_x[i]-4 and x<blocks_x[i]+50+4 and y>blocks_y[i]-4 and y<blocks_y[i]+20+4:
#                 score=score+5
#                 if(y<50 or y>60):vy=-1*vy
#                 else: vx=-1*vx
#                 blocks[i]=False
#         if(bullet):
#             if blocks[i] and bullet_x>blocks_x[i]-2 and bullet_x<blocks_x[i]+50+2 and bullet_y>blocks_y[i]-2 and bullet_y<blocks_y[i]+20+2:
#                     score=score+5
#                     blocks[i]=False
#                     bullet=False
#             # else:
#             #     if(i%10<=7):
#             #         if blocks[i+2] and bullet_x+70>blocks_x[i+2]-2 and bullet_x+70<blocks_x[i+2]+50+2 and bullet_y>blocks_y[i+2]-2 and bullet_y<blocks_y[i+2]+20+2:
#             #             blocks[i+2]=False
#             #             score=score+5
#             #             bullet=False
#             #             break
#             if(i%10<=8):
#                 if blocks[i+1] and bullet_x+70>blocks_x[i+1]-2 and bullet_x+70<blocks_x[i+1]+50+2 and bullet_y>blocks_y[i+1]-2 and bullet_y<blocks_y[i+1]+20+2:
#                     blocks[i+1]=False
#                     score=score+5
#                     bullet=False
#                     break

#     vx=vx*1.0001
#     vy=vy*1.0001
#     speed=speed*1.0001
#     screen.fill((255, 255, 255))
#     for i in range(30):
#         if blocks[i]:
#             pygame.draw.rect(screen, (0, 0, 0), (blocks_x[i], blocks_y[i], 50, 20), 0)
#     if bullet:
#         pygame.draw.circle(screen, (255, 0, 0), (bullet_x, bullet_y), 2, 0)
#         pygame.draw.circle(screen, (255, 0, 0), (bullet_x+70, bullet_y), 2, 0)
#         bullet_y=bullet_y-10
#         if bullet_y<0:
#             bullet=False
#     pygame.draw.rect(screen, (255, 0, 0), (board_x, 465,5,5), 0)
#     pygame.draw.rect(screen, (255, 0, 0), (board_x+70, 465,5,5), 0)
#     pygame.draw.circle(screen, (0, 0, 255), (x, y), 10, 0)
#     pygame.draw.rect(screen, (0, 0, 255), (board_x, 470, 75, 10), 0)
#     text = font.render("Score: "+str(score), 1, (10, 10, 10))
#     text2=font.render("Time: "+str(time), 1, (10, 10, 10))
#     screen.blit(text, textpos)
#     screen.blit(text2, text2pos)
#     pygame.display.update()
#     pygame.time.delay(20)
#     if iterations%50==0:
#         time=time-1
#         iterations=0
# pygame.quit()
# exit()