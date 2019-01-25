package models;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;

public class Stocks
{
	private String stockTicker;
	private String stockName;
	private String stockDescription;
	private String stockPriceData;
	private String stockFinancialData;
	private String stockNewsData;
	private String stockIndustryData;
	
	public Stocks(String ticker, String name, String description,
			String pricedata, String financedata, String newsdata,
			String industrydata)
	{
		this.stockTicker = ticker;
		this.stockName = name;
		this.stockDescription = description;
		this.stockPriceData = pricedata;
		this.stockFinancialData = financedata;
		this.stockNewsData = newsdata;
		this.stockIndustryData = industrydata;
		try {
			saveStock();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public void saveStock() throws FileNotFoundException
	{ 
		String stockFilePath = this.stockTicker + ".csv";
		
		// Create file object for file placed at
		// stockFilePath
		FileOutputStream stockFile = new FileOutputStream(stockFilePath);
		PrintWriter pw = new PrintWriter(stockFile);
		
		// Start writing to file
		System.out.println(stockFilePath);
		pw.println(this.stockTicker + "," + this.stockName
				+ ", " + this.stockDescription + ","
				+ " Closing Price, Volume, EPS, P/E Ratio,"
				+ " News Articles, Total Revenue, Net Income,"
				+ " Total Assets, Total Liabilities, Cash,"
				+ " Net Change in Cash, Earnings Forecast");
		
		pw.println(" , , , "+this.stockPriceData
				+ ", "+"Vol, EPS, P/E, "+this.stockNewsData +", "
				+ this.stockFinancialData+", " + "Income, Assets,"
				+ "Liabilities, Cash, Change, Forecast");
		
		pw.close();
		
		System.out.println(this.stockTicker + ".csv has been written.");
	}

	public String getStockTicker() 
	{
		return stockTicker;
	}

	public void setStockTicker(String stockTicker) 
	{
		this.stockTicker = stockTicker;
	}

	public String getStockName() {
		return stockName;
	}

	public void setStockName(String stockName) 
	{
		this.stockName = stockName;
	}

	public String getStockDescription() 
	{
		return stockDescription;
	}

	public void setStockDescription(String stockDescription) 
	{
		this.stockDescription = stockDescription;
	}

	public String getStockPriceData() 
	{
		return stockPriceData;
	}

	public void setStockPriceData(String stockPriceData) 
	{
		this.stockPriceData = stockPriceData;
	}
	
	public void updateStockPriceData(String stockPriceData) 
	{
		this.stockPriceData += stockPriceData;
	}

	public String getStockFinancialData() 
	{
		return stockFinancialData;
	}

	public void setStockFinancialData(String stockFinancialData) 
	{
		this.stockFinancialData = stockFinancialData;
	}
	
	public void updateStockFinancialData(String stockFinancialData) 
	{
		this.stockFinancialData += stockFinancialData;
	}

	public String getStockNewsData() 
	{
		return stockNewsData;
	}

	public void setStockNewsData(String stockNewsData) 
	{
		this.stockNewsData = stockNewsData;
	}
	
	public void updateStockNewsData(String stockNewsData) 
	{
		this.stockNewsData += stockNewsData;
	}
	
	public String getStockIndustryData() 
	{
		return stockIndustryData;
	}

	public void setStockIndustryData(String stockIndustryData) 
	{
		this.stockIndustryData = stockIndustryData;
	}
}