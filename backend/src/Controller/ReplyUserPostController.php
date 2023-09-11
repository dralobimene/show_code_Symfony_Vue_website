<?php
// fichier: src/Controller/ReplyUserPostController.php
// vue associée: src/views/view09_replay_user_post.vue

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

use Symfony\Component\HttpFoundation\Request;
use App\Document\User;
use App\Document\Comment;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Service\JWTService;

/*
 * fichier: src/Controller/ReplyUserPostController.php
 * vue associée: src/views/view09_reply_user_post.vue
 */
class ReplyUserPostController extends AbstractController
{

    // ========================================================================

    /**
    * Count the number of replies for a given comment.
    *
    * @param DocumentManager $dm     The Document Manager to query comments.
    * @param string          $p_id   The _id of the clicked comment.
    *
    * @return int The number of replies found for the specified comment.
    */
    private function countReplies(DocumentManager $dm, $p_id): int
    {
        $count = 0;
        $allComments = $dm->getRepository(Comment::class)->findAll();

        foreach ($allComments as $comment) {
            if ($comment->getParentId() == $p_id) {
                $count += 1;
            }
        }
        return $count;
    }

    // ========================================================================

    /**
     * Find and store the replies for a given comment.
     *
     * @param DocumentManager $dm     The Document Manager to query comments.
     * @param string          $p_id   The _id of the clicked comment.
     *
     * @return array The replies found for the specified comment.
     */
    private function findReplies(DocumentManager $dm, $p_id): array
    {
        $replies = [];
        $tabRepliesForThisComment = $dm->getRepository(Comment::class)->findAll();

        foreach ($tabRepliesForThisComment as $comment) {
            if ($comment->getParentId() == $p_id) {
                $replies[] = $comment;
            }
        }

        return $replies;
    }

    // ========================================================================

    #[Route('/reply_user_post/{p_id}', name: 'app_reply_user_post', methods: ['GET', 'POST'])]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm,
                          string $p_id): JsonResponse
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

        // decoder le token et récupérer le payload
        // fait appel à la methode src/Service/JWTService
        // -- methode: decode()
        $payload = $jwt->decode($token, $this->getParameter('app.jwtsecret'));

        // Fetch connected user data based on the user_id from the payload
        // call ODM native method
        // -- methode: findOneBy()
        $userId = $payload['user_id'];
        
        // find connected user with payload defined above
        // call ODM native method
        // -- methode: findOneBy()
        $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);

        // ========================================================================

        // check if connected user is found
        if (!$user) {
            return new JsonResponse(['operation1' => 'Check token',
                                    'status1' => 'Success',
                                    'message1' => 'Valid token',
                                    'operation2' => 'Check user',
                                    'status2' => 'Error, stopped',
                                    'message2' => 'User not found'
                                    ]);
        }

        // ========================================================================

        // check if request is GET
        if (!$request->isMethod('GET')) {
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

        // ========================================================================

        // check if p_id
        if(!$p_id) {
            return new JsonResponse([
                'operation' => 'Check p_id parameter',
                'status' => 'Error, stopped',
                'message' => 'p_id parameter not provided'
            ]);
        }

        // ========================================================================

        // Get the comment by $p_id
        $comment = $dm->getRepository(Comment::class)->findOneBy(['_id' => $p_id]);

        if (!$comment) {
            return new JsonResponse([
                'operation' => 'Find comment by p_id',
                'status' => 'Error, stopped',
                'message' => 'Comment not found'
                ]);
        }

        // ========================================================================

        // get the number of replies
        $repliesCount = $this->countReplies($dm, $p_id);

        // ========================================================================

        // Get the replies for the comment
        $replies = $this->findReplies($dm, $p_id);
        
        //
        $repliesArray = [];

        // ========================================================================

        foreach ($replies as $reply) {
            $repliesArray[] = [
                'reply_id' => $reply->getId(),
                'reply_title' => $reply->getTitle(),
                'reply_content' => $reply->getContent(),
                'reply_author' => $reply->getAuthor(),
                'reply_created_at' => $reply->getCreatedAt(),
                'reply_is_published' => $reply->getIsPublished(),
                'reply_flag' => $reply->getFlag(),
                'reply_parent_id' => $reply->getParentId(),
                'reply_category' => $reply->getCategory(),
                'reply_is_new' => $reply->getIsNew(),
                'reply_published_at' => $reply->getPublishedAt(),
            ];
        }

        // token is valid
        // User is found at this point
        // Request is okay
        // id parameter is okay
        // comment is found
        // include replies if any

        // ========================================================================

        // Get the data from the request
        $data = json_decode($request->getContent(), true);

        // ========================================================================

        //
        if ($request->isMethod('POST')) {
            if ($data === null) {
                return new JsonResponse([
                    'operation' => 'Check request data',
                    'status' => 'Error, stopped',
                    'message' => 'Request data is empty or not valid JSON'
                ]);
            }

            $title = $data['title'];
            $content = $data['content'];
            $category = $data['category'];
            $parent_id = $data['parent_id'];

        }

        // ========================================================================

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
                                            // Add other fields as needed
                                          ],
                                'operation3' => 'Check request',
                                'status3' => 'Success',
                                'message3' => 'Request found: '.$request,
                                'operation4' => 'Check p_id parameter',
                                'status4' => 'p_id parameter found',
                                'message4' => 'p_id value: '.$p_id,
                                'operation5' => 'Find comment by p_id',
                                'status5' => 'Success',
                                'message5' => 'Comment found',
                                'comment' => [
                                    'comment_title' => $comment->getTitle(),
                                    'comment_id' => $comment->getId(),
                                    'comment_content' => $comment->getContent(),
                                    'comment_author' => $comment->getAuthor(),
                                    'comment_created_at' => $comment->getCreatedAt(),
                                    'comment_is_published' => $comment->getIsPublished(),
                                    'comment_flag' => $comment->getFlag(),
                                    'comment_parent_id' => $comment->getParentId(),
                                    'comment_category' => $comment->getCategory(),
                                    'comment_is_new' => $comment->getIsNew(),
                                    'comment_published_at' => $comment->getPublishedAt(),
                                    // Add other fields as needed
                                    ],
                                'operation6' => 'Check for replies', 
                                'replies_count' => $repliesCount,
                                'replies' => $repliesArray,
                                'message' => 'Reply created successfully',
                                //'reply_id' => $reply->getId(),
                                //'title' => $reply->getTitle(),
                                //'content' => $reply->getContent(),
                                //'author' => $reply->getAuthor(),
                                //'created_at' => $reply->getCreatedAt(),
                                //'is_published' => $reply->getIsPublished(),
                                //'flag' => $reply->getFlag(),
                                //'parent_id' => $reply->getParentId(),
                                //'category' => $reply->getCategory(),
                                ]);

        // ====================================================================

    }
}
