from bottle import route,run
from .proxy_store import db

@route("/choice")
def choice():
    result = db.choice()
    return result
@route("/list_all")
def list_all():
    return "\n".join(db.getall())

@route("/choice_anyway")
def choice():
    result = db.getall_waitting()
    return result

@route("/list_watting")
def list_novalid():
    return "\n".join(db.getall_waitting())

def start_run(host = "localhost",port = 9999):
    run(host=host,port=port)

