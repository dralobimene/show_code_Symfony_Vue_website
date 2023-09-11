<?php

// fichier: src/Controller/ModerateNewCommentsStep2Controller.php
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
 * fichier: src/Controller/ModerateNewCommentsStep2Controller.php
 * vue associée: aucune, agit dur la DB
 */
#[Route('/adm')]
class ModerateNewCommentsStep2Controller extends AbstractController
{
    #[Route('/moderate_new_comments_step2', name: 'app_moderate_new_comments_step2', methods: ['POST'])]
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

        // ====================================================================
        
        // Loop through the payload and update attributes you wish
        foreach ($payload as $commentId => $action) {
            // Fetch the comment by ID
            $comment = $dm->getRepository(Comment::class)->findOneBy(['_id' => $commentId]);

            if ($comment) {
                // Update the flag attribute based on the action
                $comment->setFlag($action === "accept" ? 'Modéré, accepté' : 'Modéré, refusé');
                // Update the publishedAt attribute based on the action
                $comment->setPublishedAt($action === "accept" ? new \DateTime() : null);
                //
                $comment->setIsNew($action === "accept" ? false : false);
                //
                $comment->setIsPublished($action === "accept" ? true : false);

                // 
                $dm->persist($comment);
            }
        }

        // ====================================================================

        // Flush the changes to the database
        $dm->flush();

        // ====================================================================

        // Get the count of unmanaged comments
        $unmanagedCommentsCount = $dm->getRepository(Comment::class)->count(['is_new' => true]);

        // ====================================================================

        return new JsonResponse([
            'operation1' => 'Update comments records to DB',
            'status1' => 'Success',
            'payload' => $payload,
            'unmanagedCommentsCount' => $unmanagedCommentsCount,
         ]);

        // ====================================================================

    }
}
