import json
import random
from pathlib import Path

# Method sorts tuples so that they are in alphabetical order to ensure each key matches exactly to one set of ratings.
# Also returns None when they are the exact
def sort_tuple(input_tuple:tuple):
    if input_tuple[0] == input_tuple[1]:
        return None
    if input_tuple[0]>input_tuple[1]:
        return (input_tuple[1],input_tuple[0])
    return input_tuple

# I'm pretty sure nothing in this method is named correctly since frequency is a decimal and this is like not, this is just a count but tbh idgaf nobody else will read this code
# ^ Fixed & Refactored
# counts the number of times a pair appears and returns a dictionary/map of each tuple and its respective count
def tuple_counts(dic:dict):
    counts = {}
    for result in dic: #iterate through each survey result in dictionary
        for i, key_i in  enumerate(result.keys()): #iterate through each specific image except the last one, since al images will have already have been matched with it
            for j, key_j in enumerate(result.keys()): #iterate through and match current image with other images, O(n!) algorithm
                if j <= i:
                    continue
                image_tuple =  sort_tuple((key_i,key_j))
                if image_tuple is None:
                    continue
                if image_tuple not in counts:
                    counts[image_tuple] = 1
                else:
                    counts[image_tuple] += 1
    return counts

#convert tuple counts to frequencies
def counts_to_freqs(dic:dict):
    total = sum(dic.values())
    return {key:value/total for key, value in dic.items()}

#turn subtract frequencies from 1, since those wiht lower frequncies should have a higher number to multiply by
def invert_freqs(dic:dict):
    return {key:1-value for key, value in dic.items()}

#Receives an iterable of strings and adds the directory to all of them
def add_dir(files:list,dir_to_add:str) -> list:
    dir_to_add = dir_to_add.rstrip('/\\') + '/'
    return [str(dir_to_add) + str(Path(f).name) for f in files] #both are casted to strings in case they are actually WindowsPath objects

    
class weight_randomness:
    #takes in additional data and directory of folders to be added to any files returned
    def __init__(self,additional_data:list = [],directory='/'):
        rrs_dict : dict
        with open("Anonymized_Relative_Roughness_Survey_Results.json") as js:
            rrs_dict = json.load(js)
        
        for result in additional_data:  rrs_dict.append(result) # add additional data to rrs_dict before computing

        counts : dict = tuple_counts(rrs_dict)
        self.freqs = invert_freqs(counts_to_freqs(counts))
        '''
        with open('test.json','w') as t:
            t.write(str(self.freqs))
        print("sum: " +str(sum([ 1-x for x in self.freqs.values()])))
        '''
        self.dir = directory
   
   #Takes the current image to determine the next image, weighted towards combinations which have been captured less 
    def next_rand_img(self, image:str, add_dir:bool = False):
        if(type(image) != str):
            image = image.name.split('\\')[-1]# fixed bug using this, ensures that it's only the shortened version of the filename
            image = image.split('/')[-1]
        #print("DEBUG -- NEXT RAND IMG METHOD RUNNING")
        potential_next_images = []
        for key_tuple, value in self.freqs.items():
            #print(f"DEBUG -- I'm inside of the Loop -- Image:{image},0:{key_tuple[0]},1:{key_tuple[1]}")
            if image == key_tuple[0] or image == key_tuple[1]:
                #print("DEBUG -- IMAGE WAS FOUND IN KEY_TUPLE")

                other_image = key_tuple[1] if key_tuple[0] == image else key_tuple[0]
                print((other_image,value))
                potential_next_images.append((other_image,value))

        #TODO: I need an actual failback with this because this would crash my program ngl
        if not potential_next_images:
            #print("DEBUG -- No Potential Next Images, Returning None")
            return None
        
        #get minimum frequency and maximum frequncy before generating a random flaot within range
        min_freq = min([tuple_[1] for tuple_ in potential_next_images])
        max_freq = sum([tuple_[1] for tuple_ in potential_next_images])
        r_float = random.uniform(min_freq,max_freq)
        
        freq_sum = 0
        for img in potential_next_images:
            freq_sum +=  img[1]
            if freq_sum>r_float:
                    if add_dir: return self.dir + img[0]
                    else: return img[0]
            
        # Fallback to last image if somehow we didn't select one
        if add_dir: return self.dir + potential_next_images[-1][0]
        return potential_next_images[-1][0]
    #generates n random images
    def n_random_images(self, first_image:str, n=5):
        imgs = [first_image]
        for i in range(1,n):
            #print(f"DEBUG -- {i} in n_random_images iteration \n")
            new_img = self.next_rand_img(imgs[i-1])
            #ensure that new_img is not a duplicate
            while(new_img in imgs):
                new_img = self.next_rand_img(imgs[i-1])
            if new_img is None:
                return None
            imgs.append(new_img)
        imgs = add_dir(imgs,self.dir)
        return imgs
