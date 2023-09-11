<?php
  // fichier: src/Controller/ConnectController.php
  // vue associée: src/views/view04_connect.vue
	namespace App\Controller;

	use Symfony\Component\HttpFoundation\JsonResponse;
	use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
  use Symfony\Component\Routing\Annotation\Route;
  use Symfony\Component\HttpFoundation\Request;

  use App\Document\User;
  use Doctrine\ODM\MongoDB\DocumentManager;
  use App\Service\JWTService;
  use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

	class ConnectController extends AbstractController
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

      // ======================================================================

	    #[Route('/connect', name: 'app_connect', methods: ["POST"])]
      public function index(Request $request,
                            DocumentManager $dm,
                            UserPasswordHasherInterface $uphi,
                            JWTService $jwt): JsonResponse
      {

        // Initialiser la variable $response avec une valeur par défaut
        $response = [
            'status' => 'Error',
            'message' => 'Unknown error',
        ];

        // Verifie l'existence d'un token dans les headers de la requete
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

        // données obtenues depuis view04_connect.vue
        $data = json_decode($request->getContent(), true);

        // les données reçues depuis le client python pr savoir s'il y a correspondance
        // elles st partagées par SF, Vue et PYTHON
        // ce les donnees que reçoit le controller
        $usernameOrEmail = $data['usernameOrEmail'];
        $password = $data['password'];

        //
        $nicknameResults = $dm->getRepository(User::class)->findBy(['nickname' => $usernameOrEmail]);
        
        //
        $emailResults = $dm->getRepository(User::class)->findBy(['email' => $usernameOrEmail]);

        $nicknameCount = count($nicknameResults);
        $emailCount = count($emailResults);

        $user = null;
        $confirmation = "not found";
        $fromPython = $this->checkUserAgentFromPythonOrNot($request);

        // la recherche ne trouve pas de nickname
        if ($nicknameCount == 0) {
            // la recherche ne trouve pas non plus de mail
            if ($emailCount == 0) {
                $response = [
                    'status' => 'Error',
                    'message' => 'Erreur: aucun pseudo, aucun mail',
                    'usernameOrEmail' => $usernameOrEmail,
                    'password' => $password,
                    'nicknameCount' => $nicknameCount,
                    'emailCount' => $emailCount,
                    'Confirmation' => $confirmation,
                ];
            }
            // la recherche trouve 1 mail
            if ($emailCount == 1) {
                $user = $emailResults[0];
                if ($user !== null) {
                
                    if(!$uphi->isPasswordValid($user, $password)) {
                        $confirmation = "invalid password";
                    } else {
                        $confirmation = "valid password";
                        
                        // ====================================================
                        /*
                        * creation des 3 parties d'1 token
                        * Ce token est crée qd un utilisateur se connecte.
                        * Il est ensuite stocké ds la DB mongo ds les attributs
                        * du document du nickname reconnu.
                        * Ce token n'est pas utilisé par python, uniquement
                        * par SF et Vue
                        */

                        // on cree le header
                        $header = [
                            'typ' => 'JWT',
                            'alg' => 'HS256'
                        ];

                        // on cree le payload
                        $payload = [
                            'user_id' => $user->getId()
                        ];

                        // on genere le token
                        $token = $jwt->generate($header, $payload, $this->getParameter('app.jwtsecret'));

                        // ====================================================
                        
                        /* Creation des 3 parties d'1 SECOND token.
                        * token généré par le controller SF uniquement si le
                        * 'user-agent' contient le mot 'python'. SF genere
                        * alors ce SECOND token pr l'envoyer au client python
                        */

                        $fromPython = $this->checkUserAgentFromPythonOrNot($request);

                        if($fromPython == true) {
                            // on cree le header
                            $headerForPython = [
                                'typ' => 'JWT',
                                'alg' => 'HS256'
                            ];

                            // on cree le payload
                            $payloadForPython = [
                                'user_id' => $user->getId()
                            ];

                            // on genere le token
                            $tokenForPython = $jwt->generate($headerForPython, $payloadForPython, $this->getParameter('app.jwtsecret'));

                            // on definit 1 expiration pr le token
                            $tokenForPythonExpiration = new \DateTime();
                            $tokenForPythonExpiration->modify('+1 day');

                            // MAJ le document User qui se trouve dans la
                            // MongoDB
                            $user->setTokenForPython($tokenForPython);
                            $user->setTokenForPythonExpiration($tokenForPythonExpiration);
                            $dm->persist($user);
                            $dm->flush();

                            // Ajouter le token à la response si cell-ci provient
                            // du client python
                            $responseForpython['TokenForPython'] = $tokenForPython;
                            $responseForpython['TokenForPythonExpiration'] = $tokenForPythonExpiration;
                        }

                        // ====================================================

                        $response = [
                            'status' => 'Success',
                            'message' => 'Succes: aucun pseudo, 1 mail',
                            'usernameOrEmail' => $usernameOrEmail,
                            'password' => $password,
                            'nicknameCount' => $nicknameCount,
                            'emailCount' => $emailCount,
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
                            'fromPython' => $fromPython,
                            'Confirmation' => $confirmation,
                            'Token' => $token,
                        ];

                        // ====================================================

                    }

                } else {
                    $response = [
                        'status' => 'Success',
                        'message' => 'Succes: aucun pseudo, 1 mail',
                        'usernameOrEmail' => $usernameOrEmail,
                        'password' => $password,
                        'nicknameCount' => $nicknameCount,
                        'emailCount' => $emailCount,
                        'pass_trouve' => 'user == null, pas de pass',
                        'Confirmation' => $confirmation,
                    ];
                }
                
            }
            // la recherche trouve + d'1 mail'
            if ($emailCount > 1) {
                $response = [
                    'status' => 'Error',
                    'message' => 'WARNING: aucun pseudo, plusieurs mails',
                    'usernameOrEmail' => $usernameOrEmail,
                    'password' => $password,
                    'nicknameCount' => $nicknameCount,
                    'emailCount' => $emailCount,
                    'Confirmation' => $confirmation,
                ];
            }
        // la recherche a trouvé 1 nickname
        } else if ($nicknameCount == 1) {
            // la recherche n'a pas trouvé de mail
            if ($emailCount == 0) {
                $user = $nicknameResults[0];
                if ($user !== null) {

                    if(!$uphi->isPasswordValid($user, $password)) {
                        $confirmation = "invalid password";
                    } else {
                        $confirmation = "valid password";

                        // ====================================================
                        /*
                        * creation des 3 parties d'1 token
                        * Ce token est crée qd un utilisateur se connecte.
                        * Il est ensuite stocké ds la DB mongo ds les attributs
                        * du document du nickname reconnu.
                        * Ce token n'est pas utilisé par python, uniquement
                        * par SF et Vue
                        */

                        // on cree le header
                        $header = [
                            'typ' => 'JWT',
                            'alg' => 'HS256'
                        ];

                        // on cree le payload
                        $payload = [
                            'user_id' => $user->getId()
                        ];

                        // on genere le token
                        $token = $jwt->generate($header, $payload, $this->getParameter('app.jwtsecret'));

                        // ====================================================

                        /* Creation des 3 parties d'1 SECOND token.
                        * token généré par le controller SF uniquement si le
                        * 'user-agent' contient le mot 'python'. SF genere
                        * alors ce SECOND token pr l'envoyer au client python
                        */

                        $fromPython = $this->checkUserAgentFromPythonOrNot($request);

                        if($fromPython == true) {
                            // on cree le header
                            $headerForPython = [
                                'typ' => 'JWT',
                                'alg' => 'HS256'
                            ];

                            // on cree le payload
                            $payloadForPython = [
                                'user_id' => $user->getId()
                            ];

                            // on genere le token
                            $tokenForPython = $jwt->generate($headerForPython, $payloadForPython, $this->getParameter('app.jwtsecret'));

                            // on definit 1 expiration pr le token
                            $tokenForPythonExpiration = new \DateTime();
                            $tokenForPythonExpiration->modify('+1 day');

                            // MAJ le document User qui se trouve dans la
                            // MongoDB
                            $user->setTokenForPython($tokenForPython);
                            $user->setTokenForPythonExpiration($tokenForPythonExpiration);
                            $dm->persist($user);
                            $dm->flush();

                            // Ajouter le token à la response si celle-ci provient
                            // du client python
                            $responseForpython['TokenForPython'] = $tokenForPython;
                            $responseForpython['TokenForPythonExpiration'] = $tokenForPythonExpiration;
                        }

                        // ====================================================

                        $response = [
                            'status' => 'Success',
                            'message' => 'Succes: 1 pseudo, aucun mail',
                            'usernameOrEmail' => $usernameOrEmail,
                            'password' => $password,
                            'nicknameCount' => $nicknameCount,
                            'emailCount' => $emailCount,
                            'user' => [
                                'id' => $user->getId(),
                                'nickname' => $user->getNickname(),
                                'email' => $user->getEmail(),
                                'password' => $user->getPassword(),
                                'roles' => $user->getRoles(),
                                'is_verified' => $user->getIsVerified(),
                                'is_new' => $user->getIsNew(),
                                'tokenExpiration' => $user->getTokenExpiration(),
                                'tokenForPython' => $user->getTokenForPython(),
                                'tokenForPythonExpiration' => $user->getTokenForPythonExpiration(),
                            ],
                            'fromPython' => $fromPython,
                            'Confirmation' => $confirmation,
                            'Token' => $token,
                        ];

                        // ====================================================

                    }

                } else {
                    $response = [
                        'status' => 'Success',
                        'message' => 'Succes: 1 pseudo, aucun mail',
                        'usernameOrEmail' => $usernameOrEmail,
                        'password' => $password,
                        'nicknameCount' => $nicknameCount,
                        'emailCount' => $emailCount,
                        'pass_trouve' => 'user == null, pas de pass',
                        'Confirmation' => $confirmation,
                    ];
                }
            }
            // la recherche a trouvé 1 mail
            if ($emailCount == 1) {
                $user = $nicknameResults[0];
                if ($user !== null) {

                    if(!$uphi->isPasswordValid($user, $password)) {
                        $confirmation = "invalid password";
                    } else {
                        $confirmation = "valid password";

                        // ====================================================
                        /*
                        * creation des 3 parties d'1 token
                        * Ce token est crée qd un utilisateur se connecte.
                        * Il est ensuite stocké ds la DB mongo ds les attributs
                        * du document du nickname reconnu.
                        * Ce token n'est pas utilisé par python, uniquement
                        * par SF et Vue
                        */

                        // on cree le header
                        $header = [
                            'typ' => 'JWT',
                            'alg' => 'HS256'
                        ];

                        // on cree le payload
                        $payload = [
                            'user_id' => $user->getId()
                        ];

                        // on genere le token
                        $token = $jwt->generate($header, $payload, $this->getParameter('app.jwtsecret'));

                        // ====================================================

                        /* Creation des 3 parties d'1 SECOND token.
                        * token généré par le controller SF uniquement si le
                        * 'user-agent' contient le mot 'python'. SF genere
                        * alors ce SECOND token pr l'envoyer au client python
                        */

                        $fromPython = $this->checkUserAgentFromPythonOrNot($request);

                        if($fromPython == true) {
                            // on cree le header
                            $headerForPython = [
                                'typ' => 'JWT',
                                'alg' => 'HS256'
                            ];

                            // on cree le payload
                            $payloadForPython = [
                                'user_id' => $user->getId()
                            ];

                            // on genere le token
                            $tokenForPython = $jwt->generate($headerForPython, $payloadForPython, $this->getParameter('app.jwtsecret'));

                            // on definit 1 expiration pr le token
                            $tokenForPythonExpiration = new \DateTime();
                            $tokenForPythonExpiration->modify('+1 day');

                            // MAJ le document User qui se trouve dans la
                            // MongoDB
                            $user->setTokenForPython($tokenForPython);
                            $user->setTokenForPythonExpiration($tokenForPythonExpiration);
                            $dm->persist($user);
                            $dm->flush();

                            // Ajouter le token à la response si celle-ci provient
                            // du client python
                            $responseForpython['TokenForPython'] = $tokenForPython;
                            $responseForpython['TokenForPythonExpiration'] = $tokenForPythonExpiration;
                        }
                        // ====================================================

                        $response = [
                            'status' => 'Success',
                            'message' => 'Succes: 1 pseudo, 1 mail',
                            'usernameOrEmail' => $usernameOrEmail,
                            'password' => $password,
                            'nicknameCount' => $nicknameCount,
                            'emailCount' => $emailCount,
                            'user' => [
                                'id' => $user->getId(),
                                'nickname' => $user->getNickname(),
                                'email' => $user->getEmail(),
                                'password' => $user->getPassword(),
                                'roles' => $user->getRoles(),
                                'is_verified' => $user->getIsVerified(),
                                'is_new' => $user->getIsNew(),
                                'tokenExpiration' => $user->getTokenExpiration(),
                                'tokenForPython' => $user->getTokenForPython(),
                                'tokenForPythonExpiration' => $user->getTokenForPythonExpiration(),
                            ],
                            'fromPython' => $fromPython,
                            'Confirmation' => $confirmation,
                            'Token' => $token,
                        ];

                        // ====================================================

                    }

                } else {
                    $response = [
                        'status' => 'Success',
                        'message' => 'Succes: 1 pseudo, aucun mail',
                        'usernameOrEmail' => $usernameOrEmail,
                        'password' => $password,
                        'nicknameCount' => $nicknameCount,
                        'emailCount' => $emailCount,
                        'pass_trouve' => 'user == null, pas de pass',
                        'Confirmation' => $confirmation,
                    ];
                }
                            }
            // la recherche a trouvé + d'1 mail
            if ($emailCount > 1) {
                $response = [
                    'status' => 'Error',
                    'message' => 'WARNING: 1 pseudo, plusieurs mails',
                    'usernameOrEmail' => $usernameOrEmail,
                    'password' => $password,
                    'nicknameCount' => $nicknameCount,
                    'emailCount' => $emailCount,
                    'Confirmation' => $confirmation,
                ];
            }
        // la recherche a trouvé + d'1 nickname
        } elseif ($nicknameCount > 1) {
            if ($emailCount == 0) {
                $response = [
                    'status' => 'Error',
                    'message' => 'WARNING: plusieurs pseudo, aucun mail',
                    'usernameOrEmail' => $usernameOrEmail,
                    'password' => $password,
                    'nicknameCount' => $nicknameCount,
                    'emailCount' => $emailCount,
                    'Confirmation' => $confirmation,
                ];
            }
            if ($emailCount == 1) {
                $response = [
                    'status' => 'Error',
                    'message' => 'WARNING: plusieurs pseudo, plusieurs mails',
                    'usernameOrEmail' => $usernameOrEmail,
                    'password' => $password,
                    'nicknameCount' => $nicknameCount,
                    'emailCount' => $emailCount,
                    'Confirmation' => $confirmation,
                ];
            }
            if ($emailCount > 1) {
                $response = [
                    'status' => 'Error',
                    'message' => 'WARNING: plusieurs pseudo, plusieurs mails',
                    'usernameOrEmail' => $usernameOrEmail,
                    'password' => $password,
                    'nicknameCount' => $nicknameCount,
                    'emailCount' => $emailCount,
                    'Confirmation' => $confirmation,
                ];
            }
        } else {
            $response = [
                'status' => 'Error',
                'message' => 'Situation non gérée',
            ];
        }

        return new JsonResponse($response);
	    }
	}

