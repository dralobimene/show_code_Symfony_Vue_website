<?php
// fichier: src/Controller/LogoutController.php
// vue associée: src/views/view06_logout.vue

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpKernel\Exception\AccessDeniedHttpException;

use Symfony\Component\HttpFoundation\Request;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Service\JWTService;
use App\Document\User;

class LogoutController extends AbstractController
{
    #[Route('/logout', name: 'app_logout')]
    public function logout(Request $request,
                            JWTService $jwt,
                            DocumentManager $dm): JsonResponse
    {

        // ====================================================================


        try {

            // ====================================================================

            // entête authorization du header
            $authHeader = $request->headers->get('Authorization');

            // supprimer le bearer du header
            $token = substr($authHeader, 7);

            // Processus de validation du token
            // Applelle la methode depuis src/Service/JWTService
            // -- methode: validate()
            // qui elle-même
            // -- method: isValid()
            // -- method: isExpired()
            // -- method: check()
            if (!$jwt->validate($token, $this->getParameter('app.jwtsecret'))) {
                return new JsonResponse(['operation1' => 'Check token',
                                        'status1' => 'Error, stopped',
                                        'message1' => 'Invalid token'
                                        ]);
            }

            // ====================================================================

            // Token is valid at this point
            $payload = $jwt->decode($token, $this->getParameter('app.jwtsecret'));
            
            // Fetch user data based on the user_id from the payload
            $userId = $payload['user_id'];

            // Fetch user data based on the user_id from the payload
            $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);

            // ====================================================================

            // if connected user not found, return an error 
            // erreur, voir view 06: nbre de clé: 6
            if (!$user) {
                return new JsonResponse(['operation1' => 'Check token',
                                        'status1' => 'Success',
                                        'message1' => 'Valid token',
                                        'operation2' => 'Check user',
                                        'status2' => 'Error, stopped',
                                        'message2' => 'User not found'
                                        ]);
            }

            // ====================================================================
            
            // erreur, voir view 06, nbre de clé: 10
            if (!$request->isMethod('POST')) {
                return new JsonResponse(['operation1' => 'Check token',
                                        'status1' => 'Success',
                                        'message1' => 'Valid token',
                                        'operation2' => 'Check user',
                                        'status2' => 'Success',
                                        'message2' => 'User found',
                                        'user' => [
                                                'token' => $token,
                                                'id' => $user->getId(),
                                                'nickname' => $user->getNickname(),
                                                'email' => $user->getEmail(),
                                                'password' => $user->getPassword(),
                                                'roles' => $user->getRoles(),
                                                'is_verified' => $user->getIsVerified(),
                                              ],
                                        'operation3' => 'Check request',
                                        'status3' => 'Error, stopped',
                                        'message3' => 'Request not found'
                                        ]);
            }

            // ====================================================================

            // Remove the token from local storage
            $response = new JsonResponse(['status' => 'Success',
                                        'message' => 'Logged out successfully'
                                        ]);

            // delete token
            $response->headers->clearCookie('token');

            //
            return $response;

        //
        } catch (AccessDeniedHttpException $except) {
            // If AccessDeniedException is caught, return JsonResponse with error message
            return new JsonResponse(['error' => 'Access Denied from LogoutController.php',
                                    'message' => $except->getMessage()]);
        }

        // ====================================================================

    }
}
