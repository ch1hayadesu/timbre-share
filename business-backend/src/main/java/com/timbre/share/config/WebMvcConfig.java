package com.timbre.share.config;

import com.timbre.share.common.AppException;
import com.timbre.share.common.ErrorCode;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.util.List;

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    private final JwtConfig jwtConfig;

    public WebMvcConfig(JwtConfig jwtConfig) {
        this.jwtConfig = jwtConfig;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new AuthInterceptor(jwtConfig))
                .excludePathPatterns(List.of(
                        "/api/v1/user/send-code",
                        "/api/v1/user/login",
                        "/api/v1/share/public",
                        "/api/v1/voice/presets",
                        "/health",
                        "/error"
                ));
    }

    private static class AuthInterceptor implements HandlerInterceptor {
        private final JwtConfig jwtConfig;

        AuthInterceptor(JwtConfig jwtConfig) {
            this.jwtConfig = jwtConfig;
        }

        @Override
        public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
            if (handler instanceof HandlerMethod) {
                String auth = request.getHeader("Authorization");
                if (auth == null || !auth.startsWith("Bearer ")) {
                    throw AppException.unauthorized("请先登录");
                }
                String token = auth.substring(7);
                if (!jwtConfig.validateToken(token)) {
                    throw AppException.unauthorized("Token无效或已过期");
                }
                request.setAttribute("userId", jwtConfig.getUserIdFromToken(token));
            }
            return true;
        }
    }
}
