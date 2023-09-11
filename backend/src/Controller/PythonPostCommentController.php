<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Document\User;
use App\Document\Comment;

class PythonPostCommentController extends AbstractController
{

    /*
      * check si le user-agent contient le mot 'python' ou pas.
      * return true si le mot 'python' est trouvé, sinon, retourne false.
      * ce n'est pas un moyen fiable de savoir si le client est un script
      * python ou non, car le user-agent peut-être facilement modifié
      */
      private function checkUserAgentFromPythonOrNot(Request $request): bool
      {
          $user_agent = $request->headers->get('User-Agent');

          if (strpos($user_agent, 'python') !== false) {
              return true;
          }

          return false;
      }

    // ========================================================================

    #[Route('/python_post_comment', name: 'app_python_post_comment', methods: ["POST"])]
    public function index(Request $request,
                          DocumentManager $dm): JsonResponse
    {

        // ====================================================================

        // Initialize the $response variable with a default value
        $response = [
            'status' => 'Error',
            'message' => 'Unknown error',
        ];

        // ====================================================================

        // initialise un $user a null
        $user = null;

        // ====================================================================

        // Check for an existing token in the request headers
        $authorizationHeader = $request->headers->get('Authorization');
        if (!empty($authorizationHeader) && strpos($authorizationHeader, 'Bearer') === 0) {
            $existingToken = substr($authorizationHeader, 7);
            if (!empty($existingToken)) {
                return new JsonResponse([
                    'status' => 'Error',
                    'message' => 'A token already exists',
                ]);
            }
        }

        // ====================================================================

        // get datas from Python Client
        $data = json_decode($request->getContent(), true);

        // ====================================================================

        // les données reçues depuis le client python pr savoir s'il y a correspondance
        // elles st partagées par SF et PYTHON
        // Ce st les données que reçoit le controller

        // envoyé par le client python apres qu'il ait lu, stocké la clé
        // 'user_nickname' du credentials.json
        $usernameOrEmail = $data['usernameOrEmail'];

        // envoyé par le client python apres qu'il ait lu et stocké la clé
        // 'user_tokenForPython' du credentials.json
        $user_tokenForPython = $data['user_tokenForPython'];

        // envoyé par le client python apres qu'il ait lu et stocké la clé
        // 'user_tokenForPythonExpiration' du credentials.json
        $user_tokenForPythonExpiration = $data['user_tokenForPythonExpiration'];

        // envoyé par le client python, c'est le contenu du titre
        $text_titre = $data['title_content'];

        // envoyé par le client python, c'est le contenu du commentaire
        $text_content = $data['text_content'];

        // envoyé par le client python, c'est la valeur de la combolist
        $category_content = $data['category_content'];

        // ====================================================================

        // Est-ce que SF retrouve 1 document (user) à partir de ce qu'il lui
        // a été envoyé par le python client?
        // Ici  la recherche s'effectue sur le champs 'nickname' des documents
        // user de la mongo DB
        $nicknameResults = $dm->getRepository(User::class)->findBy(['nickname' => $usernameOrEmail]);

        // ====================================================================

        // Est-ce que SF retrouve 1 document (user) à partir de ce qu'il lui
        // a été envoyé par le python client?
        // Ici  la recherche s'effectue sur le champs 'email' des documents
        // user de la mongo DB
        $emailResults = $dm->getRepository(User::class)->findBy(['email' => $usernameOrEmail]);

        // ====================================================================

        // compte le nbre de documents user retouvés à partir de $usernameOrEmail sur
        // le champs nickname de la mongo DB. Il peut y avoir plusieurs
        // utilisateurs avec le meme nickname
        $nicknameCount = count($nicknameResults);

        // ====================================================================

        // compte le nbre de documents user retouvés à partir de $usernameOrEmail sur
        // le champs email de la mongo DB. Il ne peut y avoir qu'1 seul
        // utilisateur avec le meme email
        $emailCount = count($emailResults);

        // ====================================================================

        // verifie grace aux headers si la requete a ete envoyée par 1
        // client python (WARNING, ce n'est pas fiable)
        $fromPython = $this->checkUserAgentFromPythonOrNot($request);

        // ====================================================================
        
        if ($emailCount > 0) {
            // An email matching the given value was found in the DB
            if ($emailCount > 1) {
                // More than one user has the same email, this is not supposed
                // to happen as emails are unique
                $response = [
                    'status' => 'Warning',
                    'message' => 'WARNING, 2 or more same emails'
                ];
                // You might want to add some logging here
            } else {
                // Exactly one user has the given email
                $userByEmail = $emailResults[0];

                //
                if ($nicknameCount == 0) {

                    
                    // Create a new Comment object
                    $comment = new Comment(
                                            $userByEmail->getNickname(),
                                            $category_content,
                                            $text_titre,
                                            $text_content
                                            );
                    $comment->setCreatedAt(new \DateTime());
                    $comment->setPublishedAt(null);
                    $comment->setFlag('En attente de modération');
                    $comment->setIsPublished(false);
                    $comment->setParentId(null);
                    $comment->setIsNew(true);

                    // Persist and flush the Comment to the database
                    $dm->persist($comment);
                    $dm->flush();
                    

                    // No user with the given nickname found, only one user with the given email
                    $response = [
                        'status' => 'Success',
                        'message' => 'One user found with the given email, no user with the given nickname',
                        'nicknameCount' => $nicknameCount,
                        'emailCount' => $emailCount,
                        'fromPython' => $fromPython,
                        'user_tokenForPython' => $user_tokenForPython,
                        'user_tokenForPythonExpiration' => $user_tokenForPythonExpiration,
                        'text_titre' => $text_titre,
                        'text_content' => $text_content,
                        'category_content' => $category_content,
                        'user' => [
                            'id' => $userByEmail->getId(),
                            'nickname' => $userByEmail->getNickname(),
                            'email' => $userByEmail->getEmail(),
                            'password' => $userByEmail->getPassword(),
                            'roles' => $userByEmail->getRoles(),
                            'is_verified' => $userByEmail->getIsVerified(),
                            'is_new' => $userByEmail->getIsNew(),
                            'token' => $userByEmail->getToken(),
                            'tokenExpiration' => $userByEmail->getTokenExpiration(),
                            'tokenForPython' => $userByEmail->getTokenForPython(),
                            'tokenForPythonExpiration' => $userByEmail->getTokenForPythonExpiration(),
                        ],
                    ];
                } else {
                    // There is/are user(s) with the given nickname
                    // Check if any of them is the same as the user found by email
                    $matchedUsers = array_filter($nicknameResults, function($user) use ($userByEmail) {
                        return $user->getId() == $userByEmail->getId();
                    });

                    
                    if (count($matchedUsers) > 0) {
                        // Found user(s) with both the given nickname and email
                        if (count($matchedUsers) == 1) {
                            // Only one user found with both the given nickname and email
                            $user = $matchedUsers[0];


                            // Create a new Comment object
                            $comment = new Comment(
                                                    $user->getNickname(),
                                                    $category_content,
                                                    $text_titre,
                                                    $text_content
                                                    );
                            $comment->setCreatedAt(new \DateTime());
                            $comment->setPublishedAt(null);
                            $comment->setFlag('En attente de modération');
                            $comment->setIsPublished(false);
                            $comment->setParentId(null);
                            $comment->setIsNew(true);

                            // Persist and flush the Comment to the database
                            $dm->persist($comment);
                            $dm->flush();


                            $response = [
                                'status' => 'Success',
                                'message' => 'One user found with the given email and email',
                                'nicknameCount' => $nicknameCount,
                                'emailCount' => $emailCount,
                                'fromPython' => $fromPython,
                                'user_tokenForPython' => $user_tokenForPython,
                                'user_tokenForPythonExpiration' => $user_tokenForPythonExpiration,
                                'text_titre' => $text_titre,
                                'text_content' => $text_content,
                                'category_content' => $category_content,
                                'user' => [
                                    'id' => $user->getId(),
                                    'nickname' => $user->getNickname(),
                                    'email' => $user->getEmail(),
                                    'password' => $user->getPassword(),
                                    'roles' => $user->getRoles(),
                                    'is_verified' => $user->getIsVerified(),
                                    'is_new' => $user->getIsNew(),
                                    'token' => $user->getToken(),
                                    'tokenExpiration' => $user->getTokenExpiration(),
                                    'tokenForPython' => $user->getTokenForPython(),
                                    'tokenForPythonExpiration' => $user->getTokenForPythonExpiration(),
                                ],
                            ];
                        } else {
                            // Multiple users found with both the given nickname and email.
                            // This should not happen as we expect nicknames and emails
                            // to be unique together.
                            $response = [
                                'status' => 'Error',
                                'message' => 'WARNING, Multiple users found with the same nickname and email',
                            ];
                            // You might want to add some logging here
                        }
                    } else {

                        // Create a new Comment object
                        $comment = new Comment(
                                                $user->getNickname(),
                                                $category_content,
                                                $text_titre,
                                                $text_content
                                                );
                        $comment->setCreatedAt(new \DateTime());
                        $comment->setPublishedAt(null);
                        $comment->setFlag('En attente de modération');
                        $comment->setIsPublished(false);
                        $comment->setParentId(null);
                        $comment->setIsNew(true);

                        // Persist and flush the Comment to the database
                        $dm->persist($comment);
                        $dm->flush();


                        // No user found with the given nickname and email
                        // combination, but one user found with the given email
                        $response = [
                            'status' => 'Success',
                            'message' => 'No user found with the given nickname and email, but one user found with the given email',
                            'nicknameCount' => $nicknameCount,
                            'emailCount' => $emailCount,
                            'fromPython' => $fromPython,
                            'user_tokenForPython' => $user_tokenForPython,
                            'user_tokenForPythonExpiration' => $user_tokenForPythonExpiration,
                            'text_titre' => $text_titre,
                            'text_content' => $text_content,
                            'category_content' => $category_content,
                            'user' => [
                                'id' => $user->getId(),
                                'nickname' => $user->getNickname(),
                                'email' => $user->getEmail(),
                                'password' => $user->getPassword(),
                                'roles' => $user->getRoles(),
                                'is_verified' => $user->getIsVerified(),
                                'is_new' => $user->getIsNew(),
                                'token' => $user->getToken(),
                                'tokenExpiration' => $user->getTokenExpiration(),
                                'tokenForPython' => $user->getTokenForPython(),
                                'tokenForPythonExpiration' => $user->getTokenForPythonExpiration(),
                            ],
                        ];
                    }
                }
            }
        } else {
            // No user found with the given email, it could be a nickname
            if ($nicknameCount > 0) {
                // Nickname found in the database, continue your checks
                if ($nicknameCount == 1) {
                    // One user has the given nickname
                    $userByNickname = $nicknameResults[0];

                    
                    // Create a new Comment object
                    $comment = new Comment(
                                            $userByNickname->getNickname(),
                                            $category_content,
                                            $text_titre,
                                            $text_content
                                            );
                    $comment->setCreatedAt(new \DateTime());
                    $comment->setPublishedAt(null);
                    $comment->setFlag('En attente de modération');
                    $comment->setIsPublished(false);
                    $comment->setParentId(null);
                    $comment->setIsNew(true);

                    // Persist and flush the Comment to the database
                    $dm->persist($comment);
                    $dm->flush();


                    $response = [
                        'status' => 'Success',
                        'message' => 'One user has the given nickname',
                        'nicknameCount' => $nicknameCount,
                        'emailCount' => $emailCount,
                        'fromPython' => $fromPython,
                        'user_tokenForPython' => $user_tokenForPython,
                        'user_tokenForPythonExpiration' => $user_tokenForPythonExpiration,
                        'text_titre' => $text_titre,
                        'text_content' => $text_content,
                        'category_content' => $category_content,
                        'user' => [
                            'id' => $userByNickname->getId(),
                            'nickname' => $userByNickname->getNickname(),
                            'email' => $userByNickname->getEmail(),
                            'password' => $userByNickname->getPassword(),
                            'roles' => $userByNickname->getRoles(),
                            'is_verified' => $userByNickname->getIsVerified(),
                            'is_new' => $userByNickname->getIsNew(),
                            'token' => $userByNickname->getToken(),
                            'tokenExpiration' => $userByNickname->getTokenExpiration(),
                            'tokenForPython' => $userByNickname->getTokenForPython(),
                            'tokenForPythonExpiration' => $userByNickname->getTokenForPythonExpiration(),
                        ],
                    ];
                } else {
                    // Multiple users have the same nickname, this can happen
                    // as nicknames are not unique
                    
                    // Get users who have the same nickname and the given value as their email
                    $matchedUsers = array_filter($nicknameResults, function($user) use ($value) {
                        return $user->getEmail() == $value;
                    });

                    if (count($matchedUsers) == 1) {
                        // One user found with the same nickname and email
                        $userByNicknameAndEmail = $matchedUsers[0];


                        // Create a new Comment object
                        $comment = new Comment(
                                                $userByNicknameAndEmail->getNickname(),
                                                $category_content,
                                                $text_titre,
                                                $text_content
                                                );
                        $comment->setCreatedAt(new \DateTime());
                        $comment->setPublishedAt(null);
                        $comment->setFlag('En attente de modération');
                        $comment->setIsPublished(false);
                        $comment->setParentId(null);
                        $comment->setIsNew(true);

                        // Persist and flush the Comment to the database
                        $dm->persist($comment);
                        $dm->flush();


                        $response = [
                            'status' => 'Success',
                            'message' => 'One user found with the same nickname and email',
                            'nicknameCount' => $nicknameCount,
                            'emailCount' => $emailCount,
                            'fromPython' => $fromPython,
                            'user_tokenForPython' => $user_tokenForPython,
                            'user_tokenForPythonExpiration' => $user_tokenForPythonExpiration,
                            'text_titre' => $text_titre,
                            'text_content' => $text_content,
                            'category_content' => $category_content,
                            'user' => [
                                'id' => $userByNicknameAndEmail->getId(),
                                'nickname' => $userByNicknameAndEmail->getNickname(),
                                'email' => $userByNicknameAndEmail->getEmail(),
                                'password' => $userByNicknameAndEmail->getPassword(),
                                'roles' => $userByNicknameAndEmail->getRoles(),
                                'is_verified' => $userByNicknameAndEmail->getIsVerified(),
                                'is_new' => $userByNicknameAndEmail->getIsNew(),
                                'token' => $userByNicknameAndEmail->getToken(),
                                'tokenExpiration' => $userByNicknameAndEmail->getTokenExpiration(),
                                'tokenForPython' => $userByNicknameAndEmail->getTokenForPython(),
                                'tokenForPythonExpiration' => $userByNicknameAndEmail->getTokenForPythonExpiration(),
                            ],
                        ];
                    } else {
                        // No user found with the same nickname and email
                        $response = [
                            'status' => 'Warning',
                            'message' => 'WARNING, multiple users found with the same nickname, but none with the given email',
                        ];
                    }
                }
            } else {
                // No user found with the given nickname either
                $response = [
                    'status' => 'Error',
                    'message' => 'No user found with the given email or nickname'
                ];
            }
        }
        // ====================================================================

        return new JsonResponse($response);
    }
}
