from flask import Flask, request, render_template, redirect, session, flash
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, Question, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "guitar"

# debug = DebugToolbarExtension(app)


@app.route('/')
def start_page():
    return render_template('start.html', survey = surveys['satisfaction'])

@app.route('/session', methods=['POST'])
def set_session():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:num>')
def question_page(num):
    responses = session['responses']
    #redirect to proper sequential question
    if num > len(responses) or num < len(responses):
        flash("Invalid Question, Please answer this one.")
        return redirect(f'/questions/{len(responses)}')

    #remove access to questions after completion
    if len(responses) == len(surveys['satisfaction'].questions) :  
        return redirect('/thanks')

    return render_template('question.html', num = num, question = surveys['satisfaction'].questions[num-1])

@app.route('/answer', methods = ["POST"])
def handle_answer():
    answer = request.form['answer']
    
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    return redirect(f'/questions/{len(responses)}')

@app.route('/thanks')
def thankyou_page():
    return render_template('thanks.html')