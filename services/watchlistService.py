# watchlistService.py
import database.stock_holding_db as db
from exception.apiError import APIError

def getUserWatchList(email):
    try:
      user = db.getUserByEmail(email)
      watchlist = db.getUserWatchList(user.subscription_id)
      return {'watchlist' : watchlist}  
    except Exception:
      raise APIError(statusCode = 400, message = 'error occured while loading user watchlist' )