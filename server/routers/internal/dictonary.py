from typing import Optional, List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from ...models.internal import Pagination
from ...models.internal.dictonary import DataDict, DictRead, DictUpdate, DictItem, DataDictSearch, \
    DictItemSearch, DictItemSearchFilter
from ...common.response_code import ApiResponse, SearchResponse
from ...common.database import get_session
from ... import crud

router = APIRouter(prefix='/api')


@router.post('/dict/item/search', summary="字典列表查询", response_model=ApiResponse[SearchResponse[DictRead]])
async def search_items(search: Pagination[DictItemSearch], session: Session = Depends(get_session)):
    filter_type = DictItemSearchFilter(dict_id='eq', label='like', enable='eq', value='like')
    total = crud.internal.dict_item.search_total(session, search.search, filter_type.model_dump())
    items: List[DictRead] = crud.internal.dict_item.search(session, search, filter_type.model_dump())
    item_list = [DictRead.from_orm(item) for item in items]
    return ApiResponse(
        data={
            'total': total,
            'data': item_list
        }

    )


@router.post('/dict/item', summary="添加字典字段", response_model=ApiResponse[DictRead])
async def add_dict_item(dict_item: DictUpdate, session: Session = Depends(get_session)):
    new_item = crud.internal.dict_item.insert(session, DictItem(**dict_item.model_dump()))
    return ApiResponse(
        data=DictRead.from_orm(new_item)
    )


@router.put('/dict/item', summary="更新字典元素", response_model=ApiResponse)
async def update_dict_item(dict_item: DictUpdate, session: Session = Depends(get_session)):
    db_obj = crud.internal.dict_item.get(session, dict_item.id)
    crud.internal.dict_item.update(session, db_obj, dict_item)
    return ApiResponse()


@router.delete('/dict/item/{item_id}', summary="删除字典元素", )
async def del_dict_item(item_id: int, session: Session = Depends(get_session)):
    crud.internal.dict_item.delete(session, item_id)
    return ApiResponse()


@router.get("/dict/{dict_code}", summary="获取数据字典", response_model=ApiResponse[List[DictRead]],
            response_model_exclude={'data': {'__all__': {'desc', 'sort', 'enable'}}})
async def get_dict(dict_code: str, session: Session = Depends(get_session)):
    dict_items: List[DictItem] = crud.internal.dict_item.get_items_by_code(session, dict_code)
    if dict_items:
        return ApiResponse(
            data=[DictRead.from_orm(item) for item in dict_items]
        )
    else:
        return ApiResponse(
            code=404,
            message=f"无效的数据字典：{dict_code}"
        )


@router.delete("/dict/{dict_id}", summary="删除数据字典")
async def del_dict(dict_id: int, session: Session = Depends(get_session)):
    try:
        crud.internal.dict_item.delete_by_dict_id(session, dict_id)
        crud.internal.data_dict.delete(session, dict_id)
        return ApiResponse()
    except Exception as e:
        return ApiResponse(
            code=500,
            message=f"删除数据字典失败：{e}"
        )


@router.post("/dict", summary="新建数据字典", response_model=ApiResponse[DataDict])
async def add_dict(data_dict: DataDict, session: Session = Depends(get_session)):
    obj = crud.internal.data_dict.insert(session, data_dict)
    return ApiResponse(
        data=obj
    )


@router.put("/dict", summary="更新数据字典", response_model=ApiResponse[DataDict])
async def add_dict(data_dict: DataDict, session: Session = Depends(get_session)):
    db_obj = crud.internal.data_dict.get(session, data_dict.id)
    obj = crud.internal.data_dict.update(session, db_obj, data_dict)
    return ApiResponse(
        data=obj
    )


@router.post('/dict/search',
             summary="查询数据字典")
async def get_dicts(search: Pagination[DataDictSearch], session: Session = Depends(get_session)):
    filter_type = DataDictSearch(name='like', code='like')
    total = crud.internal.data_dict.search_total(session, search.search, filter_type.model_dump())
    dicts: List[DataDict] = crud.internal.data_dict.search(session, search, filter_type.model_dump())
    return ApiResponse(
        data={
            'total': total,
            'data': dicts
        }
    )
