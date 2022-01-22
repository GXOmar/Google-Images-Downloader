# Google-Images-Downloader

This script is an automated process for downloading images from [**Google Images**](https://www.google.com/imghp) using the [**Selenium WebDriver module**](https://www.selenium.dev).

The script will open a *chromium-based* web browser called [**Brave**](https://brave.com) using the **Selenium WebDriver** and get redirected to what kind of images you want to search based on the user's search query.

It'll only accept images that are at least FULL HD resolution (1920 x 1080), it will also accept bigger image resolutions too.

The idea :bulb: to write this script came when I want a new wallpaper almost every day for my desktop :desktop_computer: and it was a good idea to make it since I also learned how to work with the Selenium module.<br>
***Personally***, I mainly use this script to download cool desktop wallpapers ツ

The script will start by locating image thumbnails, then by clicking on the thumbnail it will open the image on the side window that will reveal the real image, the image resolution will be checked first if it is at least a FULL HD. Then it'll fetch the URL of the image then get downloaded.

The downloading process won't begin until X number of images requested by the user has been found, *i.e. 100 images*.

## **Fetching The image URLs**

Fetching The image URLs is done with two combined methods:

- The WebDriver will wait for the image to load for at least 15 seconds after clicking on the image thumbnail.<br>
- It will wait until the real URL is loaded instead of the place holder URL with a low quality:poop:<br>
- Identifying the real URL is done with the help of XPATH Expression.<br>
  - The Xpath functions used in this script are:
    - starts-with(@src, "https") *Check if the URL starts with "https"*
    - substring(@src, (string-length(@src) - string-length(".jpg") + 1)) = ".jpg"<br>
    *The ***substring*** function is just to identify the last part of the URL if it **ends with** an image file format i.e.(.jpg or .jpeg  or .png)*

- If all went to the plan, the URL gets fetched to a set of URLs to download later.

## **Downloading and saving images**

Downloading and saving images is executed after X number of images requested by the user has been found. The image that gets downloaded won't retain its name. Instead, it'll get assigned 12 random characters containing letters and numbers.

The images will be saved to a folder that is named after the search query that has been given to the script by the user.<br>
*i.e. D:\\<path_to_folder>\Downloaded Images from google\\<search_query_folder\>\54afh91a97sf.jpg*

- The Folder will be created after fetching the URLs is finished. If it already exists it won't be created.

## Exiting/Ending the program

The process to determine the ending of the program is done by locating the **footer** of the page and checking if it is visible in the window **ViewPort**. The program report to the user the number of images that have been successfully downloaded and the number of images that couldn't get downloaded with a notification to inform them at the end of the program.

- #### Handling the ending of the program:

  1. If the script ran normally and found the requested number of images, the browser window closes and the script proceeds to download and save the images.

  2. If the script ran normally but couldn't find the requested number of images, it will download and save whatever has been found as long as it finds at least one image URL.

  3. If the script didn't find any images that you are looking for, it will close the browser and end the program with a notification to inform the user that it couldn't find any image.

#### I hope you like it, any suggestions for the program are welcome:monocle_face: