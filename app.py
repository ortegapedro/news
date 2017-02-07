#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
import re, nltk
from nltk import word_tokenize
from pymongo import MongoClient
import json
import sys
from bson import json_util
from bson.json_util import dumps
import time
import MySQLdb
import collections
import numpy as np
import lda
reload(sys)

sys.setdefaultencoding('utf-8')

app = Flask(__name__)

def quitarStopWords(tokensList):

    archivo = open('stopWords.csv', 'r')
    stopwords = archivo.readlines()
    i=0
    #archivo = open('NoticiasSinStopWords.csv', 'a')
    #print tokensList
    for stopword in stopwords:
        x1 = stopword.rstrip('\n')
        i = 0
        while i<len(tokensList):
            #print x1, "==", tokensList[i]
            if x1 == tokensList[i]:
                tokensList.remove(x1)
                i -= 1
                #print tokensList
            i+=1

    return tokensList

def limpiarPalabras(lstWords):
    lstWordsClenaed = []
    listaCaracteres = ["'", "-", "", '¿', '.', '', '', '', "«", "»", "–", "","·","’’","‘‘","’","‘"]
    listaCaracteres.sort()
    #print "limpiando palabras..."
    for word in lstWords:
        auxWord = word
        for caracter in listaCaracteres:
            if caracter in word:
                # print word
                auxWord = auxWord.replace(caracter, '')
                # print auxWord

        if auxWord != "":
            lstWordsClenaed.append(auxWord)
    # print lstWordsClenaed
    lstWordsClenaed.sort()
    strWordsClenaed = ' '.join(lstWordsClenaed)
    return strWordsClenaed

#################DATA CLEANING##########################
def cambiarAcentos(row):
    File = open('correcciones.txt', 'r')
    correcciones = File.readlines()
    File.close()

    for correccion in correcciones:
        rem=correccion.split("||")
        #print rem
        row=row.replace(rem[0], rem[1].rstrip('\n'))
        #print rem[0]," - ",rem[1]

    return row

def quitarEtiquetas(row):
    i = 0
    linea = ""
    escribir = True

    for n in row:
        if (n == '<'):
            escribir = False
        if (n == '>'):
            escribir = True
        if (escribir == True and n != '>'):
            if n != '\n' and n != '|':
                linea = linea + str(n)
            if n == '|':
                i = i + 1
            if n == '|' and i == 2:
                linea = linea + '\n'
                linea = cambiarAcentos(linea)
                print linea
                linea = ""
                i = 0
                return linea

def limpiador(row,nombre):
    linea = ""
    escribir = True
    j=0
    while (j < len(row)-1):

        n = row[j]
        # for n in row:
        if (n == '<'):
            escribir = False
        if (n == '>'):
            escribir = True
            linea = linea + " "
        if (escribir == True and n != '>' and n != '\n'):
            if n != '\n' and n != '\t' and n != '|':
                linea = linea + str(n)

            if row[j] == '|' and row[j + 1] == '|':
                # linea = linea + '\n'
                # print linea
                linea = cambiarAcentos(linea)
                linea=linea+ ',"' + nombre + '"'
                insertarNoticia(linea)

                saveFile = open('TodasLasNoticias.csv', 'a')

                #print linea
                saveFile.write(linea)
                saveFile.write('\n')
                saveFile.close()
                linea = ""

        j = j + 1

def quitarComillas(row):
    linea = ""
    j = 0
    while (j < len(row)):
        n = row[j]
        if n != '"':
            linea = linea + str(n)
        j = j + 1
    return linea

def wordCount(texto):
    tokens = word_tokenize(texto.lower())
    sinStopWordsTokens = quitarStopWords(tokens)
    #strTokens = limpiarPalabras(sinStopWordsTokens)
    strWordsCounted = contarPalabras(sinStopWordsTokens)

    return strWordsCounted

########################################################
def contarPalabras(listaSinStopWordsTocount):
    cuenta1 = collections.Counter(listaSinStopWordsTocount)
    # se pasa a tuplas
    datos = cuenta1.items()


    # for para pasar de tuplas a lista
    frecuenciaDocumento = dict()
    listCounted=[]
    diccionario="{"
    for tupla in datos:
        # print tupla[0],tupla[1]
        listCounted.append(str(tupla[0]) + " " + str(tupla[1]))
        #se crea un diccionario
        #print "++++",tupla[0]
        #diccionario+="'"+tupla[0]+"': "+str(tupla[1])+","
        #frecuenciaDocumento[tupla[0]] = tupla[1]



    return  listCounted

