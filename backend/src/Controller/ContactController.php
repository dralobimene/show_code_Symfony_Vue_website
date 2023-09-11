<?php
// fichier: src/Controller/ContactController.php
// vue associée: src/views/view21_contact.vue

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;

use Symfony\Component\HttpFoundation\Request;
use App\Service\JWTService;
use Doctrine\ODM\MongoDB\DocumentManager;
use App\Document\User;
use App\Service\SendMailService;
use Symfony\Component\Validator\Validator\ValidatorInterface;

/*
 * fichier: src/Controller/ContactController.php
 * vue associée: src/views/view21_contact.vue
 */
class ContactController extends AbstractController
{
    #[Route('/contact', name: 'app_contact', methods: ['POST'])]
    public function index(Request $request,
                          JWTService $jwt,
                          DocumentManager $dm,
                          SendMailService $mail,
                          ValidatorInterface $vi,): JsonResponse
    {

        // ====================================================================

        // Récupère l'en-tête Authorization
        $authHeader = $request->headers->get('Authorization');

        // supprimer le bearer du header
        $token = substr($authHeader, 7);

        // ====================================================================

        // Validation du token
        // Appelle la méthode de src/Service/JWTService
        // -- méthode: validate()
        // qui appelle elle-même
        // -- méthode: isValid()
        // -- méthode: isExpired()
        // -- méthode: check()
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
        
        // Décode le token et récupère le payload
        // Appelle la méthode src/Service/JWTService
        // -- methode: findOneBy()
        $userId = $payload['user_id'];

        // Récupère les données de l'utilisateur connecté en fonction de l'user_id du payload
        // Appelle la méthode native de ODM
        $user = $dm->getRepository(User::class)->findOneBy(['_id' => $userId]); 

        // ====================================================================

        // Erreur si l'utilisateur connecté n'est pas trouvé
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

        // Crée un tableau avec les données de l'utilisateur
        $userData = [
            'token' => $token,
            'id' => $user->getId(),
            'nickname' => $user->getNickname(),
            'email' => $user->getEmail(),
            'password' => $user->getPassword(),
            'roles' => $user->getRoles(),
            'is_verified' => $user->getIsVerified(),
        ];

        // ====================================================================

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
        
        // Récupère les données de la requête
        $data = json_decode($request->getContent(), true);
        $subject = $data['subject'];
        $content = $data['content'];

        // ====================================================================

        // Prépare le contenu de l'email en plain text
        $emailContent = "Subject: " . $subject . "\r\n" . "Content: " . $content;

        // ====================================================================

        // Envoie l'email en utilisant la méthode send() avec le type de
        // contenu 'text/plain'
        $mail->sendBasicEmail(
            $user->getEmail(),  // from
            'lolo@test.fr',     // to
            $subject,           // subject
            $emailContent,      // text
            $context = [],
            'text/plain'        // content type
        );

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
                                'message3' => 'Request found'
                                ]);

        // ====================================================================

    }
}
