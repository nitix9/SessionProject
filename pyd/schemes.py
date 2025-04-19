from .base_models import *
from typing import List

#Схемы включают в себя ссылки на другие сущности для вложенного вывода
# их нужно выносиь отдельно, чтобы избежать рекурсии в импорте
class SchemaProduct(BaseProduct):
    category: BaseCategory