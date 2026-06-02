// Hàm tự động tạo và đưa Header & Navbar vào trang web
function renderHeaderNavbar() {
    // 1. Tạo chuỗi HTML cấu trúc Header & Navbar đồng bộ
    const headerHTML = `
    <header class="header-top">
        <div class="logo">
            <a href="home.html">
                <h1>🧸 G4 ToyStore</h1>
            </a>
        </div>

        <form class="search-bar" onsubmit="event.preventDefault();">
            <input type="text" placeholder="Tìm kiếm đồ chơi, thương hiệu...">
            <button type="submit"><i class="fa-solid fa-magnifying-glass"></i> Tìm</button>
        </form>

        <div class="header-actions">
            <a href="login.html" id="header-login-btn" class="btn-action btn-login">👤 Đăng Nhập</a>

            <div id="header-user-profile" class="user-profile-header">
                <img id="header-avatar-img" src="" alt="Avatar" class="user-avatar">
                <span id="header-username-text" class="user-name">G4 Member</span>
                <ul class="user-dropdown">
                    <li><a href="#"><i class="fa-regular fa-id-card"></i> Hồ sơ cá nhân</a></li>
                    <li><a href="#" onclick="handleLogout(event)" style="color: var(--primary-color);"><i class="fa-solid fa-arrow-right-from-bracket"></i> Đăng xuất</a></li>
                </ul>
            </div>

            <a href="cart.html" class="btn-action btn-cart"><i class="fa-solid fa-cart-shopping"></i> Giỏ Hàng</a>
        </div>
    </header>

    <nav class="main-nav">
        <ul class="nav-list">
            <li class="nav-item" id="menu-home"><a href="home.html">Trang Chủ</a></li>
            <li class="nav-item" id="menu-products">
                <a href="products.html">Sản Phẩm ▾</a>
                <ul class="dropdown">
                    <li><a href="products.html?cat=playground-2026">Playground 2026</a></li>
                    <li><a href="products.html?cat=qua-to-gia-nho">Quà To Giá Nhỏ</a></li>
                    <li><a href="products.html?cat=thung-gach-sang-tao">Thùng Gạch Sáng Tạo</a></li>
                    <li><a href="products.html?cat=muc-hot">Mục Hot (Bán Chạy)</a></li>
                </ul>
            </li>
            <li class="nav-item" id="menu-brands">
                <a href="#">Thương Hiệu ▾</a>
                <ul class="dropdown">
                    <li><a href="products.html?brand=lego">LEGO</a></li>
                    <li><a href="products.html?brand=hotwheels">Hot Wheels</a></li>
                    <li><a href="products.html?brand=mylittlepony">My Little Pony</a></li>
                    <li><a href="products.html?brand=bandai">Bandai</a></li>
                </ul>
            </li>
            <li class="nav-item" style="margin-left: auto;">
                <a href="../admin/dashboard.html" style="color: #ffdd59; font-weight: 700;">⚙️ Trang Quản Trị</a>
            </li>
        </ul>
    </nav>
    `;

    // 2. Chèn chuỗi HTML này vào đầu thẻ <body>
    document.body.insertAdjacentHTML('afterbegin', headerHTML);

    // 3. Tự động set class 'active' tương ứng theo trang hiện tại
    setActiveMenu();
}

// Hàm kiểm tra và kích hoạt màu sắc active cho menu điều hướng dựa trên URL
function setActiveMenu() {
    const currentUrl = window.location.pathname;
    if (currentUrl.includes('home.html') || currentUrl.endsWith('/')) {
        document.getElementById('menu-home')?.classList.add('active');
    } else if (currentUrl.includes('products.html')) {
        document.getElementById('menu-products')?.classList.add('active');
    }
}

// Hàm quản lý hiển thị trạng thái đăng nhập
function checkLoginNavbar() {
    let loggedName = localStorage.getItem("admin_name");
    let loggedAvatar = localStorage.getItem("admin_avatar");

    // Hỗ trợ đăng nhập thực tế (đọc đối tượng user từ localStorage)
    const userJSON = localStorage.getItem("user");
    if (userJSON) {
        try {
            const user = JSON.parse(userJSON);
            if (user && user.full_name) {
                loggedName = user.full_name;
                loggedAvatar = user.avatar || null;
            }
        } catch (e) {
            console.error("Lỗi parse thông tin user từ localStorage", e);
        }
    }

    const loginBtn = document.getElementById("header-login-btn");
    const userProfile = document.getElementById("header-user-profile");
    const usernameText = document.getElementById("header-username-text");
    const avatarImg = document.getElementById("header-avatar-img");

    if (!loginBtn || !userProfile) return;

    if (loggedName) {
        loginBtn.style.display = "none";
        userProfile.style.display = "flex";
        usernameText.innerText = loggedName;

        if (loggedAvatar) {
            avatarImg.src = loggedAvatar;
        } else {
            avatarImg.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(loggedName)}&background=ff6b6b&color=fff`;
        }
    } else {
        loginBtn.style.display = "inline-flex";
        userProfile.style.display = "none";
    }
}

// Xử lý Sự kiện Đăng Nhập giả lập để Demo nhanh
function handleMockLogin(e) {
    e.preventDefault();
    localStorage.setItem("admin_name", "G4 ToyStore Admin");
    localStorage.setItem("admin_avatar", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80");
    alert("Đăng nhập demo thành công!");
    checkLoginNavbar();
    window.location.reload();
}

// Xử lý Đăng Xuất tài khoản khỏi hệ thống
function handleLogout(e) {
    e.preventDefault();
    if (confirm("Bạn có muốn đăng xuất khỏi tài khoản hệ thống?")) {
        localStorage.removeItem("admin_name");
        localStorage.removeItem("admin_avatar");
        localStorage.removeItem("user");
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        alert("Đăng xuất thành công!");
        window.location.reload();
    }
}

// Kích hoạt nạp cấu trúc khi toàn bộ cây DOM của trang web sẵn sàng
window.addEventListener("DOMContentLoaded", () => {
    renderHeaderNavbar();
    checkLoginNavbar();
});