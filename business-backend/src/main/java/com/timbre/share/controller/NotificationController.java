package com.timbre.share.controller;

import com.timbre.share.common.ApiResponse;
import com.timbre.share.entity.Notification;
import com.timbre.share.repository.NotificationRepository;
import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/notification")
@RequiredArgsConstructor
public class NotificationController {

    private final NotificationRepository notificationRepository;

    @GetMapping("/list")
    public ApiResponse<?> list(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "12") int pageSize,
            HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        Page<Notification> result = notificationRepository
                .findByUserIdOrderByCreatedAtDesc(userId, PageRequest.of(page - 1, pageSize));
        return ApiResponse.paginated(result.getContent(), result.getTotalElements(), page, pageSize);
    }

    @GetMapping("/unread-count")
    public ApiResponse<?> unreadCount(HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ApiResponse.success(Map.of("count", notificationRepository.countByUserIdAndIsReadFalse(userId)));
    }

    @PostMapping("/mark-read/{notifyId}")
    public ApiResponse<?> markRead(@PathVariable Long notifyId) {
        notificationRepository.findById(notifyId).ifPresent(n -> {
            n.setIsRead(true);
            notificationRepository.save(n);
        });
        return ApiResponse.success();
    }

    @PostMapping("/mark-all-read")
    public ApiResponse<?> markAllRead(HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        notificationRepository.markAllReadByUserId(userId);
        return ApiResponse.success();
    }
}
