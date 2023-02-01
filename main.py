import pygame, pygame_gui, requests, sys, os


class MapParams(object):
    def __init__(self):
        self.lon = 2.296952
        self.lat = 48.857555
        self.zoom = 4
        self.type = "map"

    def ll(self):
        return str(self.lon) + "," + str(self.lat)

    def update(self, event):
        my_step = 0.008
        if event.key == pygame.K_w and self.zoom < 19:
            self.zoom += 1
        elif event.key == pygame.K_s and self.zoom > 2:
            self.zoom -= 1

        elif event.key == pygame.K_LEFT:
            self.lon -= my_step * 2 ** (15 - self.zoom)
        elif event.key == pygame.K_RIGHT:
            self.lon += my_step * 2 ** (15 - self.zoom)
        elif event.key == pygame.K_UP and self.lat < 85:
            self.lat += my_step * 2 ** (15 - self.zoom)
        elif event.key == pygame.K_DOWN and self.lat > -85:
            self.lat -= my_step * 2 ** (15 - self.zoom)

    def update_type(self, new_type):
        if new_type == 'схема':
            self.type = 'map'
        if new_type == 'спутник':
            self.type = 'sat'
        if new_type == 'гибрид':
            self.type = 'sat,skl'

def load_map(mp):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={mp.ll()}&z={mp.zoom}&l={mp.type}"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapParams()

    gui_manager = pygame_gui.UIManager((600, 450))

    map_type_menu = pygame_gui.elements.UIDropDownMenu(
        options_list = ["схема", "спутник", "гибрид"], starting_option='схема',
        relative_rect = pygame.Rect((10, 10), (100, 50)),
        manager=gui_manager
    )

    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000.0
        # event = pygame.event.wait()
        # не уверее что это необходимо, но на всякий сделал так
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYDOWN:
                mp.update(event)
            elif event.type == pygame.USEREVENT:
                if event.user_type == 32859: # id изменения значения меню (пишет поменять user_type на type, не слушай)
                    mp.update_type(event.text)
            gui_manager.process_events(event)

        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        gui_manager.update(time_delta)
        gui_manager.draw_ui(screen)
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()

