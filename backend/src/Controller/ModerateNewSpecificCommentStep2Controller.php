<?php
// fichier: src/Controller/ModerateNewSpecificCommentStep2Controller.php
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
 * fichier: src/Controller/ModerateNewSpecificCommentStep2Controller.php
 * vue associée: aucune, agit dur la DB
 */
#[Route('/adm')]
class ModerateNewSpecificCommentStep2Controller extends AbstractController
{
    #[Route('/moderate_new_specific_comment_step2',
            name: 'app_moderate_new_specific_comment_step2',
            methods: ['POST'])]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm): JsonResponse
    {

        // ====================================================================

        // get header Authorization
        $authHeader = $request->headers->get('Authorization');

        // supprimer le bearer du header
        $token = substr($authHeader, 7);

        // ====================================================================

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

        // ====================================================================

        // Get the commentId and action values from the request body
        $data = json_decode($request->getContent(), true);
        
        //
        $commentId = $data['commentId'] ?? null;
        
        //
        $action = $data['action'] ?? null;

        // ====================================================================

        // Find the comment using the commentId
        $comment = $dm->getRepository(Comment::class)->findOneBy(['_id' => $commentId]);

        // ====================================================================

        if (!$comment) {
            return new JsonResponse(['status' => 'Error, stopped',
                                     'message' => 'Comment not found']);
        }

        // ====================================================================

        // Perform the required action based on the value of $action
        if ($action === 'accept') {
            $comment->setIsPublished(true);
            $comment->setIsNew(false);
            $comment->setFlag("Modéré, accepté");
            // le champs published_at n'existe pas à l'origine
            // ds les documents comment. ci-dessous, on cree et
            // parametre ce nouvel attribut
            $comment->setPublishedAt(new \DateTime());
        } elseif ($action === 'refuse') {
            $comment->setIsPublished(false);
            $comment->setIsNew(false);
            $comment->setFlag("Modéré, refusé");
        } else {
            return new JsonResponse(['status' => 'Error, stopped',
                                     'message' => 'Invalid action']);
        }

        // ====================================================================

        // Save the changes
        $dm->persist($comment);
        $dm->flush();

        // ====================================================================

        // Return a JsonResponse with the action result
        return new JsonResponse(['status' => 'Success',
                                 'message' => "Comment {$action}ed"]);

        // ====================================================================

    }
}
