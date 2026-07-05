package com.timbre.share.dto.request;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import lombok.Data;

@Data
public class SendCodeRequest {
    @NotBlank
    @Pattern(regexp = "^1\\d{10}$")
    private String phone;
}
