#! python3

# Google Images Downloader.py - search and download Images from google.com
# this script will open the web browser using selenium and search for Images(1920x1080 minimum/FULL HD), get their links, and download them.
# I Mainly use this script to automatically download desktop wallpapers.
# run this code in CLI using >>> py Google\ Images\ Downloader.py

# NOTE: Images found using this script is NOT a duplicate-FREE, duplicate images maybe be downloaded again and get new random name
# if you search with the same term again were a new folder won't be created since it already exist and images found will be saved to that folder.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import requests, os, time
from uuid import uuid4
from plyer import notification
from tqdm import tqdm
from colorama.ansi import Fore as CLI_TextColor

# XPATH location of the image resolution.
Image_Resolution_XPath = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/span'
# XPATH location of the image URL with checkers that starts with "https" and ends with an image file extension (.jpg or .jpeg or .png)
ImageXPath_with_checkers = '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img\
    [@src[starts-with(., "https") and substring(., (string-length(.) - string-length(".jpg") + 1)) = ".jpg"\
              or substring(., string-length(.) - string-length(".jpeg") + 1) = ".jpeg"\
                   or substring(., string-length(.) - string-length(".png") + 1) = ".png"]]'

# Footer location in ViewPort, The program will end when the footer is visible in ViewPort(on screen)
FooterCurrentViewPort = """
footer_currentVP = document.querySelector('#ZCHFDb').getBoundingClientRect();
if (footer_currentVP.top != 0 && footer_currentVP.bottom != 0 && footer_currentVP.right != 0) { 
    return (
        footer_currentVP.top >= 0 &&
        footer_currentVP.left >= 0 &&
        footer_currentVP.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        footer_currentVP.right <= (window.innerWidth || document.documentElement.clientWidth)

    );} else {return (false) }
"""

ChromiumBrave = Options()
ChromiumBrave.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
ChromeDriverPATH = Service("C:\Program Files (x86)\chromedriver.exe")
Search_URL = "http://www.google.com/search?q={q}&tbm=isch"

FolderPath = r"D:\Omar\Pictures\Downloaded Images from google"
Success_downloads, Failure_downloads, FailedToSaveImage = 0, 0, 0 # track image stats

def fetch_image_URLs(search_query: str, MAX_number_of_images: int, wd: webdriver):
    """Locate and fetch image URLs from google.com/imghp"""
    def scroll_page(wd: webdriver):
        """Scroll the page down from it's current position + length of window ViewPort"""
        wd.execute_script("window.scrollTo(0, window.pageYOffset + window.innerHeight);")
        time.sleep(3.5)

    wd.get(Search_URL.format(q=search_query))
    print("Looking for images, Please wait...", flush=True)

    image_links = set()
    image_count = 0
    starting_position = 0
    # Create the actual progress bar to track the number of image URL being found.
    images_URL_pbar = tqdm(total=MAX_number_of_images, colour='#00cc96', desc='Images URL', bar_format='{percentage:3.0f}%|{bar}| (Total {desc} found: {n_fmt}/{total_fmt})') 

    while image_count < MAX_number_of_images:
        scroll_page(wd)
        FooterVisibilityInViewPort = wd.execute_script(FooterCurrentViewPort)
        if not FooterVisibilityInViewPort: # keep looking for images when the Footer is not visible in ViewPort.

            # find all image thumbnails in the page
            try:
                ImageThumbnails = WebDriverWait(wd, 10).until(lambda x: x.find_elements(By.CLASS_NAME, 'Q4LuWd'))
            except Exception:
                continue

            for image in ImageThumbnails[starting_position:len(ImageThumbnails)]:
                try: # click to open each image to find the real image url.
                    image.click()
                    time.sleep(0.5)
                except Exception:
                    continue # try the next image!
                
                # check the image resolution!
                if check_image_resolution(wd):
                    try:
                        # wait for a correct image url to be found using XPATH expression, this works well with WebDriverWait.
                        # using XPATH expression saves a lot of time from writing unwanted regex code, XPATH is like regex but for web pages, it uses XML path expression within the HTML DOM structure.
                        image_URL = WebDriverWait(wd, 15).until(EC.presence_of_element_located((By.XPATH, ImageXPath_with_checkers))).get_attribute('src')
                    except Exception:
                        continue # try the next image!

                    image_links.add(image_URL)
                    update_progress_bar(images_URL_pbar)

                    if len(image_links) >= MAX_number_of_images:
                        update_progress_bar(images_URL_pbar, close=True) # close the progress bar.
                        print(f"\n{CLI_TextColor.GREEN}Done, Found {len(image_links)} images{CLI_TextColor.RESET}\n", flush=True)
                        return image_links # Done!
                else:
                    continue # check the next image for a better resolution

            image_count = len(image_links)
            starting_position = len(ImageThumbnails)

        else: # Footer is visible in ViewPort!
            update_progress_bar(images_URL_pbar, close=True) # close the progress bar.
            print("Looks like you've reached the end!".center(30, '-'), flush=True)
            if len(image_links) >= 1:
                print(f"{CLI_TextColor.BLUE}Got {len(image_links)} out of {MAX_number_of_images} images!{CLI_TextColor.RESET}", flush=True)
                return image_links

            else: # this happens when no images have been found!
                print(f"{CLI_TextColor.RED}Sorry, Couldn't find any images!")
                wd.quit() # close the web browser window
                notification.notify("Failed to find images!", f"Sorry, Couldn't find any images", app_icon=r".\Notification Icons\vcsconflicting.ico")
                raise SystemExit # exit/end the program

