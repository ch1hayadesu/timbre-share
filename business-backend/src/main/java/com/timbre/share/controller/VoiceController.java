package com.timbre.share.controller;

import com.timbre.share.common.ApiResponse;
import com.timbre.share.dto.request.CloneRequest;
import com.timbre.share.service.VoiceService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/voice")
@RequiredArgsConstructor
public class VoiceController {

    private final VoiceService voiceService;

    @GetMapping("/list")
    public ApiResponse<?> listVoices(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "12") int pageSize,
            HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        Page<?> result = voiceService.listVoices(userId, page, pageSize);
        return ApiResponse.paginated(result.getContent(), result.getTotalElements(), page, pageSize);
    }

    @GetMapping("/presets")
    public ApiResponse<?> getPresets() {
        return ApiResponse.success(voiceService.getPresets());
    }

    @GetMapping("/detail/{voiceId}")
    public ApiResponse<?> getVoice(@PathVariable Long voiceId, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ApiResponse.success(voiceService.getVoice(voiceId, userId));
    }

    @PostMapping("/clone")
    public ApiResponse<?> createClone(@Valid @RequestBody CloneRequest req, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ApiResponse.success(voiceService.createCloneTask(userId, req.getVoiceName(), req.getCloneMode()));
    }

    @DeleteMapping("/delete/{voiceId}")
    public ApiResponse<?> deleteVoice(@PathVariable Long voiceId, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        voiceService.deleteVoice(voiceId, userId);
        return ApiResponse.success();
    }
}
