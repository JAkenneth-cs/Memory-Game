import pygame
import sys

def main():
    # Initialize Pygame
    pygame.init()
    
    # Constants
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Memory Game - Pygame Edition")
    clock = pygame.time.Clock()
    
    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Fill background
        screen.fill((30, 30, 30))  # Dark gray background
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
