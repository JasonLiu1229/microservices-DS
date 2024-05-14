import requests
from flask import Flask, redirect, render_template, request, url_for
from werkzeug import Response

app = Flask(__name__)


# The Username & Password of the currently logged-in User, this is used as a pseudo-cookie, as such this is not session-specific.
username = None
password = None

session_data = dict()


def save_to_session(key, value) -> None:
    session_data[key] = value


def load_from_session(key):  # -> Any | None:
    return (
        session_data.pop(key) if key in session_data else None
    )  # Pop to ensure that it is only used once


def succesful_request(r):  # -> Any:
    return r.status_code == 200


@app.route("/")
def home() -> str:
    global username

    if username is None:
        return render_template("login.html", username=username, password=password)
    else:
        # ================================
        # FEATURE (list of public events)
        #
        # Retrieve the list of all public events. The webpage expects a list of (title, date, organizer) tuples.
        # Try to keep in mind failure of the underlying microservice
        # =================================

        public_events = []

        events = requests.get("http://backend-events:8000/events", timeout=100).json()

        for event in events:
            if event["is_public"]:
                public_events.append(
                    (event["title"], event["date"], event["organizer_id"])
                )

        users = requests.get("http://backend-auth:8000/users", timeout=100).json()
        formatted_events = []
        for event in public_events:
            for user in users:
                if user["user_id"] == event[2]:
                    formatted_events.append((event[0], event[1], user["username"]))
                    break

        public_events = formatted_events

        return render_template(
            "home.html", username=username, password=password, events=public_events
        )


@app.route("/event", methods=["POST"])
def create_event() -> Response:
    title, description, date, publicprivate, invites = (
        request.form["title"],
        request.form["description"],
        request.form["date"],
        request.form["publicprivate"],
        request.form["invites"],
    )
    # ==========================
    # FEATURE (create an event)
    #
    # Given some data, create an event and send out the invites.
    # ==========================
    users = requests.get("http://backend-auth:8000/users", timeout=100).json()

    current_user_id = None
    for user in users:
        if user["username"] == username:
            current_user_id = user["user_id"]
            break

    if current_user_id == None:
        return redirect("/")

    response = requests.post(
        "http://backend-events:8000/events",
        json={
            "organizer_id": current_user_id,
            "title": title,
            "description": description,
            "date": date,
            "is_public": publicprivate == "public",
        },
        timeout=100,
    )

    users_invites = invites.split(sep=";")

    users_id_invites = []

    event = response.json()

    for user in users:
        if user["username"] in users_invites:
            users_id_invites.append(user["user_id"])

    for user_id in users_id_invites:
        requests.post(
            "http://backend-invitations:8000/invitations",
            json={
                "user_id": current_user_id,
                "event_id": event["event_id"],
                "invitee_id": user_id,
            },
            timeout=100,
        )

    return redirect("/")


@app.route("/calendar", methods=["GET", "POST"])
def calendar() -> str:
    calendar_user = (
        request.form["calendar_user"] if "calendar_user" in request.form else username
    )

    # ================================
    # FEATURE (calendar based on username)
    #
    # Retrieve the calendar of a certain user. The webpage expects a list of (id, title, date, organizer, status, Public/Private) tuples.
    # Try to keep in mind failure of the underlying microservice
    # =================================

    success = (
        True  # TODO: this might change depending on if the calendar is shared with you
    )

    if success:
        calendar = [
            (1, "Test event", "Tomorrow", "Benjamin", "Going", "Public")
        ]  # TODO: call
    else:
        calendar = None

    return render_template(
        "calendar.html",
        username=username,
        password=password,
        calendar_user=calendar_user,
        calendar=calendar,
        success=success,
    )


@app.route("/share", methods=["GET"])
def share_page() -> str:
    return render_template(
        "share.html", username=username, password=password, success=None
    )


@app.route("/share", methods=["POST"])
def share() -> str:
    share_user = request.form["username"]

    # ========================================
    # FEATURE (share a calendar with a user)
    #
    # Share your calendar with a certain user. Return success = true / false depending on whether the sharing is succesful.
    # ========================================

    success = True  # TODO
    return render_template(
        "share.html", username=username, password=password, success=success
    )


