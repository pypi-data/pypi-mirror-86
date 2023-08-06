import pygame

pygame.init()

display_larg = 600
display_comp = 480
Display = pygame.display.set_mode((display_larg, display_comp))
pygame.display.set_caption("Dumbdan's Game")
clock = pygame.time.Clock()
crashed = False

black = (0,0,0)
white = (255, 255, 255)

character_img = pygame.image.load("media/character.png")

def character(x,y):
    Display.blit(character_img, (x,y))

x = (display_larg * 0.45)
y = (display_comp * 0.8)
x_change =  0 
char_speed = 0

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            x_change = -5

        elif event.key == pygame.K_RIGHT:
            x_change = 5

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            x_change = 0 

    Display.fill(white)
    character(x,y)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
