from flask import Flask, render_template, request
from markupsafe import Markup   # ⬅️ add this line

from agent import AnswerAgent

app = Flask(__name__)
bot = AnswerAgent()           # loads the JSON KB on startup

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.form.get("msg", "")
    reply    = bot.respond(user_msg)

    if not reply:
        reply = "I’m not sure yet 🤔 — ask me something that’s in my knowledge‑base!"

    # Return a tiny HTML chunk; HTMX will drop it into the chat window
    snippet = f"""
      <div class='mb-2'><b>You:</b> {user_msg}</div>
      <div class='mb-2 text-info'><b>Bot:</b> {reply}</div>
      <hr class='my-1'>
    """
    return Markup(snippet)

if __name__ == "__main__":
    # debug=True gives hot‑reload while you develop
    app.run(debug=True)
