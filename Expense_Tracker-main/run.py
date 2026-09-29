import os

from application import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    debug = os.getenv('FLASK_DEBUG', '').lower() in {'1', 'true', 'yes'}
    app.run(debug=debug)
