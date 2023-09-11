<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

class SymfonyTestController extends AbstractController
{
    #[Route('/symfony_test', name: 'app_symfony_test')]
    public function index(): JsonResponse
    {
        $jsonObject = '{"name": "ZOZ", "lastname": "Doe"}';
		    $response = new JsonResponse($jsonObject, 200, [], true);

		    return $response;
    }
}
