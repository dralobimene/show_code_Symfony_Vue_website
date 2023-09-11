<?php
// fichier: src/Controller/CommentUserPostController.php
// vue associée: src/views/view08_comment_user_post.vue

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpKernel\Exception\AccessDeniedHttpException;

use App\Document\User;
use App\Document\Comment;
use App\Document\Category;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Service\JWTService;

/*
 * fichier: src/Controller/CommentUserPostController.php
 * vue associée: src/views/view08_comment_user_post.vue
 */
#[Route('/comment_user')]
class CommentUserPostController extends AbstractController
{
    #[Route('/post',
            name: 'app_comment_user_post',
            methods: ['GET', 'POST'])]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm): JsonResponse
    {

        // ====================================================================


        try {

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

            // Récupérer les infos de l'utilisateur connecté a partir du champs
            // user_id du payload
            // -- methode: findOneBy()
            $userId = $payload['user_id'];

            //
            $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]);

            // ====================================================================

            // entraîne une erreur si l'utilisateur n'est pas trouvé
            // ds la MongoDB
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

            // erreur
            if (!$request->isMethod('POST')) {
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

            // ====================================================================

            // token valide
            // l'utilisateur est trouvé
            // la requete est valide

            // Obtenir les informations contenues ds la requête
            $data = json_decode($request->getContent(), true);
            $title = $data['title'];
            $content = $data['content'];
            $category = $data['category'];

            // Vérifie si la category choisie par l'utilisateur depuis la
            // liste déroulante existe bien dans le document 'category'
            $queryBuilder = $dm->createQueryBuilder(Category::class);
            $queryBuilder->select('name');
            $query = $queryBuilder->getQuery();
            $categories = $query->execute()->toArray();
            
            $categoryNames = array_map(function($category) {
                return $category->getName();
            }, $categories);


            // si la caterory n'existe pas, entraîne une erreur
            if (!in_array($category, $categoryNames)) {
                return new JsonResponse([
                    'error' => 'Invalid category',
                    'message' => 'The provided category does not exist'
                ]);
            }

            // ====================================================================

            // Créer un nvel objet Comment
            $comment = new Comment(
                                    $user->getNickname(),
                                    $category,
                                    $title,
                                    $content
                                    );
            $comment->setCreatedAt(new \DateTime());
            $comment->setPublishedAt(null);
            $comment->setFlag('En attente de modération');
            $comment->setIsPublished(false);
            $comment->setParentId(null);
            $comment->setIsNew(true);

            // Persister et flusher l'objet dans la MongoDB'
            $dm->persist($comment);
            $dm->flush();

            // ====================================================================

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
                                    'status3' => 'Success',
                                    'message3' => 'Request made'
                                    ]);

            // ====================================================================

        // erreur: voir view 08, nbre de clé: 2
        } catch (AccessDeniedHttpException $except) {
            // SI une AccessDeniedException est levée, retournera une
            // JsonResponse avec un msg d'erreur
            return new JsonResponse(['error' => 'Access Denied from CommentUserPostController.php',
                                    'message' => $except->getMessage()]);
        }

        // ====================================================================

    }

}
