from datetime import datetime
import os
from sqlalchemy import or_
from functools import wraps
from flask import send_from_directory
import secrets
import uuid
from flask import abort

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify
)

from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}

from models import (
    db,
    Coordinator,
    Report
)


# --------------------------------------------------
# Flask Configuration
# --------------------------------------------------

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    secrets.token_hex(32)
)

app.config["SESSION_COOKIE_SECURE"] = True

app.config["SESSION_COOKIE_HTTPONLY"] = True

app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///faults.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
    False
)

app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "uploads"
)

app.config["MAX_CONTENT_LENGTH"] = (
    2 * 1024 * 1024
)

db.init_app(app)

def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)


# --------------------------------------------------
# Home
# --------------------------------------------------

def login_required(view):

    @wraps(view)

    def wrapped_view(
        *args,
        **kwargs
    ):

        if (
            "coordinator_id"
            not in session
        ):

            flash(
                "Please log in first.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        return view(
            *args,
            **kwargs
        )

    return wrapped_view

@app.route("/")
def home():

    total_reports = (
        Report.query.count()
    )

    open_reports = (
        Report.query
        .filter_by(status="Open")
        .count()
    )

    in_progress_reports = (
        Report.query
        .filter_by(
            status="In Progress"
        )
        .count()
    )

    closed_reports = (
        Report.query
        .filter_by(status="Closed")
        .count()
    )

    return render_template(
        "index.html",
        total_reports=total_reports,
        open_reports=open_reports,
        in_progress_reports=in_progress_reports,
        closed_reports=closed_reports
    )


# --------------------------------------------------
# Login
# --------------------------------------------------

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = (
            request.form.get("username", "")
            .strip()
        )

        password = request.form.get(
            "password"
        )

        coordinator = (
            Coordinator.query
            .filter_by(
                username=username
            )
            .first()
        )

        if (
            coordinator and
            coordinator.check_password(
                password
            )
        ):

            session["coordinator_id"] = (
                coordinator.id
            )

            flash(
                "Login successful.",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid username or password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


# --------------------------------------------------
# Logout
# --------------------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "info"
    )

    return redirect(
        url_for("home")
    )


# --------------------------------------------------
# Report Fault
# --------------------------------------------------

@app.route(
    "/report",
    methods=["GET", "POST"]
)
def report():

    if request.method == "POST":
        
        if (
            request.form.get(
                "csrf_token"
            )
            !=
            session.get(
                "csrf_token"
            )
        ):
            
            abort(403)

        photo = request.files.get(
            "photo"
        )
        
        filename = None

        if (
            photo and
            photo.filename
            and
            allowed_file(
                photo.filename
            )
            and
            photo.mimetype
            in ALLOWED_MIME_TYPES
        ):

            original_name = secure_filename(
                photo.filename
            )

            extension = (
                original_name
                .rsplit(".", 1)[1]
                .lower()
            )

            filename = (
                f"{uuid.uuid4()}.{extension}"
            )

            save_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
            
            photo.save(save_path)

        report = Report(

            category=request.form.get(
                "category"
            ),

            street=request.form.get(
                "street"
            ),

            description=request.form.get(
                "description"
            ),

            reporter_name=request.form.get(
                "reporter_name"
            ),

            reporter_cell=request.form.get(
                "reporter_cell"
            ),

            photo_filename=filename

        )

        db.session.add(report)

        db.session.commit()

        flash(
            f"Report submitted successfully. "
            f"Reference: {report.reference}",
            "success"
        )

        return redirect(
            url_for("report")
        )

    return render_template(
        "report.html"
    )


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():
     
    total_reports = (
        Report.query.count()
    )

    open_reports = (
        Report.query
        .filter_by(status="Open")
        .count()
    )

    in_progress_reports = (
        Report.query
        .filter_by(
            status="In Progress"
        )
        .count()
    )

    closed_reports = (
        Report.query
        .filter_by(status="Closed")
        .count()
    )

    pothole_count = (
        Report.query
        .filter_by(
            category="Pothole"
        )
        .count()
    )

    water_leak_count = (
        Report.query
        .filter_by(
            category="Water Leak"
        )
        .count()
    )

    streetlight_count = (
        Report.query
        .filter_by(
            category="Streetlight"
        )
        .count()
    )

    dumping_count = (
        Report.query
        .filter_by(
            category="Illegal Dumping"
        )
        .count()
    )

    other_count = (
        Report.query
        .filter_by(
            category="Other"
        )
        .count()
    )

    recent_reports = (
        Report.query
        .order_by(
            Report.created_at.desc()
        )
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",

        total_reports=total_reports,

        open_reports=open_reports,

        in_progress_reports=
        in_progress_reports,

        closed_reports=
        closed_reports,

        pothole_count=
        pothole_count,

        water_leak_count=
        water_leak_count,

        streetlight_count=
        streetlight_count,

        dumping_count=
        dumping_count,

        other_count=
        other_count,

        recent_reports=
        recent_reports,

        current_time=
        datetime.now()

    )
    
