<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Document\User;

class TestPythonController extends AbstractController
{
    #[Route('/test_python', name: 'app_test_python')]
    public function index(Request $request,
                          DocumentManager $dm): JsonResponse
    {

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

        // get datas from Python Client
        $data = json_decode($request->getContent(), true);

        // ====================================================================

        // les données reçues depuis le client python pr savoir s'il y a correspondance
        // elles st partagées par SF et PYTHON
        // Ce st les données que reçoit le controller

        // envoyé par le client python apres qu'il ait lu, stocké la clé
        // 'user_nickname' du credentials.json
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

            $responseData = [
                'status' => 'Success',
                'message' => 'One user has the given nickname',
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
