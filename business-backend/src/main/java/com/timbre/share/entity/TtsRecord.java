package com.timbre.share.entity;

import jakarta.persistence.*;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "tts_record")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TtsRecord {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long recordId;

    @Column(nullable = false)
    private Long userId;

    @Column(nullable = false)
    private Long voiceId;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String text;

    @Column(nullable = false)
    private Integer textLength;

    @Column(nullable = false, precision = 3, scale = 1)
    private BigDecimal speed;

    @Column(nullable = false)
    private Integer volume;

    @Column(nullable = false)
    private Integer pitch;

    private String audioUrl;

    @Column(nullable = false)
    private Integer status;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        if (textLength == null) textLength = text != null ? text.length() : 0;
        if (speed == null) speed = BigDecimal.valueOf(1.0);
        if (volume == null) volume = 80;
        if (pitch == null) pitch = 0;
        if (status == null) status = 0;
    }
}
