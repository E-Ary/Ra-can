from pydantic import BaseModel
from typing import Optional, List

class PackagingDetail(BaseModel):
    packaging: str
    unit_count: int
    recycling_instructions: str

class Product(BaseModel):
    barcode: str
    product_name: Optional[str]
    packaging_details: List[PackagingDetail]
    packaging_image_url: Optional[str]

