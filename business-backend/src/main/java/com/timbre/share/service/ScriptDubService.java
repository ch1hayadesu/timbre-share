package com.timbre.share.service;

import com.timbre.share.common.AppException;
import com.timbre.share.entity.ScriptDubTask;
import com.timbre.share.repository.ScriptDubTaskRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class ScriptDubService {

    private final ScriptDubTaskRepository scriptDubTaskRepository;

    public ScriptDubTask createTask(Long userId, String scriptText, String scriptName,
                                    String charset, String voiceMapping) {
        ScriptDubTask task = ScriptDubTask.builder()
                .userId(userId).scriptText(scriptText)
                .scriptName(scriptName).charset(charset)
                .voiceMapping(voiceMapping).status(0).build();
        return scriptDubTaskRepository.save(task);
    }

    public Page<ScriptDubTask> listTasks(Long userId, int page, int pageSize) {
        return scriptDubTaskRepository.findByUserIdOrderByCreatedAtDesc(userId, PageRequest.of(page - 1, pageSize));
    }

    public ScriptDubTask getTask(Long taskId, Long userId) {
        ScriptDubTask task = scriptDubTaskRepository.findById(taskId)
                .orElseThrow(() -> AppException.notFound("配音任务"));
        if (!task.getUserId().equals(userId)) {
            throw AppException.forbidden();
        }
        return task;
    }
}
