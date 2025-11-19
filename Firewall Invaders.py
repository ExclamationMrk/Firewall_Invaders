import random
import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()

screen_size = (800, 800)
gamescreen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True

star_event = pygame.USEREVENT + 1
pygame.time.set_timer(star_event, 100)

enemy_spawn_event = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_spawn_event, 20)


class BackgroundHandler:
    def __init__(self):
        self.star_images = {"1": pygame.transform.scale(pygame.image.load(r"Firewall_Invaders_Images\star_invhex.png"), (10, 10)),
                            "2": pygame.transform.scale(pygame.image.load(r"Firewall_Invaders_Images\Star_pentagon.png"), (10, 10)),
                            "3": pygame.transform.scale(pygame.image.load(r"Firewall_Invaders_Images\star_invsqr.png"), (10, 10))}
        self.star_information = []

    def create_star(self):
        star = [random.randint(1, 3), (random.randint(0, screen_size[0] + 1), screen_size[1])]
        self.star_information.append(star)

    def move_stars(self):
        posnumrunthrough = 0
        for star in self.star_information:
            if star[1][1] - 1 < -30:
                self.star_information.remove(star)

            else:
                star = [star[0], (star[1][0], star[1][1] - 1)]
                self.star_information[posnumrunthrough] = star
                posnumrunthrough += 1

    def blit(self):
        for star in self.star_information:
            if star[0] == 1:
                gamescreen.blit(self.star_images["1"], star[1])

            elif star[0] == 2:
                gamescreen.blit(self.star_images["2"], star[1])

            elif star[0] == 3:
                gamescreen.blit(self.star_images["3"], star[1])


class FireWall:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load(r"Firewall_Invaders_Images\firewall.png"), (800, 70))
        self.integrity = 1000
        self.font = pygame.font.SysFont("Impact", 30)

    def blit(self):
        gamescreen.blit(self.image, (0, screen_size[1] - 70))

        firewall_text = self.font.render("The Firewall", False, (255, 255, 255))
        rect = firewall_text.get_rect()
        rect.center = (600, screen_size[1] - 20)

        gamescreen.blit(firewall_text, (rect.x, rect.y))

        text = "System Integrity: " + str(self.integrity)
        firewall_text = self.font.render(text, False, (255, 255, 255))
        rect = firewall_text.get_rect()
        rect.centery = screen_size[1] - 20

        gamescreen.blit(firewall_text, (40, rect.y))

        text = "Menu: Esc"
        firewall_text = self.font.render(text, False, (255, 255, 255))
        rect = firewall_text.get_rect()
        rect.centery = screen_size[1] - 90

        gamescreen.blit(firewall_text, (40, rect.y))

    def take_damage(self, damage):
        self.integrity -= (damage * 10)
        if self.integrity <= 0:
            menu_instance.update_state(-1)

        else:
            pass


