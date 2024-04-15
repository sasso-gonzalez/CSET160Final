from flask import Flask, render_template, request, redirect, flash  # imported flask
from sqlalchemy import create_engine, text

c_str = "mysql://root:MySQL@localhost/canvas2_0"
engine = create_engine(c_str, echo=True)
connection = engine.connect()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/acc_display', methods=['GET'])
def get_users():
    user = connection.execute(text("select * from user")).all()  # .all() is just for retrieving/getting all the data
    # print(user)
    return render_template('acc_display.html', acc_display=user)


@app.route('/acc_display', methods=['GET'])
def displayAcc():
    return render_template('acc_display.html')


@app.route('/acc_display', methods=['POST'])
def searchAcc():  # table
    search = connection.execute(text(f'SELECT * FROM USER WHERE type = (:type)'), request.form)
    connection.commit()
    return render_template('acc_display.html', acc_display=search)


@app.route('/register', methods=['GET'])
def regisForm():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def registered():
    connection.execute(text(f'INSERT INTO USER VALUES (:id, :name, :type, :username, :password)'), request.form)
    connection.commit()  # gives a layer of protection when someone submits a form or info to the db
    # I changed the return so that you will be directed to the login page after registering - Vee
    return render_template('login.html')


@app.route('/login', methods=['GET'])
def loginForm():
    return render_template('login.html')


@app.route('/management', methods=['GET'])
def get_tests():

    all_tests = connection.execute(text("select * from TESTS")).all()  # .all() is just for retrieving/getting all the data
    print(all_tests)
    return render_template('managetests.html', management=all_tests)


@app.route('/management', methods=['POST'])
# delete function
def deleteForm():
    connection.execute(text('DELETE FROM TEST_FORM where TEST_ID = (:TEST_ID)'), request.form)
    connection.execute(text('DELETE FROM STU_DETAILS where TEST_ID = (:TEST_ID)'), request.form)
    connection.execute(text('UPDATE TEST_DETAILS SET TEST_ID = NULL WHERE TEST_ID = (:TEST_ID)'), request.form)
    connection.execute(text('DELETE FROM TESTS where TEST_ID = (:TEST_ID)'), request.form)
    connection.commit()
    return redirect('/management')


# --------------------------- START OF CREATE.HTML ---------------------------

@app.route('/create', methods=['GET'])
def createForm():
    return render_template('create.html')

  
@app.route('/create', methods=['POST'])
def insertForm():
    connection.execute(text('INSERT INTO TESTS VALUES (:TEST_ID, :TEST_NAME, :AMT_OF_STU, :TEACH_ID)'), request.form)
    connection.commit()
    return render_template('createQuestions.html')


@app.route('/createQuestions', methods=['POST', 'GET'])
def showCreate():
    # values that are entered from the browser will show up on the SQL database
    connection.execute(text('INSERT INTO TEST_FORM (Q_ID, QUEST_NUM, QUESTION, ACT_ANSWER, TEST_ID) '
                            'VALUES (:Q_ID, :QUEST_NUM, :QUESTION, :ACT_ANSWER, :TEST_ID)'), request.form)
    connection.commit()
    return render_template('createQuestions.html')

# --------------------------- END OF CREATE.HTML ---------------------------


# --------------------------- START OF EDIT.HTML ---------------------------

@app.route('/edit/<TEST_ID>', methods=['GET'])
def get_test_edit(TEST_ID):
    test = connection.execute(text(f"SELECT TEST_ID, TEST_NAME, Q_ID, QUEST_NUM, QUESTION, ACT_ANSWER, TD_ID FROM TESTS NATURAL JOIN TEST_FORM WHERE TEST_ID = {TEST_ID};")).all()
    print(test)
    return render_template('edit.html', edit=test)


