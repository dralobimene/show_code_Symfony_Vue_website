import websocket
import json


"""
WebSocketClient

Cette classe représente un client WebSocket. Elle établit une connexion
WebSocket avec un serveur à partir d'une URL spécifiée, reçoit et
analyse les messages JSON, gère les erreurs et les fermetures de connexion,
et peut mettre à jour et afficher les données des joueurs.

Attributs:
-----------
ws : instance de WebSocketApp
    Une instance de l'objet WebSocketApp qui gère la connexion WebSocket.
players : dict
    Un dictionnaire pour stocker les données des joueurs.

Méthodes:
-----------
__init__(self, url: str) -> None:
    Initialise un nouveau client WebSocket avec une URL spécifiée.

on_message(self, ws: WebSocketApp, message: str) -> None:
    Gère la réception d'un message du serveur. Le message est supposé être
    un JSON, qui est alors analysé en un objet Python. Si le type
    d'événement est 'update', les données des joueurs sont mises à jour.

on_error(self, ws: WebSocketApp, error: str) -> None:
    Gère les erreurs de la connexion WebSocket. L'erreur est affichée à l'utilisateur.

on_close(self, ws: WebSocketApp, status_code: int, reason: str) -> None:
    Est appelée lorsque la connexion WebSocket est fermée pour une raison
    quelconque. Elle informe l'utilisateur que la connexion a été fermée.

close(self) -> None:
    Ferme la connexion WebSocket.

on_open(self, ws: WebSocketApp) -> None:
    Est appelée lorsque la connexion WebSocket est établie avec succès.
    Elle informe l'utilisateur que la connexion a été ouverte.

run(self) -> None:
    Démarre le client WebSocket, ce qui signifie qu'elle commence à écouter
    et à envoyer des messages sur la connexion WebSocket.
"""
class WebSocketClient:
    def __init__(self, url):
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open

        # Objet Json pr stocker les attributs des players
        self.players = {}

    def on_message(self, ws, message):
        data = json.loads(message)
        event_type = data.get('event_type')
        if event_type == 'update':
            new_players = data.get('players')
            if new_players != self.players:
                self.players = new_players
                print("'players' array sent from server.ts to WebSocketClient.py")
                print("displayed from WebSocketClient.py")
                print("Received updated player data: {}".format(self.players))
        else:
            print("Received: {}".format(data))

    def on_error(self, ws, error):
        print("Error: {}".format(error))

    def on_close(self, ws, status_code, reason):
        print("Connection closed")

    def close(self):
        self.ws.close()

    def on_open(self, ws):
        print("connection opened")

    def run(self):
        self.ws.run_forever()
