<?php
// src/Repository/GameRepository.php

namespace App\Repository;

use Doctrine\ODM\MongoDB\Repository\DocumentRepository;
use Doctrine\ODM\MongoDB\Iterator\Iterator;

class GameRepository extends DocumentRepository
{

    // ========================================================================

    /**
     * Count documents based on the provided criteria.
     *
     * @param array $criteria
     *
     * @return int
     */
    public function count(array $criteria): int
    {
        return $this->createQueryBuilder()
            ->field('game_name')->equals($criteria['game_name'])
            ->count()
            ->getQuery()
            ->execute();
    }

    // ========================================================================

}
