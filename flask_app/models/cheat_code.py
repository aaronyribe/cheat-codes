from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash

class CheatCode:
    db = "cheat_code_schema"
    def __init__(self,data):
        self.id = data['id']
        self.description = data['description']
        self.game_id = data['game_id']
        self.submitted_by = data['submitted_by']

    @classmethod
    def update(cls,data):
        query = "UPDATE cheat_code_schema.cheat_codes SET description=%(description)s,game_id=%(game_id)s,submitted_by=%(submitted_by)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def save(cls,data):
        query = "INSERT INTO cheat_code_schema.cheat_codes (description,game_id,submitted_by) VALUES(%(description)s,%(game_id)s,%(submitted_by)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cheat_code_schema.cheat_codes;"
        results = connectToMySQL(cls.db).query_db(query)
        cheat_codes = []
        for row in results:
            cheat_codes.append( cls(row) )
        return cheat_codes

    @classmethod
    def get_by_game_id(cls,data):
        query = "SELECT * FROM cheat_code_schema.cheat_codes WHERE game_id = %(game_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        cheat_codes = []
        for row in results:
            cheat_codes.append( cls(row) )
        return cheat_codes

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM cheat_code_schema.cheat_codes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def delete_by_id(cls,data):
        query = "DELETE FROM cheat_code_schema.cheat_code WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_edit(cheat_code):
        is_valid = True
        if len(cheat_code['description']) < 10:
            flash("Description must be at least 10 characters", "cheat_code")
            is_valid= False
        return is_valid
