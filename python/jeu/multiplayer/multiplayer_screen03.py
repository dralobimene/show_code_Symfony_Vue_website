import tkinter as tk
from tkinter import ttk
import requests
import json
import os


class Connect:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Multiplayer game - screen 03')
        self.window.geometry('680x680')
        self.window.configure(bg='black')

        self.label_createGame = None
        self.button_createGame = None
        self.label_chooseGameToJoin = None
        self.dropdown_chooseGameToJoin = None
        self.button_join_game = None

        self.user_nickname = None
        self.user_tokenForPython = None

        self.response_data = None

    # =========================================================================

    def connect(self, login, password):

        #
        url = 'https://localhost:8000/test_python_get_games_from_mongo_php'

        # =====================================================================

        # Directory and file checking
        directory = "multiplayer/credentialsToPlay"
        filename = "credentialsToPlay.json"
        filepath = os.path.join(directory, filename)

        # Checking directory existence
        if os.path.exists(directory):
            print("Directory 'multiplayer/credentialsToPlay' exists: yes")
        else:
            print("Directory 'multiplayer/credentialsToPlay' exists: no")

        # Checking file existence
        if os.path.exists(filepath):
            print("File 'multiplayer/credentialsToPlay/credentialsToPlay.json' exists: yes")
        else:
            print(filepath)
            print("File 'multiplayer/credentialsToPlay/credentialsToPlay.json' exists: no")

        # If both directory and file exist, open and read the file
        if os.path.exists(directory) and os.path.exists(filepath):
            with open(filepath, 'r') as file:
                data = json.load(file)
                for key, value in data.items():
                    print(f'{key} => {value}')
                    self.user_nickname = data["user_nickname"]
                    self.user_tokenForPython = data["user_tokenForPython"]

        # =====================================================================

        #
        data = {
            'user_nickname': self.user_nickname,
            'user_tokenForPython': self.user_tokenForPython,
        }

        #
        headers = {'Content-Type': 'application/json'}

        #
        response = requests.post(url,
                                 data=json.dumps(data),
                                 headers=headers,
                                 verify=False)

        print(f'>> Status Code: {response.status_code}')
        print(f'>> Content: {response.content}')

        print(">> valeur de response.text")
        print(response.text)

        self.response_data = response.json()

        if self.response_data['user']['nickname'] == self.user_nickname and \
                self.response_data['user']['tokenForPython'] == self.user_tokenForPython and \
                self.response_data['status']:
            print("CORRESPONDANCE")
            return True

        return False

    # =========================================================================

    """
    Qd on clique sur le bouton "create game"
    """
    def createGame(self):
        self.window.destroy()
        os.system('python3.9 multiplayer/multiplayer_screen02.py')

    # =========================================================================

    """
    Qd on clique sur le bouton "join the game"
    """
    def joinTheGame(self):

        #
        game_id = self.dropdown_chooseGameToJoin.get()

        #
        file_path = 'gameIwantTojoin.txt'

        if os.path.exists(file_path):
            print("File exists, replacing it with new content...")
        else:
            print("File doesn't exist, creating it...")

        #
        with open('gameIWantToJoin.txt', 'w') as file:
            file.write(game_id)

        self.window.destroy()
        os.system('python3.9 multiplayer/multiplayer_screen04.py')

    # =========================================================================

    def connectionSuccess(self, ids):
        self.label_success = tk.Label(self.window, text="Connection successful!")
        self.label_success.grid(row=0, column=0, padx=50, pady=10, sticky='w')

        # Update the values of the dropdown menu
        self.dropdown_chooseGameToJoin['values'] = ids

    # =========================================================================

    def connectionFailure(self):
        self.label_success = tk.Label(self.window, text="A problem occurred!")
        self.label_success.grid(row=0, column=0, padx=50, pady=10, sticky='w')

    # =========================================================================

    def prepareGUI(self):

        # create a label widget
        self.label_createGame = tk.Label(self.window, text="click to go to steps to create a game:")
        self.label_createGame.grid(row=1, column=0, padx=50, pady=10, sticky='w')

        # create a button widget
        self.button_createGame = tk.Button(self.window, text="Create a game", command=self.createGame)
        self.button_createGame.grid(row=2, column=0, padx=50, pady=10, sticky='w')

        # create a label widget
        self.label_chooseGameToJoin = tk.Label(self.window, text="or choose your game from here:")
        self.label_chooseGameToJoin.grid(row=3, column=0, padx=50, pady=10, sticky='w')

        # create a Combobox widget for the dropdown menu
        self.dropdown_chooseGameToJoin = ttk.Combobox(self.window, values=[], width=30)
        self.dropdown_chooseGameToJoin.grid(row=4, column=0, padx=50, pady=10, sticky='w')

        # create a button to join a game
        self.button_join_game = tk.Button(self.window, text="Join the game", command=self.joinTheGame)
        self.button_join_game.grid(row=5, column=0, padx=50, pady=10, sticky='w')

        # =====================================================================

        connection_status = self.connect(self.user_nickname,
                                         self.user_tokenForPython)

        if connection_status:
            self.connectionSuccess(self.response_data['distinctIds'])
        else:
            self.connectionFailure()

        # =====================================================================

        # run the tkinter main loop
        self.window.mainloop()


if __name__ == '__main__':
    connect = Connect()
    connect.prepareGUI()
