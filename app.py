
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coursify.sqlite3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(225),  nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'





db.create_all()


# @app.route("/xyz")
# def xyz():
#     engine = db.engine
#     User.__table__.drop(engine)


@app.route('/')
def home():

    logged_in = session.get('logged_in', False)
    user_name = None

    if logged_in:
        user_name = session.get('user_name')
    
    # if logged_in:
    #     email = session.get('email')
    #     user = User.query.filter_by(email=email).first()
    #     if user:
    #         user_name = user.username

    # print(f"DEBUG: user_name: {user_name}")

    return render_template('index.html', logged_in=logged_in, user_name=user_name)


    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
       
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        
        new_user = User(username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        flash('You have successfully signed up!', 'success')
        return redirect(url_for('signup'))

    return render_template('signup.html')


@app.route('/login', methods=['POST','GET'])
def login():
        if request.method == 'POST':

            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()


            if user and user.password == password:
                session['email'] = email
                session['logged_in'] = True
                session['user_name'] = user.username

               
                return redirect(url_for('home'))
 
            error_message = 'Invalid email or password. Please try again.'
            return render_template('login.html', error_message=error_message)


        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=8000, debug=True)
