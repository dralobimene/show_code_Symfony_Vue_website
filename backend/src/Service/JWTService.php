<?php

namespace App\Service;

use DateTimeImmutable;

class JWTService
{
    
    /**
    * Génère un token JWT à partir des données du header, du payload et du secret fournis.
    *
    * @param array $header Le header JWT.
    * @param array $payload Le payload JWT.
    * @param string $secret Le secret utilisé pour signer le token JWT.
    * @param int $validity La durée de validité du token JWT en secondes (par défaut : 10800 s).
    * 
    * @return string Le token JWT généré.
    */
    public function generate(array $header,
                            array $payload,
                            string $secret,
                            int $validity = 10800): string
    {

        // check validity
        if($validity > 0)
        {

            // get time
            $now = new DateTimeImmutable();

            // get expiration
            $exp = $now->getTimeStamp() + $validity;

            // le payload
            $payload['iat'] = $now->getTimeStamp();

            // expiration
            $payload['exp'] = $exp;

        }


        // base64 encode header
        $base64Header = base64_encode(json_encode($header));

        // base64 encode payload
        $base64Payload = base64_encode(json_encode($payload));

        // on nettoie les valeurs encodées
        // retrait des sigles +, /  et =
        // on les supprime pas, on les remplace
        $base64Header = str_replace(['+', '/', '='], ['-', '_', ''], $base64Header);
        $base64Payload = str_replace(['+', '/', '='], ['-', '_', ''], $base64Payload);

        // on genere la signature

        // il ns faut D'ABORD definir 1 secret qui soit stocké qque part
        // ici, on le stocke ds .env.local (aller voir la valeur JWT_SECRET)
        // il est stocké manuellement par le dev
        // il faut en + aller ds config/services.yaml
        // et creer 1 param qui prend la valeur du JWT_SECRET du .env.local
        // implementé ds la sect° parameters, là aussi crée manuellement par le dev
        $secret = base64_encode($secret);

        // on rassemble les 3 parties du token et on
        // encode avec l'algo SHA256
        // l'ensemble represente la signature
        $signature = hash_hmac('sha256', $base64Header.'.'.$base64Payload, $secret, true);

        // on encode la signature en base64
        $base64Signature = base64_encode($signature);

        // on nettoie la signature
        $base64Signature = str_replace(['+', '/', '='], ['-', '_', ''], $base64Signature);

        // on peut maintenant creer le token
        $jwt = $base64Header.'.'.$base64Payload.'.'.$base64Signature;

        // le service JWTService est crée, on peut
        // l'utiliser dans les controller

        return $jwt;
    }

    // ====================================================================
    // ====================================================================

    // methodes qui vérifient
    // 1 si le token est correctement formé,
    // 2 s'il n'a pas expiré
    // on ne verifie pas encore son contenu

    // 1° verif: est ce que le $token est bien formé?

    /**
     * Vérifie si le format du token est valide.
     *
     * @param string $token Le token JWT à vérifier.
     *
     * @return bool Renvoie true si le token est valide, false sinon.
     */
    public function isValid(string $token): bool
    {
        //----------------------------------------------------------------
        return preg_match(
                '/^[a-zA-Z0-9\-\_\=]+\.[a-zA-Z0-9\-\_\=]+\.[a-zA-Z0-9\-\_\=]+$/',
                $token
        ) === 1;

    }
    
    // ====================================================================
    // ====================================================================

    // 2° verif: est ce que le token a expiré?
    // d'abord, recuperer le payload
    
    /**
     * Récupère le payload d'un token JWT.
     *
     * @param string $token Le token JWT.
     *
     * @return array Le payload du token JWT.
     */
    public function getPayload(string $token): array
    {

        // on demonte le token
        $array = explode(".", $token);

        // on decode le payload
        $payload = json_decode(base64_decode($array[1]), true);

        //
        return $payload;
    }

    // ====================================================================

    // ensuite, verifier si le token a expiré ou pas
    // methode qui renvoie 1 bool
    // 1 (true) = le $token a expiré

    /**
     * Vérifie si le token est expiré.
     *
     * @param string $token Le token JWT à vérifier.
     *
     * @return bool Renvoie true si le token est expiré, false sinon.
     */
    public function isExpired($token)
    {
        $payload = $this->getPayload($token);
        $now = new DateTimeImmutable();

        return $payload['exp'] < $now->getTimestamp();
    }

    // ====================================================================
    // ====================================================================

    // 3° verif: la signature, c-a-d, le contenu, pr checker
    // l'integrite du $token

    // d'abord, il faut recuperer le header

    /**
     * Récupère le header d'un token JWT.
     *
     * @param string $token Le token JWT.
     *
     * @return array Le header du token JWT.
     */
    public function getheader(string $token): array
    {

        // on demonte le token
        $array = explode(".", $token);

        // on decode le header
        $header = json_decode(base64_decode($array[0]), true);

        //
        return $header;
    }

    // ====================================================================

    /**
    * Vérifie si le token JWT fourni est valide en le comparant à un nouveau
    * token généré à partir des mêmes données.
    *
    * @param string $token Le token JWT à vérifier.
    * @param string $secret Le secret utilisé pour signer le token JWT.
    * 
    * @return bool Renvoie true si le token est valide, false sinon.
    *
    * AJOUTE: le type de retour: bool
    */
    public function check(string $token, string $secret): bool
    {

        // on recupere le header et le payload
        $header = $this->getheader($token);
        $payload = $this->getPayload($token);

        // on genere 1 token avec ce qu'on vient de recuperer
        $verifToken = $this->generate($header, $payload, $secret, 0);

        // si les 2 token st egaux,
        // la signature n'a pas été corrompue
        return $token === $verifToken;

    }

    // ====================================================================

    /**
     * Valide un token JWT en vérifiant sa forme, sa date d'expiration et son intégrité.
     *
     * @param string $token Le token JWT à valider.
     * @param string $secret Le secret utilisé pour signer le token JWT.
     *
     * @return bool Renvoie true si le token est valide, false sinon.
     */
    public function validate(string $token, string $secret): bool
    {
        try {
            // Cérifie si le token est correctement formé
            if (!$this->isValid($token)) {
                return false;
            }

            // Vérifie si le token est périmé ou pas
            if ($this->isExpired($token)) {
                return false;
            }

            // Vérifie le contenu du token
            if (!$this->check($token, $secret)) {
                return false;
            }

            // Posibilité d'ajouter de nouvelles vérifications
            // additionnelles

            return true;
        } catch (\Exception $e) {
            return false;
        }

    }

    // ====================================================================

    /**
     * Décrypte un token JWT et renvoie son payload.
     *
     * @param string $token Le token JWT à décrypter.
     *
     * @return array Le payload du token JWT.
     * 
     * @throws \Exception Si le format du token est invalide.
     */
    public function decode(string $token): array
    {
        // Cérifie si le token est correctement formé
        if (!$this->isValid($token)) {
            throw new \Exception('Invalid token format');
        }

        // Obtenir le payload du token
        $payload = $this->getPayload($token);

        return $payload;
    }
    // ====================================================================

}
