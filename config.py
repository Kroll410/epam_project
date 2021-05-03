import pathlib

BASE_DIR = pathlib.Path(__file__).parent


class Config:
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql:///' + str(BASE_DIR / "data" / "db.mysql")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rabb1t:22egatob@localhost/epam_project'
