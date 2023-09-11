<?php

  namespace App\Document;

  use DateTime;

  use Doctrine\Bundle\MongoDBBundle\Validator\Constraints\Unique as MongoDBUnique;
  use Doctrine\ODM\MongoDB\Mapping\Annotations as MongoDB;
  use Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface;
  
  // WARNING avec le linter ms semble qd meme necessaire pr que
  // le controller src/Controller/AdmSommaireController.php
  // puisse utiliser les methodes qui se trouvent ds
  // src/Repository/UserRepository.php
  use App\Repository\UserRepository;

	/**
   * @MongoDB\Document(collection="user", repositoryClass=UserRepository::class)
   * @MongoDBUnique(fields={"email", "nickname"})
	 */
	class User implements PasswordAuthenticatedUserInterface
	{
	    /**
	     * @MongoDB\Id
	     */
	    protected $id;
	    
	    /**
	     * @MongoDB\Field(type="string")
	     */
	    protected $nickname;
	    
	    /**
	     * @MongoDB\Field(type="string")
	     */
	    protected $email;
	    
	    /**
	     * @MongoDB\Field(type="collection")
	     */
	    protected $roles;

	    /**
	     * @MongoDB\Field(type="string")
	     */
	    protected $password;
	    
	    /**
	     * @MongoDB\Field(type="boolean")
	     */
      protected $is_verified;

      /**
       * @MongoDB\Field(type="string")
       */
      protected $token;

      /**
       * @MongoDB\Field(type="date")
       */
      protected $tokenExpiration;

      /**
       * @MongoDB\Field(type="string", nullable=true)
       */
      protected $tokenForPython;

      /**
       * @MongoDB\Field(type="date", nullable=true)
       */
      protected $tokenForPythonExpiration;

      /**
       * @MongoDB\Field(type="date", nullable=true)
       */
      protected $inscriptionDate;

      /**
	     * @MongoDB\Field(type="boolean")
	     */
      protected $is_new;

	    
	    // Contructor
	    public function __construct()
	    {
    		$this->roles = ['ROLE_USER'];
        $this->is_verified = false;
        $this->is_new = true;
	    }

	    // Add getters and setters
	    public function getId(): ?string
	    {
	    	return $this->id;
	    }
	    
	    public function getNickname(): ?string
	    {
	    	return $this->nickname;
	    }
	    
	    public function setNickname(string $nickname): self
	    {
	    	$this->nickname = $nickname;
	    	return $this;
	    }
	    
	    public function getEmail(): ?string
	    {
	    	return $this->email;
	    }
	    
	    public function setEmail(string $email): self
	    {
	    	$this->email = $email;
	    	return $this;
	    }

      /**
     * Get the value of roles
     *
     * @return array
     */
	    public function getRoles(): array
	    {
	    	return $this->roles;
	    }

      /**
     * Set the value of roles
     *
     * @param array $roles
     * @return self
     */ 
	    public function setRoles(array $roles): self
	    {
	    	$this->roles = $roles;
	    	return $this;
	    }
	    
	    public function getPassword(): ?string
	    {
	    	return $this->password;
	    }
	    
	    public function setPassword(string $password): self
	    {
	    	$this->password = $password;
	    	return $this;
	    }
	    
	    public function getIsVerified(): ?bool
	    {
	    	return $this->is_verified;
	    }
	    
	    public function setIsVerified(bool $is_verified): self
	    {
	    	$this->is_verified = $is_verified;
	    	return $this;
      }

      public function getToken(): ?string
      {
        return $this->token;
      }

      public function setToken(?string $token): self
      {
        $this->token = $token;
        return $this;
      }

      public function getTokenExpiration(): ?\DateTime
      {
        return $this->tokenExpiration;
      }

      public function setTokenExpiration(?\DateTime $tokenExpiration): self
      {
        $this->tokenExpiration = $tokenExpiration;
        return $this;
      }

      public function getTokenForPython(): ?string
      {
        return $this->tokenForPython;
      }

      public function setTokenForPython(?string $tokenForPython): self
      {
        $this->tokenForPython = $tokenForPython;
        return $this;
      }

      public function getTokenForPythonExpiration(): ?\DateTime
      {
        return $this->tokenForPythonExpiration;
      }

      public function setTokenForPythonExpiration(?\DateTime $tokenForPythonExpiration): self
      {
        $this->tokenForPythonExpiration = $tokenForPythonExpiration;
        return $this;
      }

      public function getInscriptionDate(): ?\DateTime
      {
    	  return $this->inscriptionDate;
      }
    
      public function setInscriptionDate(\DateTime $inscriptionDate): self
      {
    	  $this->inscriptionDate = $inscriptionDate;
    	  return $this;
      }

      public function getIsNew(): ?bool
	    {
	    	return $this->is_new;
	    }
	    
	    public function setIsNew(bool $is_new): self
	    {
	    	$this->is_new = $is_new;
	    	return $this;
      }

      /**
      * Convert the User object to an array.
      *
      * @return array<string,mixed>
      */
      public function toArray(): array
      {
        return [
          '_id' => $this->getId(),
          'nickname' => $this->getNickname(),
          'email' => $this->getEmail(),
          'roles' => $this->getRoles(),
          'password' => $this->getPassword(),
          'is_verified' => $this->getIsVerified(),
          'inscriptionDate' => $this->getInscriptionDate(),
          'is_new' => $this->getIsNew(),
          'token' => $this->getToken(),
          'tokenExpiration' => $this->getTokenExpiration(),
          'tokenForPython' => $this->getTokenForPython(),
          'tokenForPythonExpiration' => $this->getTokenForPythonExpiration(),
        ];
      }
	}
