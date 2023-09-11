
# permet de connaitre ds 1 liste d'elts (des fichiers ds 1 dossier)
# - l'elt courant sur lequel l'instance de la classe pointe
# - l'elt précedent
# - le prochain elt
class FileProcessor:
    def __init__(self, file_list):
        self.file_list = file_list
        self.current_index = 0

    def process_next(self):
        if self.current_index < len(self.file_list) - 1:
            print(f"Previous element is {self.file_list[self.current_index]}, current element is {self.file_list[self.current_index + 1]}, next element is {self.file_list[min(self.current_index + 2, len(self.file_list) - 1)] if self.current_index + 2 < len(self.file_list) else 'No next element'}")
            self.current_index = min(self.current_index + 1, len(self.file_list) - 1)
        else:
            print(f"Previous element is {self.file_list[self.current_index - 1]}, current element is {self.file_list[self.current_index]}, no next element")

    def process_previous(self):
        if self.current_index > 0:
            self.current_index = max(self.current_index - 1, 0)
            print(f"Previous element is {self.file_list[max(self.current_index - 1, 0)] if self.current_index > 0 else 'No previous element'}, current element is {self.file_list[self.current_index]}, next element is {self.file_list[self.current_index + 1]}")
        else:
            print(f"No previous element, current element is {self.file_list[self.current_index]}, next element is {self.file_list[self.current_index + 1]}")

    def process_next_v2(self, liste_fichiers, p_current_element):
        try:
            current_index = liste_fichiers.index(p_current_element)
            previous_element = liste_fichiers[current_index - 1] if current_index > 0 else 'No previous element'
            current_element = liste_fichiers[current_index]
            next_element = liste_fichiers[current_index + 1] if current_index < len(liste_fichiers) - 1 else 'No next element'

            print(f"Previous element is {previous_element}, current element is {current_element}, next element is {next_element}")
            return previous_element, current_element, next_element
        except ValueError:
            print("--The provided element is not in the list.")
            return None

    def process_previous_v2(self, liste_fichiers, p_current_element):
        try:
            current_index = liste_fichiers.index(p_current_element)
            previous_element = liste_fichiers[current_index - 1] if current_index > 0 else 'No previous element'
            current_element = liste_fichiers[current_index]
            next_element = liste_fichiers[current_index + 1] if current_index < len(liste_fichiers) - 1 else 'No next element'

            print(f"Previous element is {previous_element}, current element is {current_element}, next element is {next_element}")
            return previous_element, current_element, next_element
        except ValueError:
            print("-The provided element is not in the list.")
            return None

