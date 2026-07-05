package com.timbre.share.common;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;
import java.util.Map;

@Data
@AllArgsConstructor
public class ApiResponse<T> {
    private int code;
    private String message;
    private T data;

    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(ErrorCode.SUCCESS, "success", data);
    }

    public static <T> ApiResponse<T> success() {
        return success(null);
    }

    public static <T> ApiResponse<T> error(int code, String message) {
        return new ApiResponse<>(code, message, null);
    }

    public static <T> ApiResponse<Map<String, Object>> paginated(List<T> items, long total, int page, int pageSize) {
        int totalPages = (int) ((total + pageSize - 1) / pageSize);
        Map<String, Object> data = Map.of(
                "items", items,
                "pagination", Map.of(
                        "page", page,
                        "pageSize", pageSize,
                        "total", total,
                        "totalPages", totalPages
                )
        );
        return new ApiResponse<>(ErrorCode.SUCCESS, "success", data);
    }
}
