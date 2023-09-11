<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;

use Doctrine\ODM\MongoDB\DocumentManager;
use App\Document\Game;
use App\Document\User;


class TestPythonRenderMapToPythonController extends AbstractController
{
    #[Route('/test_python_render_map_to_python', name: 'app_test_python_render_map_to_python')]
    public function index(Request $request,
                          DocumentManager $dm): JsonResponse
    {

        // ====================================================================

        // Check for an existing token in the request headers
        $authorizationHeader = $request->headers->get('Authorization');
        if (!empty($authorizationHeader) && strpos($authorizationHeader, 'Bearer') === 0) {
            $existingToken = substr($authorizationHeader, 7);
            if (!empty($existingToken)) {
                return new JsonResponse([
                    'status' => 'Error',
                    'message' => 'A token already exists',
                ]);
            }
        }

        // ====================================================================

        // Get JSON content from the request
        $data = json_decode($request->getContent(), true);

        // ====================================================================

        if(!isset($data['game_name'], $data['name'])) {
            return new JsonResponse('Invalid data', 400);
        }

        $gameName = $data['game_name'];
        $name = $data['name'];

        // Get the game document from the database
        $gameDocument = $dm->createQueryBuilder(Game::class)
            ->field('game_name')->equals($gameName)
            ->field('name')->equals($name)
            ->getQuery()
            ->getSingleResult();

        // If no document was found return an error message
        if (!$gameDocument) {
            return new JsonResponse('No game found', 404);
        }

        // Convert the document to an array
        $gameArray = $gameDocument->toArray();

        //
        $user = $dm->getRepository(User::class)->findBy([
            'nickname' => $data['user_nickname'],
            'tokenForPython' => $data['user_tokenForPython'],
        ]);

        $userCount = count($user);

        if($userCount === 1) {
            $userArray = array(
                'id' => $user[0]->getId(),
                'nickname' => $user[0]->getNickname(),
                'email' => $user[0]->getEmail(),
                'password' => $user[0]->getPassword(),
                'roles' => $user[0]->getRoles(),
                'is_verified' => $user[0]->getIsVerified(),
                'is_new' => $user[0]->getIsNew(),
                'token' => $user[0]->getToken(),
                'tokenExpiration' => $user[0]->getTokenExpiration(),
                'tokenForPython' => $user[0]->getTokenForPython(),
                'tokenForPythonExpiration' => $user[0]->getTokenForPythonExpiration(),
                // add here other properties you need
            );

            $responseData = [
                'status' => 'Success',
                'message' => 'One user has the given nickname',
                'user' => $userArray,
                'gameArray' => $gameArray,
            ];

        }
        elseif($userCount === 0){
            $responseData = [
                'status' => 'Fail',
                'message' => 'No document corresponding to user collection from mongo database',
            ];
        }
        else {
            $responseData = [
                'status' => 'Fail',
                'message' => 'More than 1 corresponding to user collection from mongo database',
            ];
        }

        // ====================================================================

        return new JsonResponse($responseData);
        
    }
}