class MenuHandler:
    def __init__(self):
        self.sounds = [pygame.mixer.Sound(r"Firewall_Invaders_Images/ka-ching.mp3")]
        self.sounds[0].set_volume(.2)
        self.menu_state = 0
        self.cooldown = 0
        self.upgrade_costs = {"b_pierce": 10, "b_damage": 10, "reload_time": 100, "fw_self_scan": 500, "firewall_repair": 100}
        self.upgrade_menu = [pygame.Rect((20, 20), (760, screen_size[1] - 40)), pygame.Rect((40, 40), (720, screen_size[1] - 80))]
        self.buttons = {"b_pierce": pygame.Rect((100, screen_size[1] - 300), (150, 70)), "b_damage": pygame.Rect((315, screen_size[1] - 300), (170, 70)),
                        "reload_time": pygame.Rect((550, screen_size[1] - 300), (150, 70)), "fw_self_scan": pygame.Rect((250, screen_size[1] - 460), (300, 90)),
                        "firewall_repair": pygame.Rect((250, screen_size[1] - 180), (300, 80))}
        self.font = pygame.font.SysFont("Arial", 15)

    def update_state(self, state):
        if self.cooldown == 0:
            self.menu_state = state
            self.cooldown = 60

    def upgrading(self):
        mouse_pos = pygame.mouse.get_pos()

        for key, item in self.buttons.items():
            collision = item.collidepoint(mouse_pos)

            if collision:
                if key == "b_pierce":
                    if bullets_instance.points >= self.upgrade_costs[key]:
                        bullets_instance.points -= self.upgrade_costs[key]
                        self.upgrade_costs[key] += int((300/enemies_instance.difficulty_value) + (random.randint(1, 10)))
                        bullets_instance.upgrades[key] += 1
                        self.sounds[0].play()

                elif key == "b_damage":
                    if bullets_instance.points >= self.upgrade_costs[key]:
                        bullets_instance.points -= self.upgrade_costs[key]
                        self.upgrade_costs[key] += int((200/enemies_instance.difficulty_value) + (random.randint(1, 10)))
                        bullets_instance.upgrades[key] += 1
                        self.sounds[0].play()

                elif key == "reload_time":
                    if bullets_instance.points >= self.upgrade_costs[key] and bullets_instance.upgrades[key] > 1:
                        bullets_instance.points -= self.upgrade_costs[key]
                        self.upgrade_costs[key] += int((2000/enemies_instance.difficulty_value) + (random.randint(1, 10) * 20))
                        bullets_instance.upgrades[key] -= 1
                        self.sounds[0].play()

                elif key == "fw_self_scan":
                    if bullets_instance.points >= self.upgrade_costs[key] and bullets_instance.firewall_fire_rate != 30:
                        if bullets_instance.firewall_fire_rate == 0:
                            bullets_instance.points -= self.upgrade_costs[key]
                            bullets_instance.firewall_fire_rate = 120
                            self.upgrade_costs[key] = 1000
                            self.sounds[0].play()

                        elif bullets_instance.firewall_fire_rate == 120:
                            bullets_instance.points -= self.upgrade_costs[key]
                            bullets_instance.firewall_fire_rate = 60
                            self.upgrade_costs[key] = 3000
                            self.sounds[0].play()

                        elif bullets_instance.firewall_fire_rate == 60:
                            bullets_instance.points -= self.upgrade_costs[key]
                            bullets_instance.firewall_fire_rate = 30
                            self.upgrade_costs[key] = 99999999
                            self.sounds[0].play()

                        else:
                            pass

                elif key == "firewall_repair":
                    if firewall_instance.integrity < 1000 and bullets_instance.points >= self.upgrade_costs["firewall_repair"]:
                        bullets_instance.points -= self.upgrade_costs[key]
                        difference = (1000 - firewall_instance.integrity)/10
                        firewall_instance.integrity = 1000
                        self.upgrade_costs[key] += int(difference * enemies_instance.round)
                        self.sounds[0].play()

    def blit(self):
        if self.menu_state == 1:
            pygame.draw.rect(gamescreen, (255, 255, 255), self.upgrade_menu[0])
            pygame.draw.rect(gamescreen, (0, 0, 0), self.upgrade_menu[1])

            pygame.draw.rect(gamescreen, (255, 255, 255), self.buttons["b_pierce"])
            pygame.draw.rect(gamescreen, (255, 255, 255), self.buttons["b_damage"])
            pygame.draw.rect(gamescreen, (255, 255, 255), self.buttons["reload_time"])
            pygame.draw.rect(gamescreen, (255, 255, 255), self.buttons["fw_self_scan"])
            pygame.draw.rect(gamescreen, (255, 255, 255), self.buttons["firewall_repair"])

            text = self.font.render("Malware Test Depth", False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["b_pierce"].center

            gamescreen.blit(text, (rect.x, rect.y))

            text = "Current: " + str(bullets_instance.upgrades["b_pierce"])
            text = self.font.render(text, False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["b_pierce"].center

            gamescreen.blit(text, (rect.x, rect.y + 20))

            text = "Points Cost: " + str(self.upgrade_costs["b_pierce"])
            text = self.font.render(text, False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["b_pierce"].center

            gamescreen.blit(text, (rect.x, rect.y - 20))

            text = self.font.render("Advanced Malware Detection", False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["b_damage"].center

            gamescreen.blit(text, (rect.x, rect.y))

            text = "Current: " + str(bullets_instance.upgrades["b_damage"])
            text = self.font.render(text, False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["b_damage"].center

            gamescreen.blit(text, (rect.x, rect.y + 20))

            text = "Points Cost: " + str(self.upgrade_costs["b_damage"])
            text = self.font.render(text, False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["b_damage"].center

            gamescreen.blit(text, (rect.x, rect.y - 20))

            text = self.font.render("Malware Test Time", False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["reload_time"].center

            gamescreen.blit(text, (rect.x, rect.y))

            text = "Current: " + str(bullets_instance.upgrades["reload_time"])
            text = self.font.render(text, False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["reload_time"].center

            gamescreen.blit(text, (rect.x, rect.y + 20))

            text = "Points Cost: " + str(self.upgrade_costs["reload_time"])
            text = self.font.render(text, False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["reload_time"].center

            gamescreen.blit(text, (rect.x, rect.y - 20))

            text = self.font.render("Firewall Self Scans! Automatically Scans!", False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["fw_self_scan"].center

            gamescreen.blit(text, (rect.x, rect.y))

            text = self.font.render("Firewall Repair", False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["firewall_repair"].center

            gamescreen.blit(text, (rect.x, rect.y))

            text = "Points Cost: " + str(self.upgrade_costs["firewall_repair"])
            text = self.font.render(text, False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["firewall_repair"].center

            gamescreen.blit(text, (rect.x, rect.y - 20))

            if bullets_instance.firewall_fire_rate == 0:
                placeholder = "not unlocked"

            elif bullets_instance.firewall_fire_rate == 120:
                placeholder = "1"

            elif bullets_instance.firewall_fire_rate == 60:
                placeholder = "2"

            elif bullets_instance.firewall_fire_rate == 30:
                placeholder = "3"

            else:
                placeholder = "IDK how you did this, good job."

            text = "Self Scan Level: " + placeholder
            text = self.font.render(text, False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["fw_self_scan"].center

            gamescreen.blit(text, (rect.x, rect.y + 20))

            text = "Points Cost: " + str(self.upgrade_costs["fw_self_scan"])
            text = self.font.render(text, False, (0, 0, 0))
            rect = text.get_rect()
            rect.center = self.buttons["fw_self_scan"].center

            gamescreen.blit(text, (rect.x, rect.y - 20))

            title_font = pygame.font.SysFont("Impact", 70)
            text = "Upgrade Menu"
            text = title_font.render(text, False, (255, 255, 255))
            rect = text.get_rect()
            rect.center = (400, 100)

            gamescreen.blit(text, (rect.x, rect.y - 20))

            control_font = pygame.font.SysFont("Arial", 35)

            text = "Controls"
            text = control_font.render(text, False, (255, 255, 255))
            rect = text.get_rect()
            rect.center = (400, 150)

            gamescreen.blit(text, (rect.x, rect.y))

            text = "WS/UP-DOWN to move vertically"
            text = control_font.render(text, False, (255, 255, 255))
            rect = text.get_rect()
            rect.center = (400, 190)

            gamescreen.blit(text, (rect.x, rect.y))

            text = "Mouse to move horizontally, Spacebar/Mouseclick to shoot"
            text = control_font.render(text, False, (255, 255, 255))
            rect = text.get_rect()
            rect.center = (400, 220)

            gamescreen.blit(text, (rect.x, rect.y))

            text = "Backspace to exit program"
            text = control_font.render(text, False, (255, 255, 255))
            rect = text.get_rect()
            rect.center = (400, 250)

            gamescreen.blit(text, (rect.x, rect.y))

            text = "Your Goal: protect your firewall from the malware"
            text = control_font.render(text, False, (255, 255, 255))
            rect = text.get_rect()
            rect.center = (400, 280)

            gamescreen.blit(text, (rect.x, rect.y))

            text = "by shooting them! Don't let system integrity hit 0!"
            text = control_font.render(text, False, (255, 255, 255))
            rect = text.get_rect()
            rect.center = (400, 315)

            gamescreen.blit(text, (rect.x, rect.y))



        else:
            pass

        if self.cooldown > 0:
            self.cooldown -= 1


class Bullets:
    def __init__(self):
        self.sounds = [pygame.mixer.Sound(r"Firewall_Invaders_Images\Shoot.mp3"), pygame.mixer.Sound(r"Firewall_Invaders_Images\Explosion.mp3")]
        self.sounds[0].set_volume(.1)
        self.sounds[1].set_volume(.3)
        self.bullets = []
        self.bullet_pierces = []
        self.fire_time = 0
        self.points = 0
        self.upgrades = {"b_pierce": 2, "b_damage": 1, "reload_time": 12}
        self.firewall_fire_rate = 0
        self.firewall_reloading = 0
        self.font = pygame.font.SysFont("Impact", 24)

    def create_bullet(self, position, wall=False):
        if self.fire_time <= 0 and wall is False:
            bullet = pygame.Rect((position[0] - 1, position[1] - 10), (5, 10))
            self.bullets.append(bullet)
            self.sounds[0].play()
            self.bullet_pierces.append(self.upgrades["b_pierce"])
            self.fire_time = self.upgrades["reload_time"]

        elif wall is True:
            bullet = pygame.Rect((position[0], position[1]), (12, 10))
            self.bullets.append(bullet)
            self.bullet_pierces.append(self.upgrades["b_pierce"])
            self.fire_time = self.upgrades["reload_time"]

        else:
            pass

    def create_firewall_bullets(self):
        if self.firewall_fire_rate == 0:
            pass

        else:
            if self.firewall_reloading > 0:
                self.firewall_reloading -= 1

            else:
                self.firewall_reloading = self.firewall_fire_rate

                positions = [(367, screen_size[1]), (433, screen_size[1]), (498, screen_size[1]), (563, screen_size[1]), (629, screen_size[1]), (694, screen_size[1]), (759, screen_size[1]), (41, screen_size[1]), (106, screen_size[1]), (171, screen_size[1]), (237, screen_size[1]), (302, screen_size[1])]
                for position in positions:
                    self.create_bullet(position, wall=True)

    def move_bullets(self):
        posnumrunthrough = 0
        for bullet in self.bullets:
            bullet.y = bullet.y - 6
            self.bullets[posnumrunthrough] = bullet
            posnumrunthrough += 1

        temp_bullets = []
        temp_healths = []
        posnumrunthrough = 0
        for bullet in self.bullets:
            if bullet.y <= -10:
                pass

            else:
                temp_bullets.append(bullet)
                temp_healths.append(self.bullet_pierces[posnumrunthrough])

            posnumrunthrough += 1

        self.bullet_pierces = temp_healths
        self.bullets = temp_bullets

        self.fire_time -= 1

    def collision(self):
        posnumrunthrough = 0
        for bullet in self.bullets:
            object = bullet.collideobjects(enemies_instance.enemies)
            if object == None:
                pass
                posnumrunthrough += 1

            else:
                enemy = enemies_instance.enemies.index(object)
                enemies_instance.enemy_health[enemy] -= self.upgrades["b_damage"]
                self.bullet_pierces[posnumrunthrough] -= 1

                if enemies_instance.enemy_health[enemy] <= 0:
                    enemies_instance.enemies.remove(enemies_instance.enemies[enemy])
                    enemies_instance.enemy_health.remove(enemies_instance.enemy_health[enemy])
                    enemies_instance.difficulty_updating()
                    self.points += random.randint(1, enemies_instance.round)
                    self.sounds[1].play()

                if self.bullet_pierces[posnumrunthrough] <= 0:
                    del self.bullet_pierces[posnumrunthrough]
                    del self.bullets[posnumrunthrough]

                else:
                    posnumrunthrough += 1

    def blit(self):
        for bullet in self.bullets:
            pygame.draw.rect(gamescreen, (52, 235, 85), bullet)

        text = "Points: " + str(self.points)
        points_text = self.font.render(text, False, (255, 255, 255))

        rect = points_text.get_rect()
        rect.centery = 50

        gamescreen.blit(points_text, (30, rect.y))


class PlayerCharacter:
    def __init__(self):
        self.pos = [400, screen_size[1] - 120]
        self.sprites = {"1": pygame.transform.scale(pygame.image.load(r"Firewall_Invaders_Images\ship-01.png"), (50, 50)),
                        "2": pygame.transform.scale(pygame.image.load(r"Firewall_Invaders_Images\ship-02.png"), (50, 50)),
                        "3": pygame.transform.scale(pygame.image.load(r"Firewall_Invaders_Images\ship-03.png"), (50, 50))}
        self.velocity = [float(0), float(0)]
        self.current_sprite = 0

    def moveydown(self):
        if self.velocity[1] <= 10:
            self.velocity[1] += 1.5

    def moveyup(self):
        if self.velocity[1] >= -10:
            self.velocity[1] -= 1.5

    def finish_movement(self):
        mouse_pos = pygame.mouse.get_pos()

        self.pos[0] = mouse_pos[0] - 25

        if 10 <= self.pos[0] <= 740:
            self.pos[0] += self.velocity[0]

        else:
            if 10 >= self.pos[0]:
                self.pos[0] = 10

            elif 740 <= self.pos[0]:
                self.pos[0] = 740

        if screen_size[1] - 230 <= self.pos[1] <= screen_size[1] - 80:
            self.pos[1] += self.velocity[1]

        else:
            if screen_size[1] - 230 >= self.pos[1]:
                self.pos[1] = screen_size[1] - 230

            elif screen_size[1] - 80 <= self.pos[1]:
                self.pos[1] = screen_size[1] - 80

        if self.velocity[0] < 0:
            self.velocity[0] += .75

        elif self.velocity[0] > 0:
            self.velocity[0] -= .75

        if self.velocity[1] < 0:
            self.velocity[1] += .75

        elif self.velocity[1] > 0:
            self.velocity[1] -= .75

        if -.5 < self.velocity[0] < .5:
            self.velocity[0] = 0

        if -.5 < self.velocity[1] < .5:
            self.velocity[1] = 0

    def blit(self):
        self.current_sprite += 1
        if self.current_sprite < 10:
            gamescreen.blit(self.sprites["1"], self.pos)

        elif self.current_sprite < 20:
            gamescreen.blit(self.sprites["2"], self.pos)

        elif self.current_sprite < 29:
            gamescreen.blit(self.sprites["3"], self.pos)

        elif self.current_sprite > 29:
            self.current_sprite = 0
            gamescreen.blit(self.sprites["3"], self.pos)


class EnemyMalware:
    def __init__(self):
        self.sounds = [pygame.mixer.Sound(r"Firewall_Invaders_Images\Hit.mp3")]
        self.enemies = []
        self.enemy_health = []
        self.current_enemy_health = 1
        self.color_value = 100
        self.color_pos = True
        self.difficulty_value = 40
        self.round = 1
        self.enemies_left = 20
        self.font = pygame.font.SysFont("Impact", 24)
        self.font = pygame.font.SysFont("Impact", 24)

    def create_enemy(self):
        enemy_type = 1
        if enemy_type == 1 and random.randint(1, self.difficulty_value) == 1:
            enemy = pygame.Rect((0, 0), (20, 20))
            enemy.centerx = random.randint(30, 770)

            self.enemies.append(enemy)
            self.enemy_health.append(self.current_enemy_health)

    def move_enemies(self):
        posnumrunthrough = 0
        for enemy in self.enemies:
            enemy.y = enemy.y + 3
            self.enemies[posnumrunthrough] = enemy
            posnumrunthrough += 1

    def blit(self):
        if self.color_value < 255 and self.color_pos is True:
            self.color_value += 1

        else:
            self.color_pos = False

        if self.color_value > 100 and self.color_pos is False:
            self.color_value -= 1

        else:
            self.color_pos = True

        for enemy in self.enemies:
            if self.round % 3 == 0:
                color = (0, 0, self.color_value)

            elif self.round % 2 == 0:
                color = (0, self.color_value, 0)

            else:
                color = (self.color_value, 0, 0)

            pygame.draw.rect(gamescreen, color, enemy)

        text = "Round: " + str(self.round)
        round_text = self.font.render(text, False, (255, 255, 255))
        gamescreen.blit(round_text, (30, 70))

    def firewall_collisions(self):
        firewall_rect = pygame.Rect((0, screen_size[1] - 70), (800, 70))
        posnumrunthrough = 0
        collisions = []
        for enemy in self.enemies:
            if enemy.colliderect(firewall_rect):
                collisions.append(posnumrunthrough)

            else:
                pass

            posnumrunthrough += 1

        for item in collisions:
            firewall_instance.take_damage(1)
            self.sounds[0].play()

            del self.enemies[item]
            del self.enemy_health[item]

    def difficulty_updating(self):
        if self.enemies_left > 0:
            self.enemies_left -= 1

        else:
            if self.difficulty_value > 1:
                self.difficulty_value -= 1

            else:
                pass

            self.round += 1
            self.current_enemy_health += 1
            self.enemies_left = (int(20 * (self.difficulty_value * .1))) + self.round


background_instance = BackgroundHandler()
player_instance = PlayerCharacter()
enemies_instance = EnemyMalware()
bullets_instance = Bullets()
menu_instance = MenuHandler()
firewall_instance = FireWall()
mouseheld = 0

while running:
    gamescreen.fill((0, 0, 0))
    for event in pygame.event.get():
        if menu_instance.menu_state == 0:
            if event.type == star_event:
                background_instance.create_star()

            if event.type == enemy_spawn_event:
                enemies_instance.create_enemy()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseheld = 1

            if event.type == pygame.MOUSEBUTTONUP:
                mouseheld = 0

            if mouseheld == 1:
                bullets_instance.create_bullet((player_instance.pos[0] + 25, player_instance.pos[1] + 25))

        if event.type == pygame.MOUSEBUTTONUP and menu_instance.menu_state == 1:
            menu_instance.upgrading()

        if event.type == pygame.QUIT:
            running = False

    #Input Handling
    keys_pressed = pygame.key.get_pressed()
    mouse_pressed = pygame.mouse.get_pressed()
    if keys_pressed[pygame.K_BACKSPACE]:
        running = False

    if menu_instance.menu_state == 0:
        if keys_pressed[pygame.K_ESCAPE] or keys_pressed[pygame.K_p]:
            menu_instance.update_state(1)

        if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]:
            player_instance.moveyup()

        if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
            player_instance.moveydown()

        if keys_pressed[pygame.K_SPACE]:
            bullets_instance.create_bullet((player_instance.pos[0] + 25, player_instance.pos[1] + 25))

    elif menu_instance.menu_state == 1:
        if keys_pressed[pygame.K_ESCAPE] or keys_pressed[pygame.K_p]:
            menu_instance.update_state(0)

    #End of Input Handling

    if menu_instance.menu_state == 0:
        background_instance.move_stars()
        player_instance.finish_movement()
        bullets_instance.move_bullets()
        bullets_instance.create_firewall_bullets()
        enemies_instance.move_enemies()

        bullets_instance.collision()
        enemies_instance.firewall_collisions()

    elif menu_instance.menu_state == -1:
        pass

    elif menu_instance.menu_state == 1:
        pass

    background_instance.blit()
    bullets_instance.blit()
    enemies_instance.blit()
    firewall_instance.blit()
    player_instance.blit()
    menu_instance.blit()

    clock.tick(60)
    pygame.display.update()
