<?php
// fichier: src/Controller/AdmSommaireController
// vue associée: src/views/view11_adm_sommaire.vue

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
 * fichier: src/Controller/AdmSommaireController.php
 * vue associée: src/views/view11_adm_sommaire.vue
 */
#[Route('/adm')]
class AdmSommaireController extends AbstractController
{
    #[Route('/sommaire', name: 'app_adm_sommaire')]
    public function index(JWTService $jwt,
                          Request $request,
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
        // fait appel à la methode src/Service/JWTService
        // -- methode: decode()
        $payload = $jwt->decode($token, $this->getParameter('app.jwtsecret'));

        // Défini la variable par le champs user_id du payload
        // Fait appel à la méthode native de l'ODM'
        // -- methode: findOneBy()
        $userId = $payload['user_id'];
        
        // Recupere les infos de l'utilisateur basé sur la valeur de $userId
        $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);

        // Récupère tous les utilisateurs de la collection 'user'
        // de la MongoDB
        // -- methode: findAll()
        $allUsers = $dm->getRepository(User::class)->findAll();

        // Recupere tous les commentaires (comment & replies) de la
        // collection 'comment' de la MongoDB
        // -- methode: findAll()
        $allComments = $dm->getRepository(Comment::class)->findAll();

        // Récupère les utilisateurs vérifiés 
        // -- methode: findBy()
        $verifiedUsers = $dm->getRepository(User::class)->findBy(['is_verified' => true]);

        // Recupere les utilisateurs non vérifiés
        // -- methode: findByIsVerified()
        $unverifiedUsers = $dm->getRepository(User::class)->findByIsVerified(true);

        // 'is_new' à true
        // appelle la methode src/Repository/UserRepository
        // -- methode: findByIsNew()
        $areNewUsers = $dm->getRepository(User::class)->findByIsNew(true);

        // Recupere seulement les commentaires qui ont leur attribut
        // 'is_new' à true et leur attribut 'parent_id' à null
        // appelle la methode src/Repository/CommentRepository
        // -- methode: findByIsNew()
        $areNewComments = $dm->getRepository(Comment::class)->findByIsNew(true);

        // la methode stocke le commentaire et ses reponses et les 
        // présente cô 1 fil de discuss° d'ou le nom de la variable
        // call method src/Repository/CommentRepository
        // -- methode: findAllCommentsWithReplies()
        $areFils = $dm->getRepository(Comment::class)->findAllCommentsWithReplies();

        // ====================================================================

        // Creer des tableaux vides stocker les résultat méthodes
        // employées ci-dessus
        $users = [];
        $formattedVerifiedUsers = [];
        $formattedUnverifiedUsers = [];
        $formattedAreNewUsers = [];
        $comments = [];
        $formattedAreNewComments = [];
        $replies = [];
        $commentsWithRepliesResult = [];

        // ====================================================================

        // Hydrate le tableaux
        foreach ($allUsers as $userItem) {
            $users[] = $userItem->toArray();
        }

        // Hydrate le tableaux
        foreach ($verifiedUsers as $userItem) {
            $formattedVerifiedUsers[] = $userItem->toArray();
        }

        // Hydrate le tableaux
        foreach ($unverifiedUsers as $userItem) {
            $formattedUnverifiedUsers[] = $userItem->toArray();
        }

        // Hydrate le tableaux
        foreach ($areNewUsers as $userItem) {
            $formattedAreNewUsers[] = $userItem->toArray();
        }

        // Hydrate le tableaux
        foreach ($allComments as $comment) {
            if ($comment->getParentId() === null) {
                $comments[] = $comment->toArray();
            } else {
                $replies[] = $comment->toArray();
            }
        }

        // Hydrate le tableaux
        foreach ($areNewComments as $commentItem) {
            $formattedAreNewComments[] = $commentItem->toArray();
        }

        // Hydrate le tableaux
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

        // Retourne une erreur si l'utiisateur connecté n'est pas trouvé
        if (!$user) {
            return new JsonResponse(['operation' => 'check user',
                                    'status' => 'Error, stopped',
                                    'message' => 'User not found',
                                    ]);
        }

        // ====================================================================

        // Check if connected user has "ROLE_USER" role
        // Vérifie si l'utilisateur connecté a le rôle 'ROLE_USER'
        // Si c'est la cas, retourne une erreur (on est ds l'espace adm')
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
            ],
            'allUsers' => $users,
            'verifiedUsers' => $formattedVerifiedUsers,
            'unverifiedUsers' => $formattedUnverifiedUsers,
            'areNewUsers' => $formattedAreNewUsers,
            // 'allComments' => $allComments,
            'comments' => $comments,
            'areNewComments' => $formattedAreNewComments,
            'replies' => $replies,
            'commentsWithReplies' => $commentsWithRepliesResult,
        ];

        // ====================================================================

        return new JsonResponse($response, 200);

        // ====================================================================

    }
}