###################################################
def calcularNumerador(vect1,vect2):

    vector1=vect1.split(' ')
    vector2=vect2.split(' ')

    #print len(vector1),len(vector2)

    #palabras
    listaVector1=vector1[0::2]
    listaVector2=vector2[0::2]
    #frecuencias
    listaFrecuencias1 = vector1[1::2]
    listaFrecuencias2 = vector2[1::2]

    #interseccionde las palabras
    listaInterseccion=set(listaVector1)&set(listaVector2)
    #print l3

    numerador=0
    #if len(listaFrecuencias1) == len(listaFrecuencias2):
    for caracteristica in list(listaInterseccion):
        indicePalabraVector1 = listaVector1.index(caracteristica)
        indicePalabraVector2 = listaVector2.index(caracteristica)
        # print listaFrecuencias1[indicePalabraVector1],listaFrecuencias2[indicePalabraVector2]

        numerador = numerador + int(listaFrecuencias1[indicePalabraVector1]) * int(listaFrecuencias2[indicePalabraVector2])

        #else:

        #print "las listas no son del mismo tamaño",len(listaFrecuencias1), len(listaFrecuencias2)

    #doc = open("wordCountFailed.txt", 'a')
    #doc.writelines(listaFrecuencias1)
    #doc.write("\n")
    #doc.writelines(listaFrecuencias2)
    #doc.close()
    return numerador

def similitudCosine(numerador,sumA,sumB):

    norma = sumA*sumB
    if norma != 0:

        similarity = (numerador/ norma)
    else:
        similarity = 0
    return similarity

##################################################

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/filter/<query>")
def todasLasNoticias(query):

    bd = MySQLdb.connect("127.0.0.1", "root", "1234", "visualizadordenoticias", use_unicode=True, charset="utf8")

    cursor = bd.cursor()

    sql="SELECT Fecha,Titulo,Descripcion FROM newsall WHERE Fecha ='"+query+"'"
    cursor.execute(sql)
    print sql
    noticias = cursor.fetchall()
    json_projects = []

    for project in noticias:
        json_project = {
            'Fecha': str(project[0]),
            'Titulo': project[1],
            'Descripcion': project[2]
        }
        json_projects.append(json_project)

    news = json.dumps(json_projects)

    return news


@app.route("/categoria/<username>")
def noticias(username):
    bd = MySQLdb.connect("127.0.0.1", "root", "1234", "visualizadordenoticias", use_unicode=True, charset="utf8")

    cursor = bd.cursor()

    sql="SELECT Fecha,Titulo,Descripcion FROM newsall WHERE Categoria='"+username+"'"
    print sql
    cursor.execute(sql)

    noticias = cursor.fetchall()
    json_projects = []

    for project in noticias:
        json_project = {
            'Fecha': str(project[0]),
            'Titulo': project[1],
            'Descripcion': project[2]
        }
        json_projects.append(json_project)

    news = json.dumps(json_projects)

    return news

#Recibe un solo string con todas las palabras
def wordCountFromTable(listAll):

    #print listAll
    list = word_tokenize(listAll)
    #print list
    #print list
    #list.remove('')
    l1 = list[0::2]
    l2 = list[1::2]
    #print len(l2),l2

    listWordBeforeToDict=[]
    listFreqBeforeToDict=[]
    listTuple=[]
    for word,freq in zip(l1,l2):
        #print word, freq
        if word in listWordBeforeToDict:
            i=listWordBeforeToDict.index(word)

            sumFreq=listFreqBeforeToDict[i]+int(freq)
            listFreqBeforeToDict[i]=sumFreq
        else:
            listWordBeforeToDict.append(word)
            listFreqBeforeToDict.append(int(freq))



    for wordT,freqT in zip(listWordBeforeToDict,listFreqBeforeToDict):
        listTuple.append((wordT,freqT))

    listTuple.sort(key=lambda tup: tup[1])
    #crear una lista de tuplas para ordenarlas posteriormente
    json_projects = []
    #print len(listTuple),listTuple[0],listTuple[-1]
    for tuple in listTuple:
       json_project = {
           'text': tuple[0],
           'weight': tuple[1],
           'color': "blue"
       }

       json_projects.append(json_project)

    return json_projects

