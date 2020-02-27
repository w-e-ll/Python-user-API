from bottle import (
    Bottle, run, debug
)
from config import SERVER_SETTINGS
from logger_setup import logger
from scripts import load_swagger_yaml, uuid_filter

from handlers import (
    by_uuid, index, drop_collection,
    get_total_users, by_email,
    post_user, post_users, update_user,
    delete_user, serve_static,
)

logger.info({"Message": "Initializing Bottle..."})
# --- Configuration ----------------------------------------------------
app = application = Bottle()
app.catchall = False
wb = SERVER_SETTINGS['WEB_BASE']
app.router.add_filter("uuid", uuid_filter)
swagger_from_yaml = load_swagger_yaml()
app.config["api.swagger_spec"] = swagger_from_yaml


def setup_routing(app):
    app.route(wb+"/get_user_by_uuid/<user_uuid>", ['GET'], by_uuid)
    app.route(wb+"/get_user_by_email/<user_email>", ['GET'], by_email)
    app.route(wb+"/get_total_users", ['GET'], get_total_users)
    app.route(wb+"/home", ['GET'], index)
    app.route(wb+"/post_user", ['POST'], post_user)
    app.route(wb+"/post_users", ['POST'], post_users)
    app.route(wb+"/update_user/<user_uuid>", ['UPDATE'], update_user)
    app.route(wb+"/delete_user/<user_uuid>", ['DELETE'], delete_user)
    app.route(wb+"/drop_collection/<col_name>", ['DROP'], drop_collection)
    app.route(wb+"/docs", ['GET'], app.config["api.swagger_spec"])
    app.route("/static/<filename>", serve_static)
    app.route("/static/<filename:re:.*\\.css>", serve_static)
    app.route("/static/<filename:re:.*\\.js>", serve_static)


setup_routing(app)

# --- Run API-----------------------------------------------
if __name__ == '__main__':
    debug(True)
    run(app=app, host=SERVER_SETTINGS["SERVER_IP"],
        port=SERVER_SETTINGS["SERVER_PORT"],
        reloader=True)
