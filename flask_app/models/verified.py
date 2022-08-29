from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash

class Verified:
    db = "cheat_code_schema"
    def __init__(self,data):
        self.id = data['id']
        self.cheat_code_id = data['cheat_code_id']
        self.user_id = data['user_id']
        self.verified = data['verified']

    @classmethod
    def update(cls,data):
        query = "UPDATE cheat_code_schema.verified SET cheat_code_id=%(cheat_code_id)s,user_id=%(user_id)s,verified=%(verified)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def save(cls,data):
        query = "INSERT INTO cheat_code_schema.verified (cheat_code_id,user_id,verified) VALUES(%(cheat_code_id)s,%(user_id)s,%(verified)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cheat_code_schema.verified;"
        results = connectToMySQL(cls.db).query_db(query)
        verifieds = []
        for row in results:
            verifieds.append( cls(row) )
        return verifieds

    @classmethod
    def get_by_cheat_code_id(cls,data):
        query = "SELECT * FROM cheat_code_schema.verified WHERE cheat_code_id = %(cheat_code_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        verifieds = []
        for row in results:
            verifieds.append( cls(row) )
        return verifieds

    @classmethod
    def get_by_cheat_code_id_user_id(cls,data):
        query = "SELECT * FROM cheat_code_schema.verified WHERE cheat_code_id = %(cheat_code_id)s AND user_id = %(user_id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls( results[0] )

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM cheat_code_schema.verified WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def delete_by_id(cls,data):
        query = "DELETE FROM cheat_code_schema.verified WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query,data)

    # @staticmethod
    # def validate_edit(verified): # This function is never used since it's not created from user data, but created in the controller
    #     is_valid = True
    #     if len(verified['cheat_code_id']) < 3:
    #         flash("Title must be at least 3 characters", "cheat_code")
    #         is_valid= False
    #     if len(verified['user_id']) < 3:
    #         flash("Network must be at least 3 characters", "cheat_code")
    #         is_valid= False
    #     if len(verified['verified']) < 3:
    #         flash("Description must be at least 3 characters", "cheat_code")
    #         is_valid= False
    #     return is_valid