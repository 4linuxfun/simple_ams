from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Column, Boolean, Integer


class DataDictBase(SQLModel):
    name: str = Field(max_length=50, sa_column_kwargs={'comment': '字典名称'})
    code: str = Field(max_length=100, sa_column_kwargs={'comment': '字典编号'})
    desc: Optional[str] = Field(max_length=100, sa_column_kwargs={'comment': '描述'})


class DataDict(DataDictBase, table=True):
    __tablename__ = 'data_dict'
    id: Optional[int] = Field(sa_column=Column('id', Integer, primary_key=True, autoincrement=True))
    dict_items: List["DictItem"] = Relationship(back_populates="dict")


class DictBase(SQLModel):
    name: str = Field(max_length=50, sa_column_kwargs={'comment': '名称'})
    data: str = Field(max_length=100, sa_column_kwargs={'comment': '数据值'})
    desc: Optional[str] = Field(max_length=100, sa_column_kwargs={'comment': '描述'})
    sort: Optional[int] = Field(sa_column_kwargs={'comment': '排序值，越小越靠前'})
    enable: bool = Field(default=True, sa_column=Column(Boolean, comment='是否启用'))
    dict_id: Optional[int] = Field(foreign_key="data_dict.id")


class DictItem(DictBase, table=True):
    __tablename__ = 'dict_item'

    id: Optional[int] = Field(sa_column=Column('id', Integer, primary_key=True, autoincrement=True))
    dict: Optional[DataDict] = Relationship(back_populates='dict_items')


class DictRead(DictBase):
    id: int


class DictUpdate(DictBase):
    id: Optional[int]
