package com.timbre.share.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "script_dub_task")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ScriptDubTask {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long taskId;

    @Column(nullable = false)
    private Long userId;

    private String scriptName;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String scriptText;

    private String charset;

    @Column(nullable = false)
    private Integer roleCount;

    @Column(columnDefinition = "JSON")
    private String voiceMapping;

    @Column(columnDefinition = "JSON")
    private String emotionResult;

    private String outputUrl;

    @Column(nullable = false)
    private Integer status;

    private String errorMessage;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
        if (roleCount == null) roleCount = 0;
        if (status == null) status = 0;
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
