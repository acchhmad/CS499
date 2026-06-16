CS-499 Milestone Two Enhanced Artifact README
Author: Ahmad Mansour

Artifact
This enhanced artifact is based on the CS-340 7-2 Project Two Grazioso Salvare dashboard. The application uses Python, MongoDB, Dash, Plotly, and dash_leaflet to display Austin Animal Center animal outcome data and filter dogs by rescue-type suitability.

Enhancements Completed
1. Refactored the AnimalShelter CRUD class for stronger software design, clearer configuration, and easier maintenance.
2. Added safer credential handling through environment variables while preserving the original classroom defaults.
3. Added validation for create, read, update, and delete inputs so invalid operations fail clearly instead of silently.
4. Added database connection verification, PyMongo-specific exception handling, and a close() method for resource cleanup.
5. Refactored the dashboard to centralize rescue filter queries in one dictionary and reuse helper functions for loading data and building table columns.
6. Improved dashboard reliability by handling missing logos, empty result sets, missing map fields, and invalid latitude/longitude values gracefully.

How to Run
1. Install required libraries: dash, jupyter_dash, dash_leaflet, plotly, pandas, pymongo.
2. Import the Austin Animal Center outcomes dataset into MongoDB using database aac and collection animals.
3. Set AAC_USERNAME and AAC_PASSWORD as environment variables, or use the original Codio classroom credentials.
4. Place animal_shelter.py and ProjectTwoDashboard.ipynb in the same folder.
5. Open the notebook and run all cells.

Original vs. Enhanced
The original artifact demonstrated the required dashboard functionality. The enhanced version improves maintainability, reliability, security awareness, and separation of concerns, which makes the code better aligned with professional software design and engineering practices.
