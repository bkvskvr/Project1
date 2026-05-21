import pygame


class Audio:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}

    def load_sound(self, name, path):
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
        except Exception as e:
            print(f"Помилка завантаження звуку {name}: {e}")

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"Звук {name} не знайдено!")