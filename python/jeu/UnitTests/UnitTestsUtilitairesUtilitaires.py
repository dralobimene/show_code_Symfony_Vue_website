import unittest
import os
from unittest.mock import patch
from utilitaires import Utilitaires


class TestSortByNumericPart(unittest.TestCase):
    """
    Classe de test pour la méthode statique sort_by_numeric_part de la classe Utilitaires.
    Cette classe hérite de la classe unittest.TestCase qui fournit les méthodes de test.
    """

    def setUp(self):
        """
        Méthode appelée avant chaque test.
        Non nécessaire ici, mais incluse pour être complet.
        """

        pass

    def test_sort_by_numeric_part_valid(self):
        """
        Teste la méthode sort_by_numeric_part avec un nom de fichier valide.
        On s'attend à ce que la méthode retourne la partie numérique du nom de fichier.
        """

        filename = "prefix_123_suffix.extension"
        result = Utilitaires.sort_by_numeric_part(filename)
        # The numeric part is 123
        self.assertEqual(result, 123)

    def test_sort_by_numeric_part_no_numeric(self):
        """
        Teste la méthode sort_by_numeric_part avec un nom de fichier qui
        ne contient pas de partie numérique
        On s'attend à ce que la méthode lève une ValueError.
        """

        filename = "prefix_suffix.extension"
        # we expect a ValueError
        with self.assertRaises(ValueError):
            result = Utilitaires.sort_by_numeric_part(filename)

    def test_sort_by_numeric_part_empty(self):
        """
        Teste la méthode sort_by_numeric_part avec une chaîne de caractères vide.
        On s'attend à ce que la méthode lève une IndexError.
        """

        filename = ""
        # Empty string, so we expect an IndexError
        with self.assertRaises(IndexError):
            result = Utilitaires.sort_by_numeric_part(filename)

    def test_sort_by_numeric_part_multiple_underscores(self):
        """
        Nous nous attendons à ce qu'une exception ValueError soit levée,
        car 'extra' n'est pas un nombre.
        """

        filename = "prefix_extra_123_suffix.extension"
        # we expect a ValueError as 'extra' is not a number
        with self.assertRaises(ValueError):
            result = Utilitaires.sort_by_numeric_part(filename)


class TestGetFileNumber(unittest.TestCase):
    """
    Classe de test pour la méthode statique get_file_number de la classe Utilitaires.
    Cette classe hérite de la classe TestCase du module unittest.
    """

    def test_get_file_number_valid(self):
        """
        Teste si la méthode get_file_number peut extraire correctement le numéro du nom de fichier
        lorsque le chemin du fichier est valide.
        """

        file_path = "/some/path/prefix_123_suffix.extension"
        result = Utilitaires.get_file_number(file_path)
        # The file number is 123
        self.assertEqual(result, 123)

    def test_get_file_number_no_number(self):
        """
        Teste si la méthode get_file_number lève une ValueError
        lorsque le nom du fichier ne contient pas de numéro.
        """

        file_path = "/some/path/prefix_suffix.extension"
        # No number in filename, so we expect a ValueError
        with self.assertRaises(ValueError):
            result = Utilitaires.get_file_number(file_path)

    def test_get_file_number_empty(self):
        """
        Teste si la méthode get_file_number lève une IndexError
        lorsque le chemin du fichier est une chaîne vide.
        """

        file_path = ""
        # Empty string, so we expect an IndexError
        with self.assertRaises(IndexError):
            result = Utilitaires.get_file_number(file_path)

class TestChooseRandomElementsFromArray(unittest.TestCase):
    """
    Classe pour tester la méthode `choose_random_elements_from_array` de la classe `Utilitaires`.
    """

    @patch('random.choice', return_value=5)
    def test_choose_random_elements_from_array(self, mock_random):
        """
        Méthode pour tester `choose_random_elements_from_array`.
        Elle vérifie si la longueur de `chosen_elements` est égale à `iterations` et
        si tous les éléments dans `chosen_elements` sont dans `array` et sont égaux à 5
        (la valeur retournée par le mock de `random.choice`).
        """

        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        iterations = 1
        chosen_elements = Utilitaires.choose_random_elements_from_array(array, iterations)

        self.assertEqual(len(chosen_elements), iterations)
        for element in chosen_elements:
            self.assertEqual(element, 5)
            self.assertTrue(element in array)


if __name__ == '__main__':
    unittest.main()
