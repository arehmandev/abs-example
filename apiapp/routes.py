from apiapp import app, db, ma, jsonify, request
from apiapp.models import Survivor, SurvivorSchema
import csv
import os
import threading
import io


survivor_schema = SurvivorSchema()
survivors_schema = SurvivorSchema(many=True)

db.create_all()


@app.route("/people", methods=["POST"])
def add_survivor():
    single = db.session.query(Survivor).filter_by(**request.json).first()
    if not single:
        single = Survivor(**request.json)
        db.session.add(single)
        db.session.commit()

    return survivor_schema.jsonify(single)


@app.route("/people", methods=["GET"])
def list():
    multiple = Survivor.query.all()
    result = survivors_schema.dump(multiple)
    return survivors_schema.jsonify(result)


@app.route("/people/<id>")
def get(id):
    result = Survivor.query.get(id)
    return survivor_schema.jsonify(result)


@app.route("/people/<id>", methods=["PUT"])
def update(id):
    result = Survivor.query.get(id)
    result.setvalues(**request.json)

    db.session.commit()
    return survivor_schema.jsonify(result)


@app.route("/people/<id>", methods=["DELETE"])
def delete(id):
    result = Survivor.query.get(id)
    db.session.delete(result)
    db.session.commit()

    return "Removed"


# This route populates the DB, added a lock to ensure no parallel population occurs
# Also added a lock file to prevent slowing down of db with multiple queries
@app.route("/load", methods=["GET"])
def load():
    csv_file = "test/titanic.csv"
    lock_file = f"{csv_file}.lock"
    lock = threading.Lock()

    with lock:
        if os.path.isfile(lock_file):
            return f"CSV data already loaded, file present: {lock_file} "

        with open(csv_file) as f:
            process_csv(f.readlines())
        x = open(lock_file, "w")
        x.write("complete")
        x.close()

    return f"All CSV data loaded from {csv_file}"


@app.route("/csv", methods=["POST"])
def csv_upload():

    data = io.StringIO(request.files['file'].stream.read().decode("UTF8"))
    return process_csv(data)


def process_csv(csv_file_data):

    csvreader = csv.reader(csv_file_data,
                           delimiter=',')

    counter = 0
    for row in csvreader:
        counter += 1
        if counter == 1:
            continue

        single_dict = dict()

        index = 0
        for field in SurvivorSchema.Meta.fields:
            if field == "id":
                continue
            single_dict[field] = row[index]

            index += 1

        entry = db.session.query(Survivor).filter_by(**single_dict).first()
        if not entry:
            entry = Survivor(**single_dict)
            db.session.add(entry)
            db.session.commit()
    return "All CSV data loaded from request"
