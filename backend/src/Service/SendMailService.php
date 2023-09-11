<?php
    namespace App\Service;

    use Symfony\Bridge\Twig\Mime\TemplatedEmail;
    use Symfony\Component\Mailer\MailerInterface;
    use Symfony\Component\Mime\Email;

    // ========================================================================

	  class SendMailService
    {

        private $mailer;

        // ========================================================================
        
        /**
         * Constructeur de la classe SendMailService.
         *
         * @param MailerInterface $mailer Instance de MailerInterface pour l'envoi d'e-mails.
         */
        public function __construct(MailerInterface $mailer)
        {
            $this->mailer = $mailer;
        }

        // ========================================================================

        /**
         * Envoie un e-mail avec le contenu fourni, en utilisant le système de messagerie Symfony.
         *
         * @param string $from L'adresse e-mail de l'expéditeur.
         * @param string $to L'adresse e-mail du destinataire.
         * @param string $subject L'objet de l'e-mail.
         * @param string $content Le contenu HTML de l'e-mail.
         * @param array $context Les variables de contexte à utiliser dans le contenu HTML de l'e-mail.
         * 
         * @return void
         */
        public function send(
            string $from,
            string $to,
            string $subject,
            string $content,
            array $context
        ): void
        {
            //On crée le mail
            $email = (new TemplatedEmail())
                ->from($from)
                ->to($to)
                ->subject($subject)
                ->htmlTemplate('email01/activation_email.html.twig')
                ->context($context);

            // On envoie le mail
            $this->mailer->send($email);
        }

        // ========================================================================

        /**
         * Envoie un e-mail de texte brut avec le contenu fourni, en utilisant le système de messagerie Symfony.
         *
         * @param string $from L'adresse e-mail de l'expéditeur.
         * @param string $to L'adresse e-mail du destinataire.
         * @param string $subject L'objet de l'e-mail.
         * @param string $content Le contenu en texte brut de l'e-mail.
         * @param array $context Les variables de contexte à utiliser dans le contenu de l'e-mail. Par défaut, ce paramètre est un tableau vide.
         * 
         * @return void
         */
        public function sendBasicEmail(
                        string $from,
                        string $to,
                        string $subject,
                        string $content,
                        array $context = []
        ): void
        {
            $email = (new Email())
                ->from($from)
                ->to($to)
                ->subject($subject)
                ->text($content);
                
            //
            $this->mailer->send($email);
        }
    }
