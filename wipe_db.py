""""
This Script wipes all data from the four tables:
likes,follows,users and posts.
It is for making testing the database easier

-----------------------Instructions:--------------------
From the terminal (with the virtual environment enabled)
run the following command: python wipe_db.py

-------------------------------------------------------
"""

from app.models import Post,Like,User,Follow
from app import db

def db_wipe(db_table):
    """Wipes all rows from db_table"""
    rows = db_table.query.all()
    
    for row in rows:
        db.session.delete(row)
        db.session.commit()
    print('Wiping successful\n')
    
tables = [Post,Like,User,Follow]

try:
    for table in tables:
        print('Attempting to wipe table: ' + table.__tablename__)
        db_wipe(table)
    
    print('\nSuccessfully removed data from all tables')

except Exception as e:
    print(e)