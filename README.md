# 1. Install python 2.4
2. Install the following packages
-flask
-nltk
-json
-sys
-MySQLdb
-collections
-numpy
-lda

3. import news.sql into your mysql server
4. look for line createQuery in app.py using ctrl+f. In the line MySQLdb.connect("127.0.0.1", "root", "1234", "news", use_unicode=True, charset="utf8") change the user (root) and password (1234).
5. start the proyect using : python app.py

 
