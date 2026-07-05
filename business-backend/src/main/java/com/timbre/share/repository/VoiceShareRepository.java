package com.timbre.share.repository;

import com.timbre.share.entity.VoiceShare;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface VoiceShareRepository extends JpaRepository<VoiceShare, Long> {
    Optional<VoiceShare> findByVoiceId(Long voiceId);

    Page<VoiceShare> findByStatusOrderByDownloadCountDescCreatedAtDesc(Integer status, Pageable pageable);
}
