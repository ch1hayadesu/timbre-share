package com.timbre.share.service;

import com.timbre.share.common.AppException;
import com.timbre.share.dto.request.TtsRequest;
import com.timbre.share.entity.TtsRecord;
import com.timbre.share.entity.Voice;
import com.timbre.share.repository.TtsRecordRepository;
import com.timbre.share.repository.VoiceRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class TtsService {

    private final TtsRecordRepository ttsRecordRepository;
    private final VoiceRepository voiceRepository;

    public TtsRecord synthesize(Long userId, TtsRequest req) {
        Voice voice = voiceRepository.findById(req.getVoiceId())
                .orElseThrow(() -> AppException.notFound("音色"));
        if (!voice.getUserId().equals(userId)
                && !"preset".equals(voice.getSource())
                && !"shared".equals(voice.getSource())) {
            throw AppException.forbidden();
        }
        if (voice.getStatus() != 1) {
            throw AppException.paramError("音色尚未就绪");
        }
        TtsRecord record = TtsRecord.builder()
                .userId(userId).voiceId(req.getVoiceId())
                .text(req.getText()).speed(req.getSpeed())
                .volume(req.getVolume()).pitch(req.getPitch())
                .status(0).build();
        return ttsRecordRepository.save(record);
    }

    public Page<TtsRecord> listHistory(Long userId, int page, int pageSize) {
        return ttsRecordRepository.findByUserIdOrderByCreatedAtDesc(userId, PageRequest.of(page - 1, pageSize));
    }

    public TtsRecord getRecord(Long recordId, Long userId) {
        TtsRecord record = ttsRecordRepository.findById(recordId)
                .orElseThrow(() -> AppException.notFound("合成记录"));
        if (!record.getUserId().equals(userId)) {
            throw AppException.forbidden();
        }
        return record;
    }
}
