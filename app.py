from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


# We need to post the answers from the survey questions into the responses list

@app.get('/')
def show_survey():
    """ Returns a render template of survey start """
    return render_template("survey_start.html", 
                            title=survey.title, 
                            instructions=survey.instructions, 
                            questions=survey.questions)

@app.post("/begin")
def redirect_to_first_question():
    """ It'll redirect you to the start of the question/0"""
    session["responses"] = []
    return redirect('/question/0')


@app.get("/question/<int:question_index>")
def show_questions(question_index):
    """ Returns a render template of the question """ 
    # Scenario where user choose question number that is larger than the number of questions we actually have
    # user submits question 8 but user has completed all the questions
    if question_index >= len(session["responses"]) and len(session["responses"]) == len(survey.questions):
        return redirect('/completion')
    # user submits question 8 but only has completed 1
    elif question_index >= len(session["responses"]) and len(session["responses"]) < len(survey.questions):
        return render_template("question.html", question=survey.questions[len(session["responses"])])
    else: 
        return render_template("question.html", question=survey.questions[question_index])
    


@app.post("/answer")
def save_answer_to_responses():
    answer = request.form["answer"]
    
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    # if question index +1 is greater than the total questions we have render complete
    #otherwise render next question
    if len(responses) == len(survey.questions):
        return redirect('/completion')
    # if the question number is outside of the range

    # if the questio number is inside of the range but not the next question
    # ex. if they only answered question 1 but they put 3 in the URL, how do you make them go to question 2
    else:
        return redirect(f"/question/{len(responses)}")

@app.get("/completion")
def show_form_completion():
    # session["responses"] = []
    return render_template("completion.html")