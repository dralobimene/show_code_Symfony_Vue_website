<?php

namespace App\Document;

use Doctrine\ODM\MongoDB\Mapping\Annotations as MongoDB;
use MongoDB\BSON\ObjectId;

// WARNING avec le linter ms semble qd meme necessaire pr que
// le controller src/Controller/AdmSommaireController.php
// puisse utiliser les methodes qui se trouvent ds
// src/Repository/CommentRepository.php
use App\Repository\GameRepository;

/**
 * @MongoDB\Document(collection="game", repositoryClass=GameRepository::class)
 */
class Game
{
    /**
     * @MongoDB\Id
     */
    protected $id;

    /**
     * @MongoDB\Field(type="string")
     */
    protected $game_name;
    
    /**
     * @MongoDB\Field(type="string")
     */
    protected $name;
    
    /**
     * @MongoDB\Field(type="string")
     */
    protected $level;

    /**
	   * @MongoDB\Field(type="hash")
	   */
	  protected $exit_tile;

    /**
	   * @MongoDB\Field(type="hash")
	   */
	  protected $entry_tile;

    /**
	   * @MongoDB\Field(type="collection")
	   */
	  protected $white_tiles_array;

    /**
	   * @MongoDB\Field(type="collection")
	   */
	  protected $blue_tiles_array;

    /**
	   * @MongoDB\Field(type="collection")
	   */
	  protected $total_tiles_array;

    /**
	   * @MongoDB\Field(type="collection")
	   */
	  protected $rooms_tiles_array;

    /**
	   * @MongoDB\Field(type="collection")
	   */
    protected $attributes_rooms_array;

    // constructeur
    /**
     * @param string $game_name
     * @param string $name
     * @param string $level
     * @param collection $exit_tile
     * @param collection $entry_tile
     * @param collection $white_tiles_array
     * @param collection $blue_tiles_array
     * @param collection $total_tiles_array
     * @param collection $rooms_tiles_array
     * @param collection $attributes_rooms_array
     */
    public function __construct($game_name,
                                $name,
                                $level,
                                $exit_tile,
                                $entry_tile,
                                $white_tiles_array,
                                $blue_tiles_array,
                                $total_tiles_array,
                                $rooms_tiles_array,
                                $attributes_rooms_array)
    {
        $this->id = new ObjectId();
        $this->game_name = $game_name;
        $this->name = $name;
        $this->level = $level;
        $this->exit_tile = $exit_tile;
        $this->entry_tile = $entry_tile;
        $this->white_tiles_array = $white_tiles_array;
        $this->blue_tiles_array = $blue_tiles_array;
        $this->total_tiles_array = $total_tiles_array;
        $this->rooms_tiles_array = $rooms_tiles_array;
        $this->attributes_rooms_array = $attributes_rooms_array;
    }

    // getters and setters
    public function getId(): ?string
    {
    	return $this->id;
    }
    
    public function getGameName(): ?string
    {
    	return $this->game_name;
    }
    
    public function setGameName(string $game_name): self
    {
    	$this->game_name = $game_name;
    	return $this;
    }
    
    public function getName(): ?string
    {
    	return $this->name;
    }
    
    public function setName(string $name): self
    {
    	$this->name = $name;
    	return $this;
    }
    
    public function getLevel(): ?string
    {
    	return $this->level;
    }
    
    public function setLevel(string $level): self
    {
    	$this->level = $level;
    	return $this;
    }

    /**
     * Get the value of exit_tile
     *
     * @return array
     */
	    public function getExitTile(): array
	    {
	    	return $this->exit_tile;
	    }

      /**
     * Set the value of exit_tile
     *
     * @param array $exit_tile
     * @return self
     */ 
	    public function setExitTile(array $exit_tile): self
	    {
	    	$this->exit_tile = $exit_tile;
	    	return $this;
      }

    /**
     * Get the value of entry_tile
     *
     * @return array
     */
	    public function getEntryTile(): array
	    {
	    	return $this->entry_tile;
	    }

      /**
     * Set the value of entry_tile
     *
     * @param array $entry_tile
     * @return self
     */ 
	    public function setEntryTile(array $entry_tile): self
	    {
	    	$this->entry_tile = $entry_tile;
	    	return $this;
      }

    /**
     * Get the value of white_tiles_array
     *
     * @return array
     */
	    public function getWhiteTilesArray(): array
	    {
	    	return $this->white_tiles_array;
	    }

      /**
     * Set the value of white_tiles_array
     *
     * @param array $white_tiles_array
     * @return self
     */ 
	    public function setWhiteTilesArray(array $white_tiles_array): self
	    {
	    	$this->white_tiles_array = $white_tiles_array;
	    	return $this;
      }

    /**
     * Get the value of blue_tiles_array
     *
     * @return array
     */
	    public function getBlueTilesArray(): array
	    {
	    	return $this->blue_tiles_array;
	    }

      /**
     * Set the value of blue_tiles_array
     *
     * @param array $blue_tiles_array
     * @return self
     */ 
	    public function setBlueTilesArray(array $blue_tiles_array): self
	    {
	    	$this->blue_tiles_array = $blue_tiles_array;
	    	return $this;
      }

    /**
     * Get the value of total_tiles_array
     *
     * @return array
     */
	    public function getTotalTilesArray(): array
	    {
	    	return $this->total_tiles_array;
	    }

      /**
     * Set the value of total_tiles_array
     *
     * @param array $total_tiles_array
     * @return self
     */ 
	    public function setTotalTilesArray(array $total_tiles_array): self
	    {
	    	$this->total_tiles_array = $total_tiles_array;
	    	return $this;
      }

    /**
     * Get the value of rooms_tiles_array
     *
     * @return array
     */
	    public function getRoomsTilesArray(): array
	    {
	    	return $this->rooms_tiles_array;
	    }

      /**
     * Set the value of rooms_tiles_array
     *
     * @param array $rooms_tiles_array
     * @return self
     */ 
	    public function setRoomsTilesArray(array $rooms_tiles_array): self
	    {
	    	$this->rooms_tiles_array = $rooms_tiles_array;
	    	return $this;
      }

    /**
     * Get the value of attributes_rooms_array
     *
     * @return array
     */
	    public function getAttributesRoomsArray(): array
	    {
	    	return $this->attributes_rooms_array;
	    }

      /**
     * Set the value of attributes_rooms_array
     *
     * @param array $attributes_rooms_array
     * @return self
     */ 
	    public function setAttributesRoomsArray(array $attributes_rooms_array): self
	    {
	    	$this->attributes_rooms_array = $attributes_rooms_array;
	    	return $this;
      }

    /**
      * Convert the Game object to an array.
      *
      * @return array<string,mixed>
      */
      public function toArray(): array
      {
        return [
          'id' => $this->getId(),
          'game_name' => $this->getGameName(),
          'name' => $this->getName(),
          'level' => $this->getLevel(),
          'exit_tile' => $this->getExitTile(),
          'entry_tile' => $this->getEntryTile(),
          'white_tiles_array' => $this->getWhiteTilesArray(),
          'blue_tiles_array' => $this->getBlueTilesArray(),
          'total_tiles_array' => $this->getTotalTilesArray(),
          'rooms_tiles_array' => $this->getRoomsTilesArray(),
          'attributes_rooms_array' => $this->getAttributesRoomsArray(),
        ];
      }
	}
