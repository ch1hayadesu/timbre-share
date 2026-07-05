package com.timbre.share.controller;

import com.timbre.share.common.ApiResponse;
import com.timbre.share.dto.request.ScriptDubRequest;
import com.timbre.share.service.ScriptDubService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/script-dub")
@RequiredArgsConstructor
public class ScriptDubController {

    private final ScriptDubService scriptDubService;

    @PostMapping("/create")
    public ApiResponse<?> createTask(@Valid @RequestBody ScriptDubRequest req, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ApiResponse.success(scriptDubService.createTask(
                userId, req.getScriptText(), req.getScriptName(),
                req.getCharset(), req.getVoiceMapping()));
    }

    @GetMapping("/list")
    public ApiResponse<?> listTasks(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "12") int pageSize,
            HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        Page<?> result = scriptDubService.listTasks(userId, page, pageSize);
        return ApiResponse.paginated(result.getContent(), result.getTotalElements(), page, pageSize);
    }

    @GetMapping("/detail/{taskId}")
    public ApiResponse<?> getTask(@PathVariable Long taskId, HttpServletRequest request) {
        Long userId = (Long) request.getAttribute("userId");
        return ApiResponse.success(scriptDubService.getTask(taskId, userId));
    }
}
