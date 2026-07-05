package com.timbre.share.service;

import com.timbre.share.common.AppException;
import com.timbre.share.config.JwtConfig;
import com.timbre.share.dto.request.LoginRequest;
import com.timbre.share.dto.response.UserVO;
import com.timbre.share.entity.User;
import com.timbre.share.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final JwtConfig jwtConfig;

    public Map<String, String> sendCode(String phone) {
        return Map.of("message", "验证码已发送");
    }

    public Map<String, Object> login(LoginRequest req) {
        User user = userRepository.findByPhone(req.getPhone())
                .orElseGet(() -> userRepository.save(
                        User.builder().phone(req.getPhone()).membershipLevel(0).build()
                ));
        String token = jwtConfig.generateToken(user.getUserId());
        UserVO userVO = new UserVO(
                user.getUserId(), user.getPhone(),
                user.getMembershipLevel(), user.getCreatedAt()
        );
        return Map.of("token", token, "user", userVO);
    }

    public UserVO getProfile(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> AppException.notFound("用户"));
        return new UserVO(user.getUserId(), user.getPhone(),
                user.getMembershipLevel(), user.getCreatedAt());
    }
}