# --------------------------------------------------
# Manage Reports
# --------------------------------------------------

@app.route("/reports")
@login_required
def reports():

    query = Report.query

    search = request.args.get(
        "search",
        ""
    )

    category = request.args.get(
        "category",
        ""
    )

    status = request.args.get(
        "status",
        ""
    )

    if search:

        query = query.filter(
            
            or_(
                
            Report.reference.contains(search),
            
            Report.street.contains(search),
            
            Report.description.contains(search)
            
            )
        )

    if category:

        query = query.filter_by(
            category=category
        )

    if status:

        query = query.filter_by(
            status=status
        )

    reports = (
        query
        .order_by(
            Report.created_at.desc()
        )
        .all()
    )

    return render_template(
        "reports.html",
        reports=reports
    )

# --------------------------------------------------
# Check Status
# --------------------------------------------------

@app.route(
    "/status",
    methods=["GET", "POST"]
)
def check_status():

    report = None

    if request.method == "POST":

        if (
            request.form.get(
                "csrf_token"
            )
            !=
            session.get(
                "csrf_token"
            )
        ):
            abort(403)

        reference = (
            request.form.get(
                "reference",
                ""
            )
            .strip()
            .upper()
        )

        report = Report.query.filter_by(
            reference=reference
        ).first()

        if not report:

            flash(
                "No report found with that reference number.",
                "warning"
            )

    return render_template(
        "status.html",
        report=report
    )

# --------------------------------------------------
# API Report Summary
# --------------------------------------------------

@app.route(
    "/api/reports/summary"
)
@login_required
def reports_summary():

    return jsonify({

        "total":
        Report.query.count(),

        "open":
        Report.query.filter_by(
            status="Open"
        ).count(),

        "in_progress":
        Report.query.filter_by(
            status="In Progress"
        ).count(),

        "closed":
        Report.query.filter_by(
            status="Closed"
        ).count(),

        "potholes":
        Report.query.filter_by(
            category="Pothole"
        ).count(),

        "water_leaks":
        Report.query.filter_by(
            category="Water Leak"
        ).count(),

        "streetlights":
        Report.query.filter_by(
            category="Streetlight"
        ).count(),

        "illegal_dumping":
        Report.query.filter_by(
            category="Illegal Dumping"
        ).count(),

        "other":
        Report.query.filter_by(
            category="Other"
        ).count()

    })

# --------------------------------------------------
# Update Status
# --------------------------------------------------

@app.route(
    "/reports/<int:report_id>/update",
    methods=["POST"]
)
@login_required
def update_report_status(
    report_id
):
    
    if (
        request.form.get(
            "csrf_token"
        )
        !=
        session.get(
            "csrf_token"
        )
    ):

        abort(403)
    
    report = (
        Report.query
        .get_or_404(report_id)
    )

    status = request.form.get(
        "status"
    )
    
    allowed_statuses = [
    
        "Open",
    
        "In Progress",
    
        "Closed"
    
        ]
    
    if status not in allowed_statuses:
    
        abort(400)
    
    report.status = status

    db.session.commit()

    flash(
        "Report status updated.",
        "success"
    )

    return redirect(
        url_for("reports")
    )

@app.route(
    "/reports/<int:report_id>"
)
@login_required
def report_detail(
    report_id
):

    report = Report.query.get_or_404(
        report_id
    )

    return render_template(
        "report_detail.html",
        report=report
    )

# --------------------------------------------------
# Offline Page
# --------------------------------------------------

@app.route("/service-worker.js")
def service_worker():

    return send_from_directory(

        "static",

        "service-worker.js",

        mimetype="application/javascript"

    )

@app.route("/offline")
def offline():

    return render_template(
        "offline.html"
    )

@app.after_request
def add_security_headers(response):

    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"

    response.headers[
        "X-Frame-Options"
    ] = "DENY"

    response.headers[
        "Content-Security-Policy"
    ] = (
        "default-src 'self'; "
        "script-src 'self' "
        "https://cdn.jsdelivr.net "
        "'unsafe-inline'; "
        "style-src 'self' "
        "https://cdn.jsdelivr.net "
        "'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self' "
        "https://cdn.jsdelivr.net;"
    )

    return response

@app.before_request
def generate_csrf_token():

    if "csrf_token" not in session:

        session["csrf_token"] = (
            secrets.token_hex(16)
        )
        
@app.context_processor
def inject_csrf_token():

    return {

        "csrf_token":
        session.get(
            "csrf_token"
        )

    }
    
# --------------------------------------------------
# Create Database
# --------------------------------------------------

with app.app_context():

    db.create_all()

    if not Coordinator.query.filter_by(
        username="admin"
    ).first():

        admin = Coordinator(
            username="admin"
        )

        admin.set_password(
            "Admin123!"
        )

        db.session.add(admin)

        db.session.commit()
        
# --------------------------------------------------
# Run Application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )
    