#CONTAR ENTIDADES##########################
def wordCountEntities(listAll):


    print listAll
    list=[]
    lista = listAll.split('||')
    for elemento in lista:
        if elemento!='':
            list.append(elemento)

    #print list
    #list.remove('')
    l1 = list[0::2]
    l2 = list[1::2]
    #print len(l2),l2
    #print l1
    #print l2
    listWordBeforeToDict=[]
    listFreqBeforeToDict=[]
    listTuple=[]
    for word,freq in zip(l1,l2):
        #print word, freq
        if word in listWordBeforeToDict:
            i=listWordBeforeToDict.index(word)

            sumFreq=listFreqBeforeToDict[i]+int(freq)
            listFreqBeforeToDict[i]=sumFreq
        else:
            listWordBeforeToDict.append(word)
            listFreqBeforeToDict.append(int(freq))



    for wordT,freqT in zip(listWordBeforeToDict,listFreqBeforeToDict):
        listTuple.append((wordT,freqT))

    listTuple.sort(key=lambda tup: tup[1])
    #crear una lista de tuplas para ordenarlas posteriormente
    json_projects = []
    #print len(listTuple),listTuple[0],listTuple[-1]
    for tuple in listTuple:
       json_project = {
           'text': tuple[0],
           'weight': tuple[1],
           'color': "blue"
       }

       json_projects.append(json_project)

    return json_projects

####################################

#obtiene los datos para la nube a partir de una categoria
@app.route("/cloud/<username>")
def cloud(username):
    bd = MySQLdb.connect("127.0.0.1", "root", "1234", "visualizadordenoticias", use_unicode=True, charset="utf8")

    cursor = bd.cursor()

    sql="SELECT WordCountTexto FROM newsall WHERE Categoria='"+username.title()+"'"
    #print sql
    cursor.execute(sql)

    WordCountTexto = cursor.fetchall()



    #formar un solo string
    list=""
    for WordCount in WordCountTexto:
        #print str(WordCount[0])

        list=list+str(WordCount[0]).encode("utf8")+" "
    #print list
    jsonWordCount=wordCountFromTable(list)
    cloud = json.dumps(jsonWordCount)
    #print cloud
    return cloud

def crearVectorCounsulta(username):
    print username.decode('utf-8')
    texto = quitarComillas(username.decode('utf-8'))
    tokens = word_tokenize(texto.lower())
    sinStopWordsTokens = quitarStopWords(tokens)

    strWordsCounted = contarPalabras(sinStopWordsTokens)
    strWordsCountedConsulta = ' '.join(strWordsCounted)

    RaizSumatoriaCuadradosConsulta = 0
    for llaveNumero in strWordsCounted:
        numero = llaveNumero.split(' ')
        RaizSumatoriaCuadradosConsulta = RaizSumatoriaCuadradosConsulta + (int(numero[1]) * int(numero[1]))

    datosVector=[strWordsCountedConsulta,RaizSumatoriaCuadradosConsulta]
    return datosVector

