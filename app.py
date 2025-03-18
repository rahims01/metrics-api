from flask import Flask, render_template
from api.metrics_handler import metrics_bp
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

def create_app():
    app = Flask(__name__)
    app.register_blueprint(metrics_bp, url_prefix='/api')

    @app.route('/')
    def swagger_ui():
        return render_template('swagger-ui.html')

    return app

def create_prometheus_app(app):
    return DispatcherMiddleware(app, {'/metrics': make_wsgi_app()})

if __name__ == '__main__':
    app = create_app()
    prometheus_app = create_prometheus_app(app)
    run_simple('0.0.0.0', 8080, prometheus_app)