import pygame
import sys

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)  
        font = pygame.font.Font(None, 36)
        text_surf = font.render(self.text, True, (0, 0, 0))  
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()


class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        room_width = self.game.current_room.width
        room_height = self.game.current_room.height
        button_width = 200
        button_height = 50
        # Центрируем кнопки по горизонтали, размещаем по вертикали на 30%, 40%, 50% высоты
        continue_button = Button(room_width * 0.5 - button_width / 2, room_height * 0.3,
                                button_width, button_height, "Continue", self.game.toggle_pause)
        settings_button = Button(room_width * 0.5 - button_width / 2, room_height * 0.4,
                                button_width, button_height, "Settings", self.open_settings)
        exit_button = Button(room_width * 0.5 - button_width / 2, room_height * 0.5,
                            button_width, button_height, "Exit Game", self.exit_game)
        self.buttons = [continue_button, settings_button, exit_button]

    def open_settings(self):
        print("Settings menu opened")  

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.rect = pygame.Rect(x, y, 40, 40)  # Меньше игрока
        self.direction = 1  # 1 — вправо, -1 — влево
        self.vision_range = 100  # Дальность обзора
    
    def can_see_player(self, player):
        player_rect = pygame.Rect(player.x, player.y, 50, 50)
        vision_rect = pygame.Rect(self.x + (30 if self.direction > 0 else -self.vision_range),
                                self.y, self.vision_range, 30)
        return vision_rect.colliderect(player_rect)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)  # Красный враг

        vision_rect = pygame.Rect(self.x + (30 if self.direction > 0 else -self.vision_range),
                                self.y, self.vision_range, 30)
        pygame.draw.rect(screen, (255, 0, 0, 50), vision_rect)  # Полупрозрачный луч
    
    def update(self, player): 
        if self.can_see_player(player):
            print("Игрок замечен!")  # Позже заменим на вызов сирены
        else:
            patrol_range = game.current_room.width * 0.2  # Патрулируем 20% ширины комнаты
            if self.x < game.current_room.width * 0.3 + patrol_range:
                self.direction = 1
                self.x += self.speed
            elif self.x > game.current_room.width * 0.3:
                self.direction = -1
                self.x -= self.speed
            self.rect.x = self.x
        
    

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        new_rect = pygame.Rect(new_x, new_y, 50, 50)
        room = game.current_room
        if 0 <= new_x <= room.width - 50 and 0 <= new_y <= room.height - 50:  # Учитываем размер игрока
            # Проверка 
            for wall in room.walls:
                if new_rect.colliderect(wall):
                    return  # Столкновение — движение отменяется
                
            self.x = new_x
            self.y = new_y
    
    def can_stealth_kill(self, enemy):
        player_rect = pygame.Rect(self.x, self.y, 50 + 5, 50 + 5)
        return player_rect.colliderect(enemy.rect) and not enemy.can_see_player(self)
    
    def try_stealth_kill(self, enemies):
        for i, enemy in enumerate(enemies):
            if self.can_stealth_kill(enemy):
                del enemies[i]  # Удаляем врага
                print("Стелс-убийство!")
                return
            
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 50, 50))


class Room:
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height
        self.walls = [pygame.Rect(200, 200, 100, 20)]  # Пример стены

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, self.width, self.height), 1)
        for wall in self.walls:
            pygame.draw.rect(screen, (255, 0, 0), wall)  # Красные стены

class Game:
    def __init__(self):
        # Настройки
        self.is_paused = False
        self.game_speed = 1.0
        self.delta_time = 0.016  # 60 FPS (16 мс)

        # Комнаты
        self.rooms = [Room(1, 800, 600)]
        self.current_room = self.rooms[0]

        # Игрок
        self.player = Player(self.curent_room.width * 0.1, self.curent_room.height * 0.1)
        
        # Один враг для теста
        self.enemies = [Enemy(self.curent_room.width * 0.3, self.curent_room.height * 0.3)]  # Начальная позиция — 30% от ширины и высоты

        # Меню паузы
        self.pause_menu = PauseMenu(self)

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def set_game_speed(self, speed):
        self.game_speed = speed

    def update(self):
        if not self.is_paused:
            scaled_delta_time = self.delta_time * self.game_speed
            self.update_game_world(scaled_delta_time)
        else:
            self.update_paused_state()

    def update_game_world(self, scaled_delta_time):
        # Обработка ввода
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        self.player.move(dx, dy)
        
        # E для стелс-убийства
        if keys[pygame.K_e]:
            self.player.try_stealth_kill(self.enemies)

        # Враг
        for enemy in self.enemies:
            enemy.update(self.player)

        

    def update_paused_state(self):
        # Логика для состояния паузы (например, обновление меню)
        game.pause_menu.handle_event(event=event)

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Черный фон
        # Текущую комнату
        self.current_room.draw(screen)

        # Игрока
        self.player.draw(screen)
        
        # Враги
        for enemy in self.enemies:
            enemy.draw(screen)

        # Пауза
        if self.is_paused:
            self.pause_menu.draw(screen)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    game = Game()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game.toggle_pause()

        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)  # Поддержание 60 кадров в секунду

    pygame.quit()
    sys.exit()