from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    barcode: str
    product_name: Optional[str]
    packaging: Optional[str]
    packaging_materials: Optional[str]
    waste_disposal_instructions: Optional[str]
