package com.timbre.share.controller;

import com.timbre.share.common.ApiResponse;
import com.timbre.share.dto.request.ShareRequest;
import com.timbre.share.service.ShareService;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/share")
@RequiredArgsConstructor
public class ShareController {

    private final ShareService shareService;

    @PostMapping("/publish/{voiceId}")
    public ApiResponse<?> publish(@PathVariable Long voiceId, @RequestBody ShareRequest req,
                                  HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ApiResponse.success(shareService.shareVoice(voiceId, userId, req.getTags()));
    }

    @PostMapping("/unpublish/{voiceId}")
    public ApiResponse<?> unpublish(@PathVariable Long voiceId, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        shareService.unshareVoice(voiceId, userId);
        return ApiResponse.success();
    }

    @GetMapping("/public")
    public ApiResponse<?> listPublic(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "12") int pageSize) {
        Page<?> result = shareService.listPublic(page, pageSize);
        return ApiResponse.paginated(result.getContent(), result.getTotalElements(), page, pageSize);
    }

    @PostMapping("/download/{shareId}")
    public ApiResponse<?> download(@PathVariable Long shareId, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ApiResponse.success(shareService.downloadVoice(shareId, userId));
    }

    @GetMapping("/my-downloads")
    public ApiResponse<?> myDownloads(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "12") int pageSize,
            HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        Page<?> result = shareService.listDownloads(userId, page, pageSize);
        return ApiResponse.paginated(result.getContent(), result.getTotalElements(), page, pageSize);
    }
}
