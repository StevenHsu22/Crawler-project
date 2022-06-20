from flask import Flask
from flask_restful import Api
from user import *
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec


app = Flask(__name__)
api = Api(app)

app.config["DEBUG"] = True
# Swagger setting
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Awesome Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


api.add_resource(Brand_volume, '/search_brand')
docs.register(Brand_volume)
api.add_resource(Corp_volume, '/search_corp')
docs.register(Corp_volume)
api.add_resource(Platform_volume, '/search_platform')
docs.register(Platform_volume)
api.add_resource(Search_Branch_volume, '/search_branch')
docs.register(Search_Branch_volume)
api.add_resource(Search_comment, '/search_comment')
docs.register(Search_comment)

if __name__ == '__main__':
    app.run()