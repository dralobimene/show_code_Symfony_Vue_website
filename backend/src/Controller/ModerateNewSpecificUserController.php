<?php
// fichier: src/Controller/ModerateNewSpecificUserController {UserId}
// vue associée: src/views/view20_adm_moderate_new_specific_user.vue

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
 * fichier: src/Controller/ModerateNewSpecificUserController {commentId}
 * vue associée: src/views/view20_adm_moderate_new_specific_user.vue
 */
#[Route('/adm')]
class ModerateNewSpecificUserController extends AbstractController
{
    #[Route('/moderate_new_specific_user/{userId}', name: 'app_moderate_new_specific_user')]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm,
                          string $userId): JsonResponse
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
            return new JsonResponse(['operation' => 'Check token',
                                    'status' => 'Error, stopped',
                                    'message' => 'Invalid token'
                                    ]);
        }

        // ====================================================================

        // decoder le token et récupérer le payload
        $payload = $jwt->decode($token, $this->getParameter('app.jwtsecret'));
 
        // Fetch connected user data based on the user_id from the payload
        $userId = $payload['user_id'];

        // find connected user with payload defined above
        // call ODM native method
        // -- methode: findOneBy()
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

        // populate the array
        foreach ($allUsers as $userItem) {
            $users[] = $userItem->toArray();
        }

        // populate the array
        foreach ($verifiedUsers as $userItem) {
            $formattedVerifiedUsers[] = $userItem->toArray();
        }

        // populate the array
        foreach ($unverifiedUsers as $userItem) {
            $formattedUnverifiedUsers[] = $userItem->toArray();
        }

        // populate the array
        foreach ($areNewUsers as $userItem) {
            $formattedAreNewUsers[] = $userItem->toArray();
        }

        // populate the array
        foreach ($allComments as $comment) {
            if ($comment->getParentId() === null) {
                $comments[] = $comment->toArray();
            } else {
                $replies[] = $comment->toArray();
            }
        }

        // populate the array
        foreach ($areNewComments as $commentItem) {
            $formattedAreNewComments[] = $commentItem->toArray();
        }

        // populate the array
        foreach ($publishedComments as $commentItem) {
            $formattedPublishedComments[] = $commentItem->toArray();
        }

        // populate the array
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

        // If the connected user is not found, return an error,
        // if, so return an error
        if (!$user) {
            return new JsonResponse(['operation' => 'check user',
                                    'status' => 'Error, stopped',
                                    'message' => 'User not found',
                                    ]);
        }

        // ====================================================================

        // Check if connected user has "ROLE_USER" role
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

        return new JsonResponse($response, 200);

        // ====================================================================
        
    }
}
