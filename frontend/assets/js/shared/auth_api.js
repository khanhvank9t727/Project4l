async function loginUser(

    email,

    password
) {

    const data = await apiRequest(

        "/auth/login",

        "POST",

        {
            email,
            password
        }
    )

    saveAccessToken(
        data.access_token
    )

    saveRefreshToken(
        data.refresh_token
    )

    return data
}