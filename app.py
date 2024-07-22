from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask(__name__)
app.secret_key = 'mrs_kazemi'
ADMIN_SECRET = 'supersecretkey'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Farshad1376@',
    'db': 'student_info',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

def validate_form(first_name, last_name, age):
    errors = []
    if  not first_name or len(first_name) < 2 or len(first_name) > 50:
        errors.append("نام شما باید بین 2 تا 50 حرف باشد")
    if not last_name or len(last_name) < 2 or len(last_name) > 50:
        errors.append("نام خانوادگی شما باید بین 2 تا 50 حرف باشد")
    try:
        age = int(age)
        if age < 1 or age > 80:
            errors.append("سن شما باید بین 1 تا 80 باشد")
    except ValueError:
        errors.append("سن شما باید یک عدد معتبر باشد")
    return errors                            

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        semester = request.form.get('semester')
        age = request.form['age']

        errors = validate_form(first_name, last_name, age)

        if not errors:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    sql = """INSERT INTO students (first_name, last_name, semester, age) 
                             VALUES (%s, %s, %s, %s)"""
                    cursor.execute(sql, (first_name, last_name, semester, int(age)))
                conn.commit()
            except Exception as e:
                flash(f'An error occurred: {str(e)}', 'error')
            finally:
                conn.close()
        else:
            for error in errors:
                flash(error, 'error')

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        pass_word = request.form['password']
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """SELECT username, password FROM login_info"""
                cursor.execute(sql)
                result = cursor.fetchone()
                username = result['username']
                password = result['password']
                if user_name == username and pass_word == password:
                    return redirect(url_for('kazemi_admin_panel_only_admin'))
                else:
                    flash('invalid', 'error')
        finally:
            conn.close()        

    return render_template('login.html')

@app.route('/kazemi_admin_panel_only_admin')
def kazemi_admin_panel_only_admin():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """SELECT first_name, last_name, semester, age FROM students"""
            cursor.execute(sql)
            students = cursor.fetchall()
        conn.close()
        return render_template('admin.html', students=students) 
    except pymysql.Error as err:
        return f"Error: {err}"   

if __name__ == '__main__':
    app.run(debug=True)