
import pygame
import pygame_gui


class SubMenu1_inventory:
    def __init__(self, surface, manager, main_menu):
        self.manager = manager
        self.menu_surface = surface
        self.main_menu = main_menu
        self.panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((800, 0), (200, 800)),
                                        manager=self.manager)

        #
        self.rebuild()

        #
        self.active = True

    def rebuild(self):

        self.button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 100), (190, 50)),
                                                    text='Inventory: Back to main menu',
                                                    manager=self.manager,
                                                    container=self.panel)
    def handle_event(self, event):

        if not self.active:
            return

        # Create a new UIManager
        self.manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button1:
                    print("Button1 to go back to main menu")
                    print("from SubMenu1_inventory.py")
                    self.button1.kill()

                    # menu qui devient inactif
                    self.active = False

                    # le main menu devient actif
                    self.main_menu.active = True

                    #
                    self.main_menu.rebuild()

    def draw(self, surface):

        if not self.active:
            return

        # draw the menu_surface onto surface
        surface.blit(self.menu_surface, (0, 0))

        #
        self.manager.update(pygame.time.get_ticks() / 1000.0)

        self.manager.draw_ui(surface)
