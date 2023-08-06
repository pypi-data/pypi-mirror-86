from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models import CMSPlugin
from .models import *
from django.conf import settings
from django.shortcuts import render
from pma_python import core, control
import requests
from .models import Setting
from .models import Slide
from django import template



class Slides(CMSPluginBase):

    # form = SlidesAdminForm
    name = 'Pathomation slide'
    model = Slide
    render_template = "slides/_slides.html"
    text_enabled = True
    change_form_template = "slides/_custom.html"
    cache= True



    def render_change_form(self, request, context, *args, **kwargs):


        def user():
            try:
                for x in Setting.objects.all():
                    return x.PMACoreUsername
            except:
                pass

        def password():
            try:
                for x in Setting.objects.all():
                    return x.PMACorePassword
            except:
                pass

        user = user()
        password = password()



        headers = {
            'Accept': 'application/json',
        }

        data = {
            'grant_type': 'password',
            'client_id': '6',
            'client_secret': '9APfPpHZMoDKe6ECVYweIrAaopFXVqOSlsrfNGam',
            'username': user,
            'password': password,
            'scope': '*'
        }

        auth= requests.post('https://myapi.pathomation.com/oauth/token', headers=headers, data=data)

        try:
            accestoken =auth.json()['access_token']
        except:
            accestoken = ""

        headers2 = {
            'Accept': 'application/json',
            'Authorization': "Bearer " + accestoken,
        }

        params2 = (
            ('caller', 'Plugin Django'),
        )


        response = requests.get('https://myapi.pathomation.com/api/v1/authenticate?caller=Plugin Django', headers=headers2)


        try:
            folder = response.json()['folder']
            selected_nodes = response.json()['selected_nodes'][0]['Uri'] + "/"
            session_ID = response.json()['session_id']
        except:
            folder = ""
            selected_nodes = ""
            session_ID = ""


        sessionID = session_ID
        link = selected_nodes


        self.change_form_template = 'slides/_custom.html'
        extra = {'link': link, 'user': user, 'password': password, 'sessionID': sessionID, 'folder': folder}
        context.update(extra)
        return super(Slides, self).render_change_form(request, context, *args, **kwargs)




    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['osm_data'] = self.get_dynamic_info()
        return super(Slides, self).change_view(
            request, object_id, form_url, extra_context=extra_context)


    def render(self, context, instance, placeholder):
        def user():
            try:
                for x in Setting.objects.all():
                    return x.PMACoreUsername
            except:
                pass

        def password():
                try:
                    for x in Setting.objects.all():
                        return x.PMACorePassword
                except:
                    pass

        user = user()
        password = password()



        headers = {
            'Accept': 'application/json',
        }

        data = {
            'grant_type': 'password',
            'client_id': '6',
            'client_secret': '9APfPpHZMoDKe6ECVYweIrAaopFXVqOSlsrfNGam',
            'username': user,
            'password': password,
            'scope': '*'
        }

        auth= requests.post('https://myapi.pathomation.com/oauth/token', headers=headers, data=data)

        try:
            accestoken =auth.json()['access_token']
        except:
            accestoken = ""

        headers2 = {
            'Accept': 'application/json',
            'Authorization': "Bearer " + accestoken,
        }

        params2 = (
            ('caller', 'Plugin Django'),
        )


        response = requests.get('https://myapi.pathomation.com/api/v1/authenticate?caller=Plugin Django', headers=headers2)


        try:
            folder = response.json()['folder']
            selected_nodes = response.json()['selected_nodes'][0]['Uri'] + "/"
            session_ID = response.json()['session_id']
        except:
            folder = ""
            selected_nodes = ""
            session_ID = ""


        sessionID = session_ID
        link = selected_nodes

        context.update({
            'instance': instance,
            'slides': Slide.objects.all(),
            'placeholder': placeholder,
            'link': link,
            'sessionID': sessionID,



        })

        return context

    def icon_alt(self,instance):
        return u'Slide: %s' %instance







plugin_pool.register_plugin(Slides)

