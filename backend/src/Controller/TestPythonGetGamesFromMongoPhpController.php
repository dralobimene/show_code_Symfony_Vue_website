<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Document\Game;
use App\Document\User;

class TestPythonGetGamesFromMongoPhpController extends AbstractController
{
    #[Route('/test_python_get_games_from_mongo_php', name: 'app_test_python_get_games_from_mongo_php')]
    public function index(Request $request,
                          DocumentManager $dm): JsonResponse
    {
        // Get JSON content from the request
        $data = json_decode($request->getContent(), true);

        // Find documents in 'user' collection with matching 'nickname' and 'tokenForPython'
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

            // Get collection
            $collection = $dm->getDocumentCollection(Game::class);

            // Get distinct id values
            $distinctIds = $collection->distinct('game_name');

            // Get count of unique _id
            $distinctCount = count($distinctIds);

            $responseData = [
                'status' => 'Success',
                'count' => $distinctCount,
                'distinctIds' => $distinctIds,
                'user' => $userArray,
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

        return new JsonResponse($responseData);
    }
}
