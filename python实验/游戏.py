import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1200, 790))
pygame.display.set_caption("飞船射击游戏")

clock = pygame.time.Clock()

# 图片
alien_image = pygame.image.load('D:/python实验/alien.png')
ship_image = pygame.image.load('D:/python实验/ship.png')
bullet_image = pygame.image.load('D:/python实验/bullet.png')
star_image = pygame.image.load('D:/python实验/star.png')

ship_rect = ship_image.get_rect()
ship_rect.left = 0
ship_rect.centery = screen.get_rect().centery
ship_speed = 8
ship_movement_x = 0
ship_movement_y = 0

alien_rect = alien_image.get_rect()
alien_speed = 2
aliens = []
alien_spawn_timer = 100

bullet_rect = bullet_image.get_rect()
bullet_speed = 20
bullets = []

score = 0
level = 1
font = pygame.font.Font(None, 36)

# 添加Play按钮
play_button = pygame.Rect(300, 650, 200, 100)  # 按钮的位置和大小
newgame_button = pygame.Rect(300, 650, 200, 100)  # 新游戏按钮的位置和大小
exit_button = pygame.Rect(750, 650, 200, 100)  # 退出按钮的位置和大小
game_over = False

def draw_play_button():
    pygame.draw.rect(screen, (0, 255, 0), play_button)  # 绘制白色矩形作为按钮
    font = pygame.font.Font(None, 36)  # 设置字体和大小
    text = font.render("play", True, (0, 0, 0))  # 渲染文字
    text_rect = text.get_rect(center=play_button.center)  # 设置文字位置为按钮中心
    screen.blit(text, text_rect)  # 绘制文字

def draw_newgame_button():
    pygame.draw.rect(screen, (0, 255, 0), newgame_button)  # 绘制白色矩形作为按钮
    font = pygame.font.Font(None, 36)  # 设置字体和大小
    text = font.render("newgame", True, (0, 0, 0))  # 渲染文字
    text_rect = text.get_rect(center=newgame_button.center)  # 设置文字位置为按钮中心
    screen.blit(text, text_rect)  # 绘制文字

def draw_exit_button():
    pygame.draw.rect(screen, (0, 255, 0), exit_button)  # 绘制白色矩形作为按钮
    font = pygame.font.Font(None, 36)  # 设置字体和大小
    text = font.render("exit", True, (0, 0, 0))  # 渲染文字
    text_rect = text.get_rect(center=exit_button.center)  # 设置文字位置为按钮中心
    screen.blit(text, text_rect)  # 绘制文字

# 保存最高分到文件
def save_high_score(score):
    with open('high_score.txt', 'w') as file:
        file.write(str(score))

# 读取最高分
def load_high_score():
    try:
        with open('high_score.txt', 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def generate_stars():
    stars = []
    while len(stars) < 30:
        star = (random.randint(0, 1200 - star_image.get_width()), 
                random.randint(0, 790 - star_image.get_height()))
        if star not in stars:
            stars.append(star)
    return stars

# Generate stars
stars = generate_stars()

def spawn_alien():
    for _ in range(3): 
        alien = alien_rect.copy()
        alien.y = random.randint(0, 790 - alien_rect.height)
        alien.x = 1200
        aliens.append(alien)

def move_aliens():
    for alien in aliens:
        alien.x -= alien_speed *  level

def check_collision():
    global score, level, game_over
    aliens_to_remove = []
    bullets_to_remove = []
    
    for alien in aliens:
        if ship_rect.colliderect(alien):
            game_over = True
            
    for bullet in bullets:
        for alien in aliens:
            if bullet.colliderect(alien):
                aliens_to_remove.append(alien)
                try:
                    bullets.remove(bullet)  # Attempt to remove the bullet
                except ValueError:
                    pass  # If the bullet is not in the list, do nothing
                score += 1
                if score % 10 == 0:
                    level += 1
    
    # Remove aliens and bullets
    for alien in aliens_to_remove:
        aliens.remove(alien)
    for bullet in bullets_to_remove:
        bullets.remove(bullet)

def display_score():
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def display_level():
    level_text = font.render("Level: " + str(level), True, (255, 255, 255))
    screen.blit(level_text, (10, 50))

def reset_game():
    global game_over, score, level
    score = 0
    level = 1
    game_over = False  # 重置游戏结束标志
    bullets.clear()  # 清空子弹列表
    aliens.clear()  # 清空外星人列表
    ship_rect.left = 0 #重置飞船位置
    ship_rect.centery = screen.get_rect().centery

running = False
while not running:
    screen.fill((0, 0, 0))  # 清空屏幕
    draw_play_button()  # 绘制Play按钮
    draw_exit_button()  # 绘制exit按钮
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # 获取鼠标点击位置
            if play_button.collidepoint(mouse_pos):
                running = True
            if exit_button.collidepoint(mouse_pos):
                pygame.quit()
                quit()
    clock.tick(60)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ship_movement_x = -ship_speed
                if event.key == pygame.K_RIGHT:
                    ship_movement_x = ship_speed
                if event.key == pygame.K_UP:
                    ship_movement_y = -ship_speed
                if event.key == pygame.K_DOWN:
                    ship_movement_y = ship_speed
                if event.key == pygame.K_SPACE:
                    new_bullet = bullet_rect.copy()
                    new_bullet.centerx = ship_rect.right
                    new_bullet.bottom = ship_rect.centery+12
                    bullets.append(new_bullet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ship_movement_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    ship_movement_y = 0


        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()  # 获取鼠标点击位置
                if newgame_button.collidepoint(mouse_pos):
                    reset_game()
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()


    ship_rect.x += ship_movement_x
    ship_rect.y += ship_movement_y

    if ship_rect.left < 0:
        ship_rect.left = 0
    if ship_rect.right > 1200:
        ship_rect.right = 1200
    if ship_rect.top < 0:
        ship_rect.top = 0
    if ship_rect.bottom > 790:
        ship_rect.bottom = 790

    alien_spawn_timer -= 1
    if alien_spawn_timer <= 0 and not game_over:
        spawn_alien()
        alien_spawn_timer = 100

    move_aliens()
    check_collision()

    screen.fill((0, 0, 0))

    # 绘制星星
    for star in stars:
        screen.blit(star_image, star)
    display_score()
    display_level()

    screen.blit(ship_image, ship_rect)
    
    for bullet in bullets:
        bullet.x += bullet_speed
        if bullet.bottom > 1200:
            bullets.remove(bullet)
        
    for bullet in bullets:
        screen.blit(bullet_image, bullet)
    
    for alien in aliens:
        screen.blit(alien_image, alien)
    
    # 在游戏结束时保存最高分
    if score > load_high_score():
        save_high_score(score)

    # 在游戏结束时绘制最高分
    high_score_text = font.render("High Score: " + str(load_high_score()), True, (255, 255, 255))
    screen.blit(high_score_text, (10, 90))
    
    if game_over:
        screen.fill((0, 0, 0))  # 清空屏幕
        draw_newgame_button()  # 绘制newgame按钮
        draw_exit_button()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
