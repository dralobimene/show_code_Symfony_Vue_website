<?php
// fichier: src/Controller/ModerateNewSpecificUserStep2Controller.php
// agit sur la DB
// vue associée: src/views/view20_adm_moderate_new_specific_user.vue

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

use Symfony\Component\HttpFoundation\Request;
use App\Document\User;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Service\JWTService;

/*
 * fichier: src/Controller/ModerateNewSpecificCommentStep2Controller.php
 * agit sur la DB
 * vue associée: aucune, agit dur la DB
 */
#[Route('/adm')]
class ModerateNewSpecificUserStep2Controller extends AbstractController
{
    #[Route('/moderate_new_specific_user_step2',
            name: 'app_moderate_new_specific_user_step2',
            methods: ['POST'])]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm): JsonResponse
    {

        // ====================================================================

        //        
        $authHeader = $request->headers->get('Authorization');

        //
        $token = substr($authHeader, 7);

        // ====================================================================

        if (!$jwt->validate($token, $this->getParameter('app.jwtsecret'))) {
            return new JsonResponse(['operation1' => 'Check token',
                                    'status1' => 'Error, stopped',
                                    'message1' => 'Invalid token'
                                    ]);
        }

        // ====================================================================

        // Get the userId and action values from the request body
        $data = json_decode($request->getContent(), true);
        $userId = $data['userId'] ?? null;
        $action = $data['action'] ?? null;
        
        // Find the user using the userId
        $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);

        // ====================================================================

        if (!$user) {
            return new JsonResponse(['status' => 'Error, stopped',
                                     'message' => 'User not found']);
        }

        // ====================================================================

        // Perform the required action based on the value of $action
        if ($action === 'accept') {
            $user->setIsNew(false);
            $dm->persist($user);
        } elseif ($action === 'refuse') {
            $dm->remove($user);
        } else {
            return new JsonResponse(['status' => 'Error, stopped',
                                     'message' => 'Invalid action']);
        }

        // Save the changes
        $dm->flush();

        // ====================================================================

        // Return a JsonResponse with the action result
        return new JsonResponse(['status' => 'Success',
                                 'message' => "User {$action}ed"]);

        // ====================================================================

    }
}
