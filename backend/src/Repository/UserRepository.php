<?php
// src/Repository/UserRepository.php

namespace App\Repository;

use Doctrine\ODM\MongoDB\Repository\DocumentRepository;
use Doctrine\ODM\MongoDB\Iterator\Iterator;

class UserRepository extends DocumentRepository
{

    /**
     * Trouve les utlisateurs par leur attribut 'is_verified'
     *
     * @param bool $isVerified
     * @return Iterator
     */
    public function findByIsVerified(bool $isVerified): Iterator
    {
        return $this->createQueryBuilder()
            ->field('is_verified')->equals($isVerified)
            ->getQuery()
            ->execute();
    }

    // ========================================================================

    /**
     * Trouve les utilisateurs par leur attribut 'is_new'
     *
     * @param bool $isNew
     * @return Iterator
     */
    public function findByIsNew(bool $isNew): Iterator
    {
        return $this->createQueryBuilder()
            ->field('is_new')->equals($isNew)
            ->getQuery()
            ->execute();
    }

    // ========================================================================

    /**
     * Compte le nbre de 'documents' basé sur le critère fourni
     *
     * @param array $criteria
     *
     * @return int
     */
    public function count(array $criteria): int
    {
        return $this->createQueryBuilder()
            ->field('is_new')->equals($criteria['is_new'])
            ->count()
            ->getQuery()
            ->execute();
    }
}
