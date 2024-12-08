import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query,status
from pydantic import UUID4
from sqlalchemy import UUID


from app.faults.dao import FaultsDAO
from app.faults.schemas import DictValidation, FaultCreate, SFaults

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/faults",
    tags=["Ошибки"],
)

@router.get("/correct-data", summary="returns the correct data")
async def get_correct_data():
    return {
    "name": "John",
    "year_birth": 1999,
    "fav_animals": ["cat", "dog", "mouse"],
  }


@router.get("/false-data", summary="returns incorrect data")
async def get_false_data():
    return {
    "name": "John",
    "year": 1999,
    "fav_animals": ["cat", "dog", "mouse"],
  }


@router.post("/validate-dict",summary="I'm expecting a dictionary here, if I substitute the type with a string there will be a type error" )
async def validate_dict(value: DictValidation):
    # Проверяем, что переданное значение - строка
    
    
    return {"message": f"Valid dict received: {value}"}

# Эндпоинт для успешного запроса (200)
@router.get("/success", summary="Guaranteed 200 OK response")
async def get_success():
    return {"message": "Everything is working fine!"}
# Эндпоинт для ошибки Bad Request (400)
@router.get("/bad-request", summary="Guaranteed 400 Bad Request response")
async def get_bad_request():
    raise HTTPException(status_code=400, detail="Bad request: missing required parameters.")

# Эндпоинт для ошибки Internal Server Error (500)
@router.get("/internal-error", summary="Guaranteed 500 Internal Server Error response")
async def get_internal_error():
    raise HTTPException(status_code=500, detail="Internal server error occurred.")



@router.get("/all", summary="Get all faults", response_model=list[SFaults])
async def get_faults(
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(10, ge=1, le=100, description="Количество записей для возврата"),
    ip: str | None = Query(None, description="Фильтр по IP"),
    code_fault: int | None = Query(None, description="Фильтр по коду ошибки"),
):
    filters = {}
    if ip:
        filters['ip'] = ip
    if code_fault is not None:
        filters['code_fault'] = code_fault

    result = await FaultsDAO.find_all(offset=offset, limit=limit, **filters)
    return result

@router.get("/find_by_id/{id}", summary="Get fault by id") 
async def get_faults_by_id(id)-> SFaults:
    result = await FaultsDAO.find_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Fault not found")
    return result





@router.post("/add", summary="Add a new fault", status_code=201)
async def add_fault(fault: FaultCreate):
    data = fault.dict()  # Преобразуем Pydantic модель в обычный dict
    try:
        result = await FaultsDAO.add(**data)
        if result:
            return {"message": "Fault added successfully", "id": result["id"]}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add fault to the database"
            )
    except HTTPException as e:
        # Поймаем ошибку, сгенерированную в DAO (например, ошибка базы данных)
        raise e
    except Exception as e:
        # Обрабатываем все другие непредвиденные ошибки
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {str(e)}"
        )
    
@router.delete("/faults/")
async def delete_fault(id: Optional[UUID4] = Query(None), 
                       ip: Optional[str] = Query(None), 
                       code_fault: Optional[int] = Query(None),
                       comment: Optional[str] = Query(None)):
    """
    Удаляет запись из таблицы faults по фильтрам, переданным через query параметры.
    Параметры:
        id: UUID — идентификатор записи (необязателен).
        ip: str — IP адрес (необязателен).
        code_fault: int — код ошибки (необязателен).
        comment: str — комментарий (необязателен).
    """
    filter_params = {}
    
    if id:
        filter_params['id'] = id
    if ip:
        filter_params['ip'] = ip
    if code_fault:
        filter_params['code_fault'] = code_fault
    if comment:
        filter_params['comment'] = comment

    # Логируем передаваемые фильтры
    logger.info(f"Attempting to delete with filters: {filter_params}")
    
    try:
        # Вызов DAO-метода для удаления
        result = await FaultsDAO.delete(**filter_params)

        if result is None:  # Если записи не найдены
            logger.error(f"No records found for filters: {filter_params}")
            raise HTTPException(status_code=404, detail="Record not found")
        
        logger.info(f"Deleted {result} record(s) with filters: {filter_params}")
        return {"status": "success", "message": f"{result} record(s) deleted successfully"}

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")