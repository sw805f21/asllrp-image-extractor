import requests
from bs4 import BeautifulSoup
import cv2
import urllib.request
import os, shutil

def run_hand_sign(variant_id):
    URL = 'http://dai.cs.rutgers.edu/dai/s/occurrence?id_SignBankVariant=' + str(variant_id)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    rs_label = soup.select('center b')[0].get_text()
    hand_sign_label = rs_label
    hand_sign_label = hand_sign_label[31:]

    if "\"" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace("\"", "_")

    if "-" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace("-", "_")

    if "<" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace("<", "_")

    if ">" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace(">", "_")

    if ":" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace(":", "_")

    if "/" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace("/", "_")

    if r"\\" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace(r"\\", "_")

    if "|" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace("|", "_")

    if "?" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace("?", "_")

    if "*" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace("*", "_")

    if "@" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace("@", "_")

    if "+" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace("+", "_")

    if "." in hand_sign_label:
        hand_sign_label = hand_sign_label.replace(".", "_")

    if "(" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace("(", "_")

    if ")" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace(")", "_")

    if " " in hand_sign_label:
        hand_sign_label = hand_sign_label.replace(" ", "_")

    if "#" in hand_sign_label:
        hand_sign_label = hand_sign_label.replace("#", "_")

    counter = 3
    globals()['id_list'] = []

    def hasNumbers(inputString):
        try:
            return any(char.isdigit() for char in inputString)
        except:
            return False

    def scrape_ids(soup, counter):
        try:
            result = soup.select('tr:nth-of-type(3) tr:nth-of-type('+str(counter)+') td:nth-of-type(8)')[0].get_text()

            if hasNumbers(result) :
                id_list.append(result)
                scrape_ids(soup, counter+1)

        except:
            return

    scrape_ids(soup, counter)
    print(id_list)
    somelist = []
    for r in id_list:
        res = ''.join(filter(lambda i: i.isdigit(), r))
        somelist.append(res)
    print(somelist)

    for video in somelist:
        vid_url = 'http://dai.cs.rutgers.edu/dai/s/video?type=separate&id=' + str(video)
        pg = requests.get(vid_url)
        sp = BeautifulSoup(pg.content, 'html.parser')
        tags = sp.find_all('video')
        children = tags[0].findChildren("source" , recursive=False)
        ulz = str(children[0])
        ulz = ulz[:-3]
        ulz = ulz[13:]
        print(ulz)
        urllib.request.urlretrieve(ulz, 'videos\\' + str(video))
        vidcap = cv2.VideoCapture('videos\\' + str(video))
        success,image = vidcap.read()
        count = 0
        directory = "images\\" + hand_sign_label+ "\\" + str(video)
        if not os.path.exists(directory):
            os.makedirs(directory)

        while success:
            cv2.imwrite(directory + "\\frame%d.jpg" % count, image)     # save frame as JPEG file      
            success,image = vidcap.read()
            print('Read a new frame: ', success)
            count += 1

def clear_vid_folder():
    folder = 'videos'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

for i in range(6000):
    run_hand_sign(i)
    clear_vid_folder()
