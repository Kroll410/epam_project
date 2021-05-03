from init import app, db
from views import views

if __name__ == '__main__':
    db.create_all()
    app.run()
