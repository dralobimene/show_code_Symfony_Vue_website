import pygame
import pygame_gui
import sys
import requests
import json
import os


class Connect:

    def __init__(self):

        #
        pygame.init()

        #
        pygame.display.set_caption('multiplayer - screen 00')

        #
        self.screen = pygame.display.set_mode((1000, 800))

        #
        self.manager = pygame_gui.UIManager((1000, 800))

        #
        self.ui_elements = None

        #
        self.focused_element_index = None

        #
        self.text_entry_login = None
        self.login_text = None

        #
        self.text_entry_password = None
        self.password_text = None

        #
        self.erreur_information = None

        #
        self.running = False

    # =========================================================================

    def connect(self, login, password):

        # permettra d'informer l'utilisateur en cas d'erreur
        self.erreur_information = ""

        # permettra de savoir le nbre d'erreur
        erreur_nbre = 0

        #
        url = 'https://localhost:8000/connect'

        #
        data = {
            'usernameOrEmail': self.login_text,
            'password': self.password_text,
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

        print("==================================================================")

        print("valeur de response.status_code")
        print(response.status_code)

        print("==================================================================")

        print("valeur de response_data['status']")
        print(response_data['status'])

        print("==================================================================")

        print("valeur de response.text")
        print(response.text)

        print("==================================================================")

        print("valeur de response_data.get('user')")
        print(response_data.get('user'))
        print("valeur de Token")
        print(response_data.get('Token'))
        print("valeur de TokenForPython")
        print(response_data.get('TokenForPython'))
        print("valeur de TokenForPythonExpiration")
        print(response_data.get('TokenForPythonExpiration'))

        print("==================================================================")
        """
        print("valeur de response_text['user']['id']")
        print(response_data['user']['id'])
        print("valeur de response_text['user']['nickname']")
        print(response_data['user']['nickname'])
        print("valeur de response_text['user']['email']")
        print(response_data['user']['email'])
        print("valeur de response_text['user']['password']")
        print(response_data['user']['password'])
        print("valeur de response_text['user']['roles']")
        print(response_data['user']['roles'])
        print("valeur de response_text['user']['is_verified']")
        print(response_data['user']['is_verified'])
        print("valeur de response_text['user']['is_new']")
        print(response_data['user']['is_new'])
        """
        print("==================================================================")

        if response.status_code != 200:
            self.erreur_information += "le status code n'est pas 200"
            erreur_nbre += 1

        if self.login_text == "" or self.password_text == "":
            print("login or password empty")
            self.erreur_information += "login or password empty, "
            erreur_nbre += 1

        if response_data.get('user') is None:
            self.erreur_information += "Erreur 01. "
            print(self.erreur_information)
            erreur_nbre += 1
        else:
            if response_data['user']['nickname'] == self.login_text or \
               response_data['user']['email'] == self.login_text:
                pass
            else:
                self.erreur_information += "Erreur 02:"
                erreur_nbre += 1

        if erreur_nbre == 0:
            print("valeur de response_data['user']['nickname']")
            print(response_data['user']['nickname'])
            print("valeur de response_data['user']['tokenForPython']")
            print(response_data['user']['tokenForPython'])
            print("valeur de response_data['user']['tokenForPythonExpiration']")
            print(response_data['user']['tokenForPythonExpiration'])

            # Check if the directory exists
            if not os.path.exists('multiplayer/credentialsToPlay'):
                print("Directory 'multiplayer/credentialsToPlay' does not exist.")
                print("Creation ...")
                os.mkdir('multiplayer/credentialsToPlay')
            else:
                print("Directory 'multiplayer/credentialsToPlay' already exists")

            # Directory exists, now check if the file exists
            file_path = os.path.join('multiplayer/credentialsToPlay/',
                                     'credentialsToPlay.json')

            if os.path.isfile(file_path):
                print("'multiplayer/credentialsToPlay.json' already exists.")
                print("deletion")
                os.remove(file_path)

            # File does not exist, create the file and write to it
            print("'multiplayer/credentialsToPlay/credentialsToPlay.json' does not exist. Creating file...")

            # The dictionary you want to write to the json file
            data = {
                'user_nickname': response_data['user']['nickname'],
                'user_tokenForPython': response_data['user']['tokenForPython'],
                'user_tokenForPythonExpiration': response_data['user']['tokenForPythonExpiration']
            }

            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

            pygame.quit()
            os.system('python3.9 multiplayer/multiplayer_screen01.py')
            self.running = False
        else:
            print("erreur_nbre: " + str(erreur_nbre) + "\n")
            self.erreur_information += "Check your credentials or contact us."
            print(self.erreur_information)

        # Create new label
        self.error_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((200, 450), (600, 50)),
                                              text=self.erreur_information,
                                              manager=self.manager)

    # =========================================================================

    def prepare_GUI(self):

        # =====================================================================

        self.label_login = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 30), (500, 50)),
                                              text='Enter your login:',
                                              manager=self.manager)

        self.text_entry_login = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((225, 70),
        (500, 50)),
                                                         manager=self.manager)

        self.label_password = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((225, 130), (500, 50)),
                                                  text='Enter your password:',
                                                  manager=self.manager)

        self.text_entry_password = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((225,
        170), (500, 50)),
                                                         manager=self.manager)


        self.button_multiplayer = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 350), (500, 50)),
                                                    text='Connect',
                                                    manager=self.manager)

        self.button_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 400), (500, 50)),
                                                    text='Go back to main menu',
                                                    manager=self.manager)

        # =====================================================================

        # Declare list of interactive UI elements in the order you want
        # tab to navigate through them
        self.ui_elements = [self.text_entry_login,
                            self.text_entry_password,
                            self.button_multiplayer,
                            self.button_quit]

        # =====================================================================

        # Variable to keep track of which element is currently focused
        self.focused_element_index = 0

        # =====================================================================

        self.running = True
        while self.running:

            time_delta = pygame.time.Clock().tick(60)/1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # =============================================================

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_multiplayer:

                        self.login_text = self.text_entry_login.get_text()
                        self.password_text = self.text_entry_password.get_text()
                        self.connect(self.login_text, self.password_text)

                    if event.ui_element == self.button_quit:
                        pygame.quit()
                        os.system('python3.9 introduction.py')
                        self.running = False

                # =============================================================

                # Detect Tab key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        # Remove focus from current element
                        self.ui_elements[self.focused_element_index].unfocus()

                        # Move focus to next element (loop around if at end of list)
                        self.focused_element_index = (self.focused_element_index + 1) % len(self.ui_elements)

                        # Set focus on new element
                        self.ui_elements[self.focused_element_index].focus()

                # =============================================================

                self.manager.process_events(event)

            if self.running:
                self.manager.update(time_delta)
                self.screen.fill((0, 0, 0))
                self.manager.draw_ui(self.screen)
                pygame.display.update()


if __name__ == '__main__':
    connect_obj = Connect()
    connect_obj.prepare_GUI()
