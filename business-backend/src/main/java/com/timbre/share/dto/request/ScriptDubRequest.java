package com.timbre.share.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class ScriptDubRequest {
    private String scriptName;
    @NotBlank
    private String scriptText;
    private String charset;
    private String voiceMapping; // JSON string: {"角色名": voiceId}
}
