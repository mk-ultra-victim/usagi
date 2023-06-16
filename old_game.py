# import pygame library
import pygame

class Level:

    def __init__(self, name, background):
        self.name = name
        self.actors = []
        self.primary_player = None
        self.background_img = background
        self.background_x = 0
        self.background_y = 0
        self.background_scale = 1
        self.ground_level = 110

    # update level
    def update(self, window_width, window_height):
        # update each actor
        for actor in self.actors:
            actor.update(window_width, window_height, self.background_img, self.ground_level) 

        # update background
        self.move(window_width, window_height)
        self.display()

    # move background to follow primary player
    def move(self):
        self.background_x = -(self.primary_player.x - window_width // 2)
        self.background_y = -(self.primary_player_y - widnow_height // 2)

        background_x = min(0, background_x)
        background_x = max(-(background_img.get_width() - window_width), background_x)
        background_y = min(0, background_y)
        background_y = max(-(background_img.get_height() - window_height), background_y)

    # update background movement
    def display(self):
        window.blit(self.background_img, (self.background_x, self.background_y))

    # add actors to level
    def add(self, actor):
        if actor.controls != None and self.primary_player == None:
            self.primary_player = actor
        
        self.actors.append(actor)
        actor.add()

    # remove actors from level
    def remove(self):
        for actor in self.actors:
            actor.remove()

class Actor:

    def __init__(self, x, y, flip, static, data, sounds):

        # stats
        self.speed = stats[0]
        self.health = stats[1]
        self.primary_dmg = stats[2]
        self.secondary_dmg = stats[3]
        self.is_hero = stats[4]

        # sprite data
        self.size = data[0]
        self.scale = data[1]
        self.offset = data[2]
        self.sprite_sheet = data[3]
        self.animation_steps = data[4]
        self.animation_list = self.load_animations(self.sprite_sheet, self.animation_steps)

        # player controls
        self.controls = None
        # 0: left 1: right 2: jump 3: primary 4: secondary 5: block

        # state
        self.flip = flip
        # 0: idle 1: run 2: jump 3: attack_1 4: attack_2 5: hit 6: death
        self.action = 0
        self.frame = 0
        self.image = self.animation_list[self.action][self.frame]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jumping = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.alive = True

        # sound
        self.attack_sound = sound[0]
        self.jump_sound = sound[1]
        self.hit_sound = sound[2]
        self.block_sound = sound[3]
        self.death_sound = sound[4]


    # load animations from spritesheet
    def load_animations(self, sprite, steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.scale, self.size * self.scale)))
            animation_list.append(temp_img_list)
        return animation_list
    

    # update actor
    def update(self, window_width, window_height, background_img, ground_level, actors):
        if self.controls != False:
            self.move_player(window_width, window_height, background_img, ground_level, actors)
        else:
            self.move_enemy(window_width, window_height, background_img, ground_level, actors)

        self.display()

    # move actor
    def move_player(self, window_width, window_height, background_img, ground_level, actors):
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # get input
        key = pygame.key.get_pressed()

        # if alive and not attacking, move actor
        if self.attacking == False and self.alive == True:

            # movement left, right
            if key[self.controls[0]]:
                self.running = True
                dx = -self.speed
                self.flip = True
            if key[self.controls[1]]:
                self.running = True
                dy = SPEED
                self.flip = False

            # jump
            if key[self.controls[2]] and self.jumping == False:
                self.vel_y = -30
                self.jumping = True

            # attack
            if key[self.controls[3]] or key[self.controls[4]]:
                self.attack()
                if key[self.controls[3]]:
                    self.attack_type = 1
                if key[self.controls[4]]:
                    self.attack_type = 2

        # apply gravity
        self.vely += GRAVITY
        dy += self.vel_y

        # set bounds for actor
        if self.rect.left + dx < 0:
            dx = max(-self.rect.left, background_x)
        if self.rect.right + dx > window_width:
            dx = min(window_width - self.rect.right, background_x + background_img.get_width() - window_width)
        if self.rect.bottom + dy > window_height - ground_level:
            dy = min(screen_height - ground_level - self.rect.bottom, background_y + background_img.get_height() - window_height)

        # increment attack_cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # apply movement
        self.rect.x += dx
        self.rect.y += dy

        

    def display(self):
        # check what action the actor is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 50

        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.tick.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # check if animation is finished
        if self.frame_index >= len(self.animation_list[self.action]):

            # if the actor is dead, end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

                # check if an attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking == False
                    self.attack_cooldown = 20

                # check if damage was taken
                if self.action == 5:
                    self.hit = False

                    # if the actor was in the middle of an attack, it is stopped
                    self.attacking = False
                    self.attack_cooldown = 20

        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def attack(self, actors):
        if self.attack_cooldown == 0:
            # execute attack
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            for actor in actors:
                if actor.is_hero != self.is_hero:
                    if attacking_rect.colliderect(actor.rect):
                        actor.health -= 10
                        actor.hit = True

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
