""" Main application and routing logic for TweetR """
from flask import Flask, request, render_template
from .models import DB, User, Tweet
from decouple import config
from .functions import adduser, add_or_update_user
from .predicted import predict_user


def create_app():
    """ create + config Flask app obj """
    app = Flask(__name__)

    #  after creatin models.py  run the follow
    #  configure the app object 
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')  # get db loc from .env
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        tweets = Tweet.query.all()
        return render_template('base.html', title='Home', users=users, tweets=tweets )
    
    @app.route('/testload')
    def testload():
        adduser('NBCNews')
        users = User.query.all()
        tweets = Tweet.query.all()
        return render_template('base.html', title='Home', users=users, tweets=tweets )

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None):
        message = ''
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user1, user2 = request.values['user1'], request.values['user2']
        if user1 == user2:
            return 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2,
                                      request.values['tweet_text'])
            return user1 if prediction else user2


    @app.route('/reload')
    def reload():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB has been RESET', users=[], tweets=[])

    return app

       
#  to run from terminal : set FLASK_APP=TWpred:APP
#                   +     flask run   OR    flask shell

 