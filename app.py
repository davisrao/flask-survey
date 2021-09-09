from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
# We need to post the answers from the survey questions into the responses list

@app.get('/')
def show_survey():
    """ Returns a render template of survey start """
    return render_template("survey_start.html", 
                            title=survey.title, 
                            instructions=survey.instructions, 
                            questions=survey.questions)

@app.post("/begin")
def 
""" It'll redirect you to the start of the question/0"""

@app.get("/question/<question_index>")
def show_questions(question_index):
    """ Returns a render template of the question """
    question_index = int(request.args["question_index"])
    return render_template("question.html", question=survey.questions[question_index])
