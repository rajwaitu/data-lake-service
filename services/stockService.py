import traceback
import database.stocks_db as stockdb
from exception.apiError import APIError

def getStock(period,trend):
    try:
      scripList = []
      stock_list = stockdb.getStocksByTrend(int(period),int(trend))
      print(stock_list)

      for x in stock_list:
          scripList.append(x.scrip)

      return {'stocks' : scripList}
    except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while fetching stocks' )