@app.route("/query/<username>")
def getNews(username):
    #Se convierte el query en un vector ####################################
    username=str(username).split('||')
    print len(username)
    print type(username)
    datos = {
        "categoria": username[2],
        "fechas": [username[0], username[1]]
    }

    dataBase = createQuery(datos)
    print len(dataBase), "Recuperando documentos...."
    listToGraphWords = []
    list = ""  # alamacen el string con todas las paalbras

    if username[-1]=='':
        print "Consultando solo por categoria...."
        for row in dataBase:
            print "location: ",row[9]
            listToGraphWords.append((row[0], row[5], row[6], row[9]))  # para el grafo de palabras
            list = list + str(row[7]).encode("utf8") + "||"  # para la nube de palabras

        print "Clustering..."
        jsonGraph = clustering(listToGraphWords)
        listOfIdsPerGroup = jsonGraph['listOfIdsPerGroup']

        #noticiasRecuperadas = sorted(similarityList, key=lambda tup: tup[1], reverse=True)
        listData = []

        print "Asignando numero de topico..."
        for new in listToGraphWords:
            for id in listOfIdsPerGroup:
                idNew = id[1]
                gro = id[0]
                # print "=?", type(new[0]), type(idNew)
                if int(new[0]) == int(idNew):
                    # print "=?", new[0], idNew
                    # print gro,new
                    listData.append([gro, new])
                    break
    else:

        datosVectroConsulta=crearVectorCounsulta(username[3])
        strWordsCountedConsulta=datosVectroConsulta[0]
        RaizSumatoriaCuadradosConsulta=datosVectroConsulta[1]


        similarityList=[]

        #se calcula la similitud entre los vectores obtenidos de mysql vs vectro de consulta
        for row in dataBase:
            #print "wordCountDB",row[5]
            #print "wordCountQuery",strWordsCountedConsulta
            wordCountedDB=row[5].lower()
            numerador = calcularNumerador(wordCountedDB, strWordsCountedConsulta)

            RaizSumatoriaCuadradosDataBase=float(row[6])
            similarity = similitudCosine(numerador, RaizSumatoriaCuadradosDataBase, RaizSumatoriaCuadradosConsulta)
            # print type(similarity)
            if similarity != 0:

                # similarityList.append(str(row[0])+","+str(similarity))
                print "location: ",row[9]
                similarityList.append((row[0],similarity,row[1],row[2],row[3],row[4],row[8],row[9]))
                #se crea un solo string para hacer el word count del
                #idnew_table,WordCountTexto,RaizSumatoriaCuadrados,locations divided by ||

                listToGraphWords.append((row[0],row[5],row[6]))#para el grafo de palabras
                list = list + str(row[7]).encode("utf8") + "||" #para la nube de palabras


        print "Clustering..."
        jsonGraph = clustering(listToGraphWords)
        listOfIdsPerGroup = jsonGraph['listOfIdsPerGroup']

        noticiasRecuperadas = sorted(similarityList, key=lambda tup: tup[1], reverse=True)
        listData=[]

        print "Asignando numero de topico..."
        for new in noticiasRecuperadas:
            for id in listOfIdsPerGroup:
                idNew = id[1]
                gro = id[0]
                #print "=?", type(new[0]), type(idNew)
                if int(new[0])==int(idNew):
                    #print "=?", new[0], idNew
                    #print gro,new
                    listData.append([gro,new])
                    break

                    # asignar un grupo a cada uno de los  elemtos dentro de la la lista de similitudes
                    # print listOfIdsPerGroup


    print "data to make the graph is ready"

    # print list
    jsonWordCount = wordCountEntities(list)
    print "wordCountEntities for the cloud is ready"
    # cloud = json.dumps(jsonWordCount)
    json_News = []

    # se ordena de mayor a menor similitud
    # noticiasRecuperadas = sorted(similarityList, key=lambda tup: tup[1], reverse=True)
    # print listData

    print len(listData)
    for elemento in listData:

        if elemento[1][6] != "":
            linkImagen = elemento[1][6].split()
        else:
            linkImagen = ["http://www.annexofmarion.com/Common/images/jquery/galleria/image-not-found.png"]
            # linkImagen = ["http://www.annexofmarion.com/Common/images/jquery/galleria/image-not-found.png"]
        json_project = {
            'Fecha': str(elemento[1][3]),
            'Titulo': elemento[1][4],
            'Descripcion': elemento[1][5],
            'link': str(elemento[1][2]),
            'linkImage': str(linkImagen[0]),
            'topic': str(elemento[0] + 1),
            'location': elemento[1][7].split('||')
        }
        # print elemento[0]
        json_News.append(json_project)

    listData = []

    json_Cloud_News = {
        'news': json_News,
        'cloud': jsonWordCount,
        'jsonGraph': jsonGraph
    }
    listData.append(json_Cloud_News)
    news = json.dumps(listData)
    print "noticias similares: ", len(similarityList)

    return news

