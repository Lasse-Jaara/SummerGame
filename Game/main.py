import pygame
import os
import random
from enemy import Mossya
from xp import Xp_Orb
# === Initialization ===
pygame.init()
pygame.font.init
pygame.mixer.init()
pygame.mouse.set_visible(False)

# === Constants ===
FPS = 60
WIDTH, HEIGHT = 900, 500
SPAWN_EVENT = pygame.USEREVENT + 1
TIMER_EVENT = pygame.USEREVENT + 2

# === Window ===
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Get the absolute path to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(script_dir, 'Assets')
# === Assets ===
player_img = pygame.image.load(os.path.join(assets_dir, 'cursor.png'))
player_attack_img = pygame.image.load(os.path.join(assets_dir, 'cursor_clicked.png'))
castle_img = pygame.image.load(os.path.join(assets_dir, 'background.png'))
cursor_click_sound = pygame.mixer.Sound(os.path.join(assets_dir, 'SD_cursor_clicked.wav'))
cursor_click_sound.set_volume(0.4)
round_sound = pygame.mixer.Sound(os.path.join(assets_dir, 'round.mp3'))
card_select_sound = pygame.mixer.Sound(os.path.join(assets_dir, 'Card_select.mp3'))
card_press_sound = pygame.mixer.Sound(os.path.join(assets_dir, 'card_press.mp3'))
card_press_sound.set_volume(0.4)
orginal_upgrade_cursor_size_img = pygame.image.load(os.path.join(assets_dir, 'cursor_size_upgrade.png'))
upgrade_cursor_size_img_width, upgrade_cursor_size_img_height = orginal_upgrade_cursor_size_img.get_size()
upgrade_cursor_size_img = pygame.transform.scale(orginal_upgrade_cursor_size_img, (upgrade_cursor_size_img_width * 3, upgrade_cursor_size_img_height * 3))
# Load the font
font_path = os.path.join(assets_dir, 'ARCADECLASSIC.TTF')
font = pygame.font.Font(font_path, 36)
font_small = pygame.font.Font(font_path, 28)
font_tiny = pygame.font.Font(font_path, 20)
font_large = pygame.font.Font(font_path, 42)
# === others ===
enemy_list = []
xp_list = []
spawn_time = 5
time = 2.5
pygame.time.set_timer(SPAWN_EVENT, round(spawn_time * 1000))
pygame.time.set_timer(TIMER_EVENT, round(time * 1000))
spawn_x_min = 30
spawn_x_max = WIDTH - 30
spawn_y_min = 10
spawn_y_max = HEIGHT - 400
xp_collected = 0
paused = False
screenshot = window.copy()
hovered_card1 = False
hovered_card2 = False
cursor_multiplier = 1

