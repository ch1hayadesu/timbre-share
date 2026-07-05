package com.timbre.share.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "voice_share")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class VoiceShare {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long shareId;

    @Column(nullable = false, unique = true)
    private Long voiceId;

    @Column(nullable = false)
    private Long userId;

    @Column(nullable = false)
    private Integer downloadCount;

    @Column(nullable = false)
    private Integer status;

    private Integer auditStatus;
    private String tags;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
        if (downloadCount == null) downloadCount = 0;
        if (status == null) status = 1;
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
