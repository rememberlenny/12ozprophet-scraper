#!/usr/bin/env python
import scraperwiki
import requests
import lxml.html    

# Constants
numberofposts = 7844
post_iteration = 0
user_iteration = 0
image_iteration = 0

# One-time use
global savedusername, date_published, post_image

savedusername = 'null'
dateremovetitle = """N   E   W      Y   O   R   K      C   I   T   Y - """
dateremovere = """Re:"""
ignoredimages = ['images/12oz/statusicon/post_old.gif','images/12oz/buttons/collapse_thead.gif','images/12oz/statusicon/post_new.gif','images/12oz/reputation/reputation_pos.gif','images/12oz/reputation/reputation_highpos.gif','images/icons/icon1.gif','images/12oz/buttons/quote.gif','clear.gif', 'images/12oz/attach/jpg.gif','images/12oz/reputation/reputation_neg.gif','images/12oz/reputation/reputation_highneg.gif','images/12oz/statusicon/post_new.gif']
for i in range(1, numberofposts):

    html = requests.get("http://www.12ozprophet.com/forum/showthread.php?t=128783&page="+ str(i)).content
    dom = lxml.html.fromstring(html)

    print 'Page: ' + str(i)
    for posts in dom.cssselect('#posts'):
        for table in posts.cssselect('table'):
            
            try:
                username = table.cssselect('a.bigusername')[0].text_content()
                
                if username != savedusername:
                    if username != 'null':
                        savedusername = username
            except IndexError:
                username = 'null'
                
            try:
                post_iteration = post_iteration + 1 #my unique post id
                postdate = table.cssselect('td.alt1 div.smallfont')[0].text_content()
                postdate = postdate.replace(dateremovetitle, '')
                postdate = postdate.replace(dateremovere, '')
                postdate = postdate.strip()
                date_published = postdate
                # print '---'
                # print savedusername +' '+ postdate + ', ID: ' + str(iteration)
            except IndexError:
                postdate = 'null'
            
            for img in table.cssselect('img'):
                imagesrc = img.get('src')
                imagematch = 'false'
                
                for image in ignoredimages:
                    if image == imagesrc:
                        imagematch = 'true'
            
                if imagematch != 'true':
                    image_iteration = image_iteration + 1
                    post_image = imagesrc            
            
                
                    post = {
                        'image_id': image_iteration,
                        'image_url': post_image,
                        'post_id': post_iteration,
                        'user': savedusername,
                        'date_published': date_published,
                    }
                    print post
                
                    scraperwiki.sql.save(['image_id'], post)

