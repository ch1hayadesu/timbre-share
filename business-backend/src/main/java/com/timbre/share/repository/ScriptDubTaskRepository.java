package com.timbre.share.repository;

import com.timbre.share.entity.ScriptDubTask;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ScriptDubTaskRepository extends JpaRepository<ScriptDubTask, Long> {
    Page<ScriptDubTask> findByUserIdOrderByCreatedAtDesc(Long userId, Pageable pageable);
}
