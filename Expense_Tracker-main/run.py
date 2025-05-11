from application import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database is created before running the app
    app.run(debug=True)