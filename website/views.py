from flask import Blueprint, render_template, request, flash
from flask_login import  login_required, current_user
from .models import Note
from . import db #--> db is instansiated in __init__.py
import json
import jsonify

# different python files for different functions of the website. hmmm nice
# uses flask blueprint
# how :

views = Blueprint('views', __name__)

@views.route('/', methods=["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get('note')
        if len(note) < 1:
            flash("Note is too short!", category='error')
        else:
            new_note = Note(
                data=note,
                user_id = current_user.id
            )
            db.session.add(new_note)
            db.session.commit()
            flash("Note is added", category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note=Note.query.get(noteId)

    if note.user_id == current_user.id:
        flash("Note successfully deleted", category="success")
        db.session.delete(note)
        db.session.commit()

    return jsonify({})
