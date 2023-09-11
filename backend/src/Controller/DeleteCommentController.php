<?php
// fichier: src/Controller/DeleteCommentController
// vue associée: src/views/view12_adm_delete_comment.vue

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
 * fichier: src/Controller/DeleteCommentController.php
 * vue associée: src/views/view12_adm_delete_comment.vue
 */
#[Route('/adm')]
class DeleteCommentController extends AbstractController
{
    #[Route('/delete_comment', name: 'app_adm_delete_comment')]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm): JsonResponse
    {
        
        // ====================================================================

        // obtenir la partie 'authorization' depuis le header
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

        // ====================================================================

        // decoder le token et récupérer le payload
        // fait appel à la methode src/Service/JWTService
        // -- methode: decode()
        $payload = $jwt->decode($token, $this->getParameter('app.jwtsecret'));

        // Assigne la valeur de 'user_id' issue du payload à la variable
        // $userId
        $userId = $payload['user_id'];

        // Récupère l'utilisateur basé sur le user_id issu du payload'
        $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);

        // ====================================================================

        // Récupère tous les utilisateurs de la collection 'user'
        // de la MongoBD
        $allUsers = $dm->getRepository(User::class)->findAll();

        // Récupère tous les commentaires de la collection 'comment'
        // de la MongoDB (inclus les commentaires et les réponsese)
        $allComments = $dm->getRepository(Comment::class)->findAll();

        // Récupère tous les utilisateurs vérifiés
        $verifiedUsers = $dm->getRepository(User::class)->findBy(['is_verified' => true]);

        // Récupère tous les utilisateurs non vérifiés
        $unverifiedUsers = $dm->getRepository(User::class)->findByIsVerified(true);

        // Récupère tous les utilisateurs dont le flag 'is_new' est à true
        $areNewUsers = $dm->getRepository(User::class)->findByIsNew(true);

        // Récupère les commentaires dt le flag 'is_published' est à true
        $publishedComments = $dm->getRepository(Comment::class)->findBy(['is_published' => true]);

        // Récupère les commentaires qui ont leur flag 'is_new' à true
        $areNewComments = $dm->getRepository(Comment::class)->findByIsNew(true);

        // la methode stocke le commentaire et ses reponses et les 
        // présente cô 1 fil de discuss° d'ou le nom de la variable
        $areFils = $dm->getRepository(Comment::class)->findAllCommentsWithReplies();

        // ====================================================================

        // Stocke les utilisateurs, commentaires et réponses
        // dans des tableaux séparés.
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

        // Retourne 1 erreur si l'utilisateur connecté n'est pas trouvé dans la
        // MongoDB
        if (!$user) {
            return new JsonResponse(['operation' => 'check user',
                                    'status' => 'Error, stopped',
                                    'message' => 'User not found',
                                    ]);
        }

        // ====================================================================

        // Verifie si l'utilisateur connecté à le role "ROLE_USER"
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
                // Add other fields as needed
            ],
            'allUsers' => $users,
            'verifiedUsers' => $formattedVerifiedUsers,
            'unverifiedUsers' => $formattedUnverifiedUsers,
            'areNewUsers' => $formattedAreNewUsers,
            'allComments' => $allComments,
            'areNewComments' => $formattedAreNewComments,
            'publishedComments' => $formattedPublishedComments,
            'comments' => $comments,
            'replies' => $replies,
            'commentsWithReplies' => $commentsWithRepliesResult,
        ];

        return new JsonResponse($response, 200);
        
    }
}
