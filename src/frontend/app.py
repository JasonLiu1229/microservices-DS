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


def get_userId(username: str) -> int | None:
    users_response = requests.get("http://backend-auth:8000/users", timeout=100)
    
    if users_response.status_code != 200:
        return None
    
    users = users_response.json()
    
    for user in users:
        if user["username"] == username:
            return user["user_id"]
    return None


@app.route("/",  methods=["GET"])
def home() -> str:
    """Home page of the application."""

    global username

    if username is None:
        return render_template("login.html", username=username, password=password)
    else:
        # ================================
        # FEATURE (list of public events)
        #
        # Retrieve the list of all public events. The webpage expects a list of (event_id, title, date, organizer) tuples.
        # Try to keep in mind failure of the underlying microservice
        # =================================

        public_events = []

        events_response = requests.get("http://backend-events:8000/events", timeout=100)
        
        if events_response.status_code != 200:
            return redirect("/")
        
        events = events_response.json()

        for event in events:
            if event["is_public"]:
                public_events.append(
                    (
                        event["event_id"],
                        event["title"],
                        event["date"],
                        event["organizer_id"],
                    )
                )

        users_response = requests.get("http://backend-auth:8000/users", timeout=100)
        
        if users_response.status_code != 200:
            return redirect("/")
        
        users = users_response.json()
        
        formatted_events = []
        for event in public_events:
            for user in users:
                if user["user_id"] == event[3]:
                    formatted_events.append(
                        (event[0], event[1], event[2], user["username"])
                    )
                    break

        public_events = formatted_events

        return render_template(
            "home.html", username=username, password=password, events=public_events
        )


@app.route("/", methods=["POST"])
def process_public_event() -> Response:
    event_id, status = request.json["event"], request.json["status"]

    # ================================
    # FEATURE (participate in a public event)
    #
    # Participate in a public event. Return success = true / false depending on whether the participation is succesful.
    # ================================
    int_event_id = int(event_id)

    user_id = get_userId(username)

    new_status = (
        "accepted"
        if status == "Participate"
        else "declined" if status == "Don't Participate" else "maybe"
    )

    if user_id is None:
        return redirect("/")
    
    # check if we also have an invite for this event
    invites_output_response = requests.get(
        f"http://backend-invitations:8000/invitations?event_id={int_event_id}&invitee_id={user_id}",
        timeout=100,
    )
    
    if invites_output_response.status_code != 200:
        invites_output = []
    else:
        invites_output = invites_output_response.json()

    if len(invites_output) > 0:
        invite = invites_output[0]
        if invite["status"] == "pending":
            requests.put(
                f"http://backend-invitations:8000/invitations/{invite['invite_id']}/status/{new_status}",
                timeout=100,
            )
            requests.post(
                "http://backend-participations:8000/participations",
                json={
                    "user_id": user_id,
                    "event_id": int_event_id,
                    "status": new_status,
                },
                timeout=100,
            )
    else:
        # check if we have already participated in this event
        participations_output_response = requests.get(
            f"http://backend-participations:8000/participations?event_id={int_event_id}&user_id={user_id}",
            timeout=100,
        )
        
        if participations_output_response.status_code != 200:
            participations_output = []
        else:
            participations_output = participations_output_response.json()

        if len(participations_output) == 0:
            requests.post(
                "http://backend-participations:8000/participations",
                json={
                    "user_id": user_id,
                    "event_id": int_event_id,
                    "status": new_status,
                },
                timeout=100,
            )
        elif len(participations_output) == 1:
            if participations_output[0]["status"] != new_status:
                requests.put(
                    f"http://backend-participations:8000/participations/{participations_output[0]['participation_id']}/status/{new_status}",
                    timeout=100,
                )

    return redirect("/", code=307)


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
    users_response = requests.get("http://backend-auth:8000/users", timeout=100)
    
    if users_response.status_code != 200:
        return redirect("/")
    
    users = users_response.json()

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
    """
    Retrieve the calendar of a certain user.

    The webpage expects a list of (id, title, date, organizer, status, Public/Private) tuples.
    """
    calendar_user = (
        request.form["calendar_user"] if "calendar_user" in request.form else username
    )

    success = True if calendar_user == username else False

    calendar_user_id = get_userId(calendar_user)
    user_id = get_userId(username)

    all_calendars_response = requests.get(
        "http://backend-calendar:8000/calendars", timeout=100
    )
    
    if all_calendars_response.status_code != 200:
        return redirect("/")
    
    all_calendars = all_calendars_response.json()

    for calendar_shared in all_calendars:
        if (
            calendar_shared["user_id"] == calendar_user_id
            and calendar_shared["shared_with_id"] == user_id
        ):
            success = True
            break

    if success:
        all_participations_response = requests.get(
            "http://backend-participations:8000/participations", timeout=100
        )
        
        if all_participations_response.status_code != 200:
            return redirect("/")

        all_participations = all_participations_response.json()
        
        calendar = []

        for participation in all_participations:
            if (
                participation["user_id"] == calendar_user_id
                and participation["status"] != "declined"
            ):
                event_response = requests.get(
                    f"http://backend-events:8000/events/{participation['event_id']}",
                    timeout=100,
                )
                
                if event_response.status_code != 200:
                    continue
                
                event = event_response.json()
                
                organizer_response = requests.get(
                    f"http://backend-auth:8000/users/{event['organizer_id']}",
                    timeout=100,
                )
                
                if organizer_response.status_code != 200:
                    continue
                
                organizer = organizer_response.json()
                
                status = "Going" if participation["status"] == "accepted" else "Maybe"
                is_public = "Public" if event["is_public"] else "Private"
                string_date = event["date"].split("T")[0]
                calendar.append(
                    (
                        event["event_id"],
                        event["title"],
                        string_date,
                        organizer["username"],
                        status,
                        is_public,
                    )
                )
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
    """Share page of the application."""
    return render_template(
        "share.html", username=username, password=password, success=None
    )


