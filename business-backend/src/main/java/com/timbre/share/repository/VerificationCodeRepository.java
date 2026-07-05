package com.timbre.share.repository;

import com.timbre.share.entity.VerificationCode;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface VerificationCodeRepository extends JpaRepository<VerificationCode, Long> {
    Optional<VerificationCode> findTopByPhoneAndCodeAndUsedFalseOrderByCreatedAtDesc(String phone, String code);
}
