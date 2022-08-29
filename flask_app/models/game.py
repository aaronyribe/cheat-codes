from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash

class Game:
    db = "cheat_code_schema"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.release_year = data['release_year']
        self.posted_by = data['posted_by']

    @classmethod
    def update(cls,data):
        query = "UPDATE cheat_code_schema.games SET title=%(title)s,release_year=%(release_year)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def save(cls,data):
        query = "INSERT INTO cheat_code_schema.games (title,release_year,posted_by) VALUES(%(title)s,%(release_year)s,%(posted_by)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cheat_code_schema.games;"
        results = connectToMySQL(cls.db).query_db(query)
        games = []
        for row in results:
            games.append( cls(row))
        return games

    @classmethod
    def play(cls,data):
        query = "INSERT INTO cheat_code_schema.games_played (user_id,game_id) VALUES(%(user_id)s,%(game_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def unplay(cls,data):
        query = "DELETE FROM cheat_code_schema.games_played WHERE user_id=%(user_id)s AND game_id=%(game_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_by_user_id(cls,data):
        query = "SELECT * FROM cheat_code_schema.games AS games JOIN cheat_code_schema.games_played ON games.id=game_id WHERE user_id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        games = []
        if not results:
            return False
        for row in results:
            games.append( cls(row))
        return games

    @classmethod
    def get_by_title(cls,data):
        query = "SELECT * FROM cheat_code_schema.games WHERE title = %(title)s;" # TODO Make this a fuzzy text search
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM cheat_code_schema.games WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def delete_by_id(cls,data):
        query = "DELETE FROM cheat_code_schema.games WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_edit(game):
        is_valid = True
        if len(game['title']) < 3:
            flash("Title must be at least 3 characters", "game")
            is_valid= False
        if len(game['release_year']) < 3:
            flash("release_year must be at least 3 characters", "cheat_code")
            is_valid= False
        return is_valid