@app.route("/share", methods=["POST"])
def share() -> str:
    """Share a calendar with a user."""
    share_user = request.form["username"]

    # ========================================
    # FEATURE (share a calendar with a user)
    #
    # Share your calendar with a certain user. Return success = true / false depending on whether the sharing is succesful.
    # ========================================

    success = False
    user_id = get_userId(username)
    shared_with_id = get_userId(share_user)
    
    if user_id is None or shared_with_id is None:
        return redirect("/share")

    response = requests.post(
        "http://backend-calendar:8000/calendars",
        json={"user_id": user_id, "shared_with_id": shared_with_id},
        timeout=100,
    )

    if response.status_code == 200:
        success = True

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

    user_id = get_userId(username)

    event = requests.get(
        f"http://backend-events:8000/events/{eventid}", timeout=100
    ).json()

    int_event_id = int(eventid)

    if event["is_public"]:
        success = True
    else:
        invites_output = requests.get(
            f"http://backend-invitations:8000/invitations?event_id={int_event_id}&invitee_id={user_id}",
            timeout=100,
        ).json()

        if len(invites_output) > 0:
            success = True

    if success:
        all_participants_response = requests.get(
            "http://backend-participations:8000/participations", timeout=100
        )
        
        if all_participants_response.status_code != 200:
            return redirect("/")
        
        all_participants = all_participants_response.json()

        event_participants = []

        for participants in all_participants:
            if participants["event_id"] == int_event_id:
                event_participants.append(participants)
        
        new_event_participants = []
        
        for participant in event_participants:
            user_response = requests.get(
                f"http://backend-auth:8000/users/{participant['user_id']}", timeout=100
            )
            
            if user_response.status_code != 200:
                continue
            
            user = user_response.json()
            
            new_event_participants.append(
                (
                    user["username"],
                    "Participating" if participant["status"] == "accepted" else "Maybe Participating",
                )
            )
        
        event_participants = new_event_participants

        organizer_response = requests.get(
            f"http://backend-auth:8000/users/{event["organizer_id"]}", timeout=100
        )
        
        if organizer_response.status_code != 200:
            return redirect("/")
        
        organizer = organizer_response.json()

        string_date = event["date"].split("T")[0]
        event = [
            event["title"],
            string_date,
            organizer["username"],
            "Public" if event["is_public"] else "Private",
            event_participants,
        ]
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

    user_id = get_userId(username)

    response = requests.get(
        "http://backend-invitations:8000/invitations", timeout=100
    )
    
    if response.status_code != 200:
        return redirect("/")

    all_invites = response.json()
    user_invites = []

    for invite in all_invites:
        if invite["invitee_id"] == user_id:
            user_invites.append(invite)

    for invite in user_invites:
        if invite["status"] == "pending":
            event_response = requests.get(
                f"http://backend-events:8000/events/{invite['event_id']}", timeout=100
            )
            
            if event_response.status_code != 200:
                continue
            
            event = event_response.json()
            
            organizer_response = requests.get(
                f"http://backend-auth:8000/users/{event['organizer_id']}", timeout=100
            )
            
            if organizer_response.status_code != 200:
                continue
            
            organizer = organizer_response.json()
            
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

    user_id = get_userId(username)
    int_event_id = int(eventId)

    response = requests.get(
        f"http://backend-invitations:8000/invitations?event_id={int_event_id}&invitee_id={user_id}",
        timeout=100,
    )

    invite_event = None
    
    if response.status_code == 200:
        invite_event = response.json()[0]
    else:
        return redirect("/invites")

    new_status = (
        "accepted"
        if status == "Participate"
        else "declined" if status == "Don't Participate" else "maybe"
    )

    if invite_event is not None:
        
        if invite_event["status"] != "pending":
            return redirect("/invites")
        
        requests.put(
            f"http://backend-invitations:8000/invitations/{invite_event['invite_id']}/status/{new_status}",
            timeout=100,
        )
        requests.post(
            "http://backend-participations:8000/participations",
            json={"user_id": user_id, "event_id": int_event_id, "status": new_status},
            timeout=100,
        )

    return redirect("/invites", code=307)


@app.route("/logout")
def logout() -> Response:
    global username, password

    username = None
    password = None
    return redirect("/")
