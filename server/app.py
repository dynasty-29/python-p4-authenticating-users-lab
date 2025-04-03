#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class IndexArticle(Resource):
    
    def get(self):
        articles = [article.to_dict() for article in Article.query.all()]
        return articles, 200

class ShowArticle(Resource):

    def get(self, id):
        session['page_views'] = 0 if not session.get('page_views') else session.get('page_views')
        session['page_views'] += 1

        if session['page_views'] <= 3:

            article = Article.query.filter(Article.id == id).first()
            article_json = jsonify(article.to_dict())

            return make_response(article_json, 200)

        return {'message': 'Maximum pageview limit reached'}, 401
# login session
class Login(Resource):
    def post(self):
        data = request.get_json()

        if 'username' not in data:
            return {'message': 'Username is required'}, 400

        user = User.query.filter_by(username=data['username']).first()

        if not user:
            return {'message': 'User not found'}, 404

        session['user_id'] = user.id  # Correctly set session with user_id
        return user.to_dict(), 200

        
# logout session
class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {'message': 'Logged out successfully'}, 204
# check session    
class CheckSession(Resource):
    def get(self):
        # Check if 'user_id' is in session
        user_id = session.get('user_id')  

        if not user_id:
            return {'message': '401: Not Authorized'}, 401  # User is not logged in

        # Fetch user by user_id from the database
        user = User.query.get(user_id)  
        if not user:
            return {'message': '401: Not Authorized'}, 401  # If no user is found, unauthorized

        return {'user': user.to_dict()}, 200
         

api.add_resource(ClearSession, '/clear')
api.add_resource(IndexArticle, '/articles')
api.add_resource(ShowArticle, '/articles/<int:id>')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
