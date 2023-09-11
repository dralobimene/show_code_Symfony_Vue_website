<?php
// fichier: src/Controller/ModerateNewUsersStep2Controller.php
// vue associée: aucune, agit dur la DB
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
 * fichier: src/Controller/ModerateNewUsersStep2Controller.php
 * vue associée: aucune, agit dur la DB
 */
#[Route('/adm')]
class ModerateNewUsersStep2Controller extends AbstractController
{
    #[Route('/moderate_new_users_step2', name: 'app_moderate_new_users_step2', methods: ['POST'])]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm): JsonResponse
    {

        // ====================================================================
        
        $authHeader = $request->headers->get('Authorization');
        $token = substr($authHeader, 7);

        // ====================================================================

        if (!$jwt->validate($token, $this->getParameter('app.jwtsecret'))) {
            return new JsonResponse(['operation1' => 'Check token',
                                    'status1' => 'Error, stopped',
                                    'message1' => 'Invalid token'
                                    ]);
        }

        // ====================================================================

        // Get the JSON payload from the request
        $payload = json_decode($request->getContent(), true);

        // ====================================================================

        // Loop through the payload and update attributes you wish
        foreach ($payload as $userId => $action) {

            // Fetch the user by ID
            $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);

            if ($user) {
                if ($action === "accept") {
                    $user->setIsNew(false);
                    $dm->persist($user);
                } elseif ($action === "refuse") {
                    $user->setIsNew(false);
                    $dm->persist($user);
                }
            } else {
                return new JsonResponse(['operation1' => 'Check token',
                                    'status1' => 'Error, stopped',
                                    'message1' => 'No user found'
                                    ]);
            }
            
        }

        // ====================================================================

        // Flush the changes to the database
        $dm->flush();

        // ====================================================================

        // Get the count of unmanaged user
        $unmanagedUsersCount = $dm->getRepository(User::class)->count(['is_new' => true]);

        // ====================================================================

        return new JsonResponse([
            'operation1' => 'Update users records to DB',
            'status1' => 'Success',
            'payload' => $payload,
            'unmanagedUsersCount' => $unmanagedUsersCount,
         ]); 
    }

        // ====================================================================

}
