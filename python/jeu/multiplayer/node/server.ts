import WebSocket from 'ws';

/*
* Server Node.js
* etablit les comunications bidirectionelles entre le server et les
* clients python
*/

// les events
// - connect
// - move
// - disconnect
// st des event que reçoit le serveur de la part des clients,
// ce dernier réagit et renvoie un event de type 'update' vers tous
// les clients

// ici on fait du rapide,
// pr qque chose de + propre, il faut creer 1 classe qui soit
// jumelle à la classe python
// définit une interface Player qui a deux propriétés
// playerData de type any et id de type string
interface Player {
  playerData: any;
  id: string;
}

// instance du server
const wss = new WebSocket.Server({ port: 8080 });

// dictionnaire qui doit storer les informations de ts les joueurs.
let players: { [key: string]: Player } = {};

let numClients = 0;

// un client se connecte au server
wss.on('connection', (ws) => {

    console.log(`${new Date()} - A client connected`);

    // Qd un client se connecte, accroît le nbre de clients
    numClients++;

    //
    console.log(`${new Date()} - (v numClients), connect: Number of clients: ${numClients}`);

    // qd un client envoie un message vers le server
    ws.on('message', (message) => {
        const data = JSON.parse(message.toString());
        const eventType = data.event_type;
        const playerData = data.player;

        console.log(`${new Date()} - received eventType: ${eventType}`);

        // les actions selon le type_event
        // le message est de type 'connect'
        switch(eventType) {
            case 'connect':
                console.log(`${new Date()} - message - eventType == ${eventType}`);
                
                // met à jour l'objet players avec les données du joueur
                // (playerData) reçues dans le message du client. L'identifiant
                // du joueur (playerData.id) est utilisé comme clé dans l'objet
                // players. Si le joueur avec cet identifiant existait déjà dans
                // l'objet players, ses données sont remplacées par les nouvelles
                // données. Si le joueur n'existait pas encore, une nouvelle
                // entrée est créée dans l'objet players.
                players[playerData.id] = playerData;

                // parcourt tous les clients actuellement connectés au
                // serveur WebSocket (wss.clients). Pour chaque client,
                // elle vérifie si la connexion WebSocket est ouverte
                // (client.readyState === WebSocket.OPEN). Si la connexion
                // est ouverte, elle envoie un message à ce client. Le message
                // est une chaîne de caractères obtenue en transformant en
                // JSON un objet qui contient le type d'événement
                // (event_type: "update") et l'objet players mis à jour.
                wss.clients.forEach((client) => {
                    if (client.readyState === WebSocket.OPEN) {
                        client.send(JSON.stringify({ event_type: "update", players }));
                    }
                });

                console.log(`${new Date()}`);
                console.log(`(nbre elts tableau), connect: Number of clients: ${players.length}`);
                console.log(`(nbre elts tableau), connect: tableau des players: ${JSON.stringify(players as any)}`);
                
                break;

            // ================================================================
            /*
            // le message est de type 'move'
            case 'move':
                console.log(`${new Date()} - message - eventType == ${eventType}`);

                // met à jour l'objet players avec les données du joueur (playerData) 
                players[playerData.id] = playerData;

                // déclare un eventType "update" vers le client python
                wss.clients.forEach((client) => {
                    if (client.readyState === WebSocket.OPEN) {
                        client.send(JSON.stringify({ event_type: "update", players }));
                    }
                });

                break;
            */
            // ================================================================

            // le message est de type 'disconnect'
            case 'disconnect':
                console.log(`${new Date()} - message - eventType == ${eventType}`);
                
                // Qd un client se déconnecte, décroît le nbre de clients
                numClients--;

                //
                console.log(`(v numClients), disconnect: Number of clients: ${numClients}`);

                //
                delete players[playerData.id];

                console.log(`${new Date()}`);
                console.log(`(nbre elts tableau), disconnect: Number of clients: ${players.length}`);
                console.log(`(nbre elts tableau), disconnect: tableau des players: ${JSON.stringify(players as any)}`);

                // envoie une mise à jour à tous les clients connectés
                // avec la nouvelle liste des joueurs
                // déclare un eventType "update" vers le client python
                wss.clients.forEach((client) => {
                    if (client.readyState === WebSocket.OPEN) {
                        client.send(JSON.stringify({ event_type: "update", players }));
                    }
                });

                break;

            // ================================================================
            
            default:
                console.log(`${new Date()} - Unknown eventType, ${eventType}`);
        }
    });

    /*
    A decommenter: gere le cas ou la connex° internet disparait.
    l'event_type 'disconnect' gere le cas ou c'est l'utilisateur qui coupe
    la connex°
    */

    /*
    ws.on('close', () => {
        
        // When a client disconnects, decrease the counter and log the number of clients
        console.log("-- A client just diconnected")
        numClients--;
        console.log(`-- Number of clients: ${numClients}`);

        // remove the player from the players array on disconnect
        players = players.filter(p => p.ws !== ws);
        console.log(`-- Number of clients: ${players.length}`);
        

    });
    */

});
