<?php
// fichier controller: src/Controller/ModerateNewSpecificReplyStep2Controller
// agit directement sur la DB
// vue associée: src/views/view22_adm_moderate_new_specific_reply.vue

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

use Symfony\Component\HttpFoundation\Request;
use App\Service\JWTService;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Document\Comment;
use App\Document\User;

/*
 * fichier: src/Controller/ModerateNewSpecifiReplyController.php
 * agit directement sur la DB
 * vue associée: src/views/view22_adm_moderate_new_specific_reply.vue
 */
#[Route('/adm')]
class ModerateNewSpecificReplyStep2Controller extends AbstractController
{
    #[Route('/moderate_new_specific_reply_step2',
            name: 'app_moderate_new_specific_reply_step2',
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

        // Get the userId and action values from the request body
        $data = json_decode($request->getContent(), true);
        
        //
        $filId = $data['filId'] ?? null;

        //
        $action = $data['action'] ?? null;

        // ====================================================================
        
        // Find the reply (a comment) using the filId
        // call ODM native method
        // -- methode: findOneBy()
        $reply = $dm->getRepository(Comment::class)->findOneBy(['_id' => $filId]);

        // ====================================================================

        // Perform the required action based on the value of $action
        if ($action === 'accept') {
            $reply->setIsNew(false);
            $reply->setIsPublished(true);
            $reply->setFlag("Modéré, accepté");
            // le champs published_at n'existe pas à l'origine
            // ds les documents comment. ci-dessous, on cree et
            // parametre ce nouvel attribut
            $reply->setPublishedAt(new \DateTime());
        } elseif ($action === 'refuse') {
            $reply->setIsNew(false);
            $reply->setIsPublished(false);
            $reply->setFlag("Modéré, refusé");
        } else {
            return new JsonResponse(['status' => 'Error, stopped',
                                     'message' => 'Invalid action']);
        }

        // ====================================================================

        // Save the changes
        $dm->persist($reply);
        $dm->flush();

        // ====================================================================

        // Return a JsonResponse with the action result
        return new JsonResponse(['status' => 'Success',
                                 'message' => "Reply {$action}ed"]);

        // ====================================================================

    }
}
