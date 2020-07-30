import os

from flask import Flask
from flask import render_template, url_for
from flask import request
from flask import redirect

from flask_mail import Mail
from flask_mail import Message

from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DATABASE_URL') or 'postgres://xwggdrhjrlegut:69b5038ee6b43e03c4ebe5f032f6e3d589a76daed4aa893b597204b6dc4b0b11@ec2-35-173-94-156.compute-1.amazonaws.com:5432/dfip2ic8ku64rs'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'secret'

app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']= os.environ.get('MAIL_USERNAME') or 'intellitrak.quiz@gmail.com'
app.config['MAIL_PASSWORD']= os.environ.get('MAIL_PASSWORD') or 'quizmaster'



db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
mail = Mail(app)

course=''
quiz_name=''
description=''
account=''
current_user='Student'

class Question(db.Model):
    __tablename__ = 'questions'

    qid = db.Column(db.Integer, primary_key=True, nullable=False) #question_id
    account = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(50), nullable=False)
    quiz_name=db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    question = db.Column(db.String(500))
    choice_a = db.Column(db.String(100))
    choice_b = db.Column(db.String(100))
    choice_c = db.Column(db.String(100))
    choice_d = db.Column(db.String(100))
    choice_e = db.Column(db.String(100))
    answer = db.Column(db.String(200))



@app.route('/login', methods=['GET','POST'])
def login():
    return render_template('login.html')

@app.route('/action_login', methods=['GET','POST'])
def action_login():
    username = request.form.get('username')
    password = request.form.get('pass')
    global current_user

    if (username==(os.environ.get('ADMIN_USERNAME') or 'admin') and password== (os.environ.get('ADMIN_PASSWORD') or 'admin')):    
        current_user = "Admin"
        return redirect(url_for('edit'))
    else:
        return render_template('noaccess.html', name = current_user)

@app.route('/logout', methods=['GET','POST'])
def logout():
    return render_template('logout.html')

@app.route('/action_logout', methods=['GET','POST'])
def action_logout():
    global current_user      
    current_user = "Student"
    return redirect(url_for('home'))
  

@app.route("/", methods=['GET','POST'])
def home():

    q = db.engine.execute("select distinct course, quiz_name, description, account from questions order by course asc;")#running sql queries from python
    return render_template('home.html', quizzes=q, action='attempt', name=current_user)


@app.route("/new", methods=['GET' ,'POST'])
def new():
    if(current_user=="Admin"):
        return render_template('new.html', name=current_user)
    
    return render_template('noaccess.html', name = current_user)


@app.route("/attemptquiz", methods=['GET','POST'])
def attemptquiz():

    questions = Question.query.filter_by(quiz_name = quiz_name).order_by(Question.qid)
    return render_template('attempt_quiz.html', questions = questions ,course=course, account=account, topic=quiz_name, description = description, name=current_user)

@app.route("/newquestion", methods=['GET','POST'])
def newquestion():
    if (current_user!='Admin'):
        return render_template('noaccess.html', name = current_user)
    global course
    global quiz_name
    global description
    global account
    return render_template('newquestion.html', course=course, topic=quiz_name, description = description, account=account, name=current_user)

@app.route("/edit", methods=['GET','POST'])
def edit():
    if (current_user!='Admin'):
        return render_template('noaccess.html', name = current_user)
    q = db.engine.execute("select distinct course, quiz_name, description, account from questions order by course asc;")#running sql queries from python
    return render_template('edit.html', quizzes=q, action='edit', name=current_user)

@app.route("/edit_questions", methods=['GET','POST'])
def edit_questions():
    if (current_user!='Admin'):
        return render_template('noaccess.html', name = current_user)
    questions = Question.query.filter_by(quiz_name= quiz_name).order_by(Question.qid)
    que = Question.query.filter_by(quiz_name= quiz_name).first()
    return render_template('edit_questions.html', que = que, questions = questions,course = course,account=account, topic=quiz_name, description=description, name=current_user)


@app.route("/edit_details", methods=['GET','POST'])
def edit_details():
    if (current_user!='Admin'):
        return render_template('noaccess.html', name = current_user)
    return render_template('edit_details.html', course = course, quiz_name = quiz_name, account = account, description = description, name=current_user )

    

@app.route("/action_attempt", methods=['GET','POST'])
def action_attempt():
    global course
    global quiz_name
    global description
    global account

    quiz_name=request.form.get("form_quizname")
    course = request.form.get("form_course")
    description = request.form.get("form_description")
    account= request.form.get("form_account")

    return redirect(url_for('attemptquiz'))
@app.route("/action_newquiz", methods=['GET','POST'])
def action_newquiz():
    global course
    global quiz_name
    global description
    global account

    quiz_name=request.form.get("form_quizname")
    course = request.form.get("form_course")
    description = request.form.get("form_description")
    account = request.form.get("form_account")

    check = Question.query.filter_by(quiz_name = quiz_name)
    if(check.count()==0):
        return redirect(url_for('newquestion'))
    else:
        return render_template('quizexists.html')

