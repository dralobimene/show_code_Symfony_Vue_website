<?php

namespace App\EventListener;

use Symfony\Component\HttpKernel\Event\ExceptionEvent;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Exception\AccessDeniedHttpException;

class AccessDeniedExceptionListener
{

    /**
     * Handles kernel exceptions.
     * 
     * @param ExceptionEvent $event
     * 
     * @return void
     */
    public function onKernelException(ExceptionEvent $event): void
    {
        // You get the exception object from the received event
        $exception = $event->getThrowable();

        if ($exception instanceof AccessDeniedHttpException) {
            $response = new Response();
            $response->setContent(json_encode([
                'error' => 'Access Denied',
                'message' => $exception->getMessage(),
            ]));
            $response->setStatusCode(Response::HTTP_FORBIDDEN);
            $response->headers->set('Content-Type', 'application/json');

            // sends the modified response object to the event
            $event->setResponse($response);
        }
    }
}
