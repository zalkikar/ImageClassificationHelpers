# ImageClassificationHelpers

Helper Classes for Image Download and Cleaning in Classification Tasks

*RevImgDownloader.py*: Download images based on reverse image google search using a base image url to obtain similar images.
```
import os
classdir = os.chdir(mydir+"\\XXXXXX") # directory where class is present
from RevImgDownloader import revimgdownload # class

revimgdownload(['class1','class2'], # classes
               ['baselink_class1','baselink_class2'], # urls to base image for each class
               "",
               10, # 10 visually similar images
               "C:/Users/me/data/" # data contains folders titled class1 and class2
              )
```
*ZDhasher.py*: Target exact/near image duplicates (slight image cropping, contrast editing, etc.) using difference hashing. 

```

import os
classdir = os.chdir(mydir+"\\XXXXXX") # directory where class is present
from ZDhasher import dhasher # class
dirs = ['C:/Users/me/data/class1', # class folders
       'C:/Users/me/data/class2']
       
dhashobj = dhasher(dirs)
```

