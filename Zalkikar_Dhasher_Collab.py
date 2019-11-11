#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import dhash
import collections
from PIL import Image

class dhasher:
    
    def __init__(self, directories):
        self.directories = directories
        file_dirs, unq_files = self.filer()
        dhash_mtrx = self.difhashmtrx(file_dirs,unq_files)
        across_duplicates_files, within_duplicates_count = self.detectduplicates(dhash_mtrx,file_dirs)
        self.returndups(across_duplicates_files, within_duplicates_count)
        
    def filer(self):
        file_dirs = [[] for x in range(len(self.directories))]
        unq_files = [[] for x in range(len(self.directories))]
        counter = 0
        total_files = 0
        for d in self.directories:
            path = os.path.expanduser(d)
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)
                file_dirs[counter].append(filepath)
                unq_files[counter].append(filename[:len(filename)-4]) 
            print(len(unq_files[counter]),"total images in",path)
            total_files += len(unq_files[counter])
            counter += 1
        print('\n',total_files,"total images in all classes.")
        return file_dirs,unq_files
    
    def difhashmtrx(self, file_dirs,unq_files):
        print("\nForming Dhash (Size = 8) Matrix...")
        dif_hash_mtrx = [[] for x in range(len(self.directories))]
        c1 = 0
        unhashed = []
        for clas in file_dirs:
            for image_path in clas:
                try:
                    image = Image.open(image_path).convert("RGBA") # All palette images with transparency expressed in bytes should converted to RGBA images 
                    row, col = dhash.dhash_row_col(image)
                    image_hash = dhash.format_hex(row, col)
                    dif_hash_mtrx[c1].append(image_hash)
                except:
                    unhashed.append(image_path)
                    print(image_path," - file type is unhashable.")
            c1 += 1
        print(len(unhashed)," images ignored.")
        return dif_hash_mtrx
            
    def detectduplicates(self, dif_hash_mtrx,file_dirs):
        # Find common elements within sublists of the dhash matrix
        duplicate_indx_mtrx = []
        unq_elems_mtrx = []
        across_file_duplicates = []
        dups_in_clas = [[] for x in range(len(self.directories))]
        c1 = 0
        print("\nDhashing...")
        for z in dif_hash_mtrx:
            duplicate_indx = [i for i in range(len(z)) if not i == z.index(z[i])]
            unq_elems = [z[i] for i in range(len(z)) if i == z.index(z[i])]
            unq_elems_mtrx.append(unq_elems)
            duplicate_indx_mtrx.append(duplicate_indx)
            dups_in_clas[c1].append(len(z)-len(unq_elems))
            print(len(z)-len(unq_elems),"duplicate images within",self.directories[c1],"found.")
            c1 += 1

        # Find common elements across sublists of the dhash matrix - this should be 0 (or very close to it)
        unq_elems_mtrx_list = [item for sublist in unq_elems_mtrx for item in sublist]
        if len(unq_elems_mtrx_list) - len(set(unq_elems_mtrx_list)) == 0:
            print("No duplicate images across classes.")
        else: 
            print(len(unq_elems_mtrx_list) - len(set(unq_elems_mtrx_list)),"duplicate images across classes found.")
            unq_a = [item for item, count in collections.Counter(unq_elems_mtrx_list).items() if count > 1]
            print("\nDuplicates in 2 or more classes:")
            for a in unq_a:
                for i in range(len(file_dirs)):
                    try:
                        file_path = file_dirs[i][dif_hash_mtrx[i].index(a)]
                        across_file_duplicates.append(file_path)
                        print('\n',file_path)
                    except:
                        continue
                        #print("Image not in",self.directories[i])
        return across_file_duplicates, dups_in_clas
    
    def returndups(self,across_duplicates_files, within_duplicates_count):
        return across_duplicates_files, within_duplicates_count

