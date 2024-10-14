CREATE DATABASE IF NOT EXISTS finall;
USE finall;

-- 1. Top 5 companies by market cap in France
SELECT Company_Name, Market_Cap FROM finall.index_compositions AS c
JOIN finall.stock_market_index AS i
ON c.Index_Shortname = i.Index_Shortname
WHERE Country = "France"
ORDER BY Market_Cap DESC
LIMIT 5;

-- 2. Total Number of Employees 
SELECT i.Country, SUM(d.Num_Employees) FROM finall.index_compositions AS c
JOIN finall.stock_market_index AS i
ON c.Index_Shortname = i.Index_Shortname
JOIN finall.company_details AS d
ON c.Ticker = d.Ticker
GROUP BY i.Country;

-- 3. Top 5 companies with highest average annual return in France
SELECT c.Ticker, c.Company_Name, c.Industry, c.Avg_Annual_Return FROM index_compositions AS c
JOIN finall.stock_market_index AS i
ON c.Index_Shortname = i.Index_Shortname
WHERE Country = "France"
ORDER BY Avg_Annual_Return DESC
LIMIT 5;

-- 4. Top 5 companies with the highest total revenue in 2023 in France
SELECT f.Ticker, d.Company_Name, f.Details, f.Year, f.Value FROM financial_statements AS f
JOIN finall.company_details AS d
ON f.Ticker = d.Ticker
JOIN finall.stock_market_index AS i
ON d.Index_Shortname = i.Index_Shortname
WHERE Country = "France" AND details = "Net Income" AND Year=2023
ORDER BY f.Value DESC
LIMIT 5;

-- 5. Calculate average monthly adjusted close price of companies in main stock market index in France
SELECT p.Ticker, DATE_FORMAT(date, "%M-%Y") AS Month_Year, ROUND(AVG(Adj_Close),2) AS Avg_Monthly_Price FROM daily_stock_price as p
JOIN finall.company_details AS d
ON p.Ticker = d.Ticker
JOIN finall.stock_market_index AS i
ON d.Index_Shortname = i.Index_Shortname
WHERE Country = "France"
GROUP BY Month_Year, p.Ticker;