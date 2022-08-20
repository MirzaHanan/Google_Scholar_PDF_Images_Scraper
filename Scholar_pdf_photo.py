from selenium import webdriver

import fitz # PyMuPDF
from PIL import Image

import time
import os

from difPy import dif


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS # If .exe file is running get base path
    except Exception:
        base_path = os.path.dirname(__file__) # If .py file is running get base path
    return os.path.join(base_path, relative_path)


def getDownLoadedFileName(waitTime):
# method to get the downloaded file name
    driver.execute_script("window.open()")
    # switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    # navigate to chrome downloads
    driver.get('chrome://downloads')
    # define the endTime
    endTime = time.time()+waitTime
    while True:
        try:
            # get downloaded percentage
            downloadPercentage = driver.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # return the file name once the download is completed
                return driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
        except:
            print('"Error: Cannot Get Name of Download File"')
        time.sleep(1)
        if time.time() > endTime:
            break

def scrapImages():
    latestDownloadedFileName = getDownLoadedFileName(120) #waiting 2 minutes to complete the download
    print("Download File Name : " , latestDownloadedFileName)
    # file path you want to extract images from
    file = path + "\\" + latestDownloadedFileName
    # open the file
    pdf_file = fitz.open(file)
    # iterate over PDF pages
    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.get_images(full=False)
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.get_images(full=False), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = fitz.Pixmap(pdf_file, xref)
            pix1 = fitz.Pixmap(fitz.csRGB, base_image)
            #Save the Image
            pix1._writeIMG(f"{path}//Image{latestDownloadedFileName} - {page_index} - {image_index}.jpeg" , xref)
            pix1 = None
            base_image = None
            
            
def RemoveDuplicates(p):
    # Search the folder for duplicate Images
    search = dif(p)  
    # Store the duplicate values in l1
    l1 = list(search.result.values()) 
    # Counter to count the loop
    count = 0 
    # Loop to get the exact path of duplicate file and delete it
    for i in l1:
        aa = l1[count]['duplicates']
        count += 1
        for i in aa:
            print("Removing : " , i )
            try:
                os.remove(i)
            except:
                pass


if __name__ == "__main__":

    path = input("Enter The Path to Save Images : ")
    url = input("Enter the URL (Google Scholar Search result) : ") 
     
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
    "download.default_directory": path, #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
    })
    
    # Stars the chrome with chrome options
    driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe') , options=options) 
    
    try:
        # GET the Google Scholar URL
        driver.get(url)
    except :
        print("Re Run the App And Enter valid URL")

    #list of link type to hold all the URLs Scraped from google scholar website
    link = []

    search_results = driver.find_elements("css selector" , "div.gs_r.gs_or.gs_scl")
    for single_result in search_results:
        s = single_result.find_element("css selector" , "h3 a")
        link.append(s.get_attribute('href'))

    # Open a new tab
    driver.execute_script("window.open()")
    for l in link:        
        # switch to new tab
        driver.switch_to.window(driver.window_handles[-1])
        # if the link ends with "pdf" the download it directly
        if  l.split(".")[-1] == "pdf":
            try:
                # navigate to new link "l"
                driver.get(l)
                scrapImages()    
                driver.close()
                continue
            except:
                pass 
            
        # if the link does not ends with "pdf" takes it to sci-hub
        new_link = 'https://sci-hub.hkvisa.net/' + l
        # navigate to new link
        driver.get(new_link)
        try:
            download_btton = driver.find_element('xpath' , '//*[@id="buttons"]/ul/li[2]/a')
            download_btton.click()
            scrapImages()    
            driver.close()
        except:
            print("The pdf is not even listed on Sci Hub : " , l)
        time.sleep(5)
    
    RemoveDuplicates(path)
    
    # All windows related to driver instance will quit
    driver.quit()