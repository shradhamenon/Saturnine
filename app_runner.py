import json
from flask import Flask, request, redirect, g, render_template, make_response, session, abort, jsonify, url_for, Response
import requests
from pyfy import Spotify, ClientCreds, UserCreds, AuthError, ApiError
import os
import webbrowser
from spt_keys import KEYS
from main import mood
import datetime
import database
import display
import io

spt = Spotify()
client = ClientCreds()
state = "123"

app = Flask(__name__)


@app.route("/authorize")
def authorize():
    export_keys()
    client.load_from_env()
    spt.client_creds = client
    if spt.is_oauth_ready:
        return redirect('https://accounts.spotify.com/authorize?redirect_uri=http://127.0.0.1:5000/callback/q&client_id=&response_type=code&scope=user-read-recently-played&show_dialog=false&state=123')
    else:
        return (
            jsonify(
                {
                    "error_description": "Client needs client_id, client_secret and a redirect uri in order to handle OAauth properly"
                }
            ),
            500,
        )


@app.route("/")
def index():
    return render_template('main.html')


@app.route("/callback/q") 
def spotify_callback():
    if request.args.get("error"):
        return jsonify(dict(error=request.args.get("error_description")))
    elif request.args.get("code"):
        grant = request.args.get("code")
        callback_state = request.args.get("state")
        if callback_state != state:
            return abort(401)
        try:
            user_creds = spt.build_user_creds(grant=grant)
        except AuthError as e:
            return jsonify(dict(error_description=e.msg)), e.code
        else:
            data = mood(spt, spt.recently_played_tracks(limit=50))
            user_creds=user_creds.__dict__ 
            user_id = user_creds["id"]
            user_name = user_creds["display_name"]
            today_date = str(datetime.date.today())
            year = str(datetime.date.today().year)

            mydate = datetime.datetime.now()
            month_name = mydate.strftime("%B")
            month_number = datetime.date.today().month

            day = datetime.date.today().day
            now = datetime.datetime.now()
            day_name = now.strftime("%A")
        
            database.driver(user_id, today_date, year, month_number, month_name, day, day_name, data)
            final_data = display.dis(user_id)
            return render_template('calendar.html', data=final_data, name=user_name) 
    else:
        return abort(500)


@app.route("/is_active")
def is_active():
    return jsonify(
        dict(
            is_active=spt.is_active,
            your_tracks=url_for("tracks", _external=True),
            your_playlists=url_for("playlists", _external=True),
        )
    )

def export_keys():
    for k, v in KEYS.items():
        if v:
            os.environ[k] = v
            print("export " + k + "=" + v)


if __name__ == "__main__":
    app.secret_key = ''
    app.debug = True
    app.run()
