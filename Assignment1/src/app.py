from flask import Flask
from flask_restx import Api

from .api.newspaperNS import newspaper_ns
from .api.editorNS import editor_ns
from .api.subsribersNS import subscriber_ns

def create_app():
    paperroute_app = Flask(__name__)
    # need to extend this class for custom objects, so that they can be jsonified
    paperroute_api = Api(paperroute_app, title="PaperBack: An App for Newspaper Issue and Subscription Management")

    # add individual namespaces
    paperroute_api.add_namespace(newspaper_ns)
    paperroute_api.add_namespace(editor_ns)
    paperroute_api.add_namespace(subscriber_ns)
    return paperroute_app

if __name__ == '__main__':
    create_app().run(debug=False, port=7890)
