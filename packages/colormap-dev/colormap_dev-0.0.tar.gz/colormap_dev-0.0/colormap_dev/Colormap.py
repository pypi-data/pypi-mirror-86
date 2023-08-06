import requests
import json

class Colormap:

    def __init__(self, colormap):

        self.colormap = colormap
        self.BASE_URL = "https://cs519.herokuapp.com/colormap/"

    def load(self):
        response = requests.get(self.BASE_URL + self.colormap)
        if response.status_code != 200:
            error = response.content.decode('UTF-8')
            raise Exception(error)
        else:
            colormap = response.json()
            cdict = {'red':[], 'green':[], 'blue':[]}
            anchors = sorted(colormap['anchors'], key = lambda i: i['anchor'])
            for i in range(len(anchors)):
                cdict['red'].append((anchors[i]['anchor'], anchors[i]['red']/255, anchors[i]['red']/255))
                cdict['green'].append((anchors[i]['anchor'], anchors[i]['green']/255, anchors[i]['green']/255))
                cdict['blue'].append((anchors[i]['anchor'], anchors[i]['blue']/255, anchors[i]['blue']/255))
            return cdict
