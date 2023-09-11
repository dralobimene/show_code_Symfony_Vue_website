import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tm
import requests
import json
import os
import random
import re
import string


"""
ecran qui permet la creation du joueur en mode multiplayer
"""
class Connect:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Multiplayer game - screen 01')
        self.window.geometry('680x680')
        self.window.configure(bg='black')

        self.label_name = None
        self.entry_name = None
        self.label_life = None
        self.label_attack = None
        self.label_defense = None
        self.label_magic = None
        self.label_strength = None
        self.color_name = None

        self.button_rollDices = None

        self.label_createCharacter = None
        self.button_createCharacter = None

        self.name = None
        self.strength = None
        self.strength_value = tk.StringVar(self.window, value='Your strength will be: ')

        self.user_nickname = None
        self.user_tokenForPython = None

        self.response_data = None

        # Regular expression pattern for validating entry_name
        self.entry_pattern = re.compile(r'^[a-zA-Z][\w@-]{2,14}$')

        # Define validation command
        self.validate_command = self.window.register(self.validate_entry)

        self.entry_name = tk.Entry(self.window)
        self.entry_name.grid(row=2, column=0, padx=50, pady=10, sticky='w')

        # Define a dictionary to map color names to RGB values
        self.color_dict = {
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'black': (0, 0, 0),
            'brown': (165, 42, 42),
            'pink': (255, 192, 203),
            'purple': (128, 0, 128),
            'yellow': (255, 255, 0),
            'grey': (128, 128, 128),
        }

        #
        self.color_selection = None

    # =========================================================================

    def generate_random_string(self, length):
        """
        return a random string with 20 characters

        Args: length (int):
            number of characters to compose the string

        Returns:
            the random string
        """

        # Define the possible characters to choose from
        characters = string.ascii_letters + string.digits

        # Generate a random string by randomly choosing characters from the pool
        random_string = ''.join(random.choice(characters) for i in range(length))

        return random_string

    # =========================================================================

    def connect(self, login, password):

        #
        url = 'https://localhost:8000/test_python_get_games_from_mongo_php'

        # =====================================================================

        # Directory and file checking
        directory = "multiplayer/save"
        filename = "player.json"
        filepath = os.path.join(directory, filename)

        # Checking directory existence
        if os.path.exists(directory):
            print("Directory 'multiplayer/save' exists: yes")
        else:
            print("Directory 'multiplayer/save' exists: no")

        # Checking file existence
        if os.path.exists(filepath):
            print("File 'multiplayer/save/player.json' exists: yes")
        else:
            print(filepath)
            print("File 'multiplayer/save/player.json' exists: no")

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

    def validate_entry(self, input):
        if self.entry_pattern.fullmatch(input) or input == "":
            return True
        else:
            return False

    # =========================================================================

    def createCharacter(self):
        self.name = self.entry_name.get()
        self.color_name = self.color_selection.get()

        if self.color_name not in self.color_dict:
            print("Invalid color selection")
            tm.showerror("Error", "Invalid color selection")
            return

        if self.name and self.strength_value is not None and self.validate_entry(self.name):
            print("Creating character")

            # creer un dictionnaire json
            player_data = {
                'name': self.name,
                'strength': int(self.strength_value.get().split(":")[1].strip()),
                'attack': 100,
                'defense': 100,
                'life': 100,
                'magic': 100,
                'position': (0, 0),
                'color': self.color_dict[self.color_name],
                'radius': 8,
                'speed': 16,
                'stair_actuel': 'multiplayer/save/stairs_json/stair_1.json',
                'id': self.generate_random_string(20),
            }

            # Checking if "save" directory exists
            if not os.path.exists("multiplayer/save"):
                print("'save' directory not found. Creating 'multiplayer/save' directory...")
                os.makedirs("multiplayer/save")
            else:
                print("'multiplayer/save' directory already exists.")

            # Checking if "player.json" file exists
            if os.path.isfile("multiplayer/save/player.json"):
                print("'player.json' already exists. Deleting the file...")
                os.remove("multiplayer/save/player.json")

            # Write player_data to "player.json"
            print("Writing player data to 'player.json'...")
            with open("multiplayer/save/player.json", 'w') as json_file:
                json.dump(player_data, json_file, indent=4)

            # going to next py script
            self.window.destroy()
            os.system('python3.9 multiplayer/multiplayer_screen03.py')

        else:
            print("Unable to create character, name or strength missing")
            tm.showerror("Error", "Unable to create character, error occurred")
            self.entry_name.delete(0, 'end')

    # =========================================================================

    def rollDices(self):
        self.strength = random.randint(1, 100)
        self.strength_value.set(f"Your strength will be: {self.strength}")
        print(f"Strength set to {self.strength}")

    # =========================================================================

    def connectionSuccess(self, ids):
        self.label_success = tk.Label(self.window, text="Connection successful!")
        self.label_success.grid(row=0, column=0, padx=50, pady=10, sticky='w')

    # =========================================================================

    def connectionFailure(self):
        self.label_success = tk.Label(self.window, text="A problem occurred!")
        self.label_success.grid(row=0, column=0, padx=50, pady=10, sticky='w')

    # =========================================================================

    def prepareGUI(self):

        # create a label widget
        self.label_name = tk.Label(self.window, text="Enter name for your character")
        self.label_name.grid(row=1, column=0, padx=50, pady=10, sticky='w')

        # create a label widget
        self.label_life = tk.Label(self.window, text="your life will be 100%")
        self.label_life.grid(row=3, column=0, padx=50, pady=10, sticky='w')

        # create a label widget
        self.label_attack = tk.Label(self.window, text="Your attack will be 100%")
        self.label_attack.grid(row=4, column=0, padx=50, pady=10, sticky='w')

        # create a label widget
        self.label_defense = tk.Label(self.window, text="Your defense will be 100%")
        self.label_defense.grid(row=5, column=0, padx=50, pady=10, sticky='w')

        # create a label widget
        self.label_magic = tk.Label(self.window, text="Your magic will be 100%")
        self.label_magic.grid(row=6, column=0, padx=50, pady=10, sticky='w')

        # create a label widget
        self.label_strength = tk.Label(self.window, textvariable=self.strength_value)
        self.label_strength.grid(row=7, column=0, padx=50, pady=10, sticky='w')

        # create a button widget
        self.button_rollDices = tk.Button(self.window,
                                           text="Roll_dices",
                                           command=self.rollDices)
        self.button_rollDices.grid(row=10, column=0, padx=50, pady=10, sticky='w')

        # create a label widget
        self.label_createCharacter = tk.Label(self.window, text="click to create your character")
        self.label_createCharacter.grid(row=8, column=0, padx=50, pady=10, sticky='w')

        # create a button widget
        self.button_createCharacter = tk.Button(self.window,
                                           text="Create your character",
                                           command=self.createCharacter)
        self.button_createCharacter.grid(row=11, column=0, padx=50, pady=10, sticky='w')

        # Create color selection drop-down
        self.color_selection = ttk.Combobox(self.window, values=list(self.color_dict.keys()))
        self.color_selection.grid(row=9, column=0, padx=50, pady=10, sticky='w')
        self.color_selection.set('Select color')

        # =====================================================================

        """
        connection_status = self.connect(self.user_nickname,
                                         self.user_tokenForPython)

        if connection_status:
            self.connectionSuccess()
        else:
            self.connectionFailure()
        """
        # =====================================================================

        # run the tkinter main loop
        self.window.mainloop()


if __name__ == '__main__':
    connect = Connect()
    connect.prepareGUI()
