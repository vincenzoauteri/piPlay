import subprocess
import logging
import time
import os

bin_path = os.path.join(os.path.dirname(__file__), 'bin/')    
FIFO_PATH = bin_path+"fifo"

def start(video_file):
    subprocess.call(["/usr/bin/killall","-9","omxplayer.bin"],shell=False)
    command =  bin_path + "omxplayer" 
    logging.error(command)

    if os.path.exists(FIFO_PATH):
          os.unlink(FIFO_PATH)
    if not os.path.exists(FIFO_PATH):
        os.mkfifo(FIFO_PATH)
        my_fifo = open(FIFO_PATH, 'w+')
    logging.error(my_fifo)

    subprocess.Popen([command,"-r","-o","hdmi", video_file],stdin=my_fifo,shell=False)


def test():
    video_file = "videos/big_buck_bunny_720p_surround.mp4"
    bin_path = os.path.join(os.path.dirname(__file__), 'bin/')    
    start(video_file)
    time.sleep(2)
    fastfwd30()
    time.sleep(2)
    fastfwd30()
    time.sleep(2)
    fastfwd30()

def pause ():
    if os.path.exists(FIFO_PATH):
        my_fifo = open(FIFO_PATH, 'w+')
        my_fifo.flush()
        my_fifo.write('p')

def info ():
    if os.path.exists(FIFO_PATH):
        my_fifo = open(FIFO_PATH, 'w+')
        my_fifo.flush()
        my_fifo.write('z')

def stop():
    if os.path.exists(FIFO_PATH):
        my_fifo = open(FIFO_PATH, 'w+')
        my_fifo.flush()
        my_fifo.write('q')

def previous_chapter():
    if os.path.exists(FIFO_PATH):
        my_fifo = open(FIFO_PATH, 'w+')
        my_fifo.flush()
        my_fifo.write('i')

def next_chapter():
    if os.path.exists(FIFO_PATH):
        my_fifo = open(FIFO_PATH, 'w+')
        my_fifo.flush()
        my_fifo.write('o')
            
def rewind30():
    if os.path.exists(FIFO_PATH):
        my_fifo = open(FIFO_PATH, 'w+')
        my_fifo.flush()
        my_fifo.write("".join([chr(27),chr(91),chr(68)]))

def fastfwd30():
    if os.path.exists(FIFO_PATH):
        my_fifo = open(FIFO_PATH, 'w+')
        my_fifo.flush()
        my_fifo.write("".join([chr(27),chr(91),chr(67)]))

def volume_up():
    if os.path.exists(FIFO_PATH):
        my_fifo = open(FIFO_PATH, 'w+')
        my_fifo.flush()
        my_fifo.write('+')

def volume_down():
    if os.path.exists(FIFO_PATH):
        my_fifo = open(FIFO_PATH, 'w+')
        my_fifo.flush()
        my_fifo.write('-')

#test()
            

