import webapp2
import Cookie
import re
import cgi
import jinja2
import logging
import urllib
import subprocess 

import sys, os
sys.path.append(os.path.dirname(__file__))

from security import *

import player


jinja_env = jinja2.Environment(
        autoescape=True, loader = jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), 'templates')))


def is_video(path):
    #logging.error("is_video?:" + path)
    res = False

    try:
        if os.path.isfile(path) :
            _,file_ext = os.path.splitext(path)
            #logging.error('file_name' + file_name + "file_ext" +  file_ext)

            if file_ext in [".avi",".mp4",".mpg",".mkv"] : 
                res = True
    except:
        logging.error("excepion:" + str(error))
        pass

    logging.error("res:" + str(res))
    return res 



#General 
def render_str(template, **params):
    """Function that render a jinja template with string substitution"""
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(webapp2.RequestHandler):
    """General class to render http response"""

    def write(self, *a, **kw):
        """Write generic http response with the passed parameters"""
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """Utility function that can add new stuff to parameters passed"""
        params['style']='cerulean'

        return render_str(template, **params)

    def render(self, template, **kw):         
        """Render jinja template with named parameters"""
        self.write(self.render_str(template, **kw))
    
    def set_cookie(self, name, val):
        """Send a http header with a hashed cookie"""
        cookie[name]=val
        cookie[name]["path"]="Path='/'"
        self.response.headers.add_header('Set-Cookie',
              cookie.output())

    def read_cookie(self, name):
        """Check if requesting browser sent us a cookie"""
        cookie = self.request.cookies.get(name)
        return cookie

    def initialize(self, *a, **kw):
        """Function called before requests are processed.
           Used to check for sent cookies"""
        webapp2.RequestHandler.initialize(self, *a, **kw)





class FrontPageHandler(Handler):
    """Class used to render the main page of the site"""

    def render_front(self, entries={}):
        """utility function used to render the front page"""
        self.redirect('/explorer')

    def get(self):
        """function called when the front page is requested"""
        self.render_front()


class PiPlayerHandler(Handler):
    def post(self):
        try:
            local_path = urllib.url2pathname(self.request.get("path")) 
            logging.error("piplay:"+ local_path)
            os_path="".join([os.path.dirname(__file__),'/',local_path])
            logging.error("piplay:"+ os_path)
            if is_video(os_path) : 
                logging.error("isvideo")
                player.start(os_path)
                self.redirect("/remote");
            else :
                self.redirect("/explorer");
        except:
            logging.error("except:"+str(error))
            self.redirect("/explorer")

class ExplorerHandler(Handler):

    def get(self):
        self.post()

    def post(self):

        logging.error("post")
        local_path = urllib.url2pathname(self.request.get("path")) 


        if local_path == '' :
            local_path = "videos"

        logging.error("local_path:"+ local_path)

        try:
            #Gets the absolute path of the requested file/dir
            os_path="".join([os.path.dirname(__file__),'/',local_path])
            logging.error("os_path:"+ os_path)

            if os.path.isdir(os_path):
                logging.error("isdir")
                #gets list of files and directories in the path
                file_list = os.listdir(os_path)

                #Filters directories
                dir_list = sorted([item for item in file_list if os.path.isdir("".join([os_path,'/',item]))])
                dir_list = ['../'] + dir_list
                dir_full_path   = [urllib.pathname2url(local_path+'/'+item) for item in dir_list]
                logging.error("dir_full_path:"+str(dir_full_path))

                #Filters video files
                video_list = sorted([item for item in file_list if is_video("".join([os_path,'/',item]))])
                video_full_path = [urllib.pathname2url(local_path+'/'+item) for item in video_list]
                logging.error("video_full_path:"+str(video_full_path))


                dir_tup   = zip(dir_list,dir_full_path)
                video_tup = zip(video_list,video_full_path)

                self.render("explorer.html",dir_tup=dir_tup,video_tup=video_tup)
                #If path is a directory, further drills down the path
            else:
                logging.error("else")
                self.redirect("/explorer")


        except Exception,error:
            logging.error("excepion:" + str(error))
            self.redirect("explorer")
            return
            


            




class RemoteHandler(Handler):
    def get(self):
      self.render("remote.html")

    def post(self):
      data = self.request.get('input')
      logging.error("data")

      if data == "pause" or data == "play":
          player.pause()
      elif data == "ffwd30":
          player.fastfwd30()
      elif data == "rwnd30":
          player.rewind30()
      elif data == "volup":
          player.volume_up()
      elif data == "voldown":
          player.volume_down()
      elif data == "stop":
          player.stop()
          self.redirect("/explorer")
          return
      elif data == "next":
          player.next_chapter()
      elif data == "previous":
          player.previous_chapter()
      elif data == "info":
          player.info()
      else :
          player.stop()
          self.redirect("/explorer")
          return



      self.redirect("/remote")

class VideoPlayerHandler(Handler):
    def post(self):
      video_file = self.request.get("video")
      self.render("vplayer.html",video_file=video_file)

class LivePlayerHandler(Handler):
    def get(self):
      self.render("live.html")

class TestHandler(Handler):
    def get(self):
      self.render("test.html")


