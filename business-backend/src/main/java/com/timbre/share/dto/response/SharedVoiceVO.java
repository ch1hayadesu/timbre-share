package com.timbre.share.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class SharedVoiceVO {
    private Long shareId;
    private Long voiceId;
    private String voiceName;
    private Long userId;
    private Integer downloadCount;
    private String tags;
    private String sampleUrl;
    private LocalDateTime createdAt;
}
