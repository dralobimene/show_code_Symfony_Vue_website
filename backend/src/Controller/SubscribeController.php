<?php
// fichier src/Controller/SubscribeController.php
// vue associée: src/views/view02_subscribe.vue

namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

use Symfony\Component\Validator\Constraints as Assert;
use Symfony\Component\Validator\Validator\ValidatorInterface;

use Doctrine\ODM\MongoDB\DocumentManager;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;
use Psr\Log\LoggerInterface;

use Symfony\Component\Routing\Generator\UrlGeneratorInterface;
use DateTime;

use App\Document\User;
use App\Service\SendMailService;
use App\Service\JWTService;

class SubscribeController extends AbstractController
{

    // Ajouter UrlGeneratorInterface comme dépendance
    private $urlGenerator;

    /**
     * Constructeur de la classe SubscribeController.
     *
     * @param UrlGeneratorInterface $urlGenerator Interface pour la génération d'URLs
     */
    public function __construct(UrlGeneratorInterface $urlGenerator)
    {
        $this->urlGenerator = $urlGenerator;
    }

    // ========================================================================

    /**
     * Génère une URL absolue à partir d'un chemin et d'un token.
     *
     * @param string $path  Le nom du chemin (route) pour lequel générer l'URL
     * @param string $token Le token à inclure en tant que paramètre dans l'URL
     *
     * @return string L'URL absolue générée
     */
    private function generateAbsoluteUrl($path, $token)
    {
        // Générer l'URL absolue en utilisant le chemin et le token donnés
        $absoluteUrl = $this->urlGenerator->generate(
            $path,
            ['token' => $token],
            UrlGeneratorInterface::ABSOLUTE_URL
        );

        return $absoluteUrl;
    }

    // ========================================================================

    /**
     * Gère la requête d'inscription d'un utilisateur.
     *
     * @param Request $request L'objet de la requête HTTP entrante
     * @param ValidatorInterface $vi Interface du validateur de Symfony
     * @param DocumentManager $dm Gestionnaire de document pour Doctrine MongoDB ODM
     * @param UserPasswordHasherInterface $uphi Interface pour le hachage de mots de passe
     * @param LoggerInterface $li Interface pour les journaux de logging
     * @param SendMailService $mail Service d'envoi de mails
     * @param JWTService $jwt Service de gestion des tokens JWT
     *
     * @return JsonResponse Réponse HTTP au format JSON
     */
    #[Route('/subscribe', name: 'app_subscribe', methods: ['POST'])]
    public function index(Request $request,
                            ValidatorInterface $vi,
                            DocumentManager $dm,
                            UserPasswordHasherInterface $uphi,
                            LoggerInterface $li,
                            SendMailService $mail,
                            JWTService $jwt): JsonResponse
    {
        
        // Récupérez les données de view02_subscribe.vue
        $data = json_decode($request->getContent(), true);

        // opérateur de fusion null en PHP. C'est une façon plus courte et
        // plus pratique d'utiliser l'opérateur ternaire pour la vérification
        // des valeurs null.
        // EXPLICATIONS:
        // $data['nickname'] ?? '' : Cela signifie que si $data['nickname']
        // est défini et n'est pas NULL, alors sa valeur sera assignée à
        // $nickname. Sinon, si $data['nickname'] n'est pas défini ou est NULL,
        // alors $nickname sera une chaîne vide ('').
        $nickname = $data['nickname'] ?? '';
        $email = $data['email'] ?? '';
        $password = $data['password'] ?? '';

        // les contraintes sur le champs nickname
        $nicknameConstraint = [
            new Assert\NotBlank(),
            new Assert\Length(['min' => 3, 'max' => 20]),
            new Assert\Regex([
                'pattern' => '/^(?=.*[A-Za-z])[A-Za-z\d@\-_]{3,20}$/',
                'message' => 'Nickname must contain at least 1 letter, and may contain digits and 3 special characters (@, -, _). Length: min = 3, max = 20.',
            ]),
        ];

        // les contraintes sur le champs email
        $emailConstraint = [
            new Assert\NotBlank(),
            new Assert\Email(),
        ];

        // les contraintes sur le champs password
        $passwordConstraint = [
            new Assert\NotBlank(),
            new Assert\Length(['min' => 10, 'max' => 20]),
            new Assert\Regex([
                'pattern' => '/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@\-_])[A-Za-z\d@\-_]{10,20}$/',
                'message' => 'Password must contain at least 1 digit, 1 uppercase letter, and 1 special character (either @, -, or _). Length: min = 10, max = 20',
            ]),
        ];

        // tableau
        $errors = [];

        // elts de $errors qui represente un autre tableau
        $errors['nickname'] = $vi->validate($nickname, $nicknameConstraint);
        // elts de $errors qui represente un autre tableau
        $errors['email'] = $vi->validate($email, $emailConstraint);
        // elts de $errors qui represente un autre tableau
        $errors['password'] = $vi->validate($password, $passwordConstraint);

        $hasErrors = false;

        foreach ($errors as $errorList) {
            if (count($errorList) > 0) {
                $hasErrors = true;
                break;
            }
        }

        if ($hasErrors) {
            return new JsonResponse(['valid' => false,
                            'message' => 'You entered bad value(s) somewhere, please check and fix']);
        }

        // bloc try catch qui essaye d'inserer le nouvel enregistrement
        // dans la collection 'user' de la base de données MongoDB
        if (!$hasErrors) {
            try {
               
                //
                $user = new User();
                $user->setNickname($nickname);
                $user->setEmail($email);
                $user->setRoles(['ROLE_USER']);
                $user->setPassword($uphi->hashPassword($user, $password));
                $user->setIsVerified(false);
                $user->setInscriptionDate(new DateTime());
                $user->setIsNew(true);
                                
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

                // on definit 1 expiration pr le token
                $tokenExpiration = new \DateTime();
                $tokenExpiration->modify('+1 day');

                $user->setToken($token);
                $user->setTokenExpiration($tokenExpiration);

                // Génère l'URL absolue pour la route app_check_token avec le token donné
                $absoluteUrl = 'https://localhost:5173/view07_approve/' . $token;

                $dm->persist($user);
                $dm->flush();

                // on utilise le service pr envoyer le mail
                $mail->send(
                                'test@testService.fr',
                                $user->getEmail(),
                                'Activation de votre compte',
                                '',
                                [
                                    "user" => $user,
                                    "token" => $token,
                                    "confirmationLink" => $absoluteUrl
                                ]
                            );

                // $li = logguerInterface
                $li->info('User successfully saved: ' . $user->getId());

                return new JsonResponse(['valid' => true,
                                        'message' => 'thank you, redirection'
                                        ]);

            // catch, les infos entrées st bien formatées
            // ms au moins l'1 d'entre elles existe déjà ds la DB et
            // cô il y a 1 schema validator nickname et email sur la mongo DB...
            } catch (\MongoDB\Driver\Exception\BulkWriteException $except) {
                $li->error('Error saving user: ' . $except->getMessage());
                return new JsonResponse(['valid' => false,
                                        'message' => $except->getMessage()
                                        ]);

            // catch, au moins 1 des infos entrée ne correspond pas aux
            // patterns requis
            } catch (\Exception $except) {
                $li->error('Error saving user: ' . $except->getMessage());
                return new JsonResponse(['valid' => false,
                                'message' => 'An error occurred while saving your information.']);
            }

        }
        
    }
}
