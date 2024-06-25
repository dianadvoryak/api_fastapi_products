from datetime import datetime

from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from shift_assignment.models import shift_assignment_model
from shift_assignment.schemas import Create_Shift_Assignment, Response_Shift_Assignment, Filter_Shift_Assignment
from sqlalchemy import insert, select, update, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/shift_assignment",
    tags=["Shift_assignment"]
)


@router.post("/create")
async def create_shift_assignment(request_shift_assignment: Create_Shift_Assignment,
                                  session: AsyncSession = Depends(get_async_session)):
    try:
        query_id = select(shift_assignment_model).where(
            or_(
                shift_assignment_model.c.NomerPartii == request_shift_assignment.NomerPartii,
                str(shift_assignment_model.c.DataPartii) == str(request_shift_assignment.DataPartii)
            ))
        id_shift_assignment = await session.execute(query_id)
        if id_shift_assignment:
            update = await update_shift_assignment(id_shift_assignment.mappings().first()["id"], request_shift_assignment, session)
            return update

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

@router.post("/create")
async def create_shift_assignment(filter: Filter_Shift_Assignment, offset, limit,
                                  session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(shift_assignment_model)

        add_filters = []
        if filter.StatusZakrytiya:
            add_filters.append(shift_assignment_model.StatusZakrytiya == filter.StatusZakrytiya)
        if filter.PredstavlenieZadaniyaNaSmenu:
            add_filters.append(shift_assignment_model.batch_number == filter.PredstavlenieZadaniyaNaSmenu)
        if filter.Liniya:
            add_filters.append(shift_assignment_model.batch_date == filter.batch_date)
        if filter.Smena:
            add_filters.append(shift_assignment_model.Smena == filter.Smena)
        if filter.Brigada:
            add_filters.append(shift_assignment_model.Brigada == filter.Brigada)
        if filter.NomerPartii:
            add_filters.append(shift_assignment_model.NomerPartii == filter.NomerPartii)
        if filter.DataPartii:
            add_filters.append(shift_assignment_model.DataPartii == filter.DataPartii)
        if filter.Nomenklatura:
            add_filters.append(shift_assignment_model.Nomenklatura == filter.Nomenklatura)
        if filter.KodEKN:
            add_filters.append(shift_assignment_model.KodEKN == filter.KodEKN)
        if filter.IdentifikatorRC:
            add_filters.append(shift_assignment_model.IdentifikatorRC == filter.IdentifikatorRC)
        if filter.DataVremyaNachalaSmeny:
            add_filters.append(shift_assignment_model.DataVremyaNachalaSmeny == filter.DataVremyaNachalaSmeny)
        if filter.DataVremyaOkonchaniyaSmeny:
            add_filters.append(shift_assignment_model.DataVremyaOkonchaniyaSmeny == filter.DataVremyaOkonchaniyaSmeny)


        if add_filters:
            query = query.where(and_(*add_filters))

        query = query.offset(offset).limit(limit)
        filter_query = await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": filter_query.mappings().all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=404, detail={
            "status": "not found",
            "data": None,
            "details": None
        })