@app.route("/action_newquestion", methods=['GET','POST'])
def action_newquestion():
    new_ques = Question(account = request.form.get("form_account"), course=request.form.get("form_course"), quiz_name = request.form.get("form_quizname"), description = request.form.get("form_description"), \
                            question=request.form.get("form_question"), choice_a = request.form.get("form_a"), choice_b = request.form.get("form_b"), choice_c = request.form.get("form_c"),\
                            choice_d = request.form.get("form_d"), choice_e = request.form.get("form_e"), answer = request.form.get("form_answer"))
    db.session.add(new_ques)
    db.session.commit()
    return redirect(url_for('newquestion'))

@app.route("/action_deletequiz", methods=['POST'])
def action_deletequiz():
    name = request.form.get('del_quizname')
    return render_template('confirm_delete.html', quiz_name = name)

@app.route("/action_confirmdeletequiz", methods=['POST'])
def action_confirmdeletequiz():
    Question.query.filter_by(quiz_name=request.form.get('del_quizname')).delete()
    db.session.commit()
    return redirect(url_for('edit'))

@app.route("/action_editquiz", methods=['GET','POST'])
def action_editquiz():
    global course
    global quiz_name
    global description
    global account 

    quiz_name = request.form.get('edit_quizname')
    course = request.form.get('edit_course')
    description = request.form.get('edit_description')
    account = request.form.get('edit_account')

    return redirect(url_for('edit_questions'))

@app.route("/action_editquizdetails", methods=['GET','POST'])
def action_editquizdetails():
    global course
    global quiz_name
    global description
    global account 

    quiz_name = request.form.get('det_quizname')
    course = request.form.get('det_course')
    description = request.form.get('det_description')
    account = request.form.get('det_account')

    return redirect(url_for('edit_details'))


@app.route("/action_editquestion", methods=['GET','POST'])
def action_editquestion():
    tot_qs = request.form.get('tot_qs')

    for i in range(1, int(tot_qs)):
        delete = request.form.get('form_delete_'+str(i))
        q_id=request.form.get('form_qid_'+str(i))
        search = Question.query.filter_by(qid = q_id).first()
        
        if(delete=="on"):
            db.session.delete(search)
            db.session.commit()
        else:
            question = request.form.get('form_question_'+str(i))
            choice_a = request.form.get('form_a_'+str(i))
            choice_b = request.form.get('form_b_'+str(i))
            choice_c = request.form.get('form_c_'+str(i))
            choice_d = request.form.get('form_d_'+str(i))
            choice_e = request.form.get('form_e_'+str(i))
            answer = request.form.get('form_answer_'+str(i))
            
            search.question = question
            search.choice_a = choice_a
            search.choice_b = choice_b
            search.choice_c = choice_c
            search.choice_d = choice_d
            search.choice_e = choice_e
            search.answer = answer

            db.session.commit()
    
    return redirect(url_for('edit'))

@app.route("/action_update_details", methods=['GET','POST'])
def action_update_details():
    global quiz_name
    course = request.form.get('updet_course')
    quiz = request.form.get('updet_quizname')
    account = request.form.get('updet_account')
    description = request.form.get('updet_description')

    check = Question.query.filter_by(quiz_name = quiz)
    if(check.count()!=0 and quiz!=quiz_name ):
        return render_template('quizexists.html')
    
    updated = Question.query.filter_by(quiz_name=quiz_name).update({Question.course:course, Question.quiz_name:quiz, Question.description:description, Question.account:account})
    db.session.commit()
    return redirect(url_for('edit'))

@app.route("/action_addmorequestions", methods=['GET','POST'])
def action_addmorequestions():
    global course
    global quiz_name
    global description
    global account

    course=request.form.get('add_course')
    quiz_name = request.form.get('add_quizname')
    description = request.form.get('add_description')
    account = request.form.get('add_account')

    return redirect(url_for('newquestion'))

@app.route("/action_quizcomplete", methods=['GET','POST'])
def action_quizcomplete():
    studentanswers = []
    correctanswers = []
    tot_correct=0
  
    tot_questions = request.form.get('tot_qs')
    course = request.form.get('course')
    topic = request.form.get('topic')
    desc = request.form.get('description')
    account = request.form.get('account')
    name = request.form.get('stud_name')

    print(tot_questions)
    for i in range (1,int(tot_questions)+1):

        studans =request.form.get('ans_'+str(i))
        corrans = request.form.get('correct_'+str(i))
        if(studans==corrans):
            tot_correct = tot_correct+1

        studentanswers.append(studans)
        correctanswers.append(corrans)


    mailResults(account, course, topic, studentanswers, name, tot_correct, tot_questions)
    return render_template('quiz_submitted.html')


def mailResults(account, course, quiz_name, stud_answers, name, tot_correct, tot_questions):

    questions = Question.query.filter_by(quiz_name= quiz_name).order_by(Question.qid)
    print("Account: ", account)

    msg = Message("Quiz Results: " + name,
                  sender="intellitrak.quiz@gmail.com",
                  recipients=[str(account)])

    msg.html=render_template('results.html', questions = questions, course = course, topic=quiz_name, stud_answers = stud_answers, name=name, tot_correct = tot_correct, tot_questions=tot_questions)
    mail.send(msg)


if(__name__=="__main__"):
    app.run()