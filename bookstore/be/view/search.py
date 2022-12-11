from flask import Blueprint
from flask import request
from flask import jsonify
from be.model import search

bp_search = Blueprint("search", __name__, url_prefix="/search")


@bp_search.route("/multiple", methods=["POST"])
def search_multiple():
    store_id = request.json.get("store_id", "")
    title_key=request.json.get("title", "")
    author_key = request.json.get("author", "")
    book_intro_key = request.json.get("book_intro", "")
    tags_key= request.json.get("tags", "")
    args = {
        "store_id": store_id,
        "title_key": title_key,
        "author_key": author_key,
        "book_intro_key": book_intro_key,
        "tags_key": tags_key,
    }

    u = search.mySearch()
    code, message, result = u.search_multiple(args)
    return jsonify({"message": message, "book_result": result}), code

@bp_search.route("/title", methods=["POST"])
def search_title():
    title = request.json.get("title", "")
    page = request.json.get("page", "")
    if title == "":
        return jsonify({"message": "ok", "book_result": []}), 200
    page = 0 if page == "" else int(page)
    
    u = search.mySearch()
    code, message, result = u.search_by_title(title, page)
    return jsonify({"message": message, "book_result": result}), code

@bp_search.route("/tag", methods=["POST"])
def search_tag():
    tag = request.json.get("tag", "")
    page = request.json.get("page", "")
    if tag == "":
        return jsonify({"message": "ok", "book_result": []}), 200
    page = 0 if page == "" else int(page)
    
    u = search.mySearch()
    code, message, result = u.search_by_tag(tag, page)
    return jsonify({"message": message, "book_result": result}), code

@bp_search.route("/author", methods=["POST"])
def search_author():
    author = request.json.get("author", "")
    page = request.json.get("page", "")
    if author == "":
        return jsonify({"message": "ok", "book_result": []}), 200
    page = 0 if page == "" else int(page)
    
    u = search.mySearch()
    code, message, result = u.search_by_author(author, page)
    return jsonify({"message": message, "book_result": result}), code

@bp_search.route("/book_intro", methods=["POST"])
def search_book_intro():
    book_intro = request.json.get("book_intro", "")
    page = request.json.get("page", "")
    if book_intro == "":
        return jsonify({"message": "ok", "book_result": []}), 200
    page = 0 if page == "" else int(page)
    
    u = search.mySearch()
    code, message, result = u.search_by_book_intro(book_intro, page)
    return jsonify({"message": message, "book_result": result}), code

@bp_search.route("/title_store", methods=["POST"])
def search_title_store():
    title = request.json.get("title", "")
    store_id = request.json.get("store_id", "")
    page = request.json.get("page", "")
    if title == "" or store_id == "":
        return jsonify({"message": "ok", "book_result": []}), 200
    page = 0 if page == "" else int(page)
    
    u = search.mySearch()
    code, message, result = u.search_by_title_store(title, store_id, page)
    return jsonify({"message": message, "book_result": result}), code

@bp_search.route("/tag_store", methods=["POST"])
def search_tag_store():
    tag = request.json.get("tag", "")
    store_id = request.json.get("store_id", "")
    page = request.json.get("page", "")
    if tag == "" or store_id == "":
        return jsonify({"message": "ok", "book_result": []}), 200
    page = 0 if page == "" else int(page)
    
    u = search.mySearch()
    code, message, result = u.search_by_tag_store(tag, store_id, page)
    return jsonify({"message": message, "book_result": result}), code

@bp_search.route("/author_store", methods=["POST"])
def search_author_store():
    author = request.json.get("author", "")
    store_id = request.json.get("store_id", "")
    page = request.json.get("page", "")
    if author == "" or store_id == "":
        return jsonify({"message": "ok", "book_result": []}), 200
    page = 0 if page == "" else int(page)
    
    u = search.mySearch()
    code, message, result = u.search_by_author_store(author, store_id, page)
    return jsonify({"message": message, "book_result": result}), code

@bp_search.route("/book_intro_store", methods=["POST"])
def search_book_intro_store():
    book_intro = request.json.get("book_intro", "")
    store_id = request.json.get("store_id", "")
    page = request.json.get("page", "")
    if book_intro == "" or store_id == "":
        return jsonify({"message": "ok", "book_result": []}), 200
    page = 0 if page == "" else int(page)
    
    u = search.mySearch()
    code, message, result = u.search_by_book_intro_store(book_intro, store_id, page)
    return jsonify({"message": message, "book_result": result}), code

    