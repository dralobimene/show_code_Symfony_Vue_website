import pygame
import pygame_gui

import sys


from utilitaires import EventManager
from classes.SubMenu2_internet import SubMenu2_internet
from classes.SubMenu1_inventory import SubMenu1_inventory


class StartMenuFromSavedGame:
    def __init__(self, surface, manager, event_manager, player):

        #
        self.menu_surface = surface

        #
        self.manager = manager

        #
        self.event_manager = event_manager

        #
        self.panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((800, 0), (200, 800)),
                                        manager=self.manager)

        #
        self.player = None

        #
        self.rebuild()

        #
        self.submenu1_inventory = None

        #
        self.submenu2_internet = None

        #
        self.active = True

    def rebuild(self):

        self.button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 100), (100, 50)),
                                                   text='Internet',
                                                   manager=self.manager,
                                                   container=self.panel)
        self.button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 150), (100, 50)),
                                                   text='Quit',
                                                   manager=self.manager,
                                                   container=self.panel)
        self.button3 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 200), (100, 50)),
                                                   text='Save',
                                                   manager=self.manager,
                                                   container=self.panel)
        self.button4 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 250), (100, 50)),
                                                   text='Inventory',
                                                   manager=self.manager,
                                                   container=self.panel)

    def set_player(self, player):
        self.player = player

    def handle_event(self, event):
        if not self.active:
            return

        self.manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button1:
                    print("")
                    print("Button1 clicked!")
                    print("")

                    self.button1.kill()
                    self.button2.kill()
                    self.button3.kill()
                    self.button4.kill()

                    # ce menu devient inactif
                    self.active = False

                    # Open submenu2
                    self.submenu2_internet = SubMenu2_internet(self.menu_surface,
                                                               self.manager,
                                                               self)

                    # submenu2 devient actif
                    self.submenu2_internet.active = True

                if event.ui_element == self.button2:
                    print("")
                    print("Button2 clicked!")
                    print("on quitte le jeu")
                    print("")

                    self.button1.kill()
                    self.button2.kill()
                    self.button3.kill()
                    self.button4.kill()

                    # ce menu devient inactif
                    self.active = False

                    pygame.quit()
                    sys.exit()

                if event.ui_element == self.button3:
                    print("")
                    print("Button3 clicked! from StartMenuFromSavedGame.py")
                    print("Game saved")
                    print("")
                    print("attributs player depuis StartMenuFromSavedGame.py")
                    print(self.player)

                    self.event_manager.save_game(self.player.to_dict())

                if event.ui_element == self.button4:
                    print("")
                    print("Button4 clicked!")
                    print("go to inventory")
                    print("")

                    self.button1.kill()
                    self.button2.kill()
                    self.button3.kill()
                    self.button4.kill()

                    # ce menu devient inactif
                    self.active = False

                    # Open submenu1
                    self.submenu1_inventory = SubMenu1_inventory(self.menu_surface, self.manager, self)

                    # submenu1 devient actif
                    self.submenu1_inventory.active = True

    def draw(self, surface):

        if not self.active:
            return

        # draw the menu_surface onto surface
        surface.blit(self.menu_surface, (0, 0))

        self.manager.update(pygame.time.get_ticks() / 1000.0)
        self.manager.draw_ui(surface)

        if self.submenu2_internet:
            self.submenu2_internet.draw(surface)

        if self.submenu1_inventory:
            self.submenu1_inventory.draw(surface)
