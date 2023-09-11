<?php
// fichier: src/Controller/ModerateNewReplyStep2Controller.php
// agit sur la DB
// vue associée: src/views/view16_adm_moderate_new_reply.vue

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
 * fichier: src/Controller/ModerateNewReplyStep2Controller.php
 * agit sur la DB
 * vue associée: src/views/view16_adm_moderate_new_reply.vue
 */
#[Route('/adm')]
class ModerateNewReplyStep2Controller extends AbstractController
{
    #[Route('/moderate_new_reply_step2', name: 'app_moderate_new_reply_step2')]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm): JsonResponse
    {
        
        // ====================================================================

        // get header Authorization  
        $authHeader = $request->headers->get('Authorization');

        // supprimer le bearer du header
        $token = substr($authHeader, 7);

        // token validation
        // call method from src/Service/JWTService
        // -- methode: validate()
        // itself calls
        // -- method: isValid()
        // -- method: isExpired()
        // -- method: check()
        if (!$jwt->validate($token, $this->getParameter('app.jwtsecret'))) {
            return new JsonResponse(['operation1' => 'Check token',
                                    'status1' => 'Error, stopped',
                                    'message1' => 'Invalid token'
                                    ]);
        }

        // decoder le token et récupérer le payload
        $payload = $jwt->decode($token, $this->getParameter('app.jwtsecret'));

        // Fetch connected user data based on the user_id from the payload
        $userId = $payload['user_id'];

        // Fetch user data based on the user_id from the payload
        $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);

        // ====================================================================

        // Get the JSON payload from the request
        $payload = json_decode($request->getContent(), true);

        // Get the replyId from the payload
        $replyId = $payload['replyId'];

        // Get the action from the payload
        $action = $payload['action'];

        // ====================================================================
        //
        // If the connected user is not found, return an error
        if (!$user) {
            return new JsonResponse(['operation' => 'check user',
                                    'status' => 'Error, stopped',
                                    'message' => 'User not found',
                                    ]);
        }

        // ====================================================================

        // Process the action
        if ($action === 'accept') {
            // Perform accept action
            // Find the reply in the database using the DocumentManager
            $reply = $dm->getRepository(Comment::class)->findOneBy(['_id' => $replyId]);
            
            if ($reply) {
                // Update the reply attributes
                $reply->setPublishedAt(new \DateTime());
                $reply->setFlag('Modéré, accepté');
                $reply->setIsPublished(true);
                $reply->setIsNew(false);

                // Persist the changes and flush the DocumentManager
                $dm->persist($reply);
                $dm->flush();
            }

            $message = 'Reply ID accepted: ' . $replyId;

        } elseif ($action === 'refuse') {
            // Perform refuse action
            // Find the reply in the database using the DocumentManager
            $reply = $dm->getRepository(Comment::class)->findOneBy(['_id' => $replyId]);
            
            if ($reply) {
                // Update the reply attributes
                $reply->setFlag('Modéré, refusé');
                $reply->setIsNew(false);

                // Persist the changes and flush the DocumentManager
                $dm->persist($reply);
                $dm->flush();
            }

            $message = 'Reply ID refused: ' . $replyId;
        } else {
            $message = 'Invalid action';
        }

        // ====================================================================

        return new JsonResponse([
            'operation1' => 'Check token',
            'status1' => 'Success',
            'message1' => 'Reply ID processed: ' . $replyId . ' Message: ' . $message
        ]);

    }

        // ====================================================================

}
