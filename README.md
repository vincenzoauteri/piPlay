piPlay

Simple web application for media streaming on Raspberry PI.

It serves as a file explorer to select a video file, and plays it with
the omxplayer command. A simple remote let's you control the stream somewhat.

It is also possible to stream remotely on the client, as a mean to access your
library from anywhere.

Uses Python and webapp2 framework (I started with Google App Engine but the
framework doesn't let you execute local commands): on my pi I'm using Apache as a web server
with modwsgi.

Apart from setting apache, it is needed to symlink the main folder of your media library 
to a /videos directory in the root of the app.

