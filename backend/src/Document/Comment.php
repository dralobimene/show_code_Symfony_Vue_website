<?php

namespace App\Document;

use Doctrine\ODM\MongoDB\Mapping\Annotations as MongoDB;
use MongoDB\BSON\ObjectId;

// WARNING avec le linter ms semble qd meme necessaire pr que
// le controller src/Controller/AdmSommaireController.php
// puisse utiliser les methodes qui se trouvent ds
// src/Repository/CommentRepository.php
use App\Repository\CommentRepository;

/**
 * @MongoDB\Document(collection="comment", repositoryClass=CommentRepository::class)
 */
class Comment
{
    /**
     * @MongoDB\Id
     */
    protected $id;
    
    /**
     * @MongoDB\Field(type="string")
     */
    protected $author;
    
    /**
     * @MongoDB\Field(type="string")
     */
    protected $category;
    
    /**
     * @MongoDB\Field(type="string")
     */
    protected $title;
   
    /**
     * @MongoDB\Field(type="string")
     */
    protected $content;

    /**
     * @MongoDB\Field(type="date")
     */
    protected $created_at;

    /**
     * @MongoDB\Field(type="date")
     */
    protected $published_at;
   
    /**
     * @MongoDB\Field(type="string")
     */
    protected $flag;

    /**
     * @MongoDB\Field(type="bool")
     */
    protected $is_published;

    /**
     * @MongoDB\Field(type="string", nullable=true)
     */
    protected $parent_id;

    /**
	   * @MongoDB\Field(type="boolean")
	   */
    protected $is_new;


    // constructeur
    /**
     * @param string $author
     * @param string $category
     * @param string $title
     * @param string $content
     * @param \DateTime $created_at
     * @param \DateTime $published_at
     * @param string $flag
     * @param bool $is_published
     * @param string|null $parent_id
     * @param bool $is_new
     */
    public function __construct($author,
                                $category,
                                $title,
                                $content,
                                $created_at = null,
                                $published_at = null,
                                $flag = "En attente de modération",
                                $is_published = false,
                                $parent_id = null,
                                $is_new = true)
    {
        $this->id = new ObjectId();
        $this->author = $author;
        $this->category = $category;
        $this->title = $title;
        $this->content = $content;
        $this->created_at = $created_at ? $created_at : new \DateTime();
        $this->published_at = $published_at;
        $this->flag = $flag;
        $this->is_published = $is_published;
        $this->parent_id = $parent_id;
        $this->is_new = $is_new;
    }

    // getters and setters
    public function getId(): ?string
    {
    	return $this->id;
    }
    
    public function getAuthor(): ?string
    {
    	return $this->author;
    }
    
    public function setAuthor(string $author): self
    {
    	$this->author = $author;
    	return $this;
    }
    
    public function getCategory(): ?string
    {
    	return $this->category;
    }
    
    public function setCategory(string $category): self
    {
    	$this->category = $category;
    	return $this;
    }
    
    public function getTitle(): ?string
    {
    	return $this->title;
    }
    
    public function setTitle(string $title): self
    {
    	$this->title = $title;
    	return $this;
    }

    public function getContent(): ?string
    {
    	return $this->content;
    }
    
    public function setContent(string $content): self
    {
    	$this->content = $content;
    	return $this;
    }

    public function getCreatedAt(): ?\DateTime
    {
    	return $this->created_at;
    }
    
    public function setCreatedAt(\DateTime $created_at): self
    {
    	$this->created_at = $created_at;
    	return $this;
    }
    
    public function getPublishedAt(): ?\DateTime
    {
    	return $this->published_at;
    }
    
    public function setPublishedAt(?\DateTime $published_at): self
    {
    	$this->published_at = $published_at;
    	return $this;
    }
    
    public function getFlag(): ?string
    {
    	return $this->flag;
    }
    
    public function setFlag(string $flag): self
    {
    	$this->flag = $flag;
    	return $this;
    }

    /**
     * @return bool
     */
    public function getIsPublished(): bool
    {
        return $this->is_published;
    }

    /**
     * @param bool $is_published
     * @return self
     */
    public function setIsPublished(bool $is_published): self
    {
        $this->is_published = $is_published;
        return $this;
    }

    /**
     * @return string|null
     */
    public function getParentId(): ?string
    {
        return $this->parent_id;
    }

    /**
     * @param string|null $parent_id
     * @return self
     */
    public function setParentId(?string $parent_id): self
    {
        $this->parent_id = $parent_id;
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
     * @return array<string, mixed>
     */
    public function toArray(): array
    {
        return [
            'id' => $this->getId(),
            'author' => $this->getAuthor(),
            'category' => $this->getCategory(),
            'title' => $this->getTitle(),
            'content' => $this->getContent(),
            'created_at' => $this->getCreatedAt(),
            'published_at' => $this->getPublishedAt(),
            'flag' => $this->getFlag(),
            'is_published' => $this->getIsPublished(),
            'parent_id' => $this->getParentId(),
            'is_new' => $this->getIsNew()
        ];
    }

}
