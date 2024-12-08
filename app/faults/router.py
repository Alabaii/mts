from fastapi import APIRouter, HTTPException, Query,status


from app.faults.dao import FaultsDAO
from app.faults.schemas import DictValidation, FaultCreate, SFaults

router = APIRouter(
    prefix="/faults",
    tags=["Ошибки"],
)
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

@router.post("/validate-dict")
async def validate_string(value: DictValidation):
    # Проверяем, что переданное значение - строка
    
    
    return {"message": f"Valid dict received: {value}"}

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

@router.get("/{id}", summary="Get fault by id") 
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

