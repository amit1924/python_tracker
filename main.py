from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

main = Flask(__name__)

# Initialize MongoDB connection
client = MongoClient("mongodb+srv://amish198:Amit1988@cluster0.gos2qpp.mongodb.net/")
db = client["clients"]  # Replace with your database name
collection = db["client_data"]


@main.route("/")
def index():
    # Fetch client data from MongoDB
    client_data = list(collection.find())
    return render_template("index.html", client_list=client_data)


@main.route("/add", methods=["POST"])
def add_client():
    client_data = {
        "Name": request.form["name"],
        "Contact Number": request.form["contact"],
        "City": request.form["city"],
        "Country": request.form["country"],
        "Payg": request.form["payg"],
        "Email": request.form["email"],
        "Notice Period": request.form["notice_period"],
        "Relocation": request.form["relocation"],
        "Date of Joining": request.form["date_of_joining"],
        "Reminder of Joining": request.form["reminder_of_joining"],
        "Expertise": request.form["expertise"],
        "Experience": request.form["experience"],
    }

    # Insert client data into the MongoDB collection
    collection.insert_one(client_data)

    return redirect(url_for("index"))


@main.route("/edit/<string:client_id>", methods=["GET", "POST"])
def edit_client(client_id):
    client_data = collection.find_one({"_id": ObjectId(client_id)})

    if request.method == "POST":
        updated_data = {
            "Name": request.form["name"],
            "Contact Number": request.form["contact"],
            "City": request.form["city"],
            "Country": request.form["country"],
            "Payg": request.form["payg"],
            "Email": request.form["email"],
            "Notice Period": request.form["notice_period"],
            "Relocation": request.form["relocation"],
            "Date of Joining": request.form["date_of_joining"],
            "Reminder of Joining": request.form["reminder_of_joining"],
            "Expertise": request.form["expertise"],
            "Experience": request.form["experience"],
        }

        # Update client data in the MongoDB collection
        result = collection.update_one(
            {"_id": ObjectId(client_id)}, {"$set": updated_data}
        )

        if result.modified_count == 1:
            return redirect(url_for("index"))
        else:
            return render_template(
                "edit.html", client=client_data, error_message="Update failed"
            )

    return render_template("edit.html", client=client_data)


@main.route("/delete/<string:client_id>", methods=["POST"])
def delete_client(client_id):
    # Delete client data from the MongoDB collection
    collection.delete_one({"_id": ObjectId(client_id)})

    return redirect(url_for("index"))


if __name__ == "__main__":
    main.run(debug=True)
