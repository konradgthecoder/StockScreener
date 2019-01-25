package models;

import java.util.List;
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;

public class CSVReaderStocks 
{
	
	public static List<String> readStocksFromCSV(String fileName)
	{
		List<String> stockTickers = null;
		Path filePath = Paths.get(fileName);
		
		// NufferedReader instance
		try (BufferedReader br = Files.newBufferedReader(filePath,
				StandardCharsets.US_ASCII))
		{
			// Read the first line from text file 
			String line = br.readLine();
			stockTickers = Arrays.asList(line.split("\\s*,\\s*"));
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
		return stockTickers;
	}
	public static List<List<String>> readPricesFromCSV(String fileName)
	{
		List<List<String>> stockPrices = new ArrayList<List<String>>();
		Path filePath = Paths.get(fileName);
		
		// NufferedReader instance
		try (BufferedReader br = Files.newBufferedReader(filePath,
				StandardCharsets.US_ASCII))
		{
			// Read the first line from text file 
			String line = br.readLine();
			line = br.readLine();
			while (line != null)
			{
				stockPrices.add(Arrays.asList(line.split("\\s*,\\s*")));
				line = br.readLine();
			}
			
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
		return stockPrices;
	}
}
