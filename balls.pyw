"""Random number 1-9 of balls appears on the screen
User types the number and gets a response (correct or not)"""

w = 800
h = 600
radius = 15
stuffing = 10

#upper and lower bound for generation
l = 2
u = 9

#save high score
savehs = True

total = 20


import pygame, random, datetime, sys, pickle
from pygame.locals import *

pygame.init()
pygame.display.set_caption('balls')
pointsfont = pygame.font.SysFont("Arial Bold", 40)
titlefont = pygame.font.SysFont("Arial Bold Italic", 65)
ffont = pygame.font.SysFont("Arial", 25)

def geths():
    try:
        with open('score.dat', 'rb') as file:
            score = pickle.load(file)
    except:
        score = 0
    return score

def newhs(score):
    with open('score.dat', 'wb') as file:
        pickle.dump(score, file)
    return 0

def colcheck(a):
    hta = a[0]
    htb = a[1]
    r = a[2]
    if (htb[0] + r >= hta[0] + r >= htb[0] or htb[0] <= hta[0] <= htb[0] + r ) and (htb[1] + r >= hta[1] + r >= htb[1] or htb[1] <= hta[1] <= htb[1] + r):
            return True
    else:
        return False

def ballgen(w, h, r, st, num):

    l = [(None,None)] * num
    nums = []
    s = int(r+st)
    for i in range(len(l)):
        x = random.randint(0+s, w-s)
        y = random.randint(0+s, h-s)
        ht = (x-s, y-s)
        cols = map(colcheck, [(ht, (l[j][0] -s, l[j][1] -s), 2*s) for j in range(i)])
        while True in cols:
            x = random.randint(0+s, w-s)
            y = random.randint(0+s, h-s)
            ht = (x-s, y-s)
            cols = map(colcheck, [(ht, (l[j][0] -s, l[j][1] -s), 2*s) for j in range(i)])  
        l[i] = (x,y)
        nums.append(i)
     
    #print(l)
    return l, nums

display = pygame.display.set_mode((w,h))



#runtime status 0 = over; 1 = playing; 2 = beginning
status = 2

#start screen

while True:
    
    if status == 2:
        hs = 0
        display.fill((245, 245, 220))
        display.blit(display, (0,0))
        display.blit(titlefont.render('balls', True, (0,0,0)),(140,100))
        display.blit(ffont.render('count the number of balls on each screen as fast as possible', True, (0,0,0)),(140,150))
        display.blit(ffont.render('then press the corresponding number key', True, (0,0,0)),(140,200))
        display.blit(ffont.render('press anything to begin', True, (0,0,0)),(240,300))
        display.blit(ffont.render('save high score: %s (press h to toggle)' %('enabled' if savehs else 'disabled'), True, (0,0,0)),(140,400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_h:
                    savehs = 0 if savehs else 1
                    #pygame.display.update()
                else:
                    status = 1
                    nn = random.randint(l,u)
                    balls = ballgen(w,h,radius,stuffing, nn)
                    start = datetime.datetime.now()
                    score = 0
                    times = []
                    X = 0
        
    if status == 1:
        try:
            display.fill((245, 245, 220))
            display.blit(display, (0,0))
            
            #print(len(balls))
            for i in range(len(balls[0])):
                ball = balls[0][i]
                pygame.draw.circle(display,(0,0,0), (ball), radius)
                #label = myfont.render(str(balls[1][i]), 1, (255,0,0))
                #display.blit(label, (ball))
            
                
            
            
            ev = pygame.event.get()
            
            for event in ev:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    
                    if event.key == pygame.K_RETURN:
                        print(len(balls[1]))
                        continue

                    if event.key == pygame.K_r:
                        status = 2
                        
                    if pygame.K_2 <= event.key <= pygame.K_9:
                        attempt = event.key - pygame.K_0
                        kp = 1
                    elif pygame.K_KP2 <= event.key <= pygame.K_KP9:
                        attempt = event.key - pygame.K_KP0
                        kp = 1
                    else:
                        kp = 0
                        
                    if kp:
                        end = datetime.datetime.now()
                        e = end-start
                        
                        score += int(attempt==nn)
                        times.append(e.total_seconds())
                        
                        nn = random.randint(l,u)
                        balls = ballgen(w,h,radius,stuffing,nn)
                        start = datetime.datetime.now()
                        X += 1

                    
            pygame.display.update()
            if X>=total:
                    status = 0
        except pygame.error:
            break
                
    if status == 0:
            avg_time = float('%.3f' %(sum(times)/len(times)))
            accuracy = score / (total * (total-score)**2) if total-score else 1
            
            points = int(accuracy * (1/avg_time) * 10000)
            display.fill((245,245,220))
            display.blit(display, (0,0))
            display.blit(ffont.render('finished', True, (0,0,0)),(240,100))
            display.blit(ffont.render(('accuracy: %s/%s' % (score, total)), True, (0,0,0)),(240,150))
            display.blit(ffont.render(("average time: %s s" % avg_time), True, (0,0,0)),(240,200))
            display.blit(pointsfont.render(("total points: %s" % points), True, (0,0,0)),(240,250))
            if savehs:
                hs = 1 if geths()<points or hs==1 else 0
                if hs:
                    newhs(points)
                    display.blit(pointsfont.render(("new highscore: %s" % points), True, (0,0,0)),(240,300))
                else:
                    display.blit(ffont.render(("highscore: %s" % geths()), True, (0,0,0)),(240,300))
            display.blit(ffont.render('press enter to exit or R to restart', True, (0,0,0)),(240,400))
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        score = 0
                        times = []
                        X = 0
                        status = 2
                        
