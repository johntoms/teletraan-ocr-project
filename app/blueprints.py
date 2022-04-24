from __future__ import unicode_literals
from app import app


def register_blueprints():
    from app.routes.ocr_discriminate import bp_ocr
    app.register_blueprint(bp_ocr, url_prefix='/ocr')
    return app
