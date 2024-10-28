import requests
import logging

logger = logging.getLogger(__name__)

class OpenFoodFactsService:
    BASE_URL = "https://fr.openfoodfacts.org"

    @staticmethod
    def get_product_by_barcode(barcode: str) -> dict:
        url = f"{OpenFoodFactsService.BASE_URL}/api/v0/produit/{barcode}.json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Failed to get product data for barcode {barcode}.")
            return {}
