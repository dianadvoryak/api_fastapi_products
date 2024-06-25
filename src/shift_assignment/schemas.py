from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class Create_Shift_Assignment(BaseModel):
    id: int
    StatusZakrytiya: bool = Field(alias='СтатусЗакрытия')
    PredstavlenieZadaniyaNaSmenu: str = Field(alias='ПредставлениеЗаданияНаСмену')
    Liniya: str = Field(alias='Линия')
    Smena: str = Field(alias='Смена')
    Brigada: str = Field(alias='Бригада')
    NomerPartii: int = Field(alias='НомерПартии')
    DataPartii: datetime = Field(alias='ДатаПартии')
    Nomenklatura: str = Field(alias='Номенклатура')
    KodEKN: str = Field(alias='КодЕКН')
    IdentifikatorRC: str = Field(alias='ИдентификаторРЦ')


class Response_Shift_Assignment(BaseModel):
    id: int
    StatusZakrytiya: bool
    PredstavlenieZadaniyaNaSmenu: str
    Liniya: str
    Smena: str
    Brigada: str
    NomerPartii: int
    DataPartii: datetime
    Nomenklatura: str
    KodEKN: str
    IdentifikatorRC: str
    DataVremyaNachalaSmeny: datetime
    DataVremyaOkonchaniyaSmeny: datetime


class Filter_Shift_Assignment(BaseModel):
    StatusZakrytiya: Optional[bool] = Query(None),
    PredstavlenieZadaniyaNaSmenu: Optional[str] = Query(None),
    Liniya: Optional[str] = Query(None),
    Smena: Optional[str] = Query(None),
    Brigada: Optional[str] = Query(None),
    NomerPartii: Optional[int] = Query(None),
    DataPartii: Optional[datetime] = Query(None),
    Nomenklatura: Optional[str] = Query(None),
    KodEKN: Optional[str] = Query(None),
    IdentifikatorRC: Optional[str] = Query(None),
    DataVremyaNachalaSmeny: Optional[datetime] = Query(None),
    DataVremyaOkonchaniyaSmeny: Optional[datetime] = Query(None),
