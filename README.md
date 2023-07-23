# AI Influencer - Angular and Flask Project

AI Influencer is a web application that allows users to login, signup, and chat with a chatbot that responds to queries related to parenting. The application also provides users the ability to view their chat history.

## Table of Contents
- [Clone the Repository](#clone-the-repository)
- [Setup](#setup)
- [Environment Variables](#environment-variables)
- [Accessing the Angular Project](#accessing-the-angular-project)
- [Backend Routes](#backend-routes)
- [Deployed Link](#deployed-link)

## Clone the Repository

To get started, clone the AI Influencer repository from GitHub:

```bash
git clone https://github.com/kuldeep55567/AI-Infulencer.git
cd frontend
```

## Setup

1. Install the required dependencies for the backend (Flask) and the frontend (Angular) separately.

2. Set up the backend environment by installing the required packages. Run the following command inside the root directory:

```bash
pip install -r requirements.txt
```

3. Set up the frontend environment by navigating to the `angular-app` directory and installing the Angular dependencies:

```bash
cd frontend
npm install
```

## Environment Variables

Create a `.env` file in the root directory of the backend and add the following environment variables:

```plaintext
MONGO_URL=<your_mongodb_url>
OPEN_API_KEY=<your_openai_api_key>
MONGO_NAME=<your_mongodb_name>
SECRET_KEY=<your_secret_key>
```

Replace `<your_mongodb_url>`, `<your_openai_api_key>`, `<your_mongodb_name>`, and `<your_secret_key>` with your actual values.

## Accessing the Angular Project

To access the Angular project, navigate to the `angular-app` directory and use the following commands:

```bash
cd angular-app
ng serve
```

The Angular application will be available at `http://localhost:4200/` in your web browser.

## Backend Routes

The backend (Flask) provides the following routes:

1. `GET /`
   - Returns a welcome message for the backend.

2. `GET /protected`
   - Requires authentication with a valid JWT token. Returns a protected route message along with the user's name.

3. `GET /users`
   - Returns a list of all users with their information and chat history.

4. `GET /queries`
   - Requires authentication with a valid JWT token. Returns the chat history of the logged-in user.

5. `POST /signup`
   - Allows a user to sign up by providing their name, email, password, and optional queries.

6. `POST /login`
   - Allows a user to log in with their email and password. Returns an access token on successful login.

7. `POST /answer`
   - Requires authentication with a valid JWT token. Accepts a question from the user and responds with a short and precise answer from the chatbot.

## Deployed Link

[https://64bd539befc13a3bf88a5fb1--storied-licorice-17a916.netlify.app]

```

You can copy and paste this content directly into your README.md file. Don't forget to replace `<repository_url>` with your actual GitHub repository URL and add your deployed link in the "Deployed Link" section.
