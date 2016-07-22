import webapp2
import urllib2
import json
import datetime
import cgi
from google.appengine.api import users
from google.appengine.api import urlfetch

MAIN_PAGE_HEADER_HTML = """\
<html style="font-family:Arial">
    <head>
              <script src="https://code.jquery.com/jquery-2.1.3.min.js"></script>
  <script src="https://code.jquery.com/ui/1.11.2/jquery-ui.min.js"></script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>
        <title>HELLO CLOUD (CS496 Assignment 1)</title>
        <link href="http://fonts.googleapis.com/css?family=Inconsolata" rel="stylesheet"
        type="text/css"/>
        
        
        <script type="text/javascript">
    function refreshClock(){
        var t = new Date();
        var y = t.getFullYear();
        var m = t.getMonth();
        var mos = ['January','February','March','April','May','June','July','Auguest','September','October','November','December'];
        var d = t.getDate();
        var day = t.getDay();
        var days = ['Sunday','Monday','Tuesday','Wednsday','Thursday','Friday','Saturday','Sunday'];
        var hr = t.getHours();
        var meridiem = "AM";
        if(hr>12){
            hr-=12;
            meridiem="PM";
        } else if(hr==0){
            hr=12;
        }
        var min = t.getMinutes();
        min = (min<10?"0":"")+min;
        var sec = t.getSeconds();
        sec = (sec<10?"0":"")+sec;
        day = days[day]+' ' +mos[m]+' ' +d+' '+y
        document.getElementById("day").innerHTML=day;
        time = hr+":"+min+":"+sec+" "+meridiem;
        document.getElementById("clock").innerHTML=time;
        setTimeout(refreshClock,1000);
    }</script>
    
  
    
    </head>
    <body onload="refreshClock(); setInterval('refreshClock()',1000)">
        <table>
            <tr>

                <th style="font-size:1.3em;">CS 496 Assignment 1: Hello Cloud</th>

             </tr>
        </table>
         <h4 style="border-bottom:solid green"></h4>
         <p></p>
         <p></p>
         <br>
          <div class="container">
        <h4><span class="glyphicon glyphicon-calendar"></span>   CALENDAR </h4>
        <div class="well">
        Today is
        <span id="day"></span> </div></div>
        <p></p>
        <div class="container">
        <h4> <span class="glyphicon glyphicon-time"></span>   CLOCK</h4>
                
        <div class="well">
        The current time is <span id="clock" style="font-family:Inconsolata, Arial, Helvetica, san-serif;"></span>
        <script type="text/javascript">window.onload=refreshClock();</script> 
        <p></p>
        </div>
        </div>
        <div class="container">
        <h4><span class="glyphicon glyphicon-cloud"></span>   WEATHER</h4>
        </div>
"""

MAIN_PAGE_FOOTER_HTML = """
    </div>
      </table></body><footer style="clear:both;"><br><div style="font-size:0.85em;clear:both;border-top:solid green">Tatyana Vlaskin - CS496 Winter 2016</div>
    </footer></html>"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HEADER_HTML)
        self.response.write('\n')
        f = urllib2.urlopen('http://api.wunderground.com/api/e0eb935a2ef50bd7/geolookup/conditions/q/WA/Seattle.json')
        json_string = f.read()
        parsed_json = json.loads(json_string)
        location = parsed_json['location']['city']
        temp_f = parsed_json['current_observation']['temperature_string']
        feels = parsed_json['current_observation']['feelslike_string']
        icon2 = parsed_json['current_observation']['icon_url']
        icon3= parsed_json['current_observation']['icon']
        weather1 = parsed_json['current_observation']['weather']
        self.response.out.write('\n')
        #self.response.write('<table><tr>')
        #self.response.write("Current weather in "+location+" : "+weather1)
        url2 = "http://icons.wxug.com/i/c/k/"+str(icon3)+".gif"
        #self.response.write('<td>'+'<img src="'+url2+'">'+'</td>')
        #self.response.out.write('\n')
        #self.response.write( "Current temperature in %s is: %s" % (location, temp_f))
        #self.response.write('\n')
        #self.response.write('<br><em>Feels like</em> '+feels+'<td>')
        #self.response.write('<td>'+'<img src="'+icon2+'">'+'</td>')
        #self.response.write('</tr></table>')
        f.close()
        self.response.write('<div class="container">')
        self.response.write('<html><div class="well">')
        self.response.write("Current weather in "+location+" : "+weather1)
        self.response.write('<td>'+'<img src="'+url2+'">'+'</td>'+'\n')
        self.response.write( '<p>'+"Current temperature in %s : %s" % (location, temp_f)+'</p>')
        self.response.write('\n')
        self.response.write('</div></div></html>')
        self.response.write(MAIN_PAGE_FOOTER_HTML)
   
        


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
