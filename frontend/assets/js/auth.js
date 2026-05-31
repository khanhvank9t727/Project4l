const loginForm = document.getElementById(
    "loginForm"
);

loginForm.addEventListener(

    "submit",

    async function(event) {

        event.preventDefault();

        const email =
            document.getElementById("email").value;

        const password =
            document.getElementById("password").value;

        try {

            const response = await fetch(

                `${API_BASE_URL}/auth/login`,

                {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email,
                        password
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {

                alert(data.message);

                return;
            }

            localStorage.setItem(
                "access_token",
                data.access_token
            );

            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            );

            if (data.user.role === "ADMIN") {

                window.location.href =
                    "../admin/dashboard.html";
            }

            else {

                window.location.href =
                    "home.html";
            }
        }

        catch(error) {

            console.error(error);

            alert("Server error");
        }
    }
);