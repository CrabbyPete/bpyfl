import pdb
import json
import base64
import iso8601
import time
import settings

from django.shortcuts               import  render_to_response
from django.template                import  RequestContext
from django.views.decorators.csrf   import  csrf_protect

from spreadsheet                    import SpreadSheet
from datetime                       import timedelta
from xmlparse                       import parse

import contextio as c

context_io = c.ContextIO( consumer_key    = settings.CONTEXTIO['CONSUMER_KEY'],
                          consumer_secret = settings.CONTEXTIO['CONSUMER_SECRET']
                        )

def get_gmail( user, password ):
    if not settings.RUN_LOCALLY:
        account = context_io.get_accounts( email = 'webpage@bpyfl.org')[0]
        messages = account.get_messages()
    else:
        messages = []

    notices = []
    for message in messages:
        body = message.get_body()[0]
        gtime = time.gmtime( float( message.date ))
        date = time.strftime("%B %d %Y %H:%M:%S", gtime)
        notices.append({'Subject':message.subject,
                        'Date':date,
                        'text':body['content'],
                        'id':message.email_message_id })
    return notices

def home( request ):
    """ The homepage
    """
    notices = get_gmail( 'webpage@bpyfl.org', 'bergen passaic' )
    return render_to_response('index.html', {'notices':notices},
                               context_instance=RequestContext(request))


def teams( request ):
    return render_to_response('teams.html', {},
                               context_instance=RequestContext(request))

@csrf_protect
def schedule( request ):
    spreadsheet = SpreadSheet( settings.GOOGLE['email'],
                               settings.GOOGLE['password'],
                               'results2013'
                             )

    if request.method == 'POST':
        town = request.POST['town']
        level = request.POST['level']
    else:
        town =  'all'
        level = 'A1'

    worksheet = spreadsheet.get_worksheet_byname('results2013',level)
    results = worksheet.get_rows()

    if town != 'all':
        games = []
        for game in results:
            if town in game.values():
                games.append(game)
    else:
        games = results


    return render_to_response('schedule.html', {'games':games},
                               context_instance=RequestContext(request))

def standings ( request ):
    return render_to_response('standings.html', {},
                               context_instance=RequestContext(request))
def officers( request ):
        return render_to_response('officers.html', {},
                               context_instance=RequestContext(request))