from datetime import datetime

from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from shift_assignment.models import shift_assignment_model
from shift_assignment.schemas import Create_Shift_Assignment, Response_Shift_Assignment
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/shift_assignment",
    tags=["Shift_assignment"]
)


# todo: Важно: пара НомерПартии и ДатаПартии всегда уникальна! Если уже существует какая-то партия с аналогичным номером партии и датой партии, мы должны ее перезаписать.
@router.post("/create")
async def create_specific_operations(request_shift_assignment: Create_Shift_Assignment,
                                  session: AsyncSession = Depends(get_async_session)):
    try:
        status_zakrytiya = None
        if request_shift_assignment.StatusZakrytiya:
            status_zakrytiya = datetime.now()
        query = (
            insert(shift_assignment_model).
            values(
                StatusZakrytiya=request_shift_assignment.StatusZakrytiya,
                closed_at=status_zakrytiya,
                PredstavlenieZadaniyaNaSmenu=request_shift_assignment.PredstavlenieZadaniyaNaSmenu,
                Liniya=request_shift_assignment.Liniya,
                Smena=request_shift_assignment.Smena,
                Brigada=request_shift_assignment.Brigada,
                NomerPartii=request_shift_assignment.NomerPartii,
                DataPartii=request_shift_assignment.DataPartii,
                Nomenklatura=request_shift_assignment.Nomenklatura,
                KodEKN=request_shift_assignment.KodEKN,
                IdentifikatorRC=request_shift_assignment.IdentifikatorRC,
                DataVremyaNachalaSmeny=datetime.now()
            )
        )
        shift_assignment = await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": shift_assignment.mappings().all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.get("/{id}")
async def get_specific_operations(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(shift_assignment_model).where(shift_assignment_model.c.id == id)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=404, detail={
            "status": "not found",
            "data": None,
            "details": None
        })

#
# @router.post("")
# async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(operation).values(**new_operation.model_dump())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}
#
# @router.get("/main")
# async def main(session: AsyncSession = Depends(get_async_session)):
#     result = await session.execute(select(1))
#     return result.mappings().all()
