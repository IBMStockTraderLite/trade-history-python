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

from flask import Flask, request, jsonify
from modules import trade
from dbconfig import dbconfig


application = Flask(__name__)

# Flask scaffolding for the REST endpoints
# POST new trade for portfolio
@application.route('/trade-history/trade/<portfolio>', methods=['POST'])
def add_trade_wrapper(portfolio):
    #print(portfolio)
    content = request.get_json()
    print(content)
    trade_id = trade.add_trade_post(int(portfolio), content, dbconfig.get_config())
    if (trade_id is None):
        return 'Error adding trade to database', 500
    else:
       return jsonify({"tradeId": trade_id})

# GET trades for portfolio
@application.route('/trade-history/trades/<portfolio>', methods=['GET'])
def get_trades_wrapper(portfolio):

    trades = trade.trades_get(int(portfolio), dbconfig.get_config())
    if (trades is None):
        return 'Error retrieving trades from database', 500
    else:
       return jsonify(trades)

# GET portfolio totals (all time only - ytd not yet implemented)
@application.route('/trade-history/totals/<portfolio>', methods=['GET'])
def get_ytd_totals_wrapper(portfolio):
    #year  = request.args.get('year')
    #if year is None:
       #totals = trade.ytd_totals_get(int(portfolio), dbconfig.get_config())
    #else:
       #totals = trade.ytd_totals_get(int(portfolio), dbconfig.get_config(), int(year))
    totals = trade.ytd_totals_get(int(portfolio), dbconfig.get_config())
    if (totals is None):
        return 'Error retrieving totals from database', 500
    else:
       return jsonify(totals)

# GET K8s readiness probe
@application.route('/trade-history/readiness', methods=['GET'])
def readiness_wrapper():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    application.run(host= '0.0.0.0',debug=False)
