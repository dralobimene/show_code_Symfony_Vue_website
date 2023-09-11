<?php

/*
 * Lorsque vous effectuez une demande vers la route /secured_user/personal_panel,
 * JwtRequestListener vérifie si le jeton JWT est valide et, si c'est le cas,
 * la demande est transmise au PersonalPanelController pour un traitement ultérieur.
 * Si le jeton JWT est invalide ou manquant, JwtRequestListener lèvera une
 * exception, et la demande n'atteindra pas le PersonalPanelController.
 * Dans ce cas, vous recevrez une réponse d'erreur en raison du jeton JWT
 * invalide ou manquant.
 *
 * Ainsi, la validation JWT et JwtRequestListener fonctionnent ensemble.
 * L'écouteur est responsable de valider le jeton JWT pour des routes
 * spécifiques, tandis que le contrôleur gère le traitement des demandes en
 * fonction de la validité du jeton JWT et d'autres paramètres de demande.
*/

namespace App\EventListener;

use App\Service\JWTService;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;
use Symfony\Component\HttpKernel\Event\RequestEvent;
use Symfony\Component\HttpKernel\Exception\AccessDeniedHttpException;
use Symfony\Component\HttpKernel\KernelEvents;

class JwtRequestListener implements EventSubscriberInterface
{

    // ========================================================================

    private JWTService $jwtService;
    private string $jwtSecret;

    // ========================================================================

    public function __construct(JWTService $jwtService, string $jwtSecret)
    {
        $this->jwtService = $jwtService;
        $this->jwtSecret = $jwtSecret;
    }

    // ========================================================================

    /**
    * Méthode appelée à chaque requête du kernel.
    * Vérifie si la route actuelle nécessite un jeton JWT valide.
    *
    * @param RequestEvent $event L'événement de requête reçu.
    * 
    * @return void
    * 
    * @throws AccessDeniedHttpException Si le jeton JWT est invalide ou manquant.
    *
    * AJOUTE: le type de retour: void
    */

    // V1
    /*
    public function onKernelRequest(RequestEvent $event): void
    {
        $request = $event->getRequest();
        $route = $request->attributes->get('_route');

        // Only check JWT for the secured_user01_personal_panel route
        if ($route === 'app_secured_user01_personal_panel') {
            $authorizationHeader = $request->headers->get('Authorization');
            $jwtToken = substr($authorizationHeader, 7);

            if (!$this->jwtService->validate($jwtToken, $this->jwtSecret)) {
                $message = 'Error from JWT token,';
                $message .= 'definition to src/EventListener/JwtRequestListener.php';
                $message .= 'Exception throwed to SF controller: app_secured_user01_personal_panel';
                $message .= 'and view05_secured_user_personal_panel.vue';
                throw new AccessDeniedHttpException($message);
            }
        }
    }
    */

    // V2
    public function onKernelRequest(RequestEvent $event): void
    {
        $request = $event->getRequest();
        $route = $request->attributes->get('_route');

        // Define an array of secured routes and corresponding Vue files
        $securedRoutes = [
            'app_secured_user01_personal_panel' => 'view05_secured_user_personal_panel.vue',
            'app_test_jwt_listener' => 'test_jwt_listener_route',
        ];

        // Check JWT for the secured routes in the array
        if (array_key_exists($route, $securedRoutes)) {
            $authorizationHeader = $request->headers->get('Authorization');
            $jwtToken = substr($authorizationHeader, 7);

            if (!$this->jwtService->validate($jwtToken, $this->jwtSecret)) {
                $message = 'Error from JWT token, ';
                $message .= 'definition file: src/EventListener/JwtRequestListener.php, ';
                $message .= "Exception thrown: SF controller: {$route}, ";
                $message .= "and {$securedRoutes[$route]}";
                throw new AccessDeniedHttpException($message);
            }
        }
    }

    // ========================================================================

    /**
    * Retourne un tableau d'abonnements d'événements de kernel pour ce subscriber.
    *
    * @return array Le tableau d'abonnements d'événements de kernel pour ce subscriber.
    *
    * AJOUTE: type de retour: array
    */
    public static function getSubscribedEvents(): array
    {
        return [
            KernelEvents::REQUEST => 'onKernelRequest',
        ];
    }

    // ========================================================================

}
