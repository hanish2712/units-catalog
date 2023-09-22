from pydantic import BaseModel
from typing import List, Optional, Union, Dict

# Unit data model - V0


class UnitConv(BaseModel):
    multiplier: float
    offset: float


class PhysQuant(BaseModel):
    externalId: Optional[str] = None
    name: str
    quantity: str
    description: Optional[str] = None
    reference: Optional[str] = None
    units: List[str] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.externalId = str(self.quantity).lower()


class PhysUnit(BaseModel):
    externalId: Optional[str] = None
    name: Optional[str] = None
    quantity: Optional[str] = None
    longName: Optional[str] = None
    aliasNames: List[str] = []
    # symbol: Optional[str] = None
    conversion: Optional[UnitConv]
    # description: Optional[str] = None
    source: Optional[str] = None
    sourceReference: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.externalId = str(self.quantity).lower() + ":" + str(self.name).lower()
