# Google_Scholar_PDF_Images_Scraper
 
link to download the chrome driver for your version of chrome:

https://chromedriver.chromium.org/downloads

This scraper takes two inputs from user:
- Path to Save The Images
- Google Scholar Search Results

Then the scraper Open Chrome Browser 
GoTo the provided google scholar search results page
Check all the Indiviual links on the search result page
- If the page is a link to pdf then start downloading it directly
- If the page is not a link to pdf the go to Sci-Hub and download the pdf from there
- If the pdf is not even listed to Sci-Hub the Ignore that link.

After Downloading the pdf from search result page:
- Collect all the Images from Downloaded Pdf

After collecting all the images from single pdf, 
It then downloads the new pdf and collect all the images from that pdf 
and continue doing that untill the last link on that page.

After downloading and collecting all the images from a single search result page

It removes all the duplicate images collected from all the pdfs
