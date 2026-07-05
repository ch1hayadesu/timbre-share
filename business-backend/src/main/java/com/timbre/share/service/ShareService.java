package com.timbre.share.service;

import com.timbre.share.common.AppException;
import com.timbre.share.dto.response.SharedVoiceVO;
import com.timbre.share.entity.Voice;
import com.timbre.share.entity.VoiceDownload;
import com.timbre.share.entity.VoiceShare;
import com.timbre.share.repository.VoiceDownloadRepository;
import com.timbre.share.repository.VoiceRepository;
import com.timbre.share.repository.VoiceShareRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ShareService {

    private final VoiceShareRepository voiceShareRepository;
    private final VoiceRepository voiceRepository;
    private final VoiceDownloadRepository voiceDownloadRepository;

    public SharedVoiceVO shareVoice(Long voiceId, Long userId, String tags) {
        Voice voice = voiceRepository.findById(voiceId)
                .orElseThrow(() -> AppException.notFound("音色"));
        if (!voice.getUserId().equals(userId)) throw AppException.forbidden();
        if (voice.getStatus() != 1) throw AppException.paramError("音色正在训练中，无法分享");
        if (voiceShareRepository.findByVoiceId(voiceId).isPresent()) {
            throw AppException.paramError("该音色已分享");
        }
        VoiceShare share = VoiceShare.builder()
                .voiceId(voiceId).userId(userId).tags(tags).build();
        share = voiceShareRepository.save(share);
        return new SharedVoiceVO(share.getShareId(), voice.getVoiceId(),
                voice.getVoiceName(), userId, 0, tags, voice.getSampleUrl(), share.getCreatedAt());
    }

    public void unshareVoice(Long voiceId, Long userId) {
        VoiceShare share = voiceShareRepository.findByVoiceId(voiceId)
                .orElseThrow(() -> AppException.notFound("分享记录"));
        if (!share.getUserId().equals(userId)) throw AppException.forbidden();
        share.setStatus(0);
        voiceShareRepository.save(share);
    }

    public Page<VoiceShare> listPublic(int page, int pageSize) {
        return voiceShareRepository.findByStatusOrderByDownloadCountDescCreatedAtDesc(
                1, PageRequest.of(page - 1, pageSize));
    }

    @Transactional
    public Voice downloadVoice(Long shareId, Long userId) {
        VoiceShare share = voiceShareRepository.findById(shareId)
                .orElseThrow(() -> AppException.notFound("分享记录"));
        if (share.getStatus() != 1) throw AppException.notFound("分享记录");

        Voice original = voiceRepository.findById(share.getVoiceId())
                .orElseThrow(() -> AppException.notFound("音色"));

        Voice copy = Voice.builder()
                .userId(userId).voiceName(original.getVoiceName())
                .cloneMode(original.getCloneMode()).status(1)
                .source("shared").sourceShareId(shareId)
                .modelPath(original.getModelPath()).sampleUrl(original.getSampleUrl())
                .build();
        copy = voiceRepository.save(copy);

        VoiceDownload download = VoiceDownload.builder()
                .shareId(shareId).userId(userId).voiceId(share.getVoiceId()).build();
        voiceDownloadRepository.save(download);

        share.setDownloadCount(share.getDownloadCount() + 1);
        voiceShareRepository.save(share);

        return copy;
    }

    public Page<VoiceDownload> listDownloads(Long userId, int page, int pageSize) {
        return voiceDownloadRepository.findByUserIdOrderByCreatedAtDesc(userId, PageRequest.of(page - 1, pageSize));
    }
}
