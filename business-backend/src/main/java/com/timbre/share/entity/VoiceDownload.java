package com.timbre.share.entity;

import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "voice_download")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class VoiceDownload {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long downloadId;

    private Long shareId;

    @Column(nullable = false)
    private Long userId;

    @Column(nullable = false)
    private Long voiceId;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
