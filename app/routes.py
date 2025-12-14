from flask import Blueprint, request, redirect, url_for, jsonify
from sqlalchemy import exists
from app.db import db, Url

import validators
import secrets

bp = Blueprint('main', __name__)

@bp.route('/hello')
def hello():
    return 'Hello, World!'

@bp.route('/shorten', methods= ['POST'])
def shorten_url():
    url = request.args.get('url')

    if not url:
        return jsonify({"error": "Missing url query parameters"}), 400
    
    if not validators.url(url):
        return jsonify({"error": f"{url} is not a valid format"}), 400
    
    normalized_url = url.rstrip('/')
    if not url:
        return jsonify({"error": "Missing 'url' query parameter"}), 400

    if db.session.query(exists().where((Url.url == url) | (Url.url == normalized_url))).scalar():
        return jsonify ({"error": f"{url} already exists in the database"}), 400
    
    # Loop to make sure the short_code is unique 
    max_attempts = 5
    for _ in range(max_attempts):
        short_code = secrets.token_urlsafe(8)
        if  not db.session.execute(db.select(Url).where(Url.short_code == short_code)).scalar():
            break
    else:
        return jsonify({
            "error": "failed to generate unique short codes after assigned max attempts"
        }), 500
    
    newUrl = Url(
        url= normalized_url,
        short_code = short_code
    )

    try:          
        db.session.add(newUrl)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({
            "error" : "An unexpected server error ocurred."
        }), 500

    return jsonify({
        "url": newUrl.url,
        "short_code" : newUrl.short_code
        })

@bp.route('/<short_url>', methods= ['GET'])
def redirect_url(short_url):
    return jsonify({"url": short_url})