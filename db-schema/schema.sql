create database stock_holding_db;


CREATE TABLE stock_holding_db.subscription_plan (
    id int NOT NULL AUTO_INCREMENT,
	name varchar(20),
    PRIMARY KEY (id)
);

CREATE TABLE stock_holding_db.portfolio_class (
    code varchar(10) NOT NULL,
	name varchar(20),
    PRIMARY KEY (code)
);


CREATE TABLE stock_holding_db.users (
    subscription_id varchar(20) NOT NULL,
	user_name varchar(20),
    email varchar(20) unique,
    user_password varchar(20),
    subscription_plan int,
    activation_date datetime,
    expiry_date datetime,
    PRIMARY KEY (subscription_id),
	FOREIGN KEY (subscription_plan) REFERENCES subscription_plan(id)
);


CREATE TABLE stock_holding_db.user_portfolio (
    id int NOT NULL AUTO_INCREMENT,
	portfolio varchar(20),
    subscription_id varchar(20),
    portfolio_code varchar(10),
    PRIMARY KEY (id),
    FOREIGN KEY (subscription_id) REFERENCES users(subscription_id),
    FOREIGN KEY (portfolio_code) REFERENCES portfolio_class(code)
);


CREATE TABLE stock_holding_db.holding (
    id int NOT NULL AUTO_INCREMENT,
    subscription_id varchar(20) NOT NULL,
    portfolio int,
	company_name varchar(50),
    symbol varchar(20),
    quantity int,
    avarage_price float,
    PRIMARY KEY (id),
    FOREIGN KEY (subscription_id) REFERENCES users(subscription_id),
    FOREIGN KEY (portfolio) REFERENCES user_portfolio(id)
);


CREATE TABLE stock_holding_db.investment (
    id int NOT NULL AUTO_INCREMENT,
    subscription_id varchar(20) NOT NULL,
	portfolio int,
    holding_date date,
    investment_amount int,
    holding int,
    profit_loss int,
    PRIMARY KEY (id),
    FOREIGN KEY (subscription_id) REFERENCES users(subscription_id),
    FOREIGN KEY (portfolio) REFERENCES user_portfolio(id)
);

CREATE TABLE stock_holding_db.user_watchlist (
    id int NOT NULL AUTO_INCREMENT,
	company_code varchar(20),
    watchlist_price float,
    created date,
    user varchar(20),
    PRIMARY KEY (id),
    FOREIGN KEY (user) REFERENCES users(subscription_id)
);

insert into stock_holding_db.user_watchlist (company_code,watchlist_price,created,user)
values('IEX',600,'2021-09-17','admin'),
('RADICO',900,'2021-09-17','admin');