from app import create_app
from app.config import Config


if __name__ == "__main__":
    app = create_app(Config)
    app.run(host="0.0.0.0", port=5000, debug=True)
