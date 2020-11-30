from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Configure db
# db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Lopawq22!'
app.config['MYSQL_DB'] = 'instadb'


mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        username = userDetails['username']
        name = userDetails['name']
        if mysql.connection.cursor():
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO userprofile(username, name) VALUES(%s, %s)", (username, name))
            mysql.connection.commit()
            cur.close()
        else:
            print("ERROR: MYSQL connection not complete")
            exit(1)
        return redirect('/users')
    return render_template('home.html')


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM userprofile")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html', userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=False, threaded=True)
