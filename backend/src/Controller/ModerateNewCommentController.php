<?php
// fichier: src/Controller/ModerateNewCommentController
// vue associée: src/views/view14_adm_moderate_new_comment.vue

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
 * fichier: src/Controller/ModerateNewCommentController.php
 * vue associée: src/views/view14_adm_moderate_new_comment.vue
 */
#[Route('/adm')]
class ModerateNewCommentController extends AbstractController
{
    #[Route('/moderate_new_comment', name: 'app_adm_moderate_new_comment')]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm): JsonResponse
    {

        // ====================================================================

        // entête authorization du header
        $authHeader = $request->headers->get('Authorization');
        
        // supprimer le bearer du header
        $token = substr($authHeader, 7);

        // Processus de validation du token
        // Applelle la methode depuis src/Service/JWTService
        // -- methode: validate()
        // qui elle-même
        // -- method: isValid()
        // -- method: isExpired()
        // -- method: check()
        if (!$jwt->validate($token, $this->getParameter('app.jwtsecret'))) {
            return new JsonResponse(['operation' => 'Check token',
                                    'status' => 'Error, stopped',
                                    'message' => 'Invalid token'
                                    ]);
        }

        // decoder le token et récupérer le payload
        $payload = $jwt->decode($token, $this->getParameter('app.jwtsecret'));

        // Fetch connected user data based on the user_id from the payload
        $userId = $payload['user_id'];

        // Fetch user data based on the user_id from the payload
        $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);

        // ====================================================================

        // Fetch all users from the 'user' collection
        $allUsers = $dm->getRepository(User::class)->findAll();

        // Fetch all comments from the 'comment' collection
        // comments AND replies
        $allComments = $dm->getRepository(Comment::class)->findAll();

        // Fetch verified users
        $verifiedUsers = $dm->getRepository(User::class)->findBy(['is_verified' => true]);

        // Fetch all unverified users
        $unverifiedUsers = $dm->getRepository(User::class)->findByIsVerified(true);

        // Fetch all is_new attributes users
        $areNewUsers = $dm->getRepository(User::class)->findByIsNew(true);

        // Fetch is_published comments
        $publishedComments = $dm->getRepository(Comment::class)->findBy(['is_published' => true]);

        // Fetch all ONLY comments with is_new attribute == true and
        // parent_id attribute == null
        $areNewComments = $dm->getRepository(Comment::class)->findByIsNew(true);

        // la methode stocke le commentaire et ses reponses et les 
        // présente cô 1 fil de discuss° d'ou le nom de la variable
        $areFils = $dm->getRepository(Comment::class)->findAllCommentsWithReplies();

        // ====================================================================

        // Separate users, comments and replies
        $users = [];
        $formattedVerifiedUsers = [];
        $formattedUnverifiedUsers = [];
        $formattedAreNewUsers = [];
        $comments = [];
        $formattedAreNewComments = [];
        $formattedPublishedComments = [];
        $replies = [];
        $commentsWithRepliesResult = [];

        // ====================================================================
        
        foreach ($allUsers as $userItem) {
            $users[] = $userItem->toArray();
        }

        foreach ($verifiedUsers as $userItem) {
            $formattedVerifiedUsers[] = $userItem->toArray();
        }

        foreach ($unverifiedUsers as $userItem) {
            $formattedUnverifiedUsers[] = $userItem->toArray();
        }

        foreach ($areNewUsers as $userItem) {
            $formattedAreNewUsers[] = $userItem->toArray();
        }

        foreach ($allComments as $comment) {
            if ($comment->getParentId() === null) {
                $comments[] = $comment->toArray();
            } else {
                $replies[] = $comment->toArray();
            }
        }

        foreach ($areNewComments as $commentItem) {
            $formattedAreNewComments[] = $commentItem->toArray();
        }

        foreach ($publishedComments as $commentItem) {
            $formattedPublishedComments[] = $commentItem->toArray();
        }

        foreach ($areFils as $item) {
            $commentsWithRepliesResult[] = [
                'comment' => $item['comment']->toArray(),
                'replies' => array_map(function ($reply) {
                    return $reply->toArray();
                }, $item['replies']),
                'containNewReply' => $item['containNewReply'] ?? false,
            ];
        }

        // ====================================================================

        // If the connected user is not found, return an error
        if (!$user) {
            return new JsonResponse(['operation' => 'check user',
                                    'status' => 'Error, stopped',
                                    'message' => 'User not found',
                                    ]);
        }

        // ====================================================================

        // Check if connected user has "ROLE_USER" role,
        // otherwise return an error
        if (in_array('ROLE_USER', $user->getRoles())) {
            return new JsonResponse(['operation' => 'check user',
                                    'status' => 'Error, stopped',
                                    'message' => 'User role == ["ROLE_USER"]',
                                    ]);
        }

        // ====================================================================
        
        $response = [
            'status' => 'Success',
            'message' => 'Secured data',
            'user' => [
                'token' => $token,
                'id' => $user->getId(),
                'nickname' => $user->getNickname(),
                'email' => $user->getEmail(),
                'password' => $user->getPassword(),
                'roles' => $user->getRoles(),
                'is_verified' => $user->getIsVerified(),
                'inscriptionDate' => $user->getInscriptionDate(),
                'is_new' => $user->getIsNew(),
                // Add other fields as needed
            ],
            'allUsers' => $users,
            'verifiedUsers' => $formattedVerifiedUsers,
            'unverifiedUsers' => $formattedUnverifiedUsers,
            'areNewUsers' => $formattedAreNewUsers,
            // 'allComments' => $allComments,
            'areNewComments' => $formattedAreNewComments,
            'publishedComments' => $formattedPublishedComments,
            'comments' => $comments,
            'replies' => $replies,
            'commentsWithReplies' => $commentsWithRepliesResult,
        ];

        // ====================================================================

        return new JsonResponse($response, 200);
        
    }
}
