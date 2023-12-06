from flask import Blueprint, jsonify, request, abort
from main import db
from models.threads import Thread
from schemas.thread_schema import thread_schema, threads_schema

threads = Blueprint('threads', __name__, url_prefix='/threads')

@threads.route("/", methods=["GET"])
def get_users():
    stmt = db.select(Thread)
    threads_list = db.session.scalars(stmt)
    result = threads_schema.dump(threads_list)

    return jsonify(result)
