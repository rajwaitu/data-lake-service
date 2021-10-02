import database.stock_holding_db as db
from exception.apiError import APIError

def getUser(email):
    user = db.getUserByEmail(email)
    userResponse = {}
    userResponse['subscription_id'] = user.subscription_id
    userResponse['user_name'] = user.user_name
    userResponse['email'] = user.email
    userResponse['user_password'] = user.user_password
    userResponse['activation_date'] = user.activation_date
    userResponse['expiry_date'] = user.expiry_date
    userResponse['subscription_plan'] = user.subscription.name
    return userResponse

def getUserPortfolioById(id):
    user_portfolio = db.getUserPortfolioById(id)
    user_portfolio_response = {}
    user_portfolio_response['id']  = user_portfolio.id
    user_portfolio_response['portfolioName']  = user_portfolio.portfolioName
    return user_portfolio_response

def getUserPortfolio(email):
    try:
      user = db.getUserByEmail(email)
      user_portfolio = db.getUserPortfolioByUser(user.subscription_id)
      user_portfolio_response = {}

      for x in user_portfolio:
          if x.portfolioType.name in user_portfolio_response.keys():
             user_portfolio_response[x.portfolioType.name].append({'portfolio':x.portfolioName,'id':x.id})
          else:
             user_portfolio_response[x.portfolioType.name] = [{'portfolio':x.portfolioName,'id':x.id}]

      return user_portfolio_response
    except APIError as err:
      raise APIError(statusCode = err.statusCode, message = err.message )