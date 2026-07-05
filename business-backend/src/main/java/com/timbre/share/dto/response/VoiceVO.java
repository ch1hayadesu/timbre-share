package com.timbre.share.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class VoiceVO {
    private Long voiceId;
    private Long userId;
    private String voiceName;
    private Integer cloneMode;
    private Integer status;
    private String source;
    private String rawAudioUrl;
    private String modelPath;
    private String sampleUrl;
    private String errorMessage;
    private Integer retryCount;
    private LocalDateTime createdAt;
}
