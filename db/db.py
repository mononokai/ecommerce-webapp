from sqlalchemy import create_engine


engine = create_engine("mysql://david@localhost/ecommerce_webapp", echo=True)
conn = engine.connect()