from flask import Flask, request, jsonify, abort, render_template, redirect, url_for

app = Flask(__name__)

# In-Memory Daten (statt DB)
todo_lists = {}
todo_entries = {}

list_counter = 1
entry_counter = 1

# ----------------------------
# HTML Routes
# ----------------------------

# Startseite - alle Listen
@app.route("/")
def home():
    return render_template("index.html", lists=todo_lists.values())

# Liste anzeigen + Einträge
@app.route("/list/<int:list_id>")
def show_list(list_id):
    if list_id not in todo_lists:
        abort(404)
    entries = [e for e in todo_entries.values() if e["list_id"] == list_id]
    return render_template("list.html", list=todo_lists[list_id], entries=entries)

# ----------------------------
# HTML Form Aktionen
# ----------------------------

# Neue Liste erstellen
@app.route("/todo-list", methods=["POST"])
def create_list():
    name = request.form.get("name")
    if not name:
        return "Name fehlt", 400

    global list_counter
    new_list = {"id": list_counter, "name": name}
    todo_lists[list_counter] = new_list
    list_counter += 1

    return redirect(url_for("home"))

# Liste löschen
@app.route("/delete-list/<int:list_id>", methods=["POST"])
def delete_list_html(list_id):
    if list_id in todo_lists:
        global todo_entries
        todo_entries = {k: v for k, v in todo_entries.items() if v["list_id"] != list_id}
        del todo_lists[list_id]
    return redirect(url_for("home"))

# Neuer Eintrag in Liste
@app.route("/todo-list/<int:list_id>", methods=["POST"])
def create_entry(list_id):
    if list_id not in todo_lists:
        return "Liste nicht gefunden", 404

    name = request.form.get("name")
    description = request.form.get("description")
    if not name or not description:
        return "Ungültiger Body", 400

    global entry_counter
    new_entry = {
        "id": entry_counter,
        "list_id": list_id,
        "name": name,
        "description": description
    }
    todo_entries[entry_counter] = new_entry
    entry_counter += 1

    return redirect(url_for("show_list", list_id=list_id))

# Eintrag löschen
@app.route("/delete-entry/<int:entry_id>", methods=["POST"])
def delete_entry_html(entry_id):
    if entry_id in todo_entries:
        del todo_entries[entry_id]
    return redirect(request.referrer or url_for("home"))

# ----------------------------
# JSON REST API (optional)
# ----------------------------

# Alle Listen als JSON
@app.route("/todo-list", methods=["GET"])
def get_lists():
    return jsonify(list(todo_lists.values())), 200

# Alle Einträge einer Liste
@app.route("/todo-list/<int:list_id>", methods=["GET"])
def get_entries(list_id):
    if list_id not in todo_lists:
        return jsonify({"error": "List not found"}), 404
    entries = [e for e in todo_entries.values() if e["list_id"] == list_id]
    return jsonify(entries), 200

# Eintrag aktualisieren via JSON
@app.route("/todo-list/entry/<int:entry_id>", methods=["PATCH"])
def update_entry(entry_id):
    if entry_id not in todo_entries:
        return jsonify({"error": "Entry not found"}), 404
    data = request.get_json()
    if not data or "name" not in data or "description" not in data:
        return jsonify({"error": "Invalid body"}), 400
    todo_entries[entry_id]["name"] = data["name"]
    todo_entries[entry_id]["description"] = data["description"]
    return jsonify(todo_entries[entry_id]), 200

# Eintrag löschen via JSON
@app.route("/todo-list/entry/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    if entry_id not in todo_entries:
        return jsonify({"error": "Entry not found"}), 404
    del todo_entries[entry_id]
    return "", 204

# ----------------------------
# Server starten
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=True)
