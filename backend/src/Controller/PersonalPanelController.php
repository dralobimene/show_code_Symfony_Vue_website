<?php
// fichier: src/Controller/PersonalPanelController.php
// vue associée: src/views/view05_secured_user_personal_panel

/*
 * Lorsque vous effectuez une demande vers la route /secured_user/personal_panel,
 * JwtRequestListener vérifie si le jeton JWT est valide et, si c'est le cas,
 * la demande est transmise au PersonalPanelController pour un traitement ultérieur.
 * Si le jeton JWT est invalide ou manquant, JwtRequestListener lèvera une
 * exception, et la demande n'atteindra pas le PersonalPanelController.
 * Dans ce cas, vous recevrez une réponse d'erreur en raison du jeton JWT
 * invalide ou manquant.
 *
 * Ainsi, la validation JWT et JwtRequestListener fonctionnent ensemble.
 * L'écouteur est responsable de valider le jeton JWT pour des routes
 * spécifiques, tandis que le contrôleur gère le traitement des demandes en
 * fonction de la validité du jeton JWT et d'autres paramètres de demande.
*/

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;

use App\Document\User;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Service\JWTService;

/*
 * fichier: src/Controller/PersonalPanelController.php
 * vue associée: src/views/view05_secured_user_personal_panel.vue
 */
#[Route('/secured_user')]
class PersonalPanelController extends AbstractController
{

    
    #[Route('/personal_panel', name: 'app_secured_user_personal_panel')]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm): JsonResponse
    {

        // ========================================================================

        // get header Authorization
        $authHeader = $request->headers->get('Authorization');
        
        // supprimer le bearer du header
        $token = substr($authHeader, 7);

        // ========================================================================

        // token validation
        // call method from src/Service/JWTService
        // -- methode: validate()
        // itself calls
        // -- method: isValid()
        // -- method: isExpired()
        // -- method: check()

        if (!$jwt->validate($token, $this->getParameter('app.jwtsecret'))) {
            return new JsonResponse(['status' => 'Error',
                                    'message' => 'Invalid token'
                                    ]);
        }

        // ========================================================================

        // decoder le token et récupérer le payload
        // fait appel à la methode src/Service/JWTService
        // -- methode: decode()
        $payload = $jwt->decode($token, $this->getParameter('app.jwtsecret'));

        // Fetch connected user data based on the user_id from the payload
        $userId = $payload['user_id'];

        // find connected user with payload defined above
        // call ODM native method
        // -- methode: findOneBy()
        $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);

        // ========================================================================

        // If the user is not found, return an error
        if (!$user) {
            return new JsonResponse(['status' => 'Error',
                                    'message' => 'User not found'
                                    ]);
        }

        // ========================================================================

        $response = [
            'status' => 'Success',
            'message' => 'Secured data',
            'user' => [
                'token' => $token,
                'id' => $user->getId(),
                'nickname' => $user->getNickname(),
                'email' => $user->getEmail(),
                'password' => $user->getPassword(),
                'roles' => $user->getRoles(),
                'is_verified' => $user->getIsVerified(),
                'inscription_date' => $user->getInscriptionDate(),
            ],
        ];

        // ========================================================================
 
        return new JsonResponse($response, 200);

        // ========================================================================

    }
    

    /*
    * Route pr tester le bon fonctionnement du fichier:
    * src/EventListener/JwtRequestListener.php
    * methode: testJwtListener()
    * https://localhost:8000/secured_user/test_jwt_listener
    */
    /*
    #[Route('/test_jwt_listener', name: 'app_test_jwt_listener')]
    public function testJwtListener(): JsonResponse
    {

        // Récupérer le header Authorization
        $authHeader = $request->headers->get('Authorization');

        // Supprimer le "Bearer " du header
        $token = substr($authHeader, 7);

        // Récupérer le payload du token sans effectuer de validation,
        // car JwtRequestListener l'a déjà fait
        $payload = $jwt->decode($token, $this->getParameter('app.jwtsecret'), false);

        // Supposons que vous ayez une condition pour vérifier ici
        $isAdmin = $payload['isAdmin'] ?? false;

        //
        if (!$isAdmin) {
            throw $this->createAccessDeniedException();
        }

        return new JsonResponse([
            'status' => 'Success',
            'message' => 'This route does not require JWT validation'
        ]);
    }
    */

}
