# S&P 500 Data Collection and Storage Docker Container

This Docker container contains a deployment flow written in Python and built with [Prefect.io](https://www.prefect.io/), a workflow automation and orchestration platform. The deployment flow retrieves data about the companies listed in the S&P 500 index from a Wikipedia page, scrapes financial data from an API using the data from Wikipedia, and organizes the data into CSV files that are loaded into an AWS S3 Bucket that can be easily accessed by analytical teams. 

## Requirements

- Docker
- Prefect Cloud API key and workspace
- AWS access key, secret key, and region name
- [Alphvantage](https://www.alphavantage.co/) API key

## Usage

To use this Docker container, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the cloned repository in your terminal.
3. Build the Docker container using the following command:
```
docker build -t sp500-data-container .
```
4. Run the container using the following command:
```
docker run -d sp500-data-container
```

The `run.sh` script, which is run as part of the CMD command in the Dockerfile, logs into the Prefect Cloud, builds a deployment for the main flow, applies the deployment, and starts an agent pool. Once the flow is running, it performs the following steps:

1. Makes a GET request to a Wikipedia site that contains data about the companies listed in the S&P 500.
2. Writes the response HTML file to an AWS S3 bucket using the `boto3` library.
3. Starts a local file server that serves the HTML file.
4. Uses a Scrapy crawler and BeautifulSoup to scrape the desired table from the Wikipedia page.
5. Cleans and organizes the scraped data into a Python list containing each company's stock ticker and other info.
6. Passes the data into a function that retrieves the stock ticker for each company and makes a GET request to an API that returns quarterly and annual balance sheet data for each company in JSON format.
7. Writes the returned JSON files to an S3 bucket.
8. Reads the JSON files from the S3 bucket and organizes them into two CSV files, one for annual reports and another for quarterly reports for all companies.
9. Writes the master annual reports and master quarterly reports CSV files to an S3 bucket so that analytical teams can retrieve them.

## Contributing

If you find any issues with this Docker container, feel free to open an issue or submit a pull request. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
