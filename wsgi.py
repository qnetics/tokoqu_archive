from src.routes import app
from src.config import configurations

if __name__ == "__main__":

    configuration = configurations()
    app.run(host = configuration.host, port = configuration.port, threaded = True)