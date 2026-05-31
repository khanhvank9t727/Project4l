document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault(); // 🚨 chặn reload trang

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch("http://localhost:5000/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        });

        const data = await res.json();

        if (res.ok) {
            alert("Login success!");
            window.location.href = "../home.html"; // đổi theo project bạn
        } else {
            document.getElementById("errorMsg").innerText = data.message || "Login failed";
        }

    } catch (err) {
        console.error(err);
        document.getElementById("errorMsg").innerText = "Cannot connect to server";
    }
});