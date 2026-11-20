from sqlalchemy import Enum as SQLEnum

def enum_column(enum_cls):
    return SQLEnum(enum_cls,
                   native_enum=False,
                   length=20,
                   values_callable=lambda e: [m.value for m in e])