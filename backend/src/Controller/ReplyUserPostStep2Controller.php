<?php
// fichier: src/Controller/ReplyUserPostStep2Controller.php
// vue associée: src/views/view09_replay_user_post.vue

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

use Symfony\Component\HttpFoundation\Request;
use App\Document\Comment;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Service\JWTService;

/*
 * fichier: src/Controller/ReplyUserPostStep2Controller.php
 * vue associée: src/views/view09_reply_user_post.vue
 */
class ReplyUserPostStep2Controller extends AbstractController
{

    #[Route('/reply_user_post_step2', name: 'app_reply_user_post_step2', methods: ['POST'])]
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

        // ====================================================================

        // Get the posted
        $user = json_decode($request->request->get('user'), true);
        $comment = json_decode($request->request->get('comment'), true);
        $additionalData = json_decode($request->request->get('additionalData'), true);

        /*
        PR DEBUGGAGE: permet de connaitre les infos envoyées
        depuis le formulaire de la view09
        */

        /*
        // For now, return the received data as JsonResponse
        // return new JsonResponse("ok");
        return new JsonResponse([
            'user' => $user,
            'comment' => $comment,
            'additionalData' => $additionalData
        ]);
        */

        // ====================================================================

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

        if (!$comment) {
            return new JsonResponse([
                'operation' => 'Find comment',
                'status' => 'Error, stopped',
                'message' => 'Comment not found'
                ]);
        }

        // ====================================================================

        if (!$request->isMethod('POST')) {
            return new JsonResponse([
                'operation' => 'Check request',
                'status' => 'Error, stopped',
                'message' => 'Request is not POST method'
            ]);
        }
        
        // Do something with the data

        // title: data from input field
        $title = $additionalData['title'];
        // content: data from textarea
        $content = $additionalData['content'];
        // category: data from parent comment
        $category = $comment['comment_category'];
        // parent_id: data from parent comment
        $parent_id = $comment['comment_id'];

        // create a new comment object (as reply)
        $reply = new Comment(
                            $user['nickname'],
                            $category,
                            $title,
                            $content
                            );
        $reply->setCreatedAt(new \DateTime());
        $reply->setPublishedAt(null);
        $reply->setFlag('En attente de modération');
        $reply->setIsPublished(false);
        $reply->setParentId($parent_id);
        $reply->setIsNew(true);

        // Persist and flush the reply to the database
        $dm->persist($reply);
        $dm->flush();

        // Return the JsonResponse with the new reply data
        return new JsonResponse([
            'operation' => 'Create reply',
            'status' => 'Success',
            'reply' => [
                'author' => $reply->getAuthor(),
                'category' => $reply->getCategory(),
                'title' => $reply->getTitle(),
                'content' => $reply->getContent(),
                'created_at' => $reply->getCreatedAt(),
                'published_at' => $reply->getPublishedAt(),
                'flag' => $reply->getFlag(),
                'is_published' => $reply->getIsPublished(),
                'parent_id' => $reply->getParentId(),
                'is_new' => $reply->getIsNew(),
            ]
        ]);
         
    }
}
