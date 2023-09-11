<?php
// fichier: src/Controller/IndexController
// vue asssociée: src/views/view01.vue

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
 * fichier: src/Controller/IndexController.php
 * vue associée: src/views/view01.vue
 */
class IndexController extends AbstractController
{
    #[Route('/index', name: 'app_index')]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm): JsonResponse
    {

        // ====================================================================

        // Récupère tous les commentaires de la collection
        // comment de la base de données.
        $allComments = $dm->getRepository(Comment::class)->findAll();

        // déclare 2 tableaux vides ou seront stockés les commentaires et
        // les réponses
        $comments = [];
        $replies = [];

        foreach ($allComments as $comment) {
            // Vérifie si le commentaire n'a pas de getParentId
            // (c'est un commentaire de niveau supérieur).
            if ($comment->getParentId() === null) {
                $comments[] = $comment->toArray();
            } else {
                // Sinon le commentaire a un parent, donc c'est une réponse.
                $replies[] = $comment->toArray();
            }
        }

        // ====================================================================

        // Récupère le header 'Authorization' de la requête.
        $authHeader = $request->headers->get('Authorization');
        
        // Récupère le token JWT en supprimant le préfixe 'Bearer '.
        $token = substr($authHeader, 7);

        // Vérifie si le token JWT est valide.
        if (!$jwt->validate($token, $this->getParameter('app.jwtsecret'))) {
            return new JsonResponse([
                                    'status' => 'Error',
                                    'message' => 'Invalid token',
                                    'comments' => $comments,
                                    'replies' => $replies
                                    ]);
        }

        // decoder le token et récupérer le payload
        $payload = $jwt->decode($token, $this->getParameter('app.jwtsecret'));

        // Récupère l'ID de l'utilisateur à partir du payload du token JWT.
        $userId = $payload['user_id'];

        // Récupère l'utilisateur de la base de données.
        $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);

        // si l'utilisateur n'est pas trouvé, alors renverra un Json
        // contenant uniquement les commentaires et leur(s) eventuelle(s) réponse(s)
        if (!$user) {
            return new JsonResponse([
                                    'status' => 'Error',
                                    'message' => 'User not found',
                                    'comments' => $comments,
                                    'replies' => $replies
                                    ]);
        }

        // ====================================================================

        // Prépare la réponse JSON.
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
            ],
            'comments' => $comments,
            'replies' => $replies,
        ];

        return new JsonResponse($response, 200);

    }
}
