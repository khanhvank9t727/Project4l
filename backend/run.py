#!/usr/bin/env python3

import os

from app import create_app


app = create_app()


if __name__ == '__main__':

    debug = os.getenv(
        'FLASK_DEBUG',
        True
    )

    port = int(
        os.getenv(
            'FLASK_PORT',
            5000
        )
    )

    print(
        f"Starting development server on http://localhost:{port}"
    )

    app.run(

        host='0.0.0.0',

        port=port,

        debug=debug
    )