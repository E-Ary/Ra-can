from fastapi import APIRouter, HTTPException, Path
from app.services.openfoodfacts_service import OpenFoodFactsService
from app.models.product import Product
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/scan",
    tags=["scan"]
)

def get_localized_value(value: str, preferred_languages: list = ['fr', 'en']) -> str:
    if value:
        entries = value.split(',')
        for lang in preferred_languages:
            for entry in entries:
                parts = entry.strip().split(':')
                if len(parts) == 2:
                    lang_code, text = parts
                    if lang_code == lang:
                        return text
                else:
                    return entry.strip()
    return "Inconnu"

@router.get("/{barcode}", response_model=Product)
def scan_barcode(barcode: str = Path(..., title="Product Barcode", regex="^\d{8,13}$")):
    try:
        data = OpenFoodFactsService.get_product_by_barcode(barcode)
    except Exception as e:
        logger.error(f"Error fetching data for barcode {barcode}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
    if data.get("status") == 1:
        product_data = data.get("product", {})
        packaging_text_fr = product_data.get("packaging_text_fr", "")
        packaging_info = (
            product_data.get("ecoscore_data", {})
            .get("adjustments", {})
            .get("packaging", {})
            .get("packagings", [])
        )
        logger.info(f"packing text fr: {packaging_text_fr}") # delete this line
        image_url = product_data.get("image_packaging_url")
        packaging_details = []
        for item in packaging_info:
            weight = item.get("weight_measured")
            weight_unit = item.get("weight_measured_unit")
            if weight is None:
                weight = item.get("weight_estimated")
                weight_unit = item.get("weight_estimated_unit")
            if weight is None:
                weight = 0.0
                weight_unit = "g ?"
            else:
                weight = float(weight)

            detail = {
                "type": get_localized_value(item.get("shape")),
                "material": get_localized_value(item.get("material")),
                "weight": weight,
                "weight_unit": weight_unit or "g ?",
                "unit_count": str(item.get("number_of_units", "1")),
                "recycling": get_localized_value(item.get("recycling"))
            }
            packaging_details.append(detail)
            logger.debug(f"Packaging detail: {detail}") # delete this line

        product_name = product_data.get("product_name_fr") or product_data.get("product_name")

        product = Product(
            barcode=barcode,
            product_name = product_name,
            packaging=packaging_details,
            packaging_image_url=image_url,
        )
        logger.info(f"Product found: {product.barcode} - {product.product_name}") # delete this line

        return product
    else:
        logger.warning(f"Product not found for barcode: {barcode}")
        raise HTTPException(status_code=404, detail="Product not found")