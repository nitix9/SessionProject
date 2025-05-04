from .base_models import *
from typing import List

#Схемы включают в себя ссылки на другие сущности для вложенного вывода
# их нужно выносиь отдельно, чтобы избежать рекурсии в импорте
class SchemaProduct(BaseProduct):
    category: BaseCategory
    shop:BaseShop

class SchemaUser(BaseUser):
    role:BaseRole
    addresses: List[BaseAddress]

class SchemaOrder(BaseOrder):
    user: BaseUser
    shop: BaseShop
    address: BaseAddress
    status: BaseOrderStatus

class SchemaShop(BaseShop):
    user:BaseUser