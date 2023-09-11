
import pygame
import pygame_gui
import sys
import os
import requests
import json

"""
La principale différence entre l'utilisation de self et de l'instance connect
dans votre code réside dans la portée. Dans votre code fourni,
vous utilisez connect dans la méthode connexion qui existe en dehors de la
portée de cette méthode.

Cette approche fonctionne car connect est défini dans la portée globale
(en dehors de toute fonction ou méthode). Cependant, il est généralement
considéré comme une mauvaise pratique de référencer des variables de la portée
globale à l'intérieur d'une fonction ou d'une méthode. Cela peut conduire à
des comportements inattendus s'il existe une autre variable avec le même nom,
et cela rend le code plus difficile à comprendre et à maintenir.
"""


class Connect:

    def __init__(self):

        #
        pygame.init()

        #
        pygame.display.set_caption('Connection to post')

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
        """
        envoie le login et le password au controller SF (ConnectController.php)
        SF verifie les 2, check s'il y a correspondance avec un document ds la
        mongo DB
        python passe a l'ecran suivant
        - soit permettre de poster un commentaire
        - soit information cô quoi qque chose ne va pas
        """

        # permettra d'informer l'utilisateur en cas d'erreur
        self.erreur_information = ""

        # permettra de savoir le nbre d'erreur
        erreur_nbre = 0

        # l'URl du endpoint server
        url = 'https://localhost:8000/connect'

        # json envoyé au serveur SF
        data = {
            'usernameOrEmail': login,
            'password': password,
        }

        # def des headers, on envoie du json, dc...
        headers = {'Content-Type': 'application/json'}

        # le certificat SSL du server n'est pas digne de
        # confiance d'apres python
        # verify=False:
        # permet de ne pas verifier le certificat SSL
        # A safer approach is to include the public key certificate
        # of the certificate authority (which has signed the server
        # certificate) in your requests session. Here is an example:
        # response = requests.post(url, data=json.dumps(data), headers=headers, verify='/path/to/certfile')
        # il faut aussi verifier si le certificat SSL est au
        # format PEM, sinon, il faudra le convertir en PEM
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
            if not os.path.exists('credentialsToPostComment'):
                print("Directory 'credentialsToPostComment' does not exist.")
                print("Creation ...")
                os.mkdir('credentialsToPostComment')
            else:
                # Directory exists, now check if the file exists
                file_path = os.path.join('credentialsToPostComment', 'credentials.json')

                if os.path.isfile(file_path):
                    print("'credentials.json' already exists.")
                    print("deletion")
                    os.remove(file_path)

                # File does not exist, create the file and write to it
                print("'credentials.json' does not exist. Creating file...")

                # The dictionary you want to write to the json file
                data = {
                    'user_nickname': response_data['user']['nickname'],
                    'user_tokenForPython': response_data['user']['tokenForPython'],
                    'user_tokenForPythonExpiration': response_data['user']['tokenForPythonExpiration']
                }

                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)

                pygame.quit()
                os.system('python3.9 credentialsToPostComment/CredentialsToPostComment.py')
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

    def connexion(self):
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


        self.button_post_comment = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 350), (500, 50)),
                                                    text='Connect',
                                                    manager=self.manager)

        self.button_quit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((225, 400), (500, 50)),
                                                    text='Go back to main menu',
                                                    manager=self.manager)

        # =========================================================================

        # Declare list of interactive UI elements in the order you want
        # tab to navigate through them
        self.ui_elements = [self.text_entry_login,
                            self.text_entry_password,
                            self.button_post_comment,
                            self.button_quit]

        # =====================================================================

        # Variable to keep track of which element is currently focused
        self.focused_element_index = 0

        # =====================================================================

        self.running = True
        while self.running:
            time_delta = pygame.time.Clock().tick(60)/1000.0

            for event in pygame.event.get():

                # =============================================================

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # =============================================================

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_post_comment:

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

            # =================================================================

            self.manager.update(time_delta)

            # =================================================================

            if self.running:
                self.screen.fill((0, 0, 0))
                self.manager.draw_ui(self.screen)
                pygame.display.update()

    # =========================================================================


if __name__ == '__main__':
    connect = Connect()
    connect.connexion()
