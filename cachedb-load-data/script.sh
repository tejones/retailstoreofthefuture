#! /bin/bash
echo "Creating database"
python create_db.py
echo "Loading data"
python load_data.py
