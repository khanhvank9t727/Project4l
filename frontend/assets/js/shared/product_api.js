async function fetchProducts() {

    return await apiRequest(
        "/products"
    )
}


async function fetchProductDetail(
    productId
) {

    return await apiRequest(
        `/products/${productId}`
    )
}