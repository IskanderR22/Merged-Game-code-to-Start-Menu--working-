from flask import flash, session
from flask_bcrypt import Bcrypt
import re

from flask_app import app, DB
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import PCs

bcrypt = Bcrypt(app)

from flask_app.models import PCs


#create a class to access the database
class User:
    #Setup the constructor, with all attributes that match the users table fields. 
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pcs = [] # This is the to many part of the one to many 

    @classmethod
    def create(cls, data): #create a row of data in the database 
        query = """
            INSERT INTO users (username, email, password)
            VALUES (%(username)s, %(email)s, %(password)s);
        """

        #set the result equal to the database function, pass the database name, query, and data to create new row
        result = connectToMySQL(DB).query_db(query, data)
        return result


    @classmethod
    def get_all(cls): #get all the data from entire table
        query = "SELECT * FROM users"
        results = connectToMySQL(DB).query_db(query)

        return results




    #every function except for get_all() requires a dictionary to be passed into its parameter for data
    @classmethod
    def get_one_join(cls, data):
        #We must pass a dictionary into the query_db(query, data)
        #THIS IS THE JOIN FOR A ONE TO MANY RELATIONSHIP

        query = "SELECT * FROM users LEFT JOIN pcs ON users.id = pcs.user_id WHERE users.id = %(id)s;" # MAKE SURE THE LEFT TABLE IS plural
        results = connectToMySQL(DB).query_db(query, data)

        user = cls(results[0]) #hold the specfic user

        if results[0]['pcs.id'] != None:
            for row in results:
                row_data = {
                    **row, # This is pulling all the information from the database
                    "id": row["pcs.id"],
                    "created_at": row["pcs.created_at"],
                    "updated_at": row["pcs.updated_at"],
                    "user_id": False
                }
                user.pcs.append(PCs.PlayerCharacter(row_data)) # append to the specific user list

        return user

        # result = connectToMySQL(DB).query_db(query, data) THIS IS FOR THE ORIGINAL GET ONE METHOD BEFORE THE LEFT JOIN

        # #if the selection does not exist, return false 
        # if len(result) < 1:
        #     return False
        # else:
        #     return cls(result[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        result = connectToMySQL(DB).query_db(query, data) #THIS IS FOR THE ORIGINAL GET ONE METHOD BEFORE THE LEFT JOIN

        #if the selection does not exist, return false 
        if len(result) < 1:
            return False
        else:
            return cls(result[0])



    @classmethod
    def get_by_email(cls, data): #exactly like get one, except grab the data by a specific attribute
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query, data)
        
        if len(result) < 1:
            return False
        else:
            return cls(result[0])   

    
    @classmethod
    def update(cls, data): #edit the the data within a row of the table within database
        query = "UPDATE users SET username = %(username)s, email = %(email)s WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)

        
    @classmethod
    def delete(cls, data): #delete from a specific row, set the id
        query = "DELETE FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
            
    @staticmethod
    def validate_registration(form_data): #validation is the process of sanitizing the input from the user taken from the form
        is_valid = True 
        #set flag to true, and if any user errors are found, set flag to false 

        #use regular expression for email, validate if the user inputted a correct email, and if email is within the database
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(form_data['email']): #if the email is not formatted correctly
            flash("Invalid email format", "email")
            is_valid = False 
        logged_user = None
        if "unique_userid" in session:
            print("SEND HELP TEAM")
            logged_user = User.get_one({"id": session['unique_userid']})
        if logged_user and logged_user.email != form_data['email'] or not logged_user:
            print("WE ARE INSIDE BOYES")
            if User.get_by_email({"email": form_data['email']}): #if the email already exists within the database
                flash("The Email Already Exists", "email")
                is_valid = False     


        #validate the first and last names are inputted correctly
        if "username" in form_data:
            if len(form_data['username']) < 3:
                flash("Please enter a proper username", "username")
                is_valid = False


        #validate the password, make sure its length is at least 8 characters and the confirmation password is the same
        if "password" in form_data:
            if len(form_data['password']) < 8:
                flash("Password must be at least 8 characters.", "password")
                is_valid = False
            elif form_data['password'] != form_data['confirm']:
                flash("Password and Confirm Password must match", "confirm_password")
                is_valid = False

        return is_valid    


    

    @staticmethod
    def validate_login(form_data): #validation from the login portion

        #create an instance of the user class, but compare the email from the form data
        user = User.get_by_email({"email":form_data['email']})

        #use if statements to check if the emails match and if the password is correct
        if not user:
            flash("User Email does not exist, please try another, or register for an account", "login_email")
            return False

        #use hash function to check the inputted password from login, to the database hashed password
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash("Password was incorrect, please re-enter the proper password", "login_password")
            return False
        
        return True
