# Urban-Fix WebGIS: Nairobi Pothole & Infrastructure Management System

A Geospatial web application designed to streamline the reporting and tracking of road infrastructure issues (potholes and streetlights) within Nairobi's sub-counties. This project serves as a Final Year Project (FYP) for Geospatial Engineering.



## 🚀 Core Features
* **Interactive Reporting:** Users can report infrastructure issues with precise geographic coordinates.
* **Automated Spatial Joins:** Every report is automatically assigned to a Nairobi Sub-county using PostGIS spatial intersection logic.
* **Administrative Dashboard:** Heatmap-style insights into which sub-counties require the most attention.
* **Secure Infrastructure:** Managed via environment variables and Git-versioning.

## 🛠️ Technical Stack
* **Backend:** Django 5.x + GeoDjango
* **Database:** PostgreSQL 16 + PostGIS 3.x
* **Frontend:** Leaflet.js (Map rendering)
* **GIS Engine:** GDAL/GEOS/PROJ (via Miniconda environment)
* **Data Source:** Nairobi Sub-county boundaries (GeoJSON - ShapeName property)

## ⚙️ Local Setup

### 1. Prerequisites
* PostgreSQL with PostGIS extension installed.
* Miniconda/Anaconda with a Python 3.10+ environment.

### 2. Environment Variables
Create a `.env` file in the root directory:
```text
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432