@app.route("/event/<eventid>")
def view_event(eventid) -> str:

    # ================================
    # FEATURE (event details)
    #
    # Retrieve additional information for a certain event parameterized by an id. The webpage expects a (title, date, organizer, status, (invitee, participating)) tuples.
    # Try to keep in mind failure of the underlying microservice
    # =================================
    
    user_id = None 
    users = requests.get("http://backend-auth:8000/users", timeout=100).json()
    for user in users:
        if user["username"] == username:
            user_id = user["user_id"]
            break
    
    event = requests.get(f"http://backend-events:8000/events/{eventid}", timeout=100).json()
    
    if event["is_public"]:
        success = True
    else:
        invites = requests.get(f"http://backend-invitations:8000/invitations/{user_id}", timeout=100).json()
        success = False
        for invite in invites:
            if invite["event_id"] == eventid:
                success = True
                break

    if success:
        event = [
            "Test event",
            "Tomorrow",
            "Benjamin",
            "Public",
            [["Benjamin", "Participating"], ["Fabian", "Maybe Participating"]],
        ]  # TODO: populate this with details from the actual event
    else:
        event = None  # No success, so don't fetch the data

    return render_template(
        "event.html", username=username, password=password, event=event, success=success
    )


@app.route("/login", methods=["POST"])
def login() -> Response:
    req_username, req_password = request.form["username"], request.form["password"]

    # ================================
    # FEATURE (login)
    #
    # send the username and password to the microservice
    # microservice returns True if correct combination, False if otherwise.
    # Also pay attention to the status code returned by the microservice.
    # ================================
    if (
        requests.post(
            "http://backend-auth:8000/auth/login",
            json={"username": req_username, "password": req_password},
            timeout=100,
        ).status_code
        == 200
    ):
        success = True
    else:
        success = False

    save_to_session("success", success)
    if success:
        global username, password

        username = req_username
        password = req_password

    return redirect("/")


@app.route("/register", methods=["POST"])
def register() -> Response:

    req_username, req_password = request.form["username"], request.form["password"]

    # ================================
    # FEATURE (register)
    #
    # send the username and password to the microservice
    # microservice returns True if registration is succesful, False if otherwise.
    #
    # Registration is successful if a user with the same username doesn't exist yet.
    # ================================

    if (
        requests.post(
            "http://backend-auth:8000/auth/register",
            json={"username": req_username, "password": req_password},
            timeout=100,
        ).status_code
        == 200
    ):
        success = True
    else:
        success = False

    save_to_session("success", success)

    if success:
        global username, password

        username = req_username
        password = req_password

    return redirect("/")


@app.route("/invites", methods=["GET"])
def invites() -> str:
    # ==============================
    # FEATURE (list invites)
    #
    # retrieve a list with all events you are invited to and have not yet responded to
    # ==============================

    my_invites = []

    users = requests.get("http://backend-auth:8000/users", timeout=100).json()

    user_id = None
    for user in users:
        if user["username"] == username:
            user_id = user["user_id"]
            break

    user_invites = requests.get(
        f"http://backend-invitations:8000/invitations/{user_id}", timeout=100
    ).json()

    for invite in user_invites:
        if invite["status"] == "pending":
            event = requests.get(
                f"http://backend-events:8000/events/{invite['event_id']}", timeout=100
            ).json()
            organizer = requests.get(
                f"http://backend-auth:8000/users/{event['organizer_id']}", timeout=100
            ).json()
            my_invites.append(
                (
                    event["event_id"],
                    event["title"],
                    event["date"],
                    organizer["username"],
                    "Public" if event["is_public"] else "Private",
                )
            )

    return render_template(
        "invites.html", username=username, password=password, invites=my_invites
    )


@app.route("/invites", methods=["POST"])
def process_invite() -> Response:
    eventId, status = request.json["event"], request.json["status"]

    # =======================
    # FEATURE (process invite)
    #
    # process an invite (accept, maybe, don't accept)
    # =======================

    pass  # TODO: send to microservice

    return redirect("/invites")


@app.route("/logout")
def logout() -> Response:
    global username, password

    username = None
    password = None
    return redirect("/")
