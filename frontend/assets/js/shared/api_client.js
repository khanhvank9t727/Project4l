async function apiRequest(

    endpoint,

    method = "GET",

    body = null,

    requiresAuth = false
) {

    const headers = {

        "Content-Type": "application/json"
    }

    if (requiresAuth) {

        const token = getAccessToken()

        if (token) {

            headers["Authorization"] =
                `Bearer ${token}`
        }
    }

    const options = {

        method,
        headers
    }

    if (body) {

        options.body = JSON.stringify(
            body
        )
    }

    try {

        const response = await fetch(

            `${CONFIG.BASE_URL}${endpoint}`,

            options
        )

        const data = await response.json()

        if (!response.ok) {

            throw new Error(
                data.message || "API Error"
            )
        }

        return data

    } catch (error) {

        console.error(
            "API Request Error:",
            error
        )

        throw error
    }
}