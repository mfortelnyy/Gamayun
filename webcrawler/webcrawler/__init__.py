from webcrawler.webcrawler.spiders.web_pull import WebCrawler

if __name__ == "__main__":
    # Instantiate the WebCrawler object
    webcrawler = WebCrawler()

    # Start the crawling process
    webcrawler.start_requests()

    # Print a message indicating that the crawling process has started
    print("Crawling process started...")

    try:
        # You can add a sleep here to allow some time for the crawling process to run
        # time.sleep(60)  # Wait for 60 seconds (optional)

        # Print the WebCrawler object (you may want to remove this line if it's not necessary)
        print(webcrawler)

        # Print a success message indicating that the crawling process has completed
        print("Crawling process completed successfully.")
    except Exception as e:
        # Print any exceptions that occur during the crawling process
        print(f"An error occurred during the crawling process: {e}")
