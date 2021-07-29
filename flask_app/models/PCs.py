#import the mysqlconnection, establishes connection to the database
from flask_app.config.mysqlconnection import connectToMySQL
import re                               #re is used for regular expressions in python
from flask import flash                 #Flash to display error messages from validation
from flask_app import app, DB, bcrypt   #import app, the databse, bcrypt

#connect the other model into the file, but do not call it by its class, call the file name, then call the class using the file name
from flask_app.models import user


class PlayerCharacter:
    def __init__(self, data):
        self.id = data['id']
        if data['user_id']:                                        #prevent an infinite loop if the user_id is in the database
            self.user = user.User.get_one({"id": data['user_id']}) # this the relationship of the tables through the foreign key

        self.spec = data['class']
        self.health = data['health'] #at some point, set these number to be the data from database
        self.strength = data['strength'] 
        self.magic = data['magic'] 
        self.durability = data['durability']
        self.speed = data['speed']
        self.money = data['money']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.inventory = [] #need to have a list of the players inventory


    @classmethod
    def create(cls, data): #create a row of data in the database 
        query = """
            INSERT INTO pcs (user_id, class, health, strength, magic, durability, speed, money)
            VALUES (%(user_id)s, %(class)s, %(health)s, %(strength)s, %(magic)s, %(durability)s, %(speed)s, %(money)s);
        """

        #set the result equal to the database function, pass the database name, query, and data to create new row
        result = connectToMySQL(DB).query_db(query, data)
        return result

    @classmethod 
    def get_all(cls):
        query = "SELECT * FROM pcs"
        results = connectToMySQL(DB).query_db(query)
        print(results) #result is always a list of  dictionary

        #create list to store the all the rows from the database
        all_PCS = [] 

        for row in results:
            all_PCS.append(cls(row)) #append to a list of objects

        return all_PCS           

    @classmethod
    def get_one(cls, data):
        #We must pass a dictionary into the query_db(query, data)
        query = "SELECT * FROM pcs WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)

        #if the selection does not exist, return false 
        if len(result) < 1:
            return False
        else:
            return cls(result[0])

    @classmethod
    def update_health(cls, data): #edit the the data within a row of the table within database
        query = "UPDATE pcs SET health = %(health)s WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def update_strength(cls, data): #edit the the data within a row of the table within database
        query = "UPDATE pcs SET strength = %(strength)s WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)

    @classmethod
    def update_money(cls, data): #edit the the data within a row of the table within database
        query = "UPDATE pcs SET money = %(money)s WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)

        
class Pet:
    #Setup the constructor, with all attributes that match the users table fields. 
    def __init__(self, data):
        self.id = data['id']
        #establishing absraction and a one to many relationship
        if data['user_id']:                                        #prevent an infinite loop if the user_id is in the database
            self.user = user.User.get_one({"id": data['user_id']}) # this the relationship of the tables through the foreign key
        self.animal = data['animal']
        self.cool = data['cool']
        self.count = data['count']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data): #create a row of data in the database 
        query = """
            INSERT INTO pets (user_id, animal, cool)
            VALUES (%(user_id)s, %(animal)s, %(cool)s);
        """

        #set the result equal to the database function, pass the database name, query, and data to create new row
        result = connectToMySQL(DB).query_db(query, data)
        return result


    @classmethod
    def get_all(cls): #get all the data from entire table
        query = "SELECT * FROM pets"
        results = connectToMySQL(DB).query_db(query)
        print(results) #result is always a list of  dictionary

        #create list to store the all the rows from the database
        all_pets = [] 

        for row in results:
            all_pets.append(cls(row)) #append to a list of objects

        return all_pets   


    #every function except for get_all() requires a dictionary to be passed into its parameter for data
    @classmethod
    def get_one(cls, data):
        #We must pass a dictionary into the query_db(query, data)
        query = "SELECT * FROM pets WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)

        #if the selection does not exist, return false 
        if len(result) < 1:
            return False
        else:
            return cls(result[0])


    @classmethod
    def get_by_animal(cls, data): #exactly like get one, except grab the data by a specific attribute
        query = "SELECT * FROM pets WHERE animal = %(animal)s;"
        result = connectToMySQL(DB).query_db(query, data)
        
        if len(result) < 1:
            return False
        else:
            return cls(result[0])   


    @classmethod
    def update(cls, data): #edit the the data within a row of the table within database
        if "count" in data:
            query = "UPDATE pets SET count = %(count)s WHERE id = %(id)s;"

        else:
            query = "UPDATE pets SET animal = %(animal)s, cool = %(cool)s WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)

        
    @classmethod
    def delete(cls, data): #delete from a specific row, set the id
        query = "DELETE FROM pets WHERE id = %(id)s;"

        return connectToMySQL(DB).query_db(query, data)
        

    @staticmethod
    def validate_pet(form_data): #validation is the process of sanitizing the input from the user taken from the form
        is_valid = True 
        #set flag to true, and if any user errors are found, set flag to false 
        if len(form_data['animal']) < 2:
            flash("Animal name must be atleast 2 characters", "animal")
            is_valid = False

        if len(form_data['cool']) < 1:
            flash("Please select if the animal is cool!", "cool")
            is_valid = False


        return is_valid    
    