def getNewsPerCategoria(data):
    listToGraphWords = data[0]
    similarityList = data[1]

    jsonGraph = clustering(listToGraphWords)
    listOfIdsPerGroup = jsonGraph['listOfIdsPerGroup']
    noticiasRecuperadas = sorted(similarityList, key=lambda tup: tup[1], reverse=True)
    listData = []

    print "Asignando numero de topico..."
    for new in noticiasRecuperadas:
        for id in listOfIdsPerGroup:
            idNew = id[1]
            gro = id[0]
            # print "=?", type(new[0]), type(idNew)
            if int(new[0]) == int(idNew):
                # print "=?", new[0], idNew
                # print gro,new
                listData.append([gro, new])
                break

                # asignar un grupo a cada uno de los  elemtos dentro de la la lista de similitudes
                # print listOfIdsPerGroup
    print "wordCount for the cloud is ready"
    print "data to make the graph is ready"

    # print list
    jsonWordCount = wordCountFromTable(list)
    # cloud = json.dumps(jsonWordCount)
    json_News = []

    # se ordena de mayor a menor similitud
    noticiasRecuperadas = sorted(similarityList, key=lambda tup: tup[1], reverse=True)
    # print listData

    print len(listData)
    for elemento in listData:

        if elemento[1][6] != "":
            linkImagen = elemento[1][6].split()
        else:
            linkImagen = ["http://www.annexofmarion.com/Common/images/jquery/galleria/image-not-found.png"]
            # linkImagen = ["http://www.annexofmarion.com/Common/images/jquery/galleria/image-not-found.png"]
        json_project = {
            'Fecha': str(elemento[1][3]),
            'Titulo': elemento[1][4],
            'Descripcion': elemento[1][5],
            'link': str(elemento[1][2]),
            'linkImage': str(linkImagen[0]),
            'topic': str(elemento[0] + 1)
        }
        # print elemento[0]
        json_News.append(json_project)

    listData = []

    json_Cloud_News = {
        'news': json_News,
        'cloud': jsonWordCount,
        'jsonGraph': jsonGraph
    }
    listData.append(json_Cloud_News)
    news = json.dumps(listData)
    print "noticias similares: ", len(similarityList)

    return news
@app.route("/today/<fecha>")
def today(fecha):
    #####################################

    bd = MySQLdb.connect("127.0.0.1", "root", "1234", "visualizadordenoticias", use_unicode=True, charset="utf8")
    cursor = bd.cursor()
    sql = "SELECT Fecha,Titulo,Descripcion,WordCountTexto FROM  newsall WHERE Fecha='"+fecha+"'"
    print sql
    cursor.execute(sql)
    noticias = cursor.fetchall()
    print "getting news from today..."
    json_projects = []
    list=""
    WordsNew=[]
    for noticia in noticias:
        json_project = {
            'Fecha': str(noticia[0]),
            'Titulo': noticia[1],
            'Descripcion': noticia[2]
        }
        WordsNew.append(noticia[3])
        json_projects.append(json_project)

    list = ' '.join(WordsNew)

        #list = list + str(noticia[3]).encode("utf8") + " "
    # print list
    jsonWordCount = wordCountFromTable(list)
    newsText = json.dumps(json_projects)
    cloud = json.dumps(jsonWordCount)


    listData=[]
    json_Cloud_News={
        'news': newsText,
        'cloud': cloud
    }
    listData.append(json_Cloud_News)
    news = json.dumps(listData)
    print "the data are ready..."
    return news

#funciones para crear el grafo de palabras
#prueba
@app.route("/grafo/palabras")
def topic():
    fileJsonWords=[]
    json_graph = {
        "nodes":[
          {"name":"Todo", "group":0},
          {"name":"Ciencia y Tecnologia", "group":1},
          {"name":"Deportes", "group":2},
          {"name":"Salud", "group":3},
          {"name":"Opinion", "group":4},
          {"name":"Politica", "group":5},
          {"name":"Cultura", "group":6},
          {"name":"Entretenimiento", "group":7},
          {"name":"Finanzas", "group":8},
          {"name":"Seguridad", "group":9},
          {"name":"Sociedad", "group":10},
          {"name":"samsung", "group":11},
          {"name":"google", "group":12},
          {"name":"galaxy", "group":13}
         ],
        "links":[
          {"source":0,"target":1,"value":1},
          {"source":0,"target":2,"value":1},
          {"source":0,"target":3,"value":1},
          {"source":0,"target":4,"value":1},
          {"source":0,"target":5,"value":1},
          {"source":0,"target":6,"value":1},
          {"source":0,"target":7,"value":1},
          {"source":0,"target":8,"value":1},
          {"source":0,"target":9,"value":1},
          {"source":0,"target":10,"value":1},
          {"source":1,"target":11,"value":1},
          {"source":1,"target":12,"value":1},
          {"source":1,"target":13,"value":1}
        ]
    }
    #fileJsonWords.append(json_graph)
    jsonGraph = json.dumps(json_graph)
    return jsonGraph

