from flask import Flask, render_template
import models
from database import engine
from routers.auth import auth_blueprint
from routers.todos import todos_blueprint

app = Flask(__name__)

models.Base.metadata.create_all(bind=engine)

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(todos_blueprint, url_prefix='/todos')

@app.route('/')
def hello_world():
    return render_template('welcome.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('welcome.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
