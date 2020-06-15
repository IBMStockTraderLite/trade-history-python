#!/usr/bin/python
"""
   Copyright 2017-2019 IBM Corp All Rights Reserved

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
# Implements each REST endpoint's behavior
import pymongo
import traceback

# POST new trade
def add_trade_post(portfolio_id, new_trade, params):

    trade_id = None
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the Mongo database...')
        conn = pymongo.MongoClient(params['host'], username=params['user'], password=params['password'], authSource=params['database'], authMechanism='SCRAM-SHA-256')
        db = conn[params['database']]
        print('Connection to the Mongo database successful')

        # Get collection
        coll = db[params['collection']]

         # execute a statement
        print('Executing insert ...')
        inserted_trade = coll.insert_one(new_trade)
        print('Insert successful')

        trade_id = new_trade["trade_id"]

        # close communication with the database
        conn.close()
        conn = None
        print('Database connection closed normally.')

    except (Exception, pymongo.errors.PyMongoError) as error:
        print(error)
        print(traceback.format_exc())
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed abnormally')

    return trade_id

# GET trades for a portfolio
def trades_get(portfolio_id, params):

    query_param  = { "portfolio_id": portfolio_id }

    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the Mongo database...')
        conn = pymongo.MongoClient(params['host'], username=params['user'], password=params['password'], authSource=params['database'], authMechanism='SCRAM-SHA-256')
        db = conn[params['database']]
        print('Connection to the Mongo database successful')

        # Get collection
        coll = db[params['collection']]

         # execute a statement
        print('Executing query ...')

        docs = coll.find(query_param, { "_id": 0 })

        print('Query successful')

        trades = []
        #
        for doc in docs:
            trades.append(doc)

        # close communication with the database
        conn.close()
        conn = None
        print('Database connection closed normally.')


    except (Exception, pymongo.errors.PyMongoError) as error:
        print(error)
        print(traceback.format_exc())
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed abnormally')

    return trades

# GET YTD totals
def ytd_totals_get(portfolio_id, params):

    buy_query = [{'$match': {'$and':[{'portfolio_id': portfolio_id},{'shares': {'$gt': 0}} ] }},{ '$group': {'_id': 1, 'notional_sum': { '$sum': "$notional" },'commission_sum': { '$sum': "$commission" } }}]

    sell_query = [{'$match': {'$and':[{'portfolio_id': portfolio_id},{'shares': {'$lt': 0}} ]   }},{ '$group': {'_id': 1, 'notional_sum': { '$sum': "$notional" },'commission_sum': { '$sum': "$commission" } }}]


    totals = None
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the Mongo database...')
        #conn = pymongo.MongoClient('mongodb://%s:%s@%s:%s/%s?authSource=%s' % (username, password, params['host'], params['port'], params['database']))
        conn = pymongo.MongoClient(params['host'], username=params['user'], password=params['password'], authSource=params['database'], authMechanism='SCRAM-SHA-256')
        db = conn[params['database']]
        print('Connection to the Mongo database successful')

        # Get collection
        coll = db[params['collection']]

        totals = {}
        totals["portfolio_id"] = portfolio_id

        totals["year"] = "all"

        totals["commission"] = 0.00
        totals["buy"] = 0.00
        totals["sell"] = 0.00

        # execute a statement
        print('Executing buy query ...')

        buy_totals = list(coll.aggregate(buy_query))

        print('Buy query successful')

        if buy_totals is not None and len(buy_totals) > 0:
            totals["commission"] = buy_totals[0]['commission_sum']
            totals["buy"] = buy_totals[0]['notional_sum']
            print('Executing sell query ...')
            sell_totals = list(coll.aggregate(sell_query))
            print('Sell query successful')
            if sell_totals is not None and len(sell_totals) > 0:
                totals["commission"] += sell_totals[0]['commission_sum']
                totals["sell"] = (sell_totals[0]['notional_sum'] * -1)
        else:
            print('Portfolio empty - returning zeroes')

        # close communication with the database
        conn.close()
        conn = None
        print('Database connection closed normally.')


    except (Exception, pymongo.errors.PyMongoError) as error:
        print(error)
        print(traceback.format_exc())
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed abnormally')

    return totals
