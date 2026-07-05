package com.timbre.share.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class ScriptDubVO {
    private Long taskId;
    private Long userId;
    private String scriptName;
    private String scriptText;
    private String charset;
    private Integer roleCount;
    private String voiceMapping;
    private String emotionResult;
    private String outputUrl;
    private Integer status;
    private String errorMessage;
    private LocalDateTime createdAt;
}
