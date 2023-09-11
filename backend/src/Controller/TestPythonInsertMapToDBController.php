<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Filesystem\Filesystem;

use Doctrine\ODM\MongoDB\DocumentManager;
use App\Document\Game;


class TestPythonInsertMapToDBController extends AbstractController
{
    #[Route('/test_python_insert_map_to_db', name: 'app_test_python_insert_map_to_db')]
    public function index(Request $request,
                          DocumentManager $dm): JsonResponse
    {

        // sert à l'ecriture des fichiers, la sect° + bas qui est commentée'
        $filesystem = new Filesystem();

        // Get JSON content from the request
        $data = json_decode($request->getContent(), true);

        // You can now access the data from the Python script
        $game_name = $data['game_name'];
        $name = $data['name'];
        $level = $data['level'];
        $exit_tile = $data['exit_tile'];
        $entry_tile = $data['entry_tile'];
        $white_tiles_array = $data['white_tiles_array'];
        $blue_tiles_array = $data['blue_tiles_array'];
        $total_tiles_array = $data['total_tiles_array'];
        $rooms_tiles_array = $data['rooms_tiles_array'];
        $attributes_rooms_array = $data['attributes_rooms_array'];

        // TODO: Insert data into database
        // Create a new Game object
        $game = new Game($game_name,
                         $name,
                         $level,
                         $exit_tile,
                         $entry_tile,
                         $white_tiles_array,
                         $blue_tiles_array,
                         $total_tiles_array,
                         $rooms_tiles_array,
                         $attributes_rooms_array);

        // Persist and flush the Game to the database
        $dm->persist($game);
        $dm->flush();

        // ====================================================================
        
        // pr verifier que les documents inséres ds la collection game
        // de la mongo DB sont corrects
        // Save the game instance data to a JSON file
        $jsonData = json_encode($game->toArray(), JSON_PRETTY_PRINT);
        $filesystem->dumpFile(__DIR__.'/../../CR/'.$game_name.'_'.$name.'.json', $jsonData);

        // Get all Game documents
        $repository = $dm->getRepository(Game::class);
        $games = $repository->findAll();

        // Loop through each Game and write it to a separate file
        foreach ($games as $game) {
            // Convert Game document to array then to JSON
            $jsonData = json_encode($game->toArray(), JSON_PRETTY_PRINT);

            // Determine file name
            $fileName = $game->getGameName() . '_' . $game->getName() . '.json';

            // Write JSON to file
            $filesystem->dumpFile(__DIR__ . '/../../CRfrommongo/' . $fileName, $jsonData);
        }        
        

        return new JsonResponse('Data received successfully');
        
    }
}
