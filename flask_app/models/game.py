from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash

class Game:
    db = "cheat_code_schema"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.release_year = data['release_year']


    @classmethod
    def update(cls,data):
        query = "UPDATE cheat_code_schema.games SET title=%(title)s,release_year=%(release_year)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def save(cls,data):
        query = "INSERT INTO cheat_code_schema.games (title,release_year) VALUES(%(title)s,%(release_year)s)"
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
    def get_by_title(cls,data):
        query = "SELECT * FROM cheat_code_schema.games WHERE title = %(title)s;"
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
        if len(game['release_year']) < 3: # TODO This might be an int
            flash("release_year must be at least 3 characters", "game")
            is_valid= False
        return is_valid