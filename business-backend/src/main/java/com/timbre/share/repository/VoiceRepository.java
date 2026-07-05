package com.timbre.share.repository;

import com.timbre.share.entity.Voice;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface VoiceRepository extends JpaRepository<Voice, Long> {
    Page<Voice> findByUserIdOrderByCreatedAtDesc(Long userId, Pageable pageable);

    List<Voice> findBySource(String source);

    long countByUserIdAndStatus(Long userId, Integer status);

    Page<Voice> findByVoiceNameContainingIgnoreCase(String keyword, Pageable pageable);
}
