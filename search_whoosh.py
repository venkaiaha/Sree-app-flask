## standard imports
import os
import sys
import json
import logging
import asyncio

## Whoosh imports
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import StemmingAnalyzer
import whoosh.index as index
from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm

## Mongodb connection
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
print('Mongo client created successfully')
db = client['sri-dev']
print('connected to sri-dev database')

## websockets
import websockets
IP = '0.0.0.0'
PORT = 5003

class MyFuzzyTerm(FuzzyTerm):
    """
    inhertef class of FuzzyTerm which is used for fuzzy searches.
    """
    def __init__(self, fieldname, text, boost=1.0, maxdist=3, \
                  prefixlength=3, constantscore=True):
         super(MyFuzzyTerm, self).__init__(fieldname, text, boost, \
                maxdist, prefixlength, constantscore)

def dict_values_to_text(d):
    """
    forms a single string by joining values in 
    a dictionary including nested fields.
    """
    body = []
    def recur(d):
        for v in d.values():
            if type(v) == dict:
                recur(v)
            elif v != "" and type(v) != bool:
                body.append(str(v))
    recur(d)
    # print(f"dict to text {d['_id']} success")
    return " ".join(body)

def create_schema():
    """
    creates schema object for search.
    """
    schema = Schema(idx=ID(stored=True),
                data=STORED,
                body=TEXT(analyzer=StemmingAnalyzer()),
                )
    print("schema creation successful")
    return schema

def create_index(schema, index_name):
    """
    creates index object for different searches.
    """
    if not os.path.exists(index_name):
        os.mkdir(index_name)
    ix = index.create_in(index_name, schema)
    print(f"index {index_name} created successfully")
    return ix

def get_data(collection):
    """
    gets data from mongodb collections.
    """
    col = db[collection]
    cursor = col.find({})
    data = list(cursor)
    print(f"{collection} data loaded sucessfully")
    return data

def loader(index, col):
    """
    takes collection data as input and writes 
    to different indexes.
    """
    writer = index.writer()
    feed_data = get_data(col)
    for doc in feed_data:
        idx = doc["_id"]
        data = doc
        # data = json.dumps(doc)
        # print(data)
        body = dict_values_to_text(doc)
        writer.add_document(idx=idx,data=data,body=body)
    writer.commit()
    print(f"{index} loaded successfully")

def search(ix, search_key):
    qp = QueryParser("body", schema=ix.schema, termclass=MyFuzzyTerm)
    q = qp.parse(search_key)
    try:
        with ix.searcher() as s:
            results = s.search(q)
            data = [res['data'] for res in results]
        return {"hits":len(data), "data":data, "error":None, "msg":"Success"}
    except Exception as e:
        return {"hits":None, "data":None, "error":str(e),\
                "msg":"Invalid search / unknown error"}

schema = create_schema()
ix_company = create_index(schema, 'index_company')
ix_customer = create_index(schema, 'index_customer')
loader(ix_company,'company')
loader(ix_customer,'customer')
# search(ix_company, sys.argv[1])
# search(ix_customer, sys.argv[2])

async def process_data(websocket, path):
    try:
        data = await websocket.recv()
        try:
            data = json.loads(data)
            print(f"query: {data}")
            search_key = data['args']
            c_type = data['c_type']
            if c_type == 'company':
                resp = search(ix_company,search_key)
            elif c_type == 'customer':
                resp = search(ix_customer,search_key)
            print(f"No. of hits: {resp['hits']}")
        except Exception as e:
            resp = {"msg":f"Invalid input, reason: {str(e)}"}
            print(resp)
        await websocket.send(json.dumps(resp))
    except Exception as error:
        *misc, exc_tb = sys.exc_info()
        print(" Type & error: " + str(error.__repr__() + \
                    " Reason: " + error.__doc__) + \
                    " Line No: " + str(exc_tb.tb_lineno))

start_server = websockets.serve(process_data, IP, PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
