from datetime import datetime

from pydantic import BaseModel, Field


class Create_Shift_Assignment(BaseModel):
    id: int
    StatusZakrytiya: bool = Field(alias='СтатусЗакрытия')
    PredstavlenieZadaniyaNaSmenu: str = Field(alias='ПредставлениеЗаданияНаСмену')
    Liniya: str = Field(alias='Линия')
    Smena: str = Field(alias='Смена')
    Brigada:str = Field(alias='Бригада')
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
    Brigada:str
    NomerPartii: int
    DataPartii: datetime
    Nomenklatura: str
    KodEKN: str
    IdentifikatorRC: str
    DataVremyaNachalaSmeny: datetime
    DataVremyaOkonchaniyaSmeny: datetime

