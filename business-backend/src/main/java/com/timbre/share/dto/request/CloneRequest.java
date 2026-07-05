package com.timbre.share.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class CloneRequest {
    @NotBlank
    @Size(max = 100)
    private String voiceName;

    private Integer cloneMode = 0;
}
