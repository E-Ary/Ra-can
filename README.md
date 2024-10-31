# Ra'Can : Waste Disposal Assistant API

An API built with FastAPI that determines proper waste disposal methods based on product barcodes. It integrates with the French version of the OpenFoodFacts API to fetch product information and provides guidance on how to dispose of the packaging correctly.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

## Features

- Scan product barcodes to retrieve product information.
- Determine proper waste disposal instructions for packaging.
- Integrate with the French OpenFoodFacts API.
- Automatically generated interactive API documentation with Swagger UI and ReDoc.
- Structured logging for easier debugging and monitoring.

## Architecture

The project follows a modular architecture with a clear separation of concerns:

- **app/main.py**: Entry point of the application.
- **Routers**: Define API endpoints.
- **Services**: Handle business logic and external API interactions.
- **Models**: Define data models using Pydantic.
- **Utils**: Utility functions and helpers.

## Prerequisites

- **Python 3.8+** installed on your machine.
- **Git** for version control.
- **Virtualenv** for managing dependencies.

## Installation

1. **Clone the repository**

   ```bash
   git clone git@github.com:E-Ary/Ra-can.git
   cd Ra-can
   ```

2. **Create a virtual environment**

# For Windows

python -m venv venv
venv\Scripts\activate

# For macOS/Linux

python3 -m venv venv
source venv/bin/activate

3. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**

   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the API documentation**

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

3. **Test the API**

Use the interactive documentation to test the API endpoints.

## API Endpoints

- GET /
  - Description: Root endpoint for testing.
  - Response:

```json
{
  "message": "Welcome to the Waste Disposal Assistant API"
}
```

- GET /scan/{barcode}
  - Description: Retrieve product information and waste disposal instructions by barcode.
  - Parameters:
    - `barcode` (str): The barcode number of the product.
  - Response:

```json
{
  "barcode": "3155251205296",
  "product_name": "Tartine Doux",
  "packaging_details": [
    {
      "packaging": "L'opercule métal",
      "unit_count": 1,
      "recycling_instructions": "recyclable dans toute la France"
    },
    {
      "packaging": "La barquette et le couvercle",
      "unit_count": 1,
      "recycling_instructions": "recyclables selon votre commune"
    }
  ],
  "packaging_image_url": "https://images.openfoodfacts.org/images/products/315/525/120/5296/packaging_fr.176.400.jpg"
}
```

- Error Responses:
  - 404 Not Found: Product not found.

**Project Structure**

```md
backend/
├── app/
│ ├── main.py
│ ├── routers/
│ │ ├── **init**.py
│ │ └── scan.py
│ ├── services/
│ │ ├── **init**.py
│ │ └── openfoodfacts_service.py
│ ├── models/
│ │ ├── **init**.py
│ │ └── product.py
│ └── utils/
│ ├── **init**.py
│ └── helpers.py
├── requirements.txt
├── .gitignore
└── README.md
```

**Technologies Used**

- Python 3.13+
- FastAPI: A modern, fast web framework for building APIs with Python 3.6+ based on standard Python type hints.
- Uvicorn: A lightning-fast ASGI server implementation, using uvloop and httptools.
- Requests: A simple HTTP library for Python.
- Pydantic: Data validation and settings management using Python type annotations.
