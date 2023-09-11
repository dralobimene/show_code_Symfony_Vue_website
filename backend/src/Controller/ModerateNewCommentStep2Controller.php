<?php
// fichier: src/Controller/ModerateNewCommentStep2Controller.php
// vue associée: aucune, agit sur la DB

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

use Symfony\Component\HttpFoundation\Request;
use App\Document\Comment;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Service\JWTService;

/*
 * fichier: src/Controller/ModerateNewCommentStep2Controller.php
 * vue associée: aucune, agit sur la DB
 */
#[Route('/adm')]
class ModerateNewCommentStep2Controller extends AbstractController
{
    #[Route('/moderate_new_comment_step2', name: 'app_moderate_new_comment_step2', methods: ['POST'])]
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

        // Get the JSON payload from the request
        $payload = json_decode($request->getContent(), true);

        // Get the commentId from the payload
        $commentId = $payload['commentId'];

        // Get the action from the payload
        $action = $payload['action'];

        // ====================================================================

        // Process the action
        if ($action === 'accept') {
            // Perform accept action
            // Find the comment in the database using the DocumentManager
            $comment = $dm->getRepository(Comment::class)->findOneBy(['_id' => $commentId]);
            
            if ($comment) {
                // Update the comment attributes
                $comment->setPublishedAt(new \DateTime());
                $comment->setFlag('Modéré, accepté');
                $comment->setIsPublished(true);
                $comment->setIsNew(false);

                // Persist the changes and flush the DocumentManager
                $dm->persist($comment);
                $dm->flush();
            }

            $message = 'Comment ID accepted: ' . $commentId;
        } elseif ($action === 'refuse') {
            // Perform refuse action
            // Find the comment in the database using the DocumentManager
            $comment = $dm->getRepository(Comment::class)->findOneBy(['_id' => $commentId]);
            
            if ($comment) {
                // Update the comment attributes
                $comment->setFlag('Modéré, refusé');
                $comment->setIsNew(false);

                // Persist the changes and flush the DocumentManager
                $dm->persist($comment);
                $dm->flush();
            }
            
            $message = 'Comment ID refused: ' . $commentId;
        } else {
            $message = 'Invalid action';
        }

        // ====================================================================

        return new JsonResponse([
            'operation1' => 'Check token',
            'status1' => 'Success',
            'message1' => 'Comment ID processed: ' . $commentId . ' Message: ' . $message
        ]);

        // ====================================================================

    }
}
