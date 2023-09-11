<?php
// fichier: src/Controller/ModerateNewUserStep2Controller.php
// vue associée: aucune, agit sur la DB

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

use Symfony\Component\HttpFoundation\Request;
use App\Document\Comment;
use App\Document\User;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Service\JWTService;

/*
 * fichier: src/Controller/ModerateNewUserStep2Controller.php
 * vue associée: aucune, agit dur la DB
 */
#[Route('/adm')]
class ModerateNewUserStep2Controller extends AbstractController
{
    #[Route('/moderate_new_user_step2', name: 'app_moderate_new_user_step2', methods: ['POST'])]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm): JsonResponse
    {
        
        // ====================================================================
        
        $authHeader = $request->headers->get('Authorization');
        $token = substr($authHeader, 7);

        if (!$jwt->validate($token, $this->getParameter('app.jwtsecret'))) {
            return new JsonResponse(['operation1' => 'Check token',
                                    'status1' => 'Error, stopped',
                                    'message1' => 'Invalid token'
                                    ]);
        }

        // Get the JSON payload from the request
        $payload = json_decode($request->getContent(), true);

        // Get the commentId from the payload
        $userId = $payload['userId'];

        // Get the action from the payload
        $action = $payload['action'];

        // ====================================================================

        // Process the action
        if ($action === 'accept') {
            // Perform accept action
            // Find the user in the database using the DocumentManager
            $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);
            
            if ($user) {
                // Update the user attributes
                $user->setIsNew(false);

                // Persist the changes and flush the DocumentManager
                $dm->persist($user);
                $dm->flush();
            }

            $message = 'User ID accepted: ' . $userId;
        } elseif ($action === 'refuse') {
            // Perform refuse action
            // Find the user in the database using the DocumentManager
            $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);
            
            if ($user) {
                // Remove the user from the database
                $dm->remove($user);
                $dm->flush();
            }

            $message = 'User ID refused and removed: ' . $userId;
        } else {
            $message = 'Invalid action';
        }

        // ====================================================================

        return new JsonResponse([
            'operation1' => 'Check token',
            'status1' => 'Success',
            'message1' => 'User ID processed: ' . $userId . ' Message: ' . $message
        ]);

    }
}
