<?php
// src/Repository/CommentRepository.php

namespace App\Repository;

use Doctrine\ODM\MongoDB\Repository\DocumentRepository;
use Doctrine\ODM\MongoDB\Iterator\Iterator;

class CommentRepository extends DocumentRepository
{

    /**
     * Finds comment by the is_published attribute.
     *
     * @param bool $isPublished
     * @return Iterator
     */
    public function findByIsPublished(bool $isPublished): Iterator
    {
        return $this->createQueryBuilder()
            ->field('is_published')->equals($isPublished)
            ->getQuery()
            ->execute();
    }

    // ========================================================================

    /**
     * Finds ONLY COMMENTS by the is_new attribute.
     * with parent_id attribute == null
     *
     * @param bool $isNew
     * @return Iterator
     */
    public function findByIsNew(bool $isNew): Iterator
    {
        return $this->createQueryBuilder()
            ->field('is_new')->equals($isNew)
            ->field('parent_id')->equals(null)
            ->getQuery()
            ->execute();
    }

    // ========================================================================

    /**
     * Finds all comments and their replies.
     * Si au moins 1 réponse a son attribut is_new à true alors le dernier
     * elt du tableau sera a true. Si aucune réponse ne contient son attribut
     * is_new a true, alors le dernier elt du tableau sera à false
     *
     * stocke dc
     * - le commentaire
     * - les réponses Eventuelles
     * - 1 boolean pr savoir s'il y a des nvelles réponses ou pas
     *
     * @return array
     */
    public function findAllCommentsWithReplies(): array
    {

        $commentsWithReplies = [];

    // Find all comments with parent_id == null
    $comments = $this->createQueryBuilder()
        ->field('parent_id')->equals(null)
        ->getQuery()
        ->execute();

    foreach ($comments as $comment) {
        $containNewReply = false;

        // Find replies for each comment (where parent_id == comment's _id)
        $replies = $this->createQueryBuilder()
            ->field('parent_id')->equals($comment->getId())
            ->getQuery()
            ->execute();

        foreach ($replies as $reply) {
            if ($reply->getIsNew()) {
                $containNewReply = true;
                break;
            }
        }

        $commentWithReplies = [
            'comment' => $comment,
            'replies' => iterator_to_array($replies),
            'containNewReply' => $containNewReply
        ];

        array_push($commentsWithReplies, $commentWithReplies);
    }

    return $commentsWithReplies;

    }

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
            ->field('is_new')->equals($criteria['is_new'])
            ->count()
            ->getQuery()
            ->execute();
    }

    // ========================================================================

}
