from flask import url_for, redirect, flash, request, jsonify
from routes.api.v1 import router
from models.movie import Movie


@router.route('/movie', methods=['GET'])
def get_movies():
    return jsonify(Movie.to_dict_all())


@router.route('/movie/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.get_by_id(movie_id)
    return jsonify(movie.to_dict())


@router.route('/movie', methods=['POST'])
def new_movie():
    form = request.form.to_dict()
    title = form.get('title', None)
    year = form.get('year', None)
    if not title or not year or len(year) != 4 or len(title) > 60:
        flash('Invalid input.', 'danger')
        return redirect(url_for('index_bp.index'))

    Movie.new(form)
    flash('Item created', 'success')
    return redirect(url_for('index_bp.index'))


@router.route('/movie/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    form = request.get_json()
    title = form.get('title', None)
    year = form.get('year', None)
    if not title or not year or len(year) != 4 or len(title) > 60:
        flash('Invalid input.')
        return redirect(url_for('index_bp.index'))

    Movie.update_by_id(movie_id, form)
    flash('Item updated', 'success')
    updated_movie = Movie.get_by_id(movie_id)
    return jsonify(updated_movie.to_dict())


@router.route('/movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    deleted_movie = Movie.get_by_id(movie_id)
    Movie.delete_by_id(movie_id)
    flash('Item deleted', 'warning')
    return jsonify(deleted_movie.to_dict())
