<h1 align="center">
  <a href="http://quizz-master.herokuapp.com">Quiz Master</a>
</h1>
<p align="center">
  <a href="https://github.com/theakashanand/quiz-master/releases"><img alt="Release" src="https://img.shields.io/github/release/theakashanand/quiz-master.svg"/></a>
  <a href="https://github.com/theakashanand/quiz-master"><img alt="Code Size" src="https://img.shields.io/github/languages/code-size/theakashanand/quiz-master.svg"/></a>
  <a href="http://quizz-master.herokuapp.com"><img alt="Demo" src="https://img.shields.io/badge/demo-online-green.svg"/></a>
</p>

<p>
The source code for Intellitrak's Quiz Master web-application. Quiz Master is an online web-application to enable institutions conduct online multiple-choice quizzes for their students. 

Instructors with admin accounts on the site can create and upload quizzes onto the site, which students may attempt. Student's responses and final scores are shared to the email address of the instructor who created the quiz, so that their performance can be analysed.
</p>

## What's new?

#### v1.0.0
* First release.
* Admin users may create and upload mulitple choice quizzes; upto 5 options per question
* Each quiz is assigned to a course, and is given a description and unique quiz name
* Results are sent to the email of the admin
* Students can view all quizzes on the home page and select one to attempt
* Admins can edit quiz questions and quiz details, or delete quizzes on the edit page


## Getting started

### Demo
Live demo running on <a href="www.quizz-master.herokuapp.com">www.quizz-master.herokuapp.com</a>

### Dependencies

* Python 3
* HTML 5

### Setup
Clone this repo to your local machine and cd into the new directory
```
git clone https://github.com/theakashanand/quiz-master.git
cd quiz-master
```
Create a virtual environment within the new directory and activate it
```
virtualenv venv -p python3
source venv/bin/activate
```
pip install the required python modules using:
```
pip install -r requirements.txt
```
Run the web application on your local server using
```
python application.py
```
By default the web application should be running on localhost:5000



