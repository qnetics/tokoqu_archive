from threading import Thread
from src.routes import app
# from waitress import serve
# from werkzeug.middleware.profiler import ProfilerMiddleware

# run the application
if __name__ == "__main__":
    # app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[5], profile_dir='./profile')
    # serve(app)
    app.run()