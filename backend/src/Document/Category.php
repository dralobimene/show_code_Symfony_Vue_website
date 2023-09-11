<?php

namespace App\Document;

use Doctrine\ODM\MongoDB\Mapping\Annotations as MongoDB;
use MongoDB\BSON\ObjectId;

/**
 * @MongoDB\Document(collection="category")
 */
class Category
{

    /**
     * @MongoDB\Id
     */ 
    protected $_id;

    /**
     * @MongoDB\Field(type="string")
     */
    protected $name;

    /**
     * @MongoDB\Field(type="string")
     */
    protected $description;

    /**
     * @MongoDB\Field
     */
    protected $metadata;

    // constructeur
    /**
     * Constructor
     * @param string $name
     * @param string $description
     * @param mixed $metadata
     */
    public function __construct($name,
                                $description,
                                $metadata)
    {
        $this->_id = new ObjectId();
        $this->name = $name;
        $this->description = $description;
        $this->metadata = $metadata;
    }

    // Getters / Setters
    public function getId(): ?string
    {
        return $this->_id;
    }

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(string $name): self
    {
        $this->name = $name;
    }

    public function getDescription(): ?string
    {
        return $this->description;
    }

    public function setDescription(string $description): self
    {
        $this->description = $description;
    }

    /**
     * @return mixed
     */
    public function getMetadata(): mixed
    {
        return $this->metadata;
    }

    /**
     * @param mixed $metadata
     * @return void
     */
    public function setMetadata($metadata): void
    {
        $this->metadata = $metadata;
    }

    /**
     * @return array<string, mixed>
     */
    public function toArray(): array
    {
        return [
            '_id' => $this->getId(),
            'name' => $this->getName(),
            'description' => $this->getDescription(),
            'metadata' => $this->metadata,
        ];
    }
}
