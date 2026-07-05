package com.timbre.share.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
public class UserVO {
    private Long userId;
    private String phone;
    private Integer membershipLevel;
    private LocalDateTime createdAt;
}
