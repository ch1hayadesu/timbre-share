package com.timbre.share.controller;

import com.timbre.share.common.ApiResponse;
import com.timbre.share.dto.request.TtsRequest;
import com.timbre.share.service.TtsService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/tts")
@RequiredArgsConstructor
public class TtsController {

    private final TtsService ttsService;

    @PostMapping("/synthesize")
    public ApiResponse<?> synthesize(@Valid @RequestBody TtsRequest req, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ApiResponse.success(ttsService.synthesize(userId, req));
    }

    @GetMapping("/history")
    public ApiResponse<?> listHistory(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "12") int pageSize,
            HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        Page<?> result = ttsService.listHistory(userId, page, pageSize);
        return ApiResponse.paginated(result.getContent(), result.getTotalElements(), page, pageSize);
    }

    @GetMapping("/record/{recordId}")
    public ApiResponse<?> getRecord(@PathVariable Long recordId, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ApiResponse.success(ttsService.getRecord(recordId, userId));
    }
}
