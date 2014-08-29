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
    res = False
    try:
        ext=path[-3:]
    except:
        pass
    if ext in ["avi","mp4","mpg","mkv"] : 
      res = True

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


class ExplorerHandler(Handler):
    def get(self):
        local_path = urllib.url2pathname(self.request.get("path"))

        logging.error(local_path)
        if local_path == '' :
            local_path = "videos/"

        try:
            os_path=os.path.join(os.path.dirname(__file__),local_path)
            logging.error(os_path)
            file_path =  os_path[:-1]
            if os.path.isfile(file_path) is True:
                logging.error("isfile!")
                if is_video(file_path) is True:
                    #self.redirect(file_path)
                    player.start(file_path)
                    self.render("remote.html");
                    return   

            if re.search("videos",os_path) <= 0:
                os_path=os.path.join(os.path.dirname(__file__),"videos")

            file_list = os.listdir(os_path)


            dir_list = sorted([item for item in file_list if os.path.isdir("".join([os_path,'/',item]))])
            dir_list = ['..'] + dir_list
            
            video_list = sorted([item for item in file_list if is_video(item)])

        except Exception,error:
            logging.error("excepion:" + str(error))
            self.redirect("explorer")
            return


        video_full_path = [(urllib.pathname2url(local_path+item)) for item in video_list]
        dir_full_path   = [(urllib.pathname2url(local_path+item)) for item in dir_list]

        dir_tup   = zip(dir_list,dir_full_path)
        video_tup = zip(video_list,video_full_path)

        self.render("explorer.html",dir_tup=dir_tup,video_tup=video_tup)

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
    def get(self):
      video_file = self.request.get("video")
      self.render("vplayer.html",video_file=video_file)

class TestHandler(Handler):
    def get(self):
      self.render("test.html")


