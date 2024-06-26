from datetime import datetime

from database import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from shift_assignment.models import shift_assignment_model
from products.models import products_model
from shift_assignment.schemas import Create_Shift_Assignment, Response_Shift_Assignment, Filter_Shift_Assignment
from sqlalchemy import insert, select, update, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post("/create")
async def create_shift_assignment(request_products: Create_Shift_Assignment,
                                  session: AsyncSession = Depends(get_async_session)):
    try:
        query_exist = select(shift_assignment_model).where(shift_assignment_model.c.NomerPartii == request_products.NomerPartii)
        if not query_exist:
            raise HTTPException(status_code=500, detail={
                "status": "error",
                "data": None,
                "details": None
            })

        query = (
            insert(products_model).
            values(
                UnikalnyjKodProdukta=request_products.UnikalnyjKodProdukta,
                NomerPartii=request_products.NomerPartii,
                DataPartii=request_products.DataPartii,
                is_aggregated=request_products.is_aggregated,
                aggregated_at=datetime.now(),
                assignment=request_products.assignment,
            )
        )
        products = await session.execute(query)
        await session.commit()

        return {
            "status": "success",
            "data": products.mappings().all(),
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

