from bottle import route,run


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

def start_run(host = "localhost",port = 9999,usedb = None):
    global db

    if usedb is None:
        from .proxy_store import Proxy_Simple_Db
        db = Proxy_Simple_Db()
    elif type(usedb) == type:
        db = usedb()
    else:
        db = usedb

    run(host=host,port=port)

