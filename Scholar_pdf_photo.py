from selenium import webdriver
import time

import fitz # PyMuPDF
from PIL import Image

from tkinter.filedialog import askdirectory
from tkinter import Tk

import os

# url = 'https://sci-hub.hkvisa.net/https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1365-2230.2009.03220.x'
# url = 'https://sci-hub.hkvisa.net/https://ijponline.biomedcentral.com/articles/10.1186/s13052-021-01097-2'
# url = 'https://sci-hub.hkvisa.net/https://www.sciencedirect.com/science/article/pii/S0002817714660359'

# url = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=oral+ulcers+clinical&btnG'


# path = input("Enter The Path to Save Images : ")


Tk().withdraw()
path =  askdirectory(title="Select a folder")

url = input("Enter the URL (Google Scholar Search result) : ") 


# driver.get(url)
# time.sleep(2)
# download_btton = driver.find_element('xpath' , '//*[@id="buttons"]/ul/li[2]/a')
# download_btton.click()

# print("****************File Download***************")

# def getDowload(link):
# path = 'C:\\Users\\fujitsu\\Downloads\\Documents'

# Check whether the specified
# path exists or not
isExist = os.path.exists(path)
if isExist == False:
    os.mkdir(path)
    

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : path}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
    
driver.get(url)
link = []

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
            print("Something")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # return the file name once the download is completed
                return driver.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
        except:
            print("****************Cannot Get Name of Download File*************** ")
        time.sleep(1)
        if time.time() > endTime:
            break

def scrapImages():
    latestDownloadedFileName = getDownLoadedFileName(15) #waiting 15 seconds to complete the download
    print("****************Download File Name *************** " , latestDownloadedFileName)
    # file path you want to extract images from
    file = path + "\\" + latestDownloadedFileName
    # open the file
    pdf_file = fitz.open(file)
    # iterate over PDF pages
    print("****************File Opened***************")
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
            # base_image = pdf_file.extract_image(xref)
            base_image = fitz.Pixmap(pdf_file, xref)
            
            # print("****************File Saved***************")    
            pix1 = fitz.Pixmap(fitz.csRGB, base_image)
            # pix1._writeIMG(f"{path}//Image{latestDownloadedFileName} - {page_index} - {image_index}.jpeg" , xref)
            pix1._writeIMG(f"Image{latestDownloadedFileName} - {page_index} - {image_index}.jpeg" , xref)
            print("****************File Saved***************")
            pix1 = None
            base_image = None



search_results = driver.find_elements("css selector" , "div.gs_r.gs_or.gs_scl")
for single_result in search_results:
    # print(single_result)
    s = single_result.find_element("css selector" , "h3 a")
    link.append(s.get_attribute('href'))


# Open a new tab
driver.execute_script("window.open()")
for l in link:
    # switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    
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
exit(driver)

