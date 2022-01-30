import pygame

pygame.init()
pygame.display.set_mode([100, 100])
while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.KEYUP:
            print(event.key)
        elif event.type == pygame.QUIT:
            quit()
