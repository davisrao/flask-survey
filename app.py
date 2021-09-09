from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
RESPONSES_KEY = "responses"



# We need to post the answers from the survey questions into the responses list

@app.get('/')
def show_survey():
    """ Returns a render template of survey start """
    return render_template("survey_start.html", #can pass in survey=survey
                            title=survey.title, 
                            instructions=survey.instructions, 
                            questions=survey.questions)

@app.post("/begin")
def redirect_to_first_question():
    """ It'll redirect you to the start of the question/0"""
    session[RESPONSES_KEY] = []
    return redirect('/question/0')


@app.get("/question/<int:question_index>")
def show_questions(question_index):
    """ Returns a render template of the question """ 
    responses = session.get(RESPONSES_KEY)


    #if they have answered no questions
    if responses is None:
        return redirect('/')

    #if they are looking for the question index that matches where they should be in the form
    elif len(responses) == question_index:
        return render_template("question.html", question=survey.questions[question_index])

    #if they have previously completed and want to enter back in
    elif len(responses) == len (survey.questions):
        flash("You have already completed the survey!")
        return redirect('/completion')

    #if they try to skip questions
    elif len(responses) < len (survey.questions) and question_index != len(responses):
        flash("Whoops! That's an invalid question")
        return render_template("question.html", question=survey.questions[len(session[RESPONSES_KEY])])

    #     # flash("You have already completed the survey!")
    #     # return redirect('/completion')
    # elif question_index > len(session[RESPONSES_KEY]) and len(session[RESPONSES_KEY]) < len(survey.questions):
    #     flash("Whoops! That's an invalid question")
    #     return render_template("question.html", question=survey.questions[len(session[RESPONSES_KEY])])
    # else: 
    #     return render_template("question.html", question=survey.questions[question_index])
    


@app.post("/answer")
def save_answer_to_responses():
    """takes answer to survey question and stores in session for user responses"""
    answer = request.form["answer"]
    
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(survey.questions):
        return redirect('/completion')
   
    else:
        return redirect(f"/question/{len(responses)}")

@app.get("/completion")
def show_form_completion():
    """shows form completion"""
    return render_template("completion.html")