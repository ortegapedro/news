# 1. install project 
1. Open database file and execute sql statements in order to create the data base.
2. import file data.sql into data base. 
3. Install python 2.7
4. Install the following python packages
-flask
-nltk
-json
-sys
-MySQLdb
-collections
-numpy
-lda
-scipy
-time
-feedparser
-hashlib

5. look for line createQuery in app.py using ctrl+f. In the line MySQLdb.connect("127.0.0.1", "root", "1234", "news", use_unicode=True, charset="utf8") change the user (root) and password (1234).
6. start the proyect using : python app.py
7. open your browser and write localhost:5000

Note:
extractor.py is the crowler which reads the ligasRSS.txt file in order to insert data visualizadordenoticias database.

 
