# Google-Images-Downloader

This script is an automated process for downloading images from [**Google Images**](https://www.google.com/imghp) using the [**Selenium WebDriver module**](https://www.selenium.dev).

The script will open a *chromium-based* web browser called [**Brave**](https://brave.com) using the **Selenium WebDriver** and get redirected to what kind of images the user wants to download based on the user's search query.

## **Overall method**

The script will start by locating images' thumbnails, then it clicks on the image thumbnail to reveal the image on the side window to load the actual image, and then it'll fetch the URL of the image and get downloaded and saved to the hard drive. *(if the user asked to check the resolution of the image, the resolution will be checked **before fetching the URL** to be at least FULL HD (1920x1080).)*

***The images won't begin downloading until X number of images requested by the user has been found.***
The script will show a progress bar to indicate the current status of the progress, like: `72%|███████    | (Total images URL found: 72/100)`

## **Fetching an image URL**

Fetching an image URL is done as follows:

- The WebDriver will wait :hourglass_flowing_sand: for the image to load for a couple of seconds after clicking on the image thumbnail.<br>
- It will wait until the URL is loaded instead of the placeholder URL with low-quality resolution :poop:<br>
- The URL gets verified by **Xpath expressions** before fetching the URL using the following methods:
    - `starts-with(@src, "https")`<br> Check if the URL starts with "https"
    - `substring(@src, (string-length(@src) - string-length(".jpg") + 1)) = ".jpg"`<br>
    The *substring* function is to identify the last part of the URL if it *ends with* one of these ( .jpg or .jpeg or .png ) image file formats.

- If all went to the plan, the URL gets fetched and added to a list of URLs to download later.

## **Downloading and saving images**

**Downloading the images** is executed after X number of images requested by the user has been found. The image that gets downloaded won't retain its name. Instead, **it'll get assigned 12 random characters containing letters and numbers.**

The **images** will be **saved** to a folder named after the search query that has been given to the script by the user.<br>
i.e. `..\..\Downloaded Images from google\<search_query_folder>\54afh91a97sf.jpg`

- *If the folder already exists, it won't be created, this only happens when you search twice with the same search query.*

## Exiting/Ending the script

The process to determine the ending of the script is done by locating the **footer** of the webpage and checking if it is visible in the window **ViewPort**.
- #### Handling the ending of the script:

  1. If the script ran normally **and** found the requested number of images, the browser window closes and the script proceeds to download and save the images.

  2. If the script ran normally **but** couldn't find the requested number of images, it will download and save whatever has been found as long as it finds at least one image URL.

  3. If the script didn't find **any** images that you are looking for, it will close the browser and end the script process with a notification to inform the user that it couldn't find any image.

#### Any suggestions for the script are welcome :monocle_face:<br>
###### Personally, I mainly use this script to download cool desktop wallpapers ツ