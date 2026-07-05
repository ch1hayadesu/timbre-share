package com.timbre.share.repository;

import com.timbre.share.entity.TtsRecord;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TtsRecordRepository extends JpaRepository<TtsRecord, Long> {
    Page<TtsRecord> findByUserIdOrderByCreatedAtDesc(Long userId, Pageable pageable);
}
