
from flask import Flask,render_template,request,jsonify,Response

from flask_bootstrap import Bootstrap5



def create_app(): 
    app=Flask(__name__,template_folder="templates")

    boostrap=Bootstrap5(app)
    

    from .routes import main
    app.register_blueprint(main)


    return app
