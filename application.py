import os

from sentinal import create_app


application = create_app(__name__)


if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    application.run(host=host, port=port, debug=True)
