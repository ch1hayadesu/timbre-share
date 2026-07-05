package com.timbre.share.service;

import com.timbre.share.common.AppException;
import com.timbre.share.dto.response.VoiceVO;
import com.timbre.share.entity.Voice;
import com.timbre.share.repository.VoiceRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class VoiceService {

    private final VoiceRepository voiceRepository;

    public Page<Voice> listVoices(Long userId, int page, int pageSize) {
        return voiceRepository.findByUserIdOrderByCreatedAtDesc(userId, PageRequest.of(page - 1, pageSize));
    }

    public List<Voice> getPresets() {
        return voiceRepository.findBySource("preset");
    }

    public Voice getVoice(Long voiceId, Long userId) {
        Voice voice = voiceRepository.findById(voiceId)
                .orElseThrow(() -> AppException.notFound("音色"));
        if (!voice.getUserId().equals(userId) && !"preset".equals(voice.getSource())) {
            throw AppException.forbidden();
        }
        return voice;
    }

    public Voice createCloneTask(Long userId, String voiceName, int cloneMode) {
        long count = voiceRepository.countByUserIdAndStatus(userId, 1);
        if (count >= 10) {
            throw AppException.paramError("音色数量已达上限（10个）");
        }
        Voice voice = Voice.builder()
                .userId(userId).voiceName(voiceName)
                .cloneMode(cloneMode).status(0).source("cloned")
                .build();
        return voiceRepository.save(voice);
    }

    public void deleteVoice(Long voiceId, Long userId) {
        Voice voice = voiceRepository.findById(voiceId)
                .orElseThrow(() -> AppException.notFound("音色"));
        if (!voice.getUserId().equals(userId)) {
            throw AppException.forbidden();
        }
        voiceRepository.delete(voice);
    }
}
