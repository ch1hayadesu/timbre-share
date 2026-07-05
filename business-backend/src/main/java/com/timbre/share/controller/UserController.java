package com.timbre.share.controller;

import com.timbre.share.common.ApiResponse;
import com.timbre.share.dto.request.LoginRequest;
import com.timbre.share.dto.request.SendCodeRequest;
import com.timbre.share.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/user")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @PostMapping("/send-code")
    public ApiResponse<?> sendCode(@Valid @RequestBody SendCodeRequest req) {
        return ApiResponse.success(userService.sendCode(req.getPhone()));
    }

    @PostMapping("/login")
    public ApiResponse<?> login(@Valid @RequestBody LoginRequest req) {
        return ApiResponse.success(userService.login(req));
    }

    @GetMapping("/profile")
    public ApiResponse<?> getProfile(HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ApiResponse.success(userService.getProfile(userId));
    }
}
