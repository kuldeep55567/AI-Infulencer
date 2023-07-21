from flask import Flask, request, jsonify
from flask_cors import CORS
from Config.db import Connection
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from dotenv import load_dotenv
from Model.User import User
import os
import openai

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)
connection = Connection()
connection.connect_to_db()
base_prompt = os.getenv("BASE_INSTRUCTIONS")
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET"])
def home():
    return jsonify({"mssg": "Welcome to the Backend of Curious Parent"})


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.objects(id=current_user_id).first()
    return jsonify({"message": f"Protected route. Welcome, {user.name}!"})

@app.route("/users", methods=["GET"])
def get_all_users():
    try:
        users = User.objects()
        users_data = [
            {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "queries": user.queries,
            }
            for user in users
        ]
        return jsonify(users_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/signup", methods=["POST"])
def signup():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]
    queries = request.json.get("queries", [])
    if User.objects(email=email).first():
        return jsonify({"message": "Email already registered"})
    user = User(name=name, email=email, password=password, queries=queries)
    user.hash_password()
    user.save()
    return jsonify({"message": "Signup successful"})


@app.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]
    user = User.objects(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"mssg": "Login Successfull", "token": access_token})


@app.route("/answer", methods=["POST"])
@jwt_required()
def answer():
    user_id = get_jwt_identity()
    question = request.get_json().get("question")
    response = openai.Completion.create(
        model="davinci:ft-personal:curious-parent-2023-07-20-19-37-07",
        prompt=base_prompt + question,
        temperature=1.18,
        max_tokens=128,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    answer_text = response.choices[0].text
    qa_entry = {"question": question, "answer": answer_text}

    try:
        user = User.objects(id=user_id).first()
        user.queries.append(qa_entry)
        user.save()

        return jsonify({"answer": answer_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
