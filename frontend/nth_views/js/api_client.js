const CONFIG_BASE_URL = "http://127.0.0.1:5000/api";

const apiClient = {
    request: async (endpoint, method = "GET", body = null) => {
        const token = localStorage.getItem('access_token');
        const headers = {
            "Content-Type": "application/json"
        };
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }
        const options = { method, headers };
        if (body) {
            options.body = JSON.stringify(body);
        }
        try {
            const response = await fetch(`${CONFIG_BASE_URL}${endpoint}`, options);
            const data = await response.json();
            if (!response.ok) {
                if (response.status === 401 || response.status === 403) {
                    if (window.location.pathname.includes('admin')) {
                        apiClient.logout();
                        return { success: false, message: data.message || "Phiên đăng nhập hết hạn" };
                    }
                }
                return { success: false, message: data.message || "API Error" };
            }
            return { success: true, data: data.data || data };
        } catch (error) {
            console.error("API Request Error:", error);
            return { success: false, message: error.message };
        }
    },
    get: (endpoint) => apiClient.request(endpoint, 'GET'),
    post: (endpoint, body) => apiClient.request(endpoint, 'POST', body),
    put: (endpoint, body) => apiClient.request(endpoint, 'PUT', body),
    delete: (endpoint) => apiClient.request(endpoint, 'DELETE'),
    logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '../user/login.html';
    }
};

// Global Role Check for Admin Pages — Verify via API
if (window.location.pathname.includes('/admin/')) {
    const token = localStorage.getItem('access_token');
    const userStr = localStorage.getItem('user');

    if (!token || !userStr) {
        window.location.href = '../user/login.html';
    } else {
        try {
            const user = JSON.parse(userStr);
            if (user.role !== "ADMIN") {
                alert("Bạn không có quyền truy cập trang quản trị!");
                window.location.href = '../user/home.html';
            }
        } catch (e) {
            window.location.href = '../user/login.html';
        }

        // Xác thực token qua server để đảm bảo token hợp lệ và user chưa bị khóa
        apiClient.get('/auth/profile').then(res => {
            if (res.success) {
                if (res.data.role !== "ADMIN") {
                    alert("Bạn không có quyền truy cập trang quản trị!");
                    apiClient.logout();
                }
            } else {
                // Token không hợp lệ hoặc bị khóa
                apiClient.logout();
            }
        }).catch(() => {
            apiClient.logout();
        });
    }
}
