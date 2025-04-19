from sqlalchemy.orm import Session
from database import engine
import models as m

m.Base.metadata.drop_all(bind=engine)  # Drop all tables
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    c1=m.Category(name='еда')
    session.add(c1)
    p1= m.Product(name='Молоко', category=c1, price=100, description='Молоко 3.2%', image_path='milk.jpg')
    session.add(p1)
    p2= m.Product(name='Хлеб',category=c1, price=50, description='Хлеб ржаной', image_path='bread.jpg')
    session.add(p2)
    session.commit()