from datetime import datetime

from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from shift_assignment.models import shift_assignment_model
from shift_assignment.schemas import Create_Shift_Assignment, Response_Shift_Assignment
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/shift_assignment",
    tags=["Shift_assignment"]
)


# todo: Важно: пара НомерПартии и ДатаПартии всегда уникальна! Если уже существует какая-то партия с аналогичным номером партии и датой партии, мы должны ее перезаписать.
@router.post("/create")
async def create_shift_assignment(request_shift_assignment: Create_Shift_Assignment,
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

@router.get("/get/{id}")
async def get_shift_assignment(id: int, session: AsyncSession = Depends(get_async_session)):
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


@router.patch("/update/{id}")
async def update_shift_assignment(id: int, request: Response_Shift_Assignment, session: AsyncSession = Depends(get_async_session)):
    try:
        query_id = select(shift_assignment_model).where(shift_assignment_model.c.id == id)
        id_shift_assignment = await session.execute(query_id)

        if not id_shift_assignment:
            return {
                    "status": "success",
                    "data": id_shift_assignment.mappings().all(),
                    "details": None
                }

        status_zakrytiya = None
        if request.StatusZakrytiya:
            status_zakrytiya = datetime.now()
        query_update = update(shift_assignment_model).where(shift_assignment_model.c.id == id).values(
                            StatusZakrytiya=request.StatusZakrytiya,
                            closed_at=status_zakrytiya,
                            PredstavlenieZadaniyaNaSmenu=request.PredstavlenieZadaniyaNaSmenu,
                            Liniya=request.Liniya,
                            Smena=request.Smena,
                            Brigada=request.Brigada,
                            NomerPartii=request.NomerPartii,
                            DataPartii=request.DataPartii,
                            Nomenklatura=request.Nomenklatura,
                            KodEKN=request.KodEKN,
                            IdentifikatorRC=request.IdentifikatorRC,
                            DataVremyaNachalaSmeny=request.DataVremyaNachalaSmeny,
                            DataVremyaOkonchaniyaSmeny=request.DataVremyaOkonchaniyaSmeny,
                        )

        shift_assignment = await session.execute(query_update)
        await session.commit()

        return {
            "status": "success",
            "data": shift_assignment.mappings().all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=404, detail={
            "status": "not found",
            "data": None,
            "details": None
        })

