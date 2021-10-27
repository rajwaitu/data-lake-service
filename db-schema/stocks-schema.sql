
create database stocks_db;

CREATE TABLE stocks_db.stock_trends_class_training (
	id int auto_increment,
    scrip varchar(20),
    start_date_range_12_mm date,
    end_date_range_12_mm date,
    start_date_range_6_mm date,
    end_date_range_6_mm date,
    label_range_12_mm tinyint,
    label_range_6_mm tinyint,
    PRIMARY KEY (id)
);

CREATE TABLE stocks_db.stocks (
	id int auto_increment,
    scrip varchar(20),
    sector varchar(20),
    trend_12_mm tinyint,
    trend_6_mm tinyint,
    price_change float,
    PRIMARY KEY (id)
);