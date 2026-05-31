def paginate_query(

    query,

    page,

    per_page=10
):

    return query.paginate(

        page=page,

        per_page=per_page,

        error_out=False
    )