def update_progress_bar(progress_bar_instance: tqdm, close=False):
    progress_bar_instance.update() if close != True else progress_bar_instance.close()

def check_image_resolution(wd: webdriver):
    """Check an image resolution, minimum image resolution should be Full HD(1920 x 1080)"""
    if DoCheckResolution == "y":
        Minimum_Width, Minimum_Hight = 1920, 1080
        try:
            # Find the image resolution, the resolution is based of what google is displaying when you hover over the image.
            # Checking the image resolution without downloading the image itself to save data (this is not a perfect way of getting an image resolution!).
            ImageWidth, unknownCharacter, ImageHight = WebDriverWait(wd, 5).until(
                EC.presence_of_element_located((By.XPATH, Image_Resolution_XPath))).get_attribute("textContent").split(' ')
        except Exception:
            return False
        ImageWidth, ImageHight = ImageWidth.replace(',', ''), ImageHight.replace(',', '') 
        return True if int(ImageWidth) >= Minimum_Width and int(ImageHight) >= Minimum_Hight else False

    else:
        return True # Quick implementation to ignore checking the image resolution form a user input.
        
def download_and_save_image(image_url: str, folder_path: str, progress_bar_instance: tqdm):
    """Download and save the image to a targeted folder with a random name assigned to the image file"""

    global Success_downloads, Failure_downloads, FailedToSaveImage

    try:
        image_content = requests.get(image_url) # download the image content!
        image_content.raise_for_status()
    except Exception as FailedToDownloadImageError:
        Failure_downloads += 1
        return print(f"\n{CLI_TextColor.RED}ERROR - Couldn't download image: {image_url} - {FailedToDownloadImageError}{CLI_TextColor.RESET}\n", flush=True)
    
    NewImageName = os.path.join(folder_path, str(uuid4()).replace('-', '')[:12] + os.path.splitext(image_url)[-1])
    # "os.path.splitext(image_url)[-1]" is to get the image extension out of image_url.
    # The final name would be like >>> D:\Omar\Pictures\Downloaded Images from google\<query>\54afh91a97sf.(jpg or jpeg or png)
    try: # open a new image file and save the image_content to it!
        with open(NewImageName, 'wb') as NewImage:
            for chunk in image_content.iter_content(100000):
                NewImage.write(chunk)
        Success_downloads += 1
        update_progress_bar(progress_bar_instance)
    except Exception as FailedToSaveImageError:
        FailedToSaveImage += 1
        return print(f"\n{CLI_TextColor.YELLOW}ERROR - Couldn't save image: {image_url} - {FailedToSaveImageError}{CLI_TextColor.RESET}\n", flush=True)

def download_images_from_google(search_query: str, driver_path: str, number_of_images: int, targeted_Folder: str):
    with webdriver.Chrome(service=driver_path, options=ChromiumBrave) as wd: # This web driver will open Brave web browser.
        wd.maximize_window()
        URLs = fetch_image_URLs(search_query, number_of_images, wd)

    Folder_path = os.path.join(targeted_Folder, search_query)
    # Create a folder in the targeted_folder with the search_query name, if that folder doesn't exists, it'll be created.
    if not os.path.exists(Folder_path):
        os.makedirs(Folder_path)
        print(f"{CLI_TextColor.MAGENTA}Folder created: {Folder_path}{CLI_TextColor.RESET}", flush=True)

    print(f"{CLI_TextColor.CYAN}Downloading the images, Please wait...{CLI_TextColor.RESET}", flush=True)
    # create the actual progress bar to track the number of images being saved to the local drive
    images_saved_pbar = tqdm(total=NumberOfImagesToSearch, colour='#00cccc', desc='images saved', bar_format='{percentage:3.0f}%|{bar}| (Total {desc}: {n_fmt}/{total_fmt})')
    for URL in URLs:
        download_and_save_image(URL, Folder_path, images_saved_pbar)
    update_progress_bar(images_saved_pbar, close=True) # close the progress bar.

if __name__ == "__main__":
    while True:
        UserSearchQuery = input("Images to search for: ")
        if UserSearchQuery == '' or UserSearchQuery.isspace():
            continue
        else:
            break
    NumberOfImagesToSearch = int(input("Number of images to download: ").strip() or 5)
    DoCheckResolution = input("Check image resolution? [y/n]: ").strip() or 'n'
    download_images_from_google(UserSearchQuery, ChromeDriverPATH, NumberOfImagesToSearch, FolderPath)
    result = f"Download complete: {CLI_TextColor.GREEN}{Success_downloads} Success, {CLI_TextColor.RED}{Failure_downloads} Failures"
    print(result + f", {CLI_TextColor.YELLOW}{FailedToSaveImage} Failed to save images" if FailedToSaveImage > 0 else result, flush=True)
    # notify me when finish downloading.
    notification.notify("Download complete!", f"Downloaded {Success_downloads} images", app_icon=r".\Notification Icons\iconfinder-check.ico")