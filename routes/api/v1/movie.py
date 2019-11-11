from flask import url_for, redirect, flash, request, jsonify
from routes.api.v1 import router
from models.movie import Movie


@router.route('/movie', methods=['GET'])
def get_movies():
    return jsonify(Movie.to_dict_all())


@router.route('/movie', methods=['POST'])
def new_movie():
    pass
