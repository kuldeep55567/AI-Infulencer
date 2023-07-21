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
import datetime

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=24)
jwt = JWTManager(app)
connection = Connection()
connection.connect_to_db()
base_prompt = "Act as a parenting influencer and respond to questions given by parents about their children. The response that you give should follow some of the rules. The name of the parent who is asking the question is given before asking every question in the format of {parent_name}, question.......Never use points to give answers, always give them in paragraphs only. Reply in the same language in which the parent is asking a question.Your Answers should be short and precise but should not look like AI.If the age of the Child is not given then ask clarifying questions such as, Hello {name of parent} Can you provide me your child's age, as it will help me know your child better? "
# first_filter = "Check these few pointers. Name of parent is given, use it to greet them before answering. If child age is not provided ask him to give child age like this. Heyy {parent_name} can you provide me child name, it will help me to understand your concern better. If you are not sure of what to answer , ask the parent to ask the question widely"
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
        users_data = []
        for user in users:
            if isinstance(user, User):
                user_data = {
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "queries": user.queries,
                }
                users_data.append(user_data)

        return jsonify(users_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/queries", methods=["GET"])
@jwt_required()
def get_user_queries():
    current_user_id = get_jwt_identity()
    user = User.objects(id=current_user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.queries)


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
    current_user_id = get_jwt_identity()
    question = request.get_json().get("question")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": f"{user.name}{question}"},
        ],
        temperature=1.18,
        max_tokens=128,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    qa_entry = {
        "question": question,
        "answer": response.choices[0].message.get("content", ""),
    }
    try:
        user = User.objects(id=current_user_id).first()
        user.queries.append(qa_entry)
        user.save()
        return jsonify({"answer": response.choices[0].message.get("content", "")})
    except Exception as e:
        return jsonify({"'error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