def crearDiccionario():
#crear vocabulario
   allWords=[]
   bd = MySQLdb.connect("127.0.0.1", "root", "1234", "visualizadordenoticias", use_unicode=True, charset="utf8")
   cursor = bd.cursor()
   sql = "SELECT idnew_table,WordCountTexto FROM newsCrawler WHERE Categoria='cienciaYtecnologia' and Fecha='2016-12-08'"
   #sql = "SELECT idnew_table,Titulo,WordCountTexto,Descripcion FROM  newsall"
   cursor.execute(sql)
   dataBase = cursor.fetchall()
   titulos=[]

   for setWords in dataBase:
      #print setWords[2]
      splitWordsFrequency = setWords[1].split(' ')
      wordsList = splitWordsFrequency[0::2]
      diccionario = set(allWords + wordsList)
      allWords=list(diccionario)#para crear el diccionario
      #titulos.append(setWords[1]+"||"+setWords[3])
      titulos.append(setWords[0])

   print len(allWords)

   dictionary=[]
   file = open("diccionario.csv", 'w')
   for word in allWords:
        dictionary.append(word+"\n")
   dictionary.sort()
   file.writelines(dictionary)
   print "dictionary is done"

   matriz=[]
   for doc in dataBase:
      #print "1"
      listofzeros = [0] * len(allWords)
      listWords = doc[1].split(' ')
      wordsList = listWords[0::2]
      freqList = listWords[1::2]
      for word,freq in zip(wordsList,freqList):

         i = allWords.index(word)
         listofzeros[i] = int(freq)
         #print listofzeros
      matriz.append(listofzeros)
   matrix=np.array(matriz)
   #print matrix


   datos = {
      "matriz":matrix,
      "vocabulario":allWords,
      "titulos":titulos
   }

   return datos
@app.route("/graph/words")
def getTopics(nTopics=13, n_top_words=6):

   datos=crearDiccionario()
   print "Datos completados..."
   #crear Matrix term X Doc
   X = datos["matriz"]
   #print list(X[0])
   vocab = datos["vocabulario"]
   #print (vocab)
   titles = datos["titulos"]
   #print len(titles)
   X.shape

   #(395, 4258)
   X.sum()
   #84010
   model = lda.LDA(n_topics=nTopics, n_iter=100, random_state=1)
   print model.fit(X)  # model.fit_transform(X) is also available
   topic_word = model.topic_word_  # model.components_ also works
   #n_top_words = 2
   #Nodes: ########################################################
   # creando las etiquetas de topicos
   json_words=[]
   json_links = []
   json_word = {
       'name': "All",
       'group': 0
   }
   json_words.append(json_word)
   n=1
   #creando ligas para el nodo principal
   while n < nTopics+1:
       json_link={
           'source': 0,
           'target': n,
           'value': 1
       }
       json_links.append(json_link)
       n=n+1


   t = 1
   while t < nTopics + 1:
       json_word = {
           'name': "Topic " + str(t),
           'group': t
       }
       json_words.append(json_word)
       t = t + 1
   #Creando ligas para los topicos
   for i, topic_dist in enumerate(topic_word):

      topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
      #esta lista contiene las palabras necesarias para el grafo
      #print topic_words
      for j, word in enumerate(topic_words):
          json_word = {
              'name': word,
              'group': t
          }
          json_words.append(json_word)


          json_link = {
              'source': i+1,
              'target': t,
              'value': 1
          }
          json_links.append(json_link)
          t = t + 1
      #print('Topic {}: {}'.format(i, ' '.join(topic_words)))


   #Links: ########################################################


   links=json.dumps(json_links)
   #file Json ########################################################
   fileJsonWords = []
   json_graph = {
       'nodes': json_words,
       'links': json_links
   }
   #fileJsonWords.append(json_graph)
   jsonGraph = json.dumps(json_graph)
   #########################################################
   print "#############################################################"

   doc_topic = model.doc_topic_
   print len(doc_topic), len(titles)
   listTopicOrdered=[]
   for text,topic in zip (titles,doc_topic):
      listTopicOrdered.append((text,topic.argmax()))

   listTopicOrdered.sort(key=lambda tup: tup[1])
   for topic in listTopicOrdered:
      print topic

   #for i in range(86):
    #  print("{} (top topic: {})".format(titles[i], doc_topic[i].argmax()))

   return jsonGraph


#Images######################################################