def draw_window(mouse_pos, left_click, Hp_text, Round_text,mouse_rect):
    #Draws the background, enemies, and player cursor each frame
    window.fill((255, 255, 255))
    window.blit(castle_img, (0, 0))
    # Texts
    #window.blit(Healt_text, (WIDTH//2, HEIGHT-45))
    # Healt
    Healt_text = font.render(Hp_text, True, (0, 0, 0))
    text_rect = Healt_text.get_rect()
    text_rect.centerx = WIDTH // 2
    text_rect.y = HEIGHT - text_rect.height
    window.blit(Healt_text, text_rect)
    # Rounds
    Rounds_text = font.render(Round_text, True, (0, 0, 0))
    text_rect = Rounds_text.get_rect()
    text_rect.centerx = WIDTH // 2
    text_rect.y = 65 - text_rect.height
    window.blit(Rounds_text, text_rect)
    # XP
    global xp_collected
    level_multiplier = 20
    xp_bar_rect = pygame.Rect(0, 0, round((xp_collected*level_multiplier)), 30)    # WIDTH = 900
    pygame.draw.rect(window, (0, 0, 0), xp_bar_rect)  # Fill for xp bar
    # XP Border
    xp_bar_border_rect = pygame.Rect(0, 0, WIDTH, 30) 
    pygame.draw.rect(window, (0, 0, 0), xp_bar_border_rect, 1) # draw border for xp bar
    # XP bar level up/reset
    if xp_bar_rect.width >= WIDTH:
        xp_collected = 0
        global paused
        paused = True

    # Handle enemy clicks and draw them
    for enemy in enemy_list[:]:
        if enemy.pygame_rect.colliderect(mouse_rect) and left_click:
            enemy.take_damage(10)
        if enemy.health <= 0:
            if enemy.died_to_castle == False:
                spawn_xp((random.randint(1, 5)), enemy.pygame_rect.x, enemy.pygame_rect.y)
            enemy_list.remove(enemy) # enemy dies
    
    for enemy in enemy_list:
        enemy.draw(window)

    for orb in xp_list[:]:
        if orb.pygame_rect.colliderect(mouse_rect):
            orb.sound()
            xp_list.remove(orb)
            xp_collected += 1
    for orb in xp_list:
        orb.draw(window)
    
    # main mouse
    if left_click:
        cursor_img = player_attack_img
        cursor_click_sound.play()
    else:
        cursor_img = player_img    

    cursor_img_width, cursor_img_height = cursor_img.get_size()

    bigger_cursor_img = pygame.transform.scale(cursor_img, 
    (int(cursor_img_width * cursor_multiplier), int(cursor_img_height * cursor_multiplier)))
    
    window.blit(bigger_cursor_img, 
    (mouse_pos[0] - bigger_cursor_img.get_width() // 2, 
     mouse_pos[1] - bigger_cursor_img.get_height() // 2))
    #pygame.draw.rect(window, (255, 0, 255), mouse_rect, 2)
    #pygame.draw.rect(window, (255, 0, 255), mouse_pos.get_rect(), 2)

    # == Debug visuals ==
    # rect = pygame.Rect(x, y, width, height)
    #castle_rect = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)
    #castle_tower_left_rect = pygame.Rect(0, HEIGHT - 90, 90, 90)
    #castle_tower_right_rect = pygame.Rect(WIDTH-90, HEIGHT - 90, 90, 90)

    #pygame.draw.rect(window, (255, 0, 255), castle_tower_left_rect, 2)
    #pygame.draw.rect(window, (255, 0, 255), castle_tower_right_rect, 2)
    #pygame.draw.rect(window, (255, 0, 0), castle_rect, 2)
    global screenshot
    pygame.display.flip()
    
    screenshot = window.copy()

def spawn_xp(count, enemy_x, enemy_y, min_range=15):
    spawn_range = 30
    for _ in range(count):
        while True:
            x = random.randint(enemy_x - spawn_range, enemy_x + spawn_range)
            y = random.randint(enemy_y - spawn_range, enemy_y + spawn_range)
            # checks if the new x and y are larger than old enemy_x and enemy_y.
            if abs(x - enemy_x) > min_range and abs(y - enemy_y) > min_range: # abs makes number have positive value. Like: abs(-5) -> 5 , abs(5) -> 5
                break
        xp = Xp_Orb(pygame_rect=pygame.Rect(x, y, 25, 25))
        xp_list.append(xp)

def spawn_enemy(count):
    #Spawns a specified number of enemies at random positions
    for _ in range(count):
        x = random.randint(spawn_x_min, spawn_x_max)
        y = random.randint(spawn_y_min, spawn_y_max)
        enemy = Mossya(pygame_rect=pygame.Rect(x, y, 25, 25))
        enemy_list.append(enemy)

def draw_upgrade_screen(left_click,mouse_pos,timer,can_upgrade_size):
    # background blur
    global screenshot
    global hovered_card1
    global hovered_card2
    global cursor_multiplier
    global paused
    blurriness = 0.9
    small = pygame.transform.smoothscale(screenshot, (WIDTH // 16*blurriness, HEIGHT // 16*blurriness))
    blurred = pygame.transform.smoothscale(small, (WIDTH, HEIGHT))
    #window.fill((1, 1, 1))  # dark background
    window.blit(blurred, (0, 0))

    # Card settings
    card_width = 200
    card_height = 300
    spacing = 50
    border_radius = 12
    border_thickness = 3

    # Colors
    fill_color = (255, 255, 255)         # Black inside
    outline_color = (0, 0, 0)  # White border
    # Position
    y = HEIGHT // 2 - card_height // 2
    x1 = WIDTH // 2 - card_width - spacing // 2
    x2 = WIDTH // 2 + spacing // 2

    # Draw Cards
    card1_rect = pygame.Rect(x1, y, card_width, card_height)
    pygame.draw.rect(window, fill_color, card1_rect, border_radius=border_radius)

    card2_rect = pygame.Rect(x2, y, card_width, card_height)
    pygame.draw.rect(window, fill_color, card2_rect, border_radius=border_radius)

    if card1_rect.collidepoint(mouse_pos):
        pygame.draw.rect(window, outline_color, card1_rect, width=border_thickness+1, border_radius=border_radius+20)
        if not hovered_card1:
            #print("hovered card1")
            card_select_sound.play()
            hovered_card1 = True     
    else:
        pygame.draw.rect(window, outline_color, card1_rect, width=border_thickness, border_radius=border_radius)
        hovered_card1 = False  # Reset when mouse leaves
    if card2_rect.collidepoint(mouse_pos):
        pygame.draw.rect(window, outline_color, card2_rect, width=border_thickness+1, border_radius=border_radius+20)
        if not hovered_card2:
            #print("hovered card1")
            card_select_sound.play()
            hovered_card2 = True  
    else:
        pygame.draw.rect(window, outline_color, card2_rect, width=border_thickness, border_radius=border_radius)
        hovered_card2 = False  # Reset when mouse leaves
        
    # Upgrade choise img
    window.blit(
        upgrade_cursor_size_img,
        (
            card1_rect.x + card1_rect.width // 2 - upgrade_cursor_size_img.get_width() // 2,
            card1_rect.centery - upgrade_cursor_size_img.get_height() // 2 - 75
        )
    )
    # main mouse
    if left_click:
        cursor_img = player_attack_img
        cursor_click_sound.play()
    else:
        cursor_img = player_img    

    cursor_img_width, cursor_img_height = cursor_img.get_size()

    bigger_cursor_img = pygame.transform.scale(cursor_img, 
    (int(cursor_img_width * cursor_multiplier), int(cursor_img_height * cursor_multiplier)))
    
    window.blit(bigger_cursor_img, 
    (mouse_pos[0] - bigger_cursor_img.get_width() // 2, 
     mouse_pos[1] - bigger_cursor_img.get_height() // 2))
    
    if timer: # I know this isint so good structure >:
        text = font_large.render("Choose upgrade!", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = WIDTH // 2
        text_rect.y = 65 - text_rect.height
        pygame.draw.rect(window, (255, 255, 255), text_rect)
        window.blit(text, text_rect)
    else:
        text = font_large.render("Choose upgrade", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = WIDTH // 2
        text_rect.y = 65 - text_rect.height
        pygame.draw.rect(window, (0, 0, 0), text_rect)
        window.blit(text, text_rect)

    if cursor_multiplier >= 16:
        can_upgrade_size = False
    #print(cursor_multiplier)
    # Render text
    text = font_small.render("Cursor size", True, (0, 0, 0))
    text_rect = text.get_rect()
    # Center text horizontally aligned with the image
    text_rect.centerx = card1_rect.x + card1_rect.width // 2
    # Position text just below the image with a small margin (e.g., 5 pixels)
    image_bottom_y = (card1_rect.centery - upgrade_cursor_size_img.get_height() // 2 - 75) + upgrade_cursor_size_img.get_height()
    text_rect.top = image_bottom_y + 5

    window.blit(text, text_rect)

    if can_upgrade_size:
        text = font_tiny.render("100 percent bigger", True, (0, 0, 0))
    else:
        text = font_tiny.render("Max out", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = card1_rect.x + card1_rect.width // 2
    image_bottom_y = (card1_rect.centery - upgrade_cursor_size_img.get_height() // 2 - 75) + upgrade_cursor_size_img.get_height()
    text_rect.top = image_bottom_y + text_rect.height + 5

    window.blit(text, text_rect)
    
    if card1_rect.collidepoint(mouse_pos) and left_click:
        #print("cliked card1_rect")
        card_press_sound.play()
        if can_upgrade_size:
            cursor_multiplier *= 2.0
        paused = False
    if card2_rect.collidepoint(mouse_pos) and left_click:
        print("cliked card2_rect - un used for now")
        #card_press_sound.play()

    pygame.display.flip()

def main():
    #Main game loop
    global spawn_time
    clock = pygame.time.Clock()
    running = True
    global paused
    global cursor_multiplier
    enemy_count = 2
    spawned_round = 0
    castle_hp = 100
    Hp = 100
    Hp_text = "Healt " + str(Hp)
    end = False
    timer = False
    can_upgrade_size = True
    while running:

        if paused: # Paused/level-up game loop
            pygame.display.set_caption("LevepUp")
            clock.tick(FPS)
            left_click = False
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        left_click = True
                elif event.type == TIMER_EVENT:
                    if timer:
                        timer = False
                    else:
                        timer = True
                    round_sound.play()
            draw_upgrade_screen(left_click,mouse_pos,timer,can_upgrade_size)

        else: # Normal game loop
            pygame.display.set_caption("SummerGame")
            clock.tick(FPS)
            left_click = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(0, 0, 12*cursor_multiplier, 12*cursor_multiplier) 
            mouse_rect.center = mouse_pos

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        left_click = True
                elif event.type == SPAWN_EVENT:
                    if len(enemy_list) < enemy_count:
                        round_sound.play()
                        spawned_round += 1
                        spawn_enemy(round(enemy_count))
                        enemy_count += enemy_count * 0.25
                        spawn_time += spawn_time * 0.15
                # Debug
                #elif event.type == pygame.KEYDOWN:
                    #if event.key == pygame.K_m:
                        #spawn_xp(20,WIDTH//2,HEIGHT//2)
                        #print("M key was pressed")
            # rect = pygame.Rect(x, y, width, height)
            castle_rect = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)
            castle_tower_left_rect = pygame.Rect(0, HEIGHT - 90, 90, 90)
            castle_tower_right_rect = pygame.Rect(WIDTH-90, HEIGHT - 90, 90, 90)
            for enemy in enemy_list:
                enemy_rect = enemy.pygame_rect
                if (not castle_rect.colliderect(enemy_rect) and
                    not castle_tower_left_rect.colliderect(enemy_rect) and
                    not castle_tower_right_rect.colliderect(enemy_rect)):
                    enemy.move()
                else:
                    enemy.die_to_castle()
                    if Hp <= 0:
                        end = True
                    Hp -= 10
            if end:
                break
            Hp_text = "Healt " + str(Hp)
            Round_text = "Round " + str(spawned_round)
            draw_window(mouse_pos, left_click, Hp_text, Round_text,mouse_rect)
            if castle_hp <= 0:
                break
    pygame.quit()


if __name__ == "__main__":
    main()
