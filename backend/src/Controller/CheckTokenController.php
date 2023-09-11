<?php
// fichier: src/Controller/CheckTokenController.php
// vue associée: src/views/view03_check_token.vue

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

use App\Document\User;
use App\Service\JWTService;
use Doctrine\ODM\MongoDB\DocumentManager;

class CheckTokenController extends AbstractController
{
    #[Route('/check_token/{token}', name: 'app_check_token', methods: ["GET"])]
    public function index($token,
                            JWTService $jwt,
                            DocumentManager $dm): JsonResponse
    {

        // on implemente les differentes verifs du jwt token
        if($jwt->isValid($token) && !$jwt->isExpired($token) && $jwt->check($token, $this->getParameter('app.jwtsecret')))
        {
            // on recupere le payload
            $payload = $jwt->getPayload($token);

            // on recupere le user qui est defini ds le token
            $user = $dm->getRepository(User::class)->find($payload['user_id']);

            // on stocke les attributs de cet user ds 1 tableau
            // grace a la methode toArray definie ds le document
            $userData = $user ? $user->toArray() : null;

            // on met a jour l'attribut is_verified à true
            if ($user && $user->getIsVerified()== false) {
                $user->setIsVerified(true);
                $dm->flush();

                // Update the $userData array after updating the is_verified attribute
                $userData = $user->toArray();
            }

            // store les 3 parties du token, la jwtsecret, les attributs de ce user
            $data = [
                "route" => "check_token/{token}",
                "valeur_token" => $token,
                "isValid" => $jwt->isValid($token),
                "payload" => $jwt->getPayload($token),
                "isExpired" => $jwt->isExpired($token),
                "check" => $jwt->check($token, $this->getParameter('app.jwtsecret')),
                "user" => $userData
        ];

            // ===============================================================

            return new JsonResponse(['valid' => true,
                                    'message' => 'CONGRATULATIONS',
                                    'token' => $token]);
        }

        // Au moins 1 des condition de la verif n'est pas passée
        return new JsonResponse(['valid' => false,
                                'message' => 'SORRY, you did not confirm your email']);
	    
        
        
    }
}
