from .base import api, CustomAPI
from .barsky_scrapper.reviews import ns as reviews_ns

api_def = CustomAPI(api,
            title='Barsky API',
            version='0.1.0',
            description='Barsky DealerRater.com Analyzer Tool',
          )

api_def.add_namespace(reviews_ns)
