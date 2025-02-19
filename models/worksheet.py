import re, os, urllib



def wsread_question(page_body, page):
    return page

def wordlist(topic_id):
    wordlist = None
    try:
        wordlist=db(db.topics.page_id==topic_id).select()
    except:
        pass
    return dict(words=wordlist)

def wsread_page(page):
    logging.warn("Running Wsread_page")
    page_body = page.body
    worksheet = db(db.plugin_wiki_tag.name=="WorkSheet").select().first()
        #FIXME
    if(worksheet != None):
    #FIXME
            if(page.tags=="|"+str(worksheet.id)+"|"):
            #replace Answer with textbox
                return page.body
        #Add all sound exampels at once
    SoundLinks=[]
    #transcription ifrst
    transcription=db(db.elan.resource_id>0).select(db.elan.ALL, orderby=db.elan.speech)
    #logging.warn(page_body)
    if transcription:
            lastword=transcription[0].speech
                    #check for repeats
            for trans in transcription:
#remove repeatd phrses in one text
                if trans.speech!=lastword:
                    if trans and trans.speech!='' and trans.speech!="?":
                        if trans.speech in page_body:
                #get resource file
                            transwav= db.resources(db.resources.id==trans.resource_id)
                            filename=transwav.name+"#t="+str(trans.start)+","+str(trans.end)
                            SoundLinks.append({'text':trans.speech,'sound':filename,'type':'trans'})
            lastword=trans.speech
   
#file examples
    #examples=os.listdir('applications/'+language+'/uploads/media/sounds')
    examples=[]

    for path, subdirs, files in os.walk('applications/'+language+'/uploads/media/sounds'):
        for name in files:
            name = os.path.split(name)[1]
            examples.append(name)
            # examples.sort(lambda x,y: -cmp(len(x), len(y)))
    examples=sorted(examples,key=lambda x: len(x))

    for example in examples:
        text=os.path.splitext(example)[0]
        if text  in page_body:
                 SoundLinks.append({'text':text,'sound':str(example), 'type':'file'})

    r = re.compile(r'(<s.*?>|<a.*?<\/a>|<img.*?>)')
    SoundLinks=sorted(SoundLinks, key=lambda k: k['text'])
    k=len(SoundLinks)

    if k>0:
        #logging.warn(page_body)
        parags=r.split(page_body)
        paragraphs=""
        item = SoundLinks[0]
        for parag in parags:
          if parag:

            if parag.startswith('<a') or parag.startswith('<source') or parag.startswith('<src=') or parag.startswith('<img '):
                paragraphs+=parag
            else:
                i=0
                while i<k:
                    item=SoundLinks[i]
                    while i<k-1 and  SoundLinks[i+1]["text"]==SoundLinks[i]["text"]:
                                #get most recent version
                                i += 1
                                item=SoundLinks[i]

                    #find pargraphs in site

                    newparags=re.split(r'(<a.*?<\/a>)',parag)

                    parag=""
                    Info=""
                    for newparag in newparags:
                        if newparag.startswith('<a') :
                            parag+=newparag
                        else:
                            if re.search(r'\W'+item["text"]+r'\W',newparag):
                                if item["type"]=="file":
                                    Sound = urllib.parse.unquote(URL(c="default", f="filedown/media/sounds", args=item["sound"]))
                                else:
                                    Sound = urllib.parse.unquote(URL(c="default", f="filedown/file", args=item["sound"]))
                                if Info=="":
                                        Info="DHTMLSound('"+str(Sound)+"','"+str(item["text"])+"');"

                                else:
                                    Info += "DHTMLSound('" + str(Sound) + "','" + str(item["text"]) + "');"
                                newparag=re.sub(r'(\W)'+item["text"]+r'(\W)', r'\1<a href="#" onMouseOver="'+str(Info)+'" > '+item["text"]+r' </a>\2',newparag)

                            parag+=newparag
                    i+=1

                paragraphs+=parag


        page_body=paragraphs

    #parser = langHTMLParser()

    #parser.feed(page_body)
    #words=parser.read_string()
    # bypass     words=page_body    
    #page_body=words

    #  else do wiki pages  last
    query = (db.plugin_wiki_page)
    pages=db(query).select(orderby="title DESC")
    
    #for pagetitle in pages:
     #       if(pagetitle.title!=page.title):
      #          page_title=re.sub('_',' ',pagetitle.title)
       #         pCap  = re.compile('\\b'+page_title+'\\b')
        #        pSmall = re.compile('\\b'+page_title.lower()+'\\b')
         #       words=re.split(r"(<s.*?>|<a.*?</a>)",page_body)
          #      i=0
           #     page_body=""
            #    while i<len(words):
             #       if words[i].startswith('<a') or words[i].startswith('<s'):
              #          pass
               #     else:
                #            substitute = '<a href="/plugin_wiki/page/'+pagetitle.title+'">'+page_title+'</a>'
                 #           words[i]= pCap.sub(substitute,words[i])
                  #          if(pCap!=pSmall):
                   #                 substitute = '<a href="/plugin_wiki/page/'+pagetitle.title+'">'+page_title.lower()+'</a>'
                    #                words[i] = pSmall.sub(substitute,words[i])
                     #       i+=2
    #            for word in words:
     #               page_body+=word
    return page_body

def answer(answer):
        w = db.plugin_wiki_page
        page = w(slug=request.arg[0])
        return dict(answer=answer, page=page) 

    
def wsimage():
        subdirectory = '/uploads/media/images/'# directory
        filename = request.args(0)
        fullpath = os.path.join(subdirectory, filename)
        if request.args(1):
                filenameadd = request.args(1)
                fullpath = os.path.join(fullpath, filenameadd)
        response.stream(os.path.join(request.folder,fullpath))
    
