from pydantic import BaseModel
from typing import Optional, List

class PackagingDetail(BaseModel):
    type: Optional[str]
    material: Optional[str]
    weight: Optional[float]
    weight_unit: Optional[str]
    unit_count: Optional[str]
    recycling: Optional[str]

class Product(BaseModel):
    barcode: str
    product_name: Optional[str]
    packaging: List[PackagingDetail]
    packaging_image_url: Optional[str]
