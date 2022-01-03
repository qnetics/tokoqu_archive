import os
from src.routes import app
from werkzeug.middleware.profiler import ProfilerMiddleware

# run the application
if __name__ == "__main__":
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[5], profile_dir='./profile')
    app.run(threaded=True, host="0.0.0.0", port=int(os.environ.get('PORT',5000)))