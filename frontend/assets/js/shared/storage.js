function saveAccessToken(token) {

    localStorage.setItem(
        "access_token",
        token
    )
}


function getAccessToken() {

    return localStorage.getItem(
        "access_token"
    )
}


function saveRefreshToken(token) {

    localStorage.setItem(
        "refresh_token",
        token
    )
}


function getRefreshToken() {

    return localStorage.getItem(
        "refresh_token"
    )
}


function clearTokens() {

    localStorage.removeItem(
        "access_token"
    )

    localStorage.removeItem(
        "refresh_token"
    )
}