from flask_restx import Namespace

__all__ = ['ns']

ns = Namespace(
    'reviews', description='from DealerRater.com McKaig Chevrolet Buick', 
    # INFO: this enables a button for authentication in the swagger documentation
    # authorization config
    # authorizations={
    #     'apikey': {
    #         'type': 'apiKey',
    #         'in': 'header',
    #         'name': 'Authorization',
    #         'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    #     },
    # }
    )