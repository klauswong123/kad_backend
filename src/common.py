from datetime import datetime


def get_current():
    dt = datetime.now()
    return str(dt).split(".")[0]