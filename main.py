# main.py

import uvicorn
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import services.userService as userservice
import services.holdingService as holdingservice
import services.investmentService as investmentservice
import services.watchlistService as watchlistService
import exception.apiError as error

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockLTP(BaseModel):
    stockLTPs: dict

class HoldingList(BaseModel):
    holdingList: list


@app.exception_handler(error.APIError)
async def unicorn_exception_handler(request: Request, exc: error.APIError):
    return JSONResponse(
        status_code=exc.statusCode,
        content={"error": exc.message},
    )

@app.get("/ping")
def ping():
    return {'status' : 'service is up and running!'}

@app.get("/subscriptions/")
def getSubscriptions():
    pass
    #return db.getSubscriptionPlan()

@app.get("/users/")
def getUsers():
    pass
    #return db.getUsers()

@app.get("/v1/api/user/email/{email}/")
def getUserByEmail(email):
    return userservice.getUser(email)

@app.get("/v1/api/user/{email}/portfolio")
def getUserPortfolio(email):
     return userservice.getUserPortfolio(email)

@app.get("/v1/api/user/portfolio/{id}")
def getUserPortfolioById(id):
     return userservice.getUserPortfolioById(id)

@app.get("/v1/api/user/{email}/portfolio/{portfolio_id}/holding")
def getUserHolding(email,portfolio_id):
    return holdingservice.getHolding(email,portfolio_id)

@app.post("/v1/api/user/{email}/portfolio/{portfolio_id}/holding")
def createUserHolding(email,portfolio_id,holdingList:HoldingList):
    return holdingservice.createOrUpdateHolding(email,portfolio_id,holdingList)

@app.get("/v1/api/user/{email}/portfolio/{portfolio_id}/investment")
def getUserInvestment(email,portfolio_id):
    return investmentservice.getInvestment(email,portfolio_id)

@app.post("/v1/api/user/{email}/portfolio/{portfolio_id}/investment")
def createUserInvestment(email,portfolio_id,stockLTP:StockLTP):
    return investmentservice.createInvestment(email,portfolio_id,stockLTP)

@app.get("/v1/api/user/{email}/watchlist")
def getUserWatchlist(email):
    return watchlistService.getUserWatchList(email)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001,reload=True)

