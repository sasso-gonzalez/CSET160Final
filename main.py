from flask import Flask, render_template, request, redirect  # imported flask
from sqlalchemy import create_engine, text


c_str = "mysql://root:MySQL8090V11@localhost/canvas2_0"
engine = create_engine(c_str, echo=True)
connection = engine.connect()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/acc_display', methods=['GET'])
def get_users():
    user = connection.execute(text("select * from user")).all()  # .all() is just for retrieving/getting all the data
    print(user)
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
    connection.execute(text('INSERT INTO USER VALUES (:id, :name, :type, :username, :password)'), request.form)
    connection.commit()  # gives a layer of protection when someone submits a form or info to the db
    return render_template('register.html')


@app.route('/login', methods=['GET'])
def loginForm():
    return render_template('login.html')


@app.route('/management', methods=['GET'])
def get_tests():
    all_tests = connection.execute(text("select * from TESTS")).all()  # .all() is just for retrieving/getting all the data
    print(all_tests)
    return render_template('managetests.html', management=all_tests)


@app.route('/management', methods=['POST'])
def deleteForm():
    connection.execute(text('DELETE FROM TEST_FORM where TEST_ID = (:TEST_ID)'), request.form)
    connection.execute(text('DELETE FROM STU_DETAILS where TEST_ID = (:TEST_ID)'), request.form)
    connection.execute(text('UPDATE TEST_DETAILS SET TEST_ID = NULL WHERE TEST_ID = (:TEST_ID)'), request.form)
    connection.execute(text('DELETE FROM TESTS where TEST_ID = (:TEST_ID)'), request.form)
    connection.commit()  # gives a layer of protection when someone submits a form or info to the db
    return redirect('/management')


@app.route('/create', methods=['GET'])
def createForm():
    all_tests = connection.execute(text("select * from TESTS")).all()
    return render_template('create.html', management=all_tests)


# --------------------------- START OF CREATE.HTML ---------------------------








































# --------------------------- END OF CREATE.HTML ---------------------------







































if __name__ == '__main__':
    app.run(debug=True)
