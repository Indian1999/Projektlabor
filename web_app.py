from flask import Flask, render_template, jsonify, request, send_from_directory, session, redirect, url_for
from functools import wraps
from server_application import ServerApplication
from process import Process
from genetic import Genetic
from constructive import Constructive
import os
import json
import hashlib
from datetime import timedelta
from config import Config

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__,
            static_folder=os.path.join(basedir, "static"),
            template_folder=os.path.join(basedir, "templates"))

app.config.from_object(Config)

def load_credentials():
    """Load user credentials from JSON file"""
    credentials_file = os.path.join(basedir, "credentials.json")
    try:
        with open(credentials_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {user["username"]: user["password_hash"] for user in data.get("users", [])}
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return {}

USERS = load_credentials()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function
server_app = ServerApplication()


server_app.load_results()

@app.route("/")
def index():
    """Main page with navigation"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login page"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_hash = hashlib.sha256((password + app.config["SECRET_KEY"]).encode()).hexdigest()

        if username in USERS and password_hash == USERS[username]:
            session["logged_in"] = True
            session.permanent = True
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("processes_page"))
        else:
            return render_template("login.html", error="Hibás felhasználónév vagy jelszó")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Logout"""
    session.pop("logged_in", None)
    return redirect(url_for("index"))

@app.route("/browse")
def browse():
    """Browse existing solutions"""
    return render_template("browse.html")

@app.route("/processes")
@login_required
def processes_page():
    """Process management page"""
    return render_template("processes.html")

@app.route("/new-process")
@login_required
def new_process():
    """Create new process page"""
    return render_template("new_process.html")

##################################
#         API végpontok          #
##################################

@app.route("/api/results")
def api_get_all_results():
    """Get all results grouped by n"""
    results_by_n = {}
    for result in server_app.results:
        n = result["n"]
        if n not in results_by_n:
            results_by_n[n] = []
        results_by_n[n].append(result)
    
    for n in results_by_n:
        results_by_n[n].sort(key=lambda x: x["result"], reverse=True)
    
    return jsonify(results_by_n)

@app.route("/api/results/<int:n>")
def api_get_results_by_n(n):
    """Get all results for a specific n"""
    results = [r for r in server_app.results if r["n"] == n]
    results.sort(key=lambda x: x["result"], reverse=True)
    return jsonify(results)

@app.route("/api/results/best/<int:n>")
def api_get_best_result(n):
    """Get best result for specific n"""
    best = server_app.get_best_space(n)
    if best:
        return jsonify(best)
    return jsonify({"error": "No results found"}), 404

@app.route("/api/processes")
@api_login_required
def api_get_processes():
    """Get all active processes"""
    processes = server_app.get_processes(format="json")
    return jsonify({
        "processes": processes,
        "active_index": server_app.active_process_index
    })

@app.route("/api/processes/add", methods=["POST"])
@api_login_required
def api_add_process():
    """Add a new process"""
    data = request.json
    solver_type = data.get("type", "genetic")

    try:
        if solver_type == "genetic":
            solver = Genetic(
                n=data["n"],
                population_size=data.get("population_size", 50),
                generations=data.get("generations", 100),
                mutation_rate=data.get("mutation_rate", 0.1),
                accuracy=data.get("accuracy", 0),
                reach=data.get("reach"),
                fitness_mode=data.get("fitness_mode", 2)
            )
        elif solver_type == "constructive":
            iterations = data.get("iterations", 1)
            if iterations < 1 or iterations > 10:
                return jsonify({"error": "Az iterációk száma 1 és 10 között kell legyen!"}), 400

            solver = Constructive(
                n=data["n"],
                accuracy=data.get("accuracy", 0),
                reach=data.get("reach"),
                strategy=data.get("strategy", "hybrid"),
                iterations=iterations
            )
        else:
            return jsonify({"error": "Invalid solver type"}), 400

        try:
            process = Process(solver, priority=data.get("priority", 0))
        except Exception as e:
            print(f"Error creating process: {e}")
            return jsonify({"error": f"Process creation failed: {str(e)}"}), 500

        try:
            server_app.add_process(process, start_immediately=data.get("start_immediately", False))
        except Exception as e:
            print(f"Error adding process: {e}")
            return jsonify({"error": f"Failed to add process: {str(e)}"}), 500

        return jsonify({"message": "Folyamat sikeresen létrehozva!"}), 200
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Unexpected error: {str(e) if str(e) else 'Unknown error'}"}), 500

@app.route("/api/processes/<int:index>/terminate", methods=["POST"])
@api_login_required
def api_terminate_process(index):
    """Terminate a process"""
    try:
        server_app.terminate_process(index)
        return jsonify({"message": "Process terminated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/processes/<int:index>/activate", methods=["POST"])
@api_login_required
def api_activate_process(index):
    """Change active process"""
    try:
        server_app.change_active_process(index)
        return jsonify({"message": "Process activated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/stats")
def api_get_stats():
    """Get overall statistics"""
    stats = {
        "total_results": len(server_app.results),
        "active_processes": len(server_app.processes),
        "n_values": list(set(r["n"] for r in server_app.results)),
        "best_by_n": {}
    }
    
    for n in stats["n_values"]:
        best = server_app.get_best_space(n)
        if best:
            stats["best_by_n"][n] = best["result"]
    
    return jsonify(stats)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)