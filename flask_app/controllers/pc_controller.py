from flask import Flask, render_template, redirect, request, session, flash, jsonify

from flask_app import app, bcrypt
from flask_app.models.user import User
from flask_app.models.PCs import PlayerCharacter
from flask_app.controllers import user_controller



@app.route("/create/wizard/<int:user_id>/<int:health>")
def new_character(user_id, health):
    print("LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOK HERE")
    print(user_id)
    print(health)

    return redirect("/hub")


@app.route("/start_menu")
def start():

    return render_template("start_menu.html")   