import pygame

pygame.init()
# Записываем переменные

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200, 675))
pygame.display.set_caption("Mario na minimalkah")
icon = pygame.image.load('images/pyGame.webp').convert()
pygame.display.set_icon(icon)

monster = pygame.image.load('images/monster/free-icon-ghost-1234844.png').convert_alpha()
monster_x = 1205
monster_y = 535
monster_list = []


bg = pygame.image.load('fonts/font_2.jpg').convert()
player = pygame.image.load('images/pl_right/right_1.png').convert_alpha()
player_name = "Игрок"
player_score = 0

walk_l = [
    pygame.image.load('images/pl_left/left_1.png').convert_alpha(),
    pygame.image.load('images/pl_left/left_2.png').convert_alpha(),
    pygame.image.load('images/pl_left/left_3.png').convert_alpha(),
    pygame.image.load('images/pl_left/left_4.png').convert_alpha(),
]

walk_r = [
    pygame.image.load('images/pl_right/right_1.png').convert_alpha(),
    pygame.image.load('images/pl_right/right_2.png').convert_alpha(),
    pygame.image.load('images/pl_right/right_3.png').convert_alpha(),
    pygame.image.load('images/pl_right/right_4.png').convert_alpha(),
]

player_speed = 5
pl_x = 100
pl_y = 530

pl_anim_count = 0
bg_x = 0

sounds = pygame.mixer.Sound('sound/maro-jump-sound-effect_1.mp3')


is_jump = False
jump_count = 8

monster_timer = pygame.USEREVENT + 1
pygame.time.set_timer(monster_timer, 3500)

label_size = pygame.font.Font('fonts/ocra(RUS BY LYAJKA).ttf', 30)
label_size_1 = pygame.font.Font('fonts/ocra(RUS BY LYAJKA).ttf', 20)
lose_label = label_size.render("You lose!!!", False, (230,200,178))
restart_label = label_size_1.render("Restart", False, 'Red')
restart_label_rect = restart_label.get_rect(topleft=(450, 340))


bullet = pygame.image.load('images/free-icon-fire-3426127.png')
bullets = []
bullets_left = 10


gameplay = True

# Создаем главный цикл нашей игры(игра работает по этому циклу)
running = True
while running:
    # Добавляем фон игры
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1200, 0))

    score_text = label_size_1.render(f"Счёт игрока: {player_score}", True, 'BLACK')
    screen.blit(score_text, (10, 10))

    if gameplay:

        # Создаём связи между игроком и монстрами
        player_rect = walk_r[0].get_rect(topleft = (pl_x, pl_y))
        monster_rect = monster.get_rect(topleft = (monster_x, monster_y))

        if monster_list:
            for i, element in enumerate(monster_list):
                screen.blit(monster, element)
                element.x -= 10
                if element.x < -5:
                    monster_list.pop(i)

                if player_rect.colliderect(element):
                    gameplay = False



        #отклик героя на нажатие кнопок
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_l[pl_anim_count], (pl_x, pl_y))
        else:
            screen.blit(walk_r[pl_anim_count], (pl_x, pl_y))


        if keys[pygame.K_LEFT] and pl_x > 50:
            pl_x -= player_speed
        elif keys[pygame.K_RIGHT]and pl_x < 300:
            pl_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE ]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    pl_y -= (jump_count ** 2) / 2
                else:
                    pl_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if is_jump and jump_count == 8:
            sounds.play()


        if pl_anim_count == 3:
            pl_anim_count = 0
        else:
            pl_anim_count += 1


        bg_x -= 2
        if bg_x == -1200:
            bg_x = 0



        if bullets:
            for i, el in enumerate(bullets):
                screen.blit(bullet, (el.x,el.y))
                el.x += 7
                if el.x > 1200:
                    bullets.pop(i)

                if monster_list:
                    for i, monster_count in enumerate(monster_list):
                        if el.colliderect(monster_count):
                            M = monster_list.pop(i)
                            bullets.pop(i)
                            player_score += 10
                            if M:
                                bullets_left += 1
    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (450, 300))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            pl_x = 100
            monster_list.clear()
            bullets.clear()
            bullets_left = 10
            player_score = 0


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == monster_timer:
            monster_list.append(monster.get_rect(topleft=(1205, 535)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_d\
                and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(pl_x + 30, pl_y + 15)))
            bullets_left -= 1


    clock.tick(15)