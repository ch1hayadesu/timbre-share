package com.timbre.share.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "voice")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Voice {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long voiceId;

    @Column(nullable = false)
    private Long userId;

    @Column(nullable = false, length = 100)
    private String voiceName;

    @Column(nullable = false)
    private Integer cloneMode;

    @Column(nullable = false)
    private Integer status;

    @Column(nullable = false, length = 20)
    private String source;

    private Long sourceShareId;
    private String rawAudioUrl;
    private String modelPath;
    private String sampleUrl;
    private String errorMessage;

    @Column(nullable = false)
    private Integer retryCount;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
        if (cloneMode == null) cloneMode = 0;
        if (status == null) status = 0;
        if (source == null) source = "cloned";
        if (retryCount == null) retryCount = 0;
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
