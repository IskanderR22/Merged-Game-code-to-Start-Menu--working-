#import the mysqlconnection, establishes connection to the database
from flask_app.config.mysqlconnection import connectToMySQL
import re                               #re is used for regular expressions in python
from flask import flash                 #Flash to display error messages from validation
from flask_app import app, DB, bcrypt   #import app, the databse, bcrypt

#connect the other model into the file, but do not call it by its class, call the file name, then call the class using the file name
from flask_app.models import user
from flask_app.models import PCs

class Consumable:
    #Setup the constructor, with all attributes that match the users table fields. 
    all_items = {}
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
        Consumable.all_items[self.name] = self.func
        self.pcs = [] #list of playable characters that the items belong to
    
    @classmethod
    def get_user_items(cls, data):
        #returns a single inventory object 
        query = """
            SELECT * FROM consumables
            LEFT JOIN inventory_items ON consumables.id = inventory_items.consumable_id
            LEFT JOIN pcs ON pcs.id = inventory_items.pc_id
            WHERE consumables.id = %(id)s;
        """

        result = connectToMySQL(DB).query_db(query, data)
        item = cls(result[0])

        if result[0]['pcs.id'] != None:
            for row in result:
                row_data = {
                    "id": row['pcs.id'],
                    "spec": row["pcs.spec"],
                    "health": row["pcs.health"],
                    "strength": row["pcs.strength"],
                    "magic": row["pcs.magic"],
                    "durability": row["pcs.durability"],
                    "speed": row["pcs.speed"],
                    "money": row["pcs.money"],
                    "inventory": row["pcs.inventory"],
                    "created_at": row["pcs.created_at"],
                    "updated_at": row["pcs.updated_at"]
                }
                item.pcs.append(PCs.PC(row_data))
        
        return item
    

    @classmethod
    def add_to_pc(cls, data):
        query = """
            INSERT INTO inventory_items (consumable_id, pc_id)
            VALUES (%(consumable_id)s, %(pc_id)s)
        """
        return connectToMySQL(DB).query_db(query, data)

@Consumable
def potion(Pc):
    #on use, add +10 to health
    Pc.health += 10
    #print("The wounds of war can be healed, but never hidden")
    
    #if using the health potion exceeds max health, it sets it to max health instead of going over
    if Pc.health >= Pc.max_health:      
        Pc.health = Pc.max_health          
        #print("The wounds of war can be healed, but never hidden")
        return Pc.health      

    return Pc.health

@Consumable
def mega_potion(Pc):
    #on use, add +25 to health
    Pc.health += 25
    #print("Death cannot be escaped! But it can be postponed")
    
    if Pc.health >= Pc.max_health:
        Pc.health = Pc.max_health
        #print("Death cannot be escaped! But it can be postponed")
        return Pc.health

    return Pc.health

@Consumable
def dmg_item(Pc, target):
    #on use, damage enemy -15 health
    target.health -= 15
    #print("A powerful blow!")
    return target.health