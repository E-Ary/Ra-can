from fastapi import APIRouter, HTTPException, Path
from app.services.openfoodfacts_service import OpenFoodFactsService
from app.models.product import Product, PackagingDetail
from typing import List
import logging
import re

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/scan",
    tags=["scan"]
)

@router.get("/{barcode}", response_model=Product)
def scan_barcode(
    barcode: str = Path(..., title="Product Barcode", regex="^\\d{8,13}$")
):
    try:
        data = OpenFoodFactsService.get_product_by_barcode(barcode)
    except Exception as e:
        logger.error(f"Error fetching data for barcode {barcode}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    if data.get("status") == 1:
        product_data = data.get("product", {})
        product_name = product_data.get("product_name_fr") or product_data.get("product_name")

        packaging_text_fr = product_data.get("packaging_text_fr", "")
        packaging_details = parse_packaging_text(packaging_text_fr)

        packaging_image_url = product_data.get("image_packaging_url")

        product = Product(
            barcode=barcode,
            product_name=product_name,
            packaging_details=packaging_details,
            packaging_image_url=packaging_image_url,
        )

        return product
    else:
        logger.warning(f"Product not found for barcode: {barcode}")
        raise HTTPException(status_code=404, detail="Product not found")

def parse_packaging_text(packaging_text: str) -> List[PackagingDetail]:
    packaging_details = []

    if not packaging_text:
        return packaging_details

    standardized_text = packaging_text.replace('\r\n', '.').replace('\n', '.')
    sentences = [sentence.strip() for sentence in standardized_text.split('.') if sentence.strip()]

    for sentence in sentences:
        quantity = 1
        packaging = ""
        recycling_instructions = "Non renseigné"

        match = re.match(r"(.+?)\s+(est|sont|doit être|doivent être)\s+(.*)", sentence, re.IGNORECASE)
        if match:
            packaging_str, _, recycling_str = match.groups()
            packaging = packaging_str.strip()
            recycling_instructions = recycling_str.strip()
        else:
            match = re.match(r"(.+?)\s+(se recycle|se recyclent|à recycler|au bac de tri)(.*)", sentence, re.IGNORECASE)
            if match:
                packaging_str, recycling_phrase, recycling_str = match.groups()
                packaging = packaging_str.strip()
                recycling_instructions = f"{recycling_phrase}{recycling_str}".strip()
            else:
                packaging = sentence.strip()
                recycling_instructions = "Non renseigné"

        packaging_detail = PackagingDetail(
            packaging=packaging or "Non renseigné",
            unit_count=quantity,
            recycling_instructions=recycling_instructions
        )
        packaging_details.append(packaging_detail)

    return packaging_details
