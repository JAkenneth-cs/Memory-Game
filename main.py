import pygame
import sys
import random

def draw_text(surface, text, font, color, x, y):
    """Helper function to draw text and return its rect"""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
    return text_rect

def main():
    # Initialize Pygame
    pygame.init()
    
    # Constants
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wrong Side Up")
    clock = pygame.time.Clock()
    
    # Fonts
    font_path = "game-assets/fonts/LondrinaSolid-Black.ttf"
    try:
        title_font = pygame.font.Font(font_path, 90)  # Larger for the title
        menu_font = pygame.font.Font(font_path, 50)
    except Exception as e:
        print(f"Warning: Could not load custom font ({e}), falling back to default.")
        title_font = pygame.font.Font(None, 90)
        menu_font = pygame.font.Font(None, 50)
        
    # State Machine
    state = "MAIN_MENU"
    
    # Colors
    WHITE = (255, 255, 255)
    GRAY = (180, 180, 180)
    BLACK = (0, 0, 0)
    BG_BASE_COLOR = (20, 60, 20)  # Dark green texture placeholder
    
    # Placeholder Lightbulb properties
    bulb_x, bulb_y = 550, 250
    base_glow_radius = 120
    
    # Main game loop
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_clicked = True
                    
        # ---------------------------------------------------------
        # STATE: MAIN MENU
        # ---------------------------------------------------------
        if state == "MAIN_MENU":
            # 1. Flickering Logic
            # Randomly determine if the light is faltering this frame
            flicker_val = random.randint(0, 100)
            is_flickering = flicker_val > 90  # 10% chance to dim heavily
            
            if is_flickering:
                bg_color = (10, 30, 10) # Much darker background
                glow_alpha = random.randint(20, 80)
                glow_radius = base_glow_radius - random.randint(20, 40)
            else:
                bg_color = BG_BASE_COLOR
                # Subtle normal pulsing
                glow_alpha = random.randint(150, 200)
                glow_radius = base_glow_radius + random.randint(-5, 5)
                
            screen.fill(bg_color)
            
            # 2. Draw Placeholder Lightbulb
            # Wire/String
            pygame.draw.line(screen, (10,10,10), (bulb_x, 0), (bulb_x, bulb_y - 20), 4)
            # Base of the bulb
            pygame.draw.rect(screen, (30,30,30), (bulb_x - 15, bulb_y - 30, 30, 20))
            
            # Draw the Glow (requires a surface with alpha)
            glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            # A soft greenish-yellow glow
            pygame.draw.circle(glow_surface, (200, 255, 150, glow_alpha), (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, (bulb_x - glow_radius, bulb_y - glow_radius))
            
            # Draw actual bulb (white circle)
            bulb_color = (200, 255, 200) if is_flickering else (240, 255, 240)
            pygame.draw.circle(screen, bulb_color, (bulb_x, bulb_y), 25)
            
            # 3. Draw Menu UI
            # Title
            draw_text(screen, "Wrong Side Up", title_font, WHITE, 50, 100)
            
            # Menu Options
            menu_items = ["Play", "How to play", "Quit"]
            start_y = 250
            
            for i, item in enumerate(menu_items):
                item_y = start_y + (i * 80)
                
                # Check for hover
                temp_rect = menu_font.render(item, True, WHITE).get_rect(topleft=(50, item_y))
                is_hovered = temp_rect.collidepoint(mouse_pos)
                
                # Apply hover effects (color change and slight shift to the right)
                color = WHITE if is_hovered else GRAY
                x_pos = 70 if is_hovered else 50
                
                rect = draw_text(screen, item, menu_font, color, x_pos, item_y)
                
                # Handle click
                if is_hovered and mouse_clicked:
                    if item == "Play":
                        state = "PLAYING"
                    elif item == "How to play":
                        state = "HOW_TO_PLAY"
                    elif item == "Quit":
                        running = False
                        
        # ---------------------------------------------------------
        # STATE: PLAYING (Placeholder)
        # ---------------------------------------------------------
        elif state == "PLAYING":
            screen.fill((30, 30, 30))
            draw_text(screen, "Game Phase Placeholder", menu_font, WHITE, 50, HEIGHT//2 - 40)
            draw_text(screen, "Press ESC to return to Menu", menu_font, GRAY, 50, HEIGHT//2 + 20)
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                state = "MAIN_MENU"
                
        # ---------------------------------------------------------
        # STATE: HOW TO PLAY (Placeholder)
        # ---------------------------------------------------------
        elif state == "HOW_TO_PLAY":
            screen.fill((20, 20, 40))
            draw_text(screen, "How to Play Instructions", menu_font, WHITE, 50, HEIGHT//2 - 40)
            draw_text(screen, "Press ESC to return to Menu", menu_font, GRAY, 50, HEIGHT//2 + 20)
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                state = "MAIN_MENU"

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
