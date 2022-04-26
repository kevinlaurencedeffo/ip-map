from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
import requests, mechanize, folium
import kivy
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty


ac='''
#:import hex kivy.utils.get_color_from_hex

<ContentNavigationDrawer>
MDScreen:
    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "IP MAP"
        specific_text_color:1, 1, 1, 1
        right_action_items:[["help"]]
        MDSwitch:
            width:dp(42)
            on_active: app.color()
        
            
    MDGridLayout:
        cols: 1
        rows: 3
        MDLabel:
            text:""
            size_hint: .1, .1
            canvas.before:
                Color:
                    rgba: 0, 1, 0, 0
        MDLabel:
            text:" "
            size_hint: .1, .1
            canvas.before:
                Color:
                    rgba: 0, 1, 0, 0
        MDGridLayout:
            cols: 1
            rows: 3
            MDTextField:
                id: fielde
                hint_text: "Already got de IP? paste it here:  "
                size_hint: .3, .3
                size: 
                radius: [25, 10, 30, 20]
            MDTextField:
                id: fielden
                hint_text: "type the name of the map file: "
                size_hint: .3, .3
                radius: [25, 10, 30, 20]
            MDGridLayout:
                cols: 1
                rows: 6
                MDFillRoundFlatIconButton:
                    icon: 'magnify'
                    text: "RECHERCHER"
                    pos_hint: { 'top' : .95, 'right': .95}
                    width: dp(5)
                    md_bg_color: app.theme_cls.primary_color
                    on_press: app.details()
                MDLabel:
                    id: lbl1
                    text:""
                MDLabel:
                    id: lbl2
                    text:""
                MDLabel:
                    id: lbl3
                    text:""
                MDLabel:
                    id: lbl4
                    text:""
                MDLabel:
                    id: lbl5
                    text:""
                                
                                
                                
        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                nav_drawer: nav_drawer
                '''

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


    
    
class Test(MDApp):
    def color(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
            
            
        else:
            self.theme_cls.theme_style = "Light"
            self.specific_text_color = "White"
    
    def build(self):
        self.title = 'IP MAP'
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(ac)
    
    def details(self):
        global lat, long
        br = mechanize.Browser()
        br.set_handle_robots(False)
        urlFoLaction = 'https://api.freegeoip.app/json/{0}?apikey=d9886160-abce-11ec-b3ad-3773a1488723'.format(self.root.ids.fielde.text)
        locationInfo = br.open(urlFoLaction)
        loc = locationInfo.read()
        locf = loc.decode('UTF-8')
    
        
        p = locf.find('"country_name":"')
        pa= p+ 16
        pay=locf.find('"',pa)
        pays=locf[pa:pay]
        self.root.ids.lbl1.text ='country= '+" "+ pays
    
        
        vi= locf.find('"city":"')
        vil = vi+8
        vill = locf.find('"', vil)
        ville = locf[vil:vill]
        self.root.ids.lbl2.text='city = '+" "+ ville
    
        
            
        x = locf.find('"latitude":')
        x1 = x+11
        x2 = locf.find(',', x)
        lat=locf[x1: x2]
        self.root.ids.lbl3.text='latitude = '+" "+ lat
        
        
        z = '"longitude":'
        y = locf.find(z)
        y1 = y+12
        y2 =locf.find(',', y)
        long = locf[y1:y2]
        self.root.ids.lbl4.text='longitude= '+" "+ long
    
        fn=self.root.ids.fielden.text
        pop= fn+'/'+self.root.ids.fielde.text
        fn= fn+'.html'

        def map(lat, long, n):
            c= folium.Map(location=[lat, long],zoomstart=20)
            folium.Marker([lat, long], popup=pop).add_to(c)
            c.save(n)
            self.root.ids.lbl5.text='map saved in /storage/emulated/0/{0}'.format(n)
            
Test().run()