@app.route('/edit/<TEST_ID>', methods=['POST'])
def editForm(TEST_ID):
    connection.execute(text(f'UPDATE TESTS SET TEST_NAME = (:TEST_NAME) WHERE Q_ID = (:Q_ID)'), request.form)
    connection.execute(text(f'UPDATE TEST_FORM SET QUESTION = (:QUESTION), ACT_ANSWER = (:ACT_ANSWER) WHERE Q_ID = (:Q_ID)'),request.form)
    connection.commit()  # gives a layer of protection when someone submits a form or info to the db
    return render_template('/edit.html')


# --------------------------- END OF EDIT.HTML ---------------------------

# --------------------------- START OF MISCELLANEOUS ---------------------------
@app.route('/tests_taken', methods=['GET'])
def get_takentests():
    usertests = connection.execute(text("SELECT * FROM TESTS")).all()
    print(usertests)
    return render_template('tests_taken.html', tests_taken=usertests)


@app.route('/tests_taken', methods=['GET'])
def displaytakentests():
    return render_template('tests_taken.html')


@app.route('/tests_taken', methods=['POST'])
def searchtakenTests():  # table
    searchtests = connection.execute(text(f'SELECT * FROM TESTS WHERE TEACH_ID = (:TEACH_ID)'), request.form)
    print(searchtests)
    connection.commit()
    return render_template('tests_taken.html', tests_taken=searchtests)


@app.route('/STU_tests/<TEST_ID>', methods=['GET'])
def getting_taken_tests(TEST_ID):
    gettaken = connection.execute(text(f"SELECT WHO_TESTED, SET_MARKS, TEACH_ID, NAME FROM TEST_DETAILS NATURAL JOIN TEACHER NATURAL JOIN USER WHERE TEST_ID = {TEST_ID};")).all()
    print(gettaken)
    return render_template('STU_tests.html', STU_tests=gettaken)

@app.route('/part_student', methods=['GET'])
def get_student():
    PARSTU = connection.execute(text('SELECT NAME, STU_ID FROM STUDENT NATURAL JOIN USER;')).all()
    print(PARSTU)
    return render_template('part_student.html', part_student=PARSTU)


@app.route('/part_student', methods=['GET'])
def displaypartstudent():
    return render_template('part_student.html')


@app.route('/part_student', methods=['POST'])
def searchingstudent():  # table
    searchstu = connection.execute(text(f'SELECT NAME, STU_ID FROM STUDENT NATURAL JOIN USER WHERE STU_ID = (:STU_ID);'), request.form)
    print(searchstu)
    return render_template('part_student.html', part_student=searchstu)


@app.route('/STU_info/<STU_ID>', methods=['GET'])
def get_part_student(STU_ID):
    get_par_student = connection.execute(text(f"SELECT WHO_TESTED, STU_ID, TEST_ID, TEST_NAME, SET_MARKS, TD_ID FROM STU_DETAILS NATURAL JOIN TESTS NATURAL JOIN TEST_DETAILS WHERE STU_ID = {STU_ID};")).all()
    print(get_par_student)
    return render_template('STU_info.html', STU_info=get_par_student)

@app.route('/STU_info/<STU_ID>', methods=['POST', 'GET'])
def update_marks(STU_ID):
    update = connection.execute(text(f"UPDATE STU_DETAILS NATURAL JOIN TESTS NATURAL JOIN TEST_DETAILS SET SET_MARKS = (:SET_MARKS) WHERE STU_ID = {STU_ID} AND TEST_ID = (:TEST_ID)"), request.form)
    print(update)
    connection.commit()
    return redirect(f'/STU_info/{STU_ID}')

@app.route('/STU_2ND/<TD_ID>', methods=['GET'])
def student_response(TD_ID):
    student_quest = connection.execute(text(f"SELECT TD_ID, WHO_TESTED, TEST_ID, Q_ID, QUEST_NUM, QUESTION, RESPONSE FROM TEST_DETAILS NATURAL JOIN TEST_FORM WHERE TD_ID = {TD_ID};")).all()
    print(student_quest)
    return render_template('STU_2ND.html', STU_2ND=student_quest)

# --------------------------- END OF MISCELLANEOUS ---------------------------


if __name__ == '__main__':
    app.run(debug=True)
