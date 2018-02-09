import requests
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import os,sys

def image_download(url,filename):
    #url is a string containing the url of the desired image
    #filename is a string containing the desired name for the file when saved
    image = urllib.request.urlretrieve(url, filename)
    return image

def image_url(url):
    #query the website and return the html to the variable page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    new_url = soup.find_all('img')[0]['src']
    return str(new_url)
    

def search_image(album_name):
    search = str(album_name) + str(' Album Artwork')
    search1 = list(search)
    url = 'https://www.google.com/search?q=' + '+'.join(search1) +'&rlz=1C1GCEA_enUS774US774&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiW6YTMxYjZAhVJ64MKHcduDXwQ_AUICigB&biw=811&bih=771'
    return url

def get_image(url):
    urlimage = image_url(url)
    print('Image downloading...')
    filename = str(input('What would you like to name the image?: ')) + str('.jpg')
    image_download(urlimage, filename)

def get_images(albums):  
    for i in albums:
        album_name = str(i)
        url = search_image(album_name)
        urlimage = image_url(url)
        filename = album_name + '.jpg'
        image_download(urlimage, filename)

def listimages(albums):
	listofimages= []
	for i in albums:
		album_name = str(i)
		image_name = album_name + '.jpg'
		listofimages.append(image_name)
	return listofimages

def make_square(im):
	x,y = im.size()
	size = max(min_size)

def create_collage():
	width = 300	
	length = 300
	print("Welcome to Album Collage Creator")
	print("--------------------------------")
	print("We'll make a collage of all your favorite albums!")
	print("First thing's first, what size collage do you want?")
	cols = int(input("How many columns?: "))
	rows = int(input("How many rows?: "))
	numofalbums = cols*rows
	listofalbums = []
	listofalbums.append(input("Please enter the name of " + str(numofalbums) + " albums: "))
	z = 0
	while z < numofalbums - 1:
		response = input("Okay, and the next one:")
		listofalbums.append(response)
		z += 1
		if len(listofalbums) == numofalbums:
			break
	print('Alright, cool! Hold on a sec while I get the collage ready')
	thumbnail_width = width//cols
	thumbnail_length = length//rows
	size1 = max(thumbnail_width, thumbnail_length)
	size = (size1, size1)
	new_im = Image.new('RGB', (width, length))
	get_images(listofalbums)
	listofimages = listimages(listofalbums)
	ims = []
	for i in listofimages:
		im = Image.open(i)
		im2 = im.crop((0,0,size1,size1))
		ims.append(im2)
	i = 0
	x = 0
	y = 0
	for col in range(cols):
		for row in range(rows):
			print(i,x,y)
			new_im.paste(ims[i], (x,y))
			i += 1
			y += size1
		x += size1
		y = 0
	new_im.save("Album_collage.jpg")

create_collage()
