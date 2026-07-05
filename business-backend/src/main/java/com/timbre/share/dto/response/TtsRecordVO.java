package com.timbre.share.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class TtsRecordVO {
    private Long recordId;
    private Long userId;
    private Long voiceId;
    private String text;
    private Integer textLength;
    private BigDecimal speed;
    private Integer volume;
    private Integer pitch;
    private String audioUrl;
    private Integer status;
    private LocalDateTime createdAt;
}
