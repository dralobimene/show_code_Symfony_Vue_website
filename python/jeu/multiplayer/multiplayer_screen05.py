import pygame
import pygame_gui
import sys
import requests
import json


class Connect:

    def __init__(self):

        #
        pygame.init()

        #
        pygame.display.set_caption('multiplayer - screen 05')

        #
        self.screen = pygame.display.set_mode((1000, 800))

        #
        self.manager = pygame_gui.UIManager((1000, 800))

        #
        self.running = False

        #
        self.login = "RPGtest33"
        self.password = "RPGtest33@1"

    # =========================================================================

    def connect(self, login, password):

        #
        url = 'https://localhost:8000/connect'

        #
        data = {
            'usernameOrEmail': self.login,
            'password': self.password,
        }

        #
        headers = {'Content-Type': 'application/json'}

        #
        response = requests.post(url,
                                 data=json.dumps(data),
                                 headers=headers,
                                 verify=False)

        #
        response_data = response.json()

        #
        print("Response Status Code: ", response.status_code)
        print("Response Data: ", response_data)

        print("==================================================================")

        print("valeur de response.status_code")
        print(response.status_code)

        print("==================================================================")

        print("valeur de response_data['status']")
        print(response_data['status'])

        print("==================================================================")

        print("valeur de response.text")
        print(response.text)

        if response_data['status']:
            return True

        return False

    # =========================================================================

    """
    Si on arrive a se connecter au controller
    https://localhost:8000/test_python, on fait apparaitre le bouton pr creer
    les variables qui vt contenir les differents stairs au format json
    """
    def ConnectionSuccess(self):
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 10), (300, 50)),
                                    text='Connection successful!',
                                    manager=self.manager)

        self.btn_to_create_game = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 130), (200, 50)),
                                     text='Create the game',
                                     manager=self.manager)

    # =========================================================================

    """
    Si on n'arrive pas à se connecter
    à https://localhost:8000/test_python
    On fait apparaitre un message
    """
    def ConnectionFailure(self):
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((350, 10), (300, 50)),
                                    text='A problem occurred.',
                                    manager=self.manager)

    # =========================================================================

    def prepare_GUI(self):

        # =====================================================================

        connection_status = self.connect(self.login, self.password)

        # =====================================================================

        if connection_status:
            self.ConnectionSuccess()
        else:
            self.ConnectionFailure()

        # =====================================================================

        self.running = True
        while self.running:
            time_delta = pygame.time.Clock().tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.manager.process_events(event)

            self.manager.update(time_delta)

            if self.running:
                self.screen.fill((0, 0, 0))
                self.manager.draw_ui(self.screen)
                pygame.display.update()


if __name__ == '__main__':
    connect_obj = Connect()
    connect_obj.prepare_GUI()
