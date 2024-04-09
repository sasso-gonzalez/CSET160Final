from flask import Flask, render_template, request  # imported flask
from sqlalchemy import create_engine, text

c_str = "mysql://root:S9e3r2e0n0a3!@localhost/canvas2"
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


# TRYING TO GET THE MANAGETESTS.HTML TO WORK
@app.route('/management', methods=['GET'])
def manageForm():
    return render_template('managetests.html')
# @app.route('/management', methods=['POST'])
# def manageForm():
#     edit = request.form("username")
#     if edit == ""
#
#     return redirect()


# @app.route('/management', methods=['POST'])
# def getman():
#
#     return render_template('managetests.html')


if __name__ == '__main__':
    app.run(debug=True)
