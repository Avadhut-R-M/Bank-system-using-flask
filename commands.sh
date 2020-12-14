pip install -r requirements.txt
psql < databse_scripts/create_db_user.sql
psql flask_project < database_content
flask db upgrade
