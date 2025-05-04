from sqlalchemy.orm import Session
from database import engine
import models as m

m.Base.metadata.drop_all(bind=engine)  # Drop all tables
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    r1=m.Role(name='customer')
    r2=m.Role(name='shop_owner')
    session.add(r2)
    session.add(r1)
    u1= m.User(name='Иван',last_name='Иванов',patronymic='Иванович',email='example@mail',password_hash='123456',role=r1,phone='123456789')
    session.add(u1)
    u2= m.User(name='Петр',last_name='Петров',patronymic='Петрович',email='example1@mail',password_hash='123456',role=r2,phone='987654321')
    session.add(u2) 
    a1= m.Address(address='г. Москва, ул. Ленина, д. 1', user=u1)
    session.add(a1)
    c1=m.Category(name='еда')
    s1= m.Shop(name='Магазин 1',user=u2)
    st1=m.OrderStatus(name='В обработке')
    session.add(st1)
    o1=m.Order(user=u1, status=st1, total_price=0.0,shop=s1,address=a1)
    session.add(o1)
    session.add(s1)
    session.add(c1)
    p1= m.Product(name='Молоко', category=c1, price=100, description='Молоко 3.2%', image_path='milk.jpg',shop=s1)
    session.add(p1)
    p2= m.Product(name='Хлеб',category=c1, price=50, description='Хлеб ржаной', image_path='bread.jpg',shop=s1)
    session.add(p2)
    session.commit()