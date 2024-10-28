from fastapi import APIRouter, HTTPException
from app.services.openfoodfacts_service import OpenFoodFactsService
from app.models.product import Product
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/scan",
    tags=["scan"]
)

@router.get("/{barcode}", response_model=Product)
def scan_barcode(barcode: str):
    data = OpenFoodFactsService.get_product_by_barcode(barcode)
    if data.get("status") == 1:
        product_data = data.get("product", {})
        print(product_data)
        product = Product(
            barcode=barcode,
            product_name=product_data.get("product_name"),
            packaging=product_data.get("packaging"),
            packaging_materials=product_data.get("packaging_materials"),
            waste_disposal_instructions=product_data.get("waste_disposal"),
        )
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")
