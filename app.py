from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)                                             #initialize main app
Scss(app)                                                           #initialize scss 


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datababa.db"
db = SQLAlchemy(app)                                                #initialize database


#1st database model... each db model means individual rows
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)                 # id is compulsory to locate, search,etc... & is unique to every task!
    content = db.Column(db.String(99), nullable=False)     # properties of this content column is string (of 99 length), must not be null
    complete =  db.Column(db.Integer, default=0)               # 0 means incomplete, 1 means complete
    created = db.Column(db.DateTime, default=datetime.utcnow)    # autogenerates time of creation of task

    def __repr__(self) -> str:                 # " ->str " is just to show what type the func is returning .. doesnt affect in runtime 
        return f"Task{self.id}"




@app.route('/',methods=['POST', 'GET'])
#home page-->
def index():
    # add a task
    if request.method == 'POST':
        current_task = request.form['content']      # 'content' is the name of the input field of form in html index file
        new_task = MyTask(content=current_task)      #feeds the current_task variable into the content property of the 'MyTask' object !!
#underrstand it like it when user puts smth into the form box, page refreshes -> sends data over to current_tasks (cuz its requesting from the form using request.form) --> then that data is sent over to the Mytask object into 'content' --> then db session adds the new_task to databse --> then commits !!
        try:
            db.session.add(new_task)        #adds the task into the database session
            db.session.commit()              # shyd saves it
            return redirect('/')            #this refrshes the page, saves the content into db, then redirects to Home pg !
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"

    #view the current tasks



    return render_template("index.html")




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    
    app.run(debug=True)
