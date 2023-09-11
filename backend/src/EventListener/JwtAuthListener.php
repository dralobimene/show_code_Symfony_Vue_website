<?php

namespace App\EventListener;

use App\Service\JWTService;
use Symfony\Component\HttpKernel\Event\RequestEvent;
use Symfony\Component\HttpKernel\Exception\AccessDeniedHttpException;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;

use Symfony\Component\HttpFoundation\JsonResponse;

class JwtAuthListener
{

    // ========================================================================

    private $jwtService;

    // ========================================================================

    public function __construct(JWTService $jwtService,
                                ParameterBagInterface $params)
    {
        $this->jwtService = $jwtService;
        $this->secret = $params->get('app.jwtsecret');
    }

    // ========================================================================

    /**
     * Méthode appelée à chaque requête du kernel. Vérifie si la route actuelle est sécurisée et si un token JWT valide est présent.
     *
     * @param RequestEvent $event L'événement de requête reçu.
     * 
     * @return void
     * 
     * @throws AccessDeniedHttpException Si l'utilisateur n'a pas accès à la ressource.
     *
     * AJOUTE: le type de retour: void
     */
    public function onKernelRequest(RequestEvent $event): void
    {
        $request = $event->getRequest();
        $route = $request->attributes->get('_route');

        // Add routes that require authentication in the array
        $securedRoutes = [

            // panneau de l'utilisateur
            // controller: src/Controller/
            // vue: view05_secured_user_peronal_panel.vue
            'app_secured_user01_personal_panel',

            // permet de poster 1 commentaire
            // controller: src/Controller/CommentUserPostController.php
            // vue: src/views/view08_comment_user_post.vue
            'app_comment_user_post',

            // permet de se déconnecter
            // controller: src/Controller/LogoutController.php
            // vue: src/views/view06_logout.vue
            'app_logout',

            // permet de repondre à 1 commentaire
            // controller: src/Controller/ReplyUserPostController.php
            // vue: src/views/view09_reply_user_post.vue
            'app_reply_user_post',
        ];

        if (in_array($route, $securedRoutes)) {
            $authorizationHeader = $request->headers->get('Authorization');

            // Log the Authorization header value
            error_log('Authorization header value: ' . $authorizationHeader);

            if (!$authorizationHeader || substr($authorizationHeader, 0, 7) !== 'Bearer ') {
                $info = "Access denied: Missing or invalid JWT token";
                $info .= " - Route: ". $route;
                throw new AccessDeniedHttpException($info);
            }

            $token = substr($authorizationHeader, 7);

            if (!$this->jwtService->validate($token, $this->secret)) {
                // throw new AccessDeniedHttpException('Access Denied: Invalid JWT token');

                if (!$this->jwtService->validate($token, $this->secret)) {
                    $response = new JsonResponse([
                        'error' => 'Access Denied from JwtAuthListener',
                        'message' => 'Invalid JWT token',
                        'route' => $route,
                    ]);
                    $response->setStatusCode(403);
                    $event->setResponse($response);
                    return;
                }
            }
        }
    }

    // ========================================================================

}
