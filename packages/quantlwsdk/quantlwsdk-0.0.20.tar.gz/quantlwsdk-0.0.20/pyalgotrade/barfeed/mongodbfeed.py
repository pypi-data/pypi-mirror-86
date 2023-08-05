# PyAlgoTrade
#
# Copyright 2011-2018 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
lw李文根据sqlitfeed来设计的
"""

from pyalgotrade.barfeed import dbfeed
from pyalgotrade.barfeed import membf
from pyalgotrade import bar
from pyalgotrade.utils import dt

import pymongo
from pyalgotrade.const import FRE_STATUS
import pandas as pd
from rqalpha.const import COMMISSION_TYPE, INSTRUMENT_TYPE
from rqalpha.data.instrument_mixin import InstrumentMixin
from rqalpha.data.base_data_source.storages import InstrumentStore
import os

def normalize_instrument(instrument):
    return instrument.upper()


# mongod DB.
# Timestamps are stored in UTC.
class mongoDatabase(dbfeed.Database):
    def __init__(self, host='localhost',dbName='indicatorModleDb'):
        # self.__instrumentIds = {}
        #
        # # If the file doesn't exist, we'll create it and initialize it.
        # initialize = False
        # if not os.path.exists(dbFilePath):
        #     initialize = True
        # self.__connection = sqlite3.connect(dbFilePath)
        # self.__connection.isolation_level = None  # To do auto-commit
        # if initialize:
        #     self.createSchema()

        client = pymongo.MongoClient(host=host, port=27017, tz_aware=True)
        self.db = client[dbName]

        instrPath = os.path.abspath(os.path.join(__file__, "../../../..", 'data4Rqalpha\instruments.pk'))
        instrStore = InstrumentStore(instrPath, None)
        self.instrusObj = InstrumentMixin(instrStore.get_all_instruments())


    def __findInstrumentId(self, instrument):
        cursor = self.__connection.cursor()
        sql = "select instrument_id from instrument where name = ?"
        cursor.execute(sql, [instrument])
        ret = cursor.fetchone()
        if ret is not None:
            ret = ret[0]
        cursor.close()
        return ret

    def __addInstrument(self, instrument):
        ret = self.__connection.execute("insert into instrument (name) values (?)", [instrument])
        return ret.lastrowid

    def __getOrCreateInstrument(self, instrument):
        # Try to get the instrument id from the cache.
        ret = self.__instrumentIds.get(instrument, None)
        if ret is not None:
            return ret
        # If its not cached, get it from the db.
        ret = self.__findInstrumentId(instrument)
        # If its not in the db, add it.
        if ret is None:
            ret = self.__addInstrument(instrument)
        # Cache the id.
        self.__instrumentIds[instrument] = ret
        return ret

    def createSchema(self):
        self.__connection.execute(
            "create table instrument ("
            "instrument_id integer primary key autoincrement"
            ", name text unique not null)")

        self.__connection.execute(
            "create table bar ("
            "instrument_id integer references instrument (instrument_id)"
            ", frequency integer not null"
            ", timestamp integer not null"
            ", open real not null"
            ", high real not null"
            ", low real not null"
            ", close real not null"
            ", volume real not null"
            ", adj_close real"
            ", primary key (instrument_id, frequency, timestamp))")
    def getPrice(self,order_book_ids, start_datetime, end_datetime, frequency='1d', fields=None, adjust_type='pre',
                  skip_suspended=False):
        #frequency = '1d' ，则start_datetime必须是datetime.date类型
        # frequency = '1m' ，则end_datetime必须是datetime.datetime类型
#fields类似掘金中字符串list，必须是list，每个元素是str



        #准备fields 成dict，这样在pymongo中查询指定字段用

        fieldsDict={}
        fieldsDict['_id']=0
        for afield in fields:
            fieldsDict[afield]=1



        for asymbl in order_book_ids:
            #
            # if self.instrusObj.instruments(asymbl).type == INSTRUMENT_TYPE.FUTURE:
            #     fileName = 'futures'
            # if self.instrusObj.instruments(asymbl).type == INSTRUMENT_TYPE.CS:
            #     fileName = 'stocks'
            fileName=self.getTableNamePrefix(asymbl)
            hqcollection = self.db[fileName + '_' + frequency]

            if frequency == FRE_STATUS.ONE_DAY.value:
                start_datetime=start_datetime.strftime("%Y-%m-%d")
                end_datetime=end_datetime.strftime("%Y-%m-%d")

                cursor = hqcollection.find({'symbol':asymbl,'eob':{'$gte': start_datetime,'$lte':end_datetime}},fieldsDict)
                df = pd.DataFrame(list(cursor))
                df['eob']=pd.to_datetime(df['eob'])

            return df

    def getBars(self, instrument, frequency, timezone=None, fromDateTime=None, toDateTime=None,\
                fields=['symbol','open','high','low','close','eob','volume']):

        dfhq=self.getPrice(instrument, fromDateTime, toDateTime, frequency=frequency, fields=fields)
        ss = dfhq.to_dict(orient='records')
        ret = []
        for adict in ss:

            adict['frequency']=frequency
            # if timezone:
            #     dateTime = dt.localize(dateTime, timezone)
            ret.append(bar.BasicBar(adict))

        return ret

    # 这个函数作用。比如 表 futures_1d这个名字，这个就是根据asymbol 得到futures这个字符串
    def getTableNamePrefix(self, asymbl):

        if self.instrusObj.instruments(asymbl).type == INSTRUMENT_TYPE.FUTURE:
            fileName = 'futures'
        if self.instrusObj.instruments(asymbl).type == INSTRUMENT_TYPE.CS:
            fileName = 'stocks'

        return fileName
    def disconnect(self):
        self.__connection.close()
        self.__connection = None


class Feed(membf.BarFeed):
    def __init__(self, dbFilePath, frequency, maxLen=None):
        super(Feed, self).__init__(frequency, maxLen)

        self.__db = Database(dbFilePath)

    def barsHaveAdjClose(self):
        return True

    def getDatabase(self):
        return self.__db

    def loadBars(self, instrument, timezone=None, fromDateTime=None, toDateTime=None):
        bars = self.__db.getBars(instrument, self.getFrequency(), timezone, fromDateTime, toDateTime)
        self.addBarsFromSequence(instrument, bars)
