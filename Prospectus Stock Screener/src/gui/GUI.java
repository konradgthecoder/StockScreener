package gui;

import java.awt.BorderLayout;
import java.util.List;

import javax.swing.JFrame;
import javax.swing.JLabel;

import models.CSVReaderStocks;
import models.Stocks;

public class GUI 
{
	public static void main(String[] args)
	{
//		Main JFrame
		JFrame window = new JFrame("Prospectus Screener");
		window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		window.setSize(800, 600);
//		Main Label
		JLabel label = new JLabel("Testing");
		
//		Add label
		window.getContentPane().add(label, BorderLayout.CENTER);
		
		window.setVisible(true);
		
//		Add buttons
		
//		Add list

//		Test Stock csv
		
		Stocks stock = new Stocks("ACB", "Aurora Cannabis", "Cannabis Company",
				null, null, null, null);
		
		List<String> stockTickers = CSVReaderStocks.readStocksFromCSV("sptsx_joined_closes.csv");
		System.out.println(stockTickers);
		List<List<String>> stockPrices = CSVReaderStocks.readPricesFromCSV("sptsx_joined_closes.csv");
		System.out.println(stockPrices.get(1));
		System.out.println(stockPrices.get(2));
		int n = 0;
		
//		for (String x : stockPrices.get(2574))
//		{
//			System.out.println(x);
//		}
		
	}
}
