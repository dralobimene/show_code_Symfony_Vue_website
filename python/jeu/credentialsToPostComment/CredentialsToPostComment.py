
import tkinter as tk
from tkinter import ttk
import requests
import json
import os


class ConnectToPost:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Post your comment')
        self.window.geometry('680x680')
        self.window.configure(bg='black')

        self.label_title = None
        self.title_comment = None
        self.label_instruction = None
        self.text_comment = None
        self.label_category = None
        self.category_comment = None
        self.button_post_comment = None
        self.button_go_back = None
        self.text_content = None

    # =========================================================================

    def go_back(self):
        self.window.destroy()
        os.system('python3 introduction.py')

    # =========================================================================

    def clear_window(self):
        # loop over all children of the window and destroy them
        for widget in self.window.winfo_children():
            widget.destroy()

    # =========================================================================

    def display_message(self, message):
        # create and display a label with the specified message
        label = tk.Label(self.window, text=message)
        label.grid(row=0, column=0, padx=50, pady=10, sticky='w')

        # create and display a button to perform an action
        button = tk.Button(self.window,
                           text="Go back to main menu",
                           command=self.go_back)
        button.grid(row=1, column=0, padx=50, pady=10, sticky='w')

    # =========================================================================

    def post(self):

        credentials_dir = "credentialsToPostComment"
        credentials_file = os.path.join(credentials_dir, "credentials.json")

        if not os.path.exists(credentials_dir):
            print(f"Directory {credentials_dir} does not exist.")
            return

        if not os.path.isfile(credentials_file):
            print(f"File {credentials_file} does not exist.")
            return

        # =====================================================================

        with open(credentials_file, 'r') as f:
            credentials = json.load(f)

        user_nickname = credentials.get("user_nickname")
        user_tokenForPython = credentials.get("user_tokenForPython")
        user_tokenForPythonExpiration = credentials.get("user_tokenForPythonExpiration")

        print(f"Nickname: {user_nickname}")
        print(f"Token: {user_tokenForPython}")
        print(f"Token Expiration: {user_tokenForPythonExpiration}")

        # =====================================================================

        # ici on récupère les valeurs des Input Fields et de
        # la liste déroulante
        self.title_content = self.title_comment.get()
        self.text_content = self.text_comment.get("1.0", "end-1c")
        self.category_content = self.category_comment.get()

        # =====================================================================

        # l'URl du endpoint server SF
        url = 'https://localhost:8000/python_post_comment'

        # json envoyé au serveur SF avec les différentes valeurs:
        # les 3 1° st issues du fichier
        # credentialsToPostComment/credentials.json
        # et des Input Fields et liste déroulante
        data = {
            'usernameOrEmail': user_nickname,
            'user_tokenForPython': user_tokenForPython,
            'user_tokenForPythonExpiration': user_tokenForPythonExpiration,
            'title_content': self.title_content,
            'text_content': self.text_content,
            'category_content': self.category_content,
        }

        # def des headers, on envoie du json, dc...
        headers = {'Content-Type': 'application/json'}

        # le certificat SSL du server n'est pas digne de
        # confiance d'apres python
        # verify=False:
        # permet de ne pas verifier le certificat SSL
        # 1 approche plus sécuritaire serait d'inclure un certificat avec une
        # clé publique émise par une authorité de certification
        # of the certificate authority (which has signed the server
        # exemple:
        # response = requests.post(url, data=json.dumps(data), headers=headers, verify='/path/to/certfile')
        # il faut aussi verifier si le certificat SSL est au
        # format PEM, sinon, il faudra le convertir en PEM
        response = requests.post(url,
                                 data=json.dumps(data),
                                 headers=headers,
                                 verify=False)

        # données renvoyés par SF
        response_data = response.json()

        # display the appropriate message based on the response status
        if response_data['status'] == "Success":
            # clear the window
            self.clear_window()
            self.display_message("Your comment is now under moderation status. Thank you.")
        else:
            # clear the window
            self.clear_window()
            self.display_message("A problem occurred, you can contact us via the website. Thank you.")

    # =========================================================================

    def prepareGUI(self):

        # create a label widget for title
        self.label_title = tk.Label(self.window, text="Please enter a title for your comment:")
        self.label_title.grid(row=0, column=0, padx=50, pady=10, sticky='w')

        # create an Entry widget for title input
        self.title_comment = tk.Entry(self.window, width=50)
        self.title_comment.grid(row=1, column=0, padx=50, pady=10, sticky='w')

        # create a label widget
        self.label_instruction = tk.Label(self.window, text="Please, write your comment:")
        self.label_instruction.grid(row=2, column=0, padx=50, pady=10, sticky='w')

        # create a Text widget for multi-line input
        self.text_comment = tk.Text(self.window, width=50, height=10)
        self.text_comment.grid(row=3, column=0, padx=50, pady=10, sticky='w')

        # create a label widget for category
        self.label_category = tk.Label(self.window, text="Please choose a category for your post:")
        self.label_category.grid(row=4, column=0, padx=50, pady=10, sticky='w')

        # create a Combobox widget for category selection
        self.category_comment = ttk.Combobox(self.window, width=50, values=["Character", "Improvements"])
        self.category_comment.grid(row=5, column=0, padx=50, pady=10, sticky='w')

        # create a button widget
        self.button_post_comment = tk.Button(self.window, text="Post comment", command=self.post)
        self.button_post_comment.grid(row=6, column=0, padx=50, pady=10, sticky='w')

        # create a button widget for going back to the main menu
        self.button_go_back = tk.Button(self.window, text="Go back to main menu", command=self.go_back)
        self.button_go_back.grid(row=7, column=0, padx=50, pady=10, sticky='w')

        # run the tkinter main loop
        self.window.mainloop()


if __name__ == '__main__':
    connectToPost = ConnectToPost()
    connectToPost.prepareGUI()
