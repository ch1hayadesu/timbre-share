package com.timbre.share.dto.request;

import jakarta.validation.constraints.*;
import lombok.Data;

import java.math.BigDecimal;

@Data
public class TtsRequest {
    @NotNull
    private Long voiceId;

    @NotBlank
    @Size(max = 1000)
    private String text;

    @DecimalMin("0.5")
    @DecimalMax("2.0")
    private BigDecimal speed = BigDecimal.valueOf(1.0);

    @Min(0)
    @Max(100)
    private Integer volume = 80;

    @Min(-12)
    @Max(12)
    private Integer pitch = 0;
}
