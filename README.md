world-wide-woody
==========================

# Installation

- Assumes python2.6 ... change to actual version
```
sudo mkdir /usr/lib/python2.6/site-packages
sudo ln -s /path/to/world_wide_woody/jinja2/jinja2 /usr/lib/python2.6/site-packages/jinja2
sudo ln -s /path/to/world_wide_woody/CherryPy-3.2.2/cherrypy /usr/lib/python2.6/site-packages/cherrypy
```

- Test path
```
python
import sys
sys.path
exit()
```

- If *site-packages* not found
```
sudo su
echo "/usr/lib/python2.6/site-packages" > /usr/lib/python2.6/dist-packages/site-packages.pth
exit
```

- Test import
```
python
import cherrypy
import jinja2
exit()
```

