from flask import Flask, render_template, redirect, request, session, flash, jsonify 
from flask_app.models.user import User 
from flask_app import app, bcrypt
from flask_app.models.PCs import PlayerCharacter


#index page, will start and display login and registration forms 
@app.route("/")
def index():
    session.clear()
    if "unique_userid" in session:
        return redirect("/users/page")

    return render_template("login.html")



#taking the form data from the registration portion of the index page
@app.route("/register/validate", methods=["POST"])
def valid_register():
    if not User.validate_registration(request.form):
        return redirect("/")


    new_hash = bcrypt.generate_password_hash(request.form['password'])
    #store all the data from the new request.form 
    new_dict = {
        **request.form,
        "password": new_hash
    }
    
    #create the new user, and store the id into new_user variable
    new_user = User.create(new_dict) #will return new id of user from database

    session["unique_userid"] = new_user #pass the id into session 

    return redirect("/hub")


#This will validate and pass the form information for login
@app.route("/login/validate", methods=["POST"])
def valid_login():
    #validate all the input and redirect back to index with error messages displaying
    if not User.validate_login(request.form):
        flash("Cannot enter users page without logging in")
        return redirect("/")

    user = User.get_by_email({"email": request.form['email']}) #get the unique email, and store the id into session

    session["unique_userid"] = user.id

    return redirect("/hub")

@app.route("/hub")
def hub_menu():
#     #If the user is not in session, redirect back into login
    if "unique_userid" not in session:
        return redirect("/")   

    dict = {"id": session["unique_userid"]}
    # return jsonify(dict)
    return render_template("character_screen.html", logged_user = User.get_one(dict))


@app.route("/api/pcs/create", methods = ['POST'])
def create_player():

    dict = {
        **request.json,
        "user_id": 1
    }

    player = PlayerCharacter.create(dict)
    return jsonify(dict)


@app.route("/api/pcs/update/health")
def update_health():

    dict = {
        **request.json,
        "user_id": session["unique_userid"]
    }

    PlayerCharacter.update_health(dict)

    return jsonify()


#logout button, will clear session and restart back to login page
@app.route("/user/logout")
def logout():
    session.clear()
    return redirect("/")




# <button class="noButtonButton titleText"><img class="titleImage" src="{{url_for('static',filename = 'Assets/TitleText_2.png') }}" alt="titleText" width="400px"></button>