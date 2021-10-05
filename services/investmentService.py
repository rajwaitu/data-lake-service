# investmentService.py
import traceback
from datetime import date
import database.stock_holding_db as db
from exception.apiError import APIError

def getInvestment(email,portfolioId):
    try:
      user = db.getUserByEmail(email)
      user_portfolio = db.getUserPortfolioById(int(portfolioId))
      investmentList = db.getInvestmentByUserAndUserPortfolio(user.subscription_id,user_portfolio.id)
      return {'investmentList' : investmentList}
    except Exception:
      raise APIError(statusCode = 400, message = 'error occured while loading user investments' )

def createInvestment(email,portfolioId,stockLTP):
    try:
      user = db.getUserByEmail(email)
      user_portfolio = db.getUserPortfolioById(int(portfolioId))
      holdingList = db.getHoldingByUserAndUserPortfolio(user.subscription_id,user_portfolio.id)

      totalInvestment,totalHoldings,netProfit = 0,0,0
      stockLTPdict = stockLTP.stockLTPs

      for holding in holdingList:
          totalQTY = holding.holdingQuantity
          totalInvestment = totalInvestment + int(totalQTY * holding.avaragePrice)
          totalHoldings = totalHoldings + int(totalQTY * float(stockLTPdict[holding.stockCode]))

      netProfit = totalHoldings - totalInvestment

      userInvestment = db.UserInvestment()
      userInvestment.holdingDate = date.today().strftime("%Y-%m-%d")
      userInvestment.investmentAmount = totalInvestment
      userInvestment.holdingValue=totalHoldings
      userInvestment.profitLoss=netProfit
      userInvestment.user=user.subscription_id
      userInvestment.userPortfolio=user_portfolio.id
      db.createInvestment(userInvestment)

      #print('totalInvestment : ' + str(totalInvestment))
      #print('totalHoldings : ' + str(totalHoldings))
      #print('netProfit : ' + str(netProfit))

      return {'msg' : 'user investment created successfully!'}
     
    except Exception:
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while creating user investments' )