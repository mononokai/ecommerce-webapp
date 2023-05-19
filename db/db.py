from sqlalchemy import create_engine


engine = create_engine("mysql+mysqldb://david@localhost/ecommerce_webapp", echo=True, isolation_level="READ UNCOMMITTED")
conn = engine.connect()