#endImages###################################################
#recibe una tabla con la frecuencia de las palabras
def createAStringFrecuencyWords(WordCountTexto):
    stringWordsFrecuency = ""
    for WordCount in WordCountTexto:
        stringWordsFrecuency = stringWordsFrecuency + str(WordCount[0]).encode("utf8") + " "
    return stringWordsFrecuency

def getFrecuencyWordsPerGroup(listGroups):
    list = listGroups.split(' ')
    #print list

    l1 = list[0::2]
    l2 = list[1::2]
    # print l1
    # print l2

    listWordBeforeToDict = []
    listFreqBeforeToDict = []
    listTuple = []
    for word, freq in zip(l1, l2):
        # print word, freq
        if word in listWordBeforeToDict:
            i = listWordBeforeToDict.index(word)
            sumFreq = listFreqBeforeToDict[i] + int(freq)
            listFreqBeforeToDict[i] = sumFreq
        else:
            listWordBeforeToDict.append(word)
            listFreqBeforeToDict.append(int(freq))

    for wordT, freqT in zip(listWordBeforeToDict, listFreqBeforeToDict):
        listTuple.append((wordT, freqT))

    listTuple.sort(key=lambda tup: tup[1],reverse=True)
    return listTuple

def createQuery(datos):
    bd = MySQLdb.connect("127.0.0.1", "root", "1234", "visualizadordenoticias", use_unicode=True, charset="utf8")
    cursor = bd.cursor()

    categorias=datos["categoria"]
    fechas=datos["fechas"]
    if categorias=="Hoy":
        sql = "SELECT idnew_table,Link,Fecha,Titulo,Descripcion,WordCountTexto,RaizSumatoriaCuadrados,Entities,Images,numeroDePalabras FROM  newsCrawler WHERE "
        sql += " Fecha ='" + (fechas[0]) + "'"
    else:
        if categorias == "Nacional":
            sql = "SELECT idnew_table,Link,Fecha,Titulo,Descripcion,WordCountTexto,RaizSumatoriaCuadrados,Entities,Images,numeroDePalabras FROM  newsCrawler WHERE "

        else:
            sql = "SELECT idnew_table,Link,Fecha,Titulo,Descripcion,WordCountTexto,RaizSumatoriaCuadrados,Entities,Images,Location FROM  newsCrawlerLema"
            sql+=" WHERE Categoria = '"+str(categorias)+"'"

            if len(fechas) ==2:
                 sql+=" and Fecha > '"+str(fechas[0])+"' and Fecha <'"+str(fechas[1])+"'"
            else:
                sql += " and Fecha ='" + (fechas[0]) + "'"
            sql+=' group by TituloMD5'
    #sql += " GROUP BY Titulo "
        #sql = "SELECT idnew_table,Link,Fecha,Titulo,Descripcion,WordCountTexto,RaizSumatoriaCuadrados,Entities,Images,numeroDePalabras FROM  newsCrawler"
    #sql += " WHERE Categoria = '" + str(categorias) + "' and idnew_table<32000"
    #sql += " WHERE  idnew_table < 5000"
    print sql
    cursor.execute(sql)
    listaDeTuplas = cursor.fetchall()
    return listaDeTuplas

