package com.timbre.share.repository;

import com.timbre.share.entity.VoiceDownload;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface VoiceDownloadRepository extends JpaRepository<VoiceDownload, Long> {
    Page<VoiceDownload> findByUserIdOrderByCreatedAtDesc(Long userId, Pageable pageable);
}
