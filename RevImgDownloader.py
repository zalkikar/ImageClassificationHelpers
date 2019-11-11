# I download based on reverse image google search using an image url to obtain similar images of our classes.

# I used a variety of links throughout to incorporate as many types of images as possible.
# In an effort to aid reproducability, I tend to use many of my source images per class from https://fr.123rf.com/
# I used this site for its isolated object pictures against white backgrounds - making for good base pictures

# Note that keywords can be also be used in this method if needed.
# If you want to do this, you will have to modify the class below to include keywords in the arguments dict.
# Also note that it is best to copy the image url from the source webpage rather than from google search results.

# In order to scrape more than 100 images at a time, a chromedriver path needs to be specified. 
# This uses selenium and an infinite scroll across a webpage.

from google_images_download import google_images_download # Install this package if you haven't already

class revimgdownload:
    
    # 1 image per clas - clas_list and link_list correspond to each other and should be the same length - lists of strings. 
    # Ex. clas_list = ["Raw","Cooked","Overcooked"], link_list = ["link1",'link2','link3'], 
    # where link1 is the base image url for Raw class, etc.
    # If possible, use only .png, .jpeg, or .jpg image link extensions
    
    # chromedriver_path should be in encoding compatible string form. 
    # ex. "C:/Users/rayzc/Downloads/chromedriver_win32/chromedriver.exe"
    # if scraping less than 100 images, you might not have to specify this path - just use ""
    
    # num_image_limit is the MAX number of images download. Sometimes there will be less
    
    # base_dir is your image directory (main folder which contains class folders of images). 
    # ex. base_dir = "C:/Users/rayzc/Downloads/Data/"
    # This should also be in encoding compatible string form
    
    def __init__(self,clas_list,link_list,chromedriver_path,num_image_limit,base_dir):
        self.classes = clas_list
        self.links = link_list
        self.chromedriver = chromedriver_path
        self.maximages = num_image_limit
        self.dir = base_dir
        self.downloader()
        
    def downloader(self):
        keywrd_dict = dict(zip(self.classes, self.links))
        for clas, link in keywrd_dict.items():
            response = google_images_download.googleimagesdownload() #Initialize
            arguments = {"chromedriver":self.chromedriver,
                         "similar_images":link,
                         "limit":self.maximages,
                         "print_urls":True,
                         "output_directory":self.dir,
                         "image_directory":clas}   #creating list of arguments
            paths = response.download(arguments)   #passing the arguments to the function
            #print(clas,"images collected.")
