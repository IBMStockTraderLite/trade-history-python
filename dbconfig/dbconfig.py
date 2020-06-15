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

import os

# MongoDB config values passed in via ENV vars
def get_config():

    # get section, default to postgresql
    required_keys = {'host','database','user','password','port'}
    db = {}
    if 'DB_HOST' in os.environ:
        db['host'] = os.environ['DB_HOST']
    else:
        db['host'] = 'localhost'

    if 'DB_NAME' in os.environ:
        db['database'] = os.environ['DB_NAME']
    else:
        db['database'] = 'tradedb'

    if 'DB_COLLECTION' in os.environ:
        db['collection'] = os.environ['DB_COLLECTION']
    else:
        db['collection'] = 'trades'

    if 'DB_USER' in os.environ:
        db['user'] = os.environ['DB_USER']
    else:
        db['user'] = 'trader'

    if 'DB_PASSWORD' in os.environ:
        db['password'] = os.environ['DB_PASSWORD']
    else:
        db['password'] = 'tradepw'

    if 'DB_PORT' in os.environ:
        db['port'] = os.environ['DB_PORT']
    else:
        db['port'] = '27017'

    if not all(key in db for key in required_keys):
        raise Exception('Missing db connect params in {0}'.format(db))

    return db
