# holdingService.py
import traceback
import database.stock_holding_db as db
from exception.apiError import APIError

def getHolding(email,portfolioId):
    try:
      user = db.getUserByEmail(email)
      user_portfolio = db.getUserPortfolioById(int(portfolioId))
      holdingList = db.getHoldingByUserAndUserPortfolio(user.subscription_id,user_portfolio.id)
      return {'holdingList' : holdingList}
    except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while loading user holdings' )

def updateHolding(email,portfolioId,holdingListObj):
  try:
      db.getUserByEmail(email)
      db.getUserPortfolioById(int(portfolioId))
      ltpDict = {}
      maximaDict = {}
      depthDict = {}
      quantityDict = {}
      avgpriceDict = {}

      for holdingDict in holdingListObj.holdingList:
          id = int(holdingDict['id'])

          if "ltp" in holdingDict:
            ltpDict[id] = float(holdingDict['ltp'])

          if "maxima" in holdingDict:
            maximaDict[id] = float(holdingDict['maxima'])

          if "depth" in holdingDict:
            depthDict[id] = float(holdingDict['depth'])

          if "quantity" in holdingDict:
            quantityDict[id] = int(holdingDict['quantity'])

          if "avgprice" in holdingDict:
            avgpriceDict[id] = float(holdingDict['avgprice'])
        
      if ltpDict:
        db.updateHoldingLTP(ltpDict)
      
      if maximaDict:
        db.updateHoldingMaxima(maximaDict)

      if depthDict:
        db.updateHoldingDepth(depthDict)

      if quantityDict:
        db.updateHoldingQuantity(quantityDict)

      if avgpriceDict:
        db.updateHoldingAvgprice(avgpriceDict)
        
      return {'status' : 200}
        
  except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while creating/updating user holdings' )

def createHolding(email,portfolioId,holdingListObj):
  try:
      user = db.getUserByEmail(email)
      db.getUserPortfolioById(int(portfolioId))
     
      for holdingDict in holdingListObj.holdingList:
        holding = db.UserHolding()
        holding.user = user.subscription_id
        holding.userPortfolio = int(portfolioId)
        holding.stockCode = str(holdingDict['scrip'])
        holding.company = str(holdingDict['company'])
        holding.holdingQuantity = int(holdingDict['quantity'])
        holding.avaragePrice = float(holdingDict['avgPrice'])
        holding.ltp = float(holdingDict['ltp'])
        db.addHolding(holding)

      return {'status' : 200}
        
  except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while creating user holdings' )

def deleteHolding(email,portfolioId,scripObj):
  try:
      user = db.getUserByEmail(email)
      db.getUserPortfolioById(int(portfolioId))

      db.deleteHolding(user.subscription_id,int(portfolioId),str(scripObj.scrip))
      return {'status' : 200}
        
  except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while creating user holdings' )