# la tupla debe de contener 4 dimensiones:idnew_table,WordCountTexto,RaizSumatoriaCuadrados,numeroDePalabras
@app.route("/graph/clustering")
def clustering(listaDeTuplas):

    listNews=list(listaDeTuplas)
    #listNews.sort(key=lambda tup: tup[3],reverse=True)
    # creando diccionario
    dimensiones = {}
    for new in listNews:
       #se coloca el indice de la noticia y el word count texto
       dimensiones[new[0]]=new[1::]

    #print listNews
    #print dimensiones
    similarityList = []

    i=0
    #calculando similitudes entre todos los vectores,
    #ENTRADA:
    #lista de tuplas con las dimensiones: idnew_table,WordCountTexto,RaizSumatoriaCuadrados
    #SALIDA:
    #lista de tuplas con tres
    #dimensiones --> (similitud, id1 ,id2)
    while i < len(listNews):
        vecti=listNews[i][1]
        raizSumi=listNews[i][2]
        j=i+1
        grupo=1
        while j < len(listNews):
            vectj = listNews[j][1]
            raizSumj = listNews[i][2]

            numerador = calcularNumerador(vecti, vectj)
            similarity = similitudCosine(numerador, float(raizSumi), float(raizSumj))
            # print type(similarity)

            #if similarity > (1-simDif):
            #print (str(similarity),listNews[j][0],listNews[j][0])
            similarityList.append((similarity,listNews[i][0],listNews[j][0]))

            j=j+1
        i=i+1

    #esta lista guarda la similitud entre dos id's, elprimer parametro corresponde a la similitud, y los otros dos son id´s
    similarityList.sort(key=lambda tup: tup[0], reverse=True)
    #print similarityList

    #Agrupando en una lista la cual almacena los id's por grupo
    #este for realiza la grupacion de id's de acuerdo a su similitud
    lista = []
    for similarity in similarityList:
        #print similarity[0],similarity[1],similarity[2]

        key1=str(similarity[1])
        key2=str(similarity[2])

        if len(lista)==0:
            lista.append(key1 + "," + key2 + ",")
            #print lista
        else:
            k1=False
            k2=False
            i=0
            j=0
            l=0
            #print "revisando la lista para ver que elementos ya se encuentran agrupados"
            while l < len(lista):
                if key1 in lista[l]:
                    k1=True
                    i=l
                if key2 in lista[l]:
                    j=l
                    k2 = True
                #if key1 == True and key2 == True:#para romper el ciclo por si encuentra las dos keys
                 #   break
                l=l+1

            #print "agrupando los elementos encontrados"

            if k1 == True and k2 == True: #ambos elementos estan en la lista, no hagas nada
               None
               #print lista
            elif k1 == False and k2 == False: #ningun elemento esta en la lista, entonces insertalos juntos
                lista.append(key1+","+key2+",")
                #print lista
            elif k1 == True:
                lista[i] = lista[i] + key2 +","

            elif k2 == True:
                lista[j] = lista[j] + key1 +","

    #cada indice de la lista hace ferencia a un grupo
                # creando las etiquetas de topicos

    #print lista

    json_words = []
    json_links = []
    #creando nodo central
    json_word = {
        'name': "All",
        'group': 0
    }
    json_words.append(json_word)
    n = 1
    # creando ligas para el nodo central
    nTopics=len(lista)
    while n < nTopics + 1:
        json_link = {
            'source': 0,
            'target': n,
            'value': 1
        }
        json_links.append(json_link)
        n = n + 1

    #colocando la palabra topic y el numero de topic
    t = 1
    while t < nTopics + 1:
        json_word = {
            'name': "Topic " + str(t),
            'group': t
        }
        json_words.append(json_word)
        t = t + 1
    ###Colocando las palabras por topico###############################################################
    wordsPerGroup = {}
    listOfIdsPerGroup = []
    for i, conjunto in enumerate(lista):
        listGroups = []
        indices = conjunto.split(',')
        indices = indices[0:-1:]

        # print indices

        for indice in indices:
            listOfIdsPerGroup.append((i,indice))
            # print i,dimensiones[int(indice)]
            id=dimensiones[int(indice)]
            #print len(id)
            #print id[0]
            #print id[1]
            #print id[2]
            listGroups.append(str(id[0]))
        # mandar tabla con la freceuncia de las palabras
            StringFrecuencyWords= ' '.join(listGroups)
        #StringFrecuencyWords = createAStringFrecuencyWords(listGroups)
        # regrea una lista de tuplas con palabra y frecencia por topico
        FrecuencyWordsPerGroup = getFrecuencyWordsPerGroup(StringFrecuencyWords)

        wordsPerGroup[i] = FrecuencyWordsPerGroup

    #print listOfIdsPerGroup
    print "Groups: ",len(wordsPerGroup)#, wordsPerGroup
    m = 0

    while m < len(wordsPerGroup):
        # print wordsPerGroup[t]
        words = 0
        while words < 5:
            #print wordsPerGroup[m][words]

            json_word = {
                'name': wordsPerGroup[m][words][0],
                'group': t
            }
            json_words.append(json_word)

            json_link = {
                'source': m + 1,
                'target': t,
                'value': 1
            }
            json_links.append(json_link)
            words = words + 1
            t = t + 1
        m = m + 1

    # file Json ########################################################

    json_graph = {
        'nodes': json_words,
        'links': json_links,
        'listOfIdsPerGroup':listOfIdsPerGroup,
        "Groups": len(wordsPerGroup)

    }


    return json_graph

##################################################

if __name__ == "__main__":

    app.run(host='0.0.0.0',port=5000,debug=True)