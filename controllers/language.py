import string

# NOte the existence of languageList!=None means this is part of dictinary interface
languageList=language

def index():
    words=dblanguage(dblanguage.Dharug.id>0).select( orderby=dblanguage.Dharug.English)

    return dict(words=words)


#FIXME language dependant
import os
import ftfy

def fix_word(word):

    word.Comment=fix_bad_unicode(word.Comment.strip())
    if word.dialect!="" and word.dialect.find(',')<0:
                colour=db(db.dialect.name==word.dialect).select()
                if colour: word.color=colour[0].color
                else: word.color='black'
    else:
                word.color='black'
    return word

def translateunicode():
    s=None
    t=None
    if (request.vars):
        text=request.vars.text_input
        s=unicode(text,'UTF-8')
        t=ftfy.fix_text_encoding(s)
    return dict(string=s, translate=t)

def  fix_bad_unicode(text):
    # creates error s=text.encode(encoding='UTF-8',errors='strict')
    s=ftfy.fix_text_encoding(text)
    return s

def search(orderbys, searchterm,typequery, dialect, extra):
    words=None
    queryexact=""
    if typequery=="English":
        queryexact=(dblanguage.Dharug.Search_English==searchterm)|dblanguage.Dharug.Search_English.startswith(searchterm+' ;')|dblanguage.Dharug.Search_English.startswith(searchterm+',')|(dblanguage.Dharug.Search_English.contains("; "+searchterm+' ' ))|(dblanguage.Dharug.Search_English.endswith("; "+searchterm))
    else:
        queryexact= dblanguage.Dharug.Language_Word==searchterm
    query=queryexact
    if extra!="Exact":
        if typequery=="English":
            query= dblanguage.Dharug.Search_English.contains(searchterm)
        else:
            query= dblanguage.Dharug.Language_Word.contains(searchterm)
    if dialect!="All":
        if dialect=="Dharawal":
            query=query&(dblanguage.Dharug.dialect=="dharawal")
        else:

            query=query&(dblanguage.Dharug.dialect!="dharawal")
   #check not uncertain origina
    query = query & (dblanguage.Dharug.uncertain==0)
    words=dblanguage(query).select(orderby=orderbys)
    if extra!="Exact":
        exactwords=dblanguage(queryexact).select(orderby=orderbys)
        words.exclude(lambda r: r in exactwords)
    return words
def wordListJson():
    import json
    try:
            name=request.args[0]
    except:
            name=None
    words=[]


def lesson():
    import json
    try:
        name=request.args[0]
    except:
        name=None
    words=[]

    if name and name!="all":
        page_id=db(db.plugin_wiki_page.slug==name).select()
        try:
                wl=wordList(page_id[0].id)
       # logging.warn(wl)
        except:
                return response.json (None) 

    else: #full list not lesson
        wl=wordDict()
   
    if wl:
        for word in wl['words']:
            word,examples=read_word(word)

            condition = dblanguage.DharugExamples.language_id==word.id

            #examples=dblanguage(condition).select(dblanguage.DharugExamples.ALL)
            exampleList=[]
            for example in examples:
                  try:
                                exampleList.append({"ex": example.Language, "ft": example.English})
                  except Exception:
                                pass
            if word.uncertain>0 : pub=False
            else: pub=True
            if word.Language_Word:
                wordTrans={"def": word.English , "examples":exampleList,"ge": word.Search_English, "ps": word.Part_of_Speech}
                words.append({"initial": word.Language_Word[0].lower(),"lx":word.Language_Word,"image": word.Image, "sound": word.Sound,"lxc": word.Comment, "publish": pub , "ge":word.English, "senses": wordTrans, "dialect": word.dialect})
        return response.json (words)
    else: 
        wl=None
        name=name.replace(" ","_")
        words=dblanguage(dblanguage.Dharug.Lesson.name==name).select()
        rows = [word for word in words]
        #cols = [word for word in words.description]
		
    wordjson=[]
    for row in words:
        wordjson.append(row)

    return dict(wordlist=wordjson)


def dictionary():
    names = db(db.dialect.id>0).select(db.dialect.name)
    numerics=[]
    dialectid=None
    alphanumeric="Exact"
    sort=request.vars['type']
    if request.args:
        order=request.args[0]
    else:
        order=sort
        orderbys=dblanguage.Dharug.Search_English
    if order==language:
        orderbys=dblanguage.Dharug.Language_Word
    elif order=='Category':
        orderbys=dblanguage.Dharug.Category

    searchterms=request.vars['query']
    dialectid="All"

    if searchterms=="None":
        searchterms=""
    try:
        alphanumeric=request.vars['numeric']
        dialectid=request.vars['dialect']
    except:
        dialectid="All"
        pass

    exact=alphanumeric
    dialect="All"
    wordlist=[]
    if dialectid: 
        for name in names:
            if dialectid in name.name:
                dialect=name.name
    if searchterms and searchterms!="":
        response.start=False	
        wordlist =search(orderbys,searchterms,sort,dialect,alphanumeric)
        numerics=['Exact','Related']
        exact="Exact"
        if (not wordlist) or wordlist==[]:
            wordlist =search(orderbys, searchterms,sort,dialect,'Related')
    else:
        wordlist=[]
        if (not(sort)):
            sort="English"
        if (not alphanumeric or alphanumeric==""):
            alphanumeric='A'
        if(sort=='English'):
            numerics=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
            condition = dblanguage.Dharug.Search_English.startswith(alphanumeric.lower())|dblanguage.Dharug.Search_English.startswith('-'+alphanumeric.lower())

            wordlist=dblanguage(condition).select(orderby=orderbys)
        elif (sort=="Category"):
            numerics=["people","animal"]
            if (not alphanumeric in numerics):
                alphanumeric="people"
        else:
            numerics=['A','BA','BE','BI', 'BU','D','J','L','M','N','NG','NY','O','S','WA', 'WE', 'WI', 'WU','YA','YE','Yi','YU']
            if (not alphanumeric in numerics):
                alphanumeric="A"
                condition = dblanguage.Dharug.Language_Word.startswith(alphanumeric.lower())|dblanguage.Dharug.Language_Word.startswith('-'+alphanumeric.lower())
                if alphanumeric=='N':
                    c2= (dblanguage.Dharug.Language_Word.startswith("na"))
                    c3=(dblanguage.Dharug.Language_Word.startswith("ne"))
                    c4=(dblanguage.Dharug.Language_Word.startswith("ni"))
                    c5= (dblanguage.Dharug.Language_Word.startswith("nu"))
                    wordlist=dblanguage(c2|c3|c4|c5).select(dblanguage.Dharug.ALL, orderby=orderbys)
                    wl2=dblanguage(c3).select(dblanguage.Dharug.ALL, orderby=orderbys)
                else:
                    wordlist=dblanguage(condition).select(orderby=orderbys)
    for word in wordlist:
        read_word(word)
    if order=='Dialect':
        #this is so cool
        wordlist=sorted(wordlist,key= lambda word: word['dialect'])
    else:
        #sort words by sound - only added now
    	wordlist=sorted(wordlist,key=lambda word: word['Sound'],reverse=True)


    top_message = language +" Dictionary"
    w = db.plugin_wiki_page
    page = w(slug='usedictionary')    
    if page: pageteaser=page.summary
    else: pageteaser=""
    return dict(start=response.start, page=pageteaser, dialect= dialect, sort=sort, exact=exact, names=names, query=searchterms, words=wordlist, top_message=top_message, numeric= alphanumeric, numerics=numerics)


def wordList(topic_id):
    wordlist=None
    try:
         lesson_id=db(db.Lesson.page_id==topic_id).select()
    except:
        try:
            lesson_id=db(db.Lesson.name==topic_id).select()
        except:
            pass
    for lesson in lesson_id:
        page_id=lesson['id']
    wordlists=db(db.Lesson_word.lesson_id==page_id).select()
    wordlist=[]
    for word in wordlists:
        wordfull=dblanguage(dblanguage.Dharug.id==word.language_id).select()
        wordlist.append(wordfull[0])
    return dict(words=wordlist)
def wordDict ():

     wordlist=None
     try:
        wordlist=dblanguage(dblanguage.Dharug.id>0).select()
     except:
         pass
     return dict(words=wordlist)

def translate_old():
    word = request.args(0) or ''
    if not request.args:
        redirect(URL(r=request, c='language' ,f='index'))
    lang= request.args(1)
    if not lang:
        lang=language
        words=(languagewords.id>0)(languagewords.language==word).select( orderby=languagewords.Search_English)

    elif lang=='English':
        words=(languagewords.id>0)(languagewords.Search_English==word).select( orderby=languagewords.language)
	
    return  dict(words=words)

def translate():
     import json
     try:
        searchterm=request.args[0]
        lang=request.args[1]
     except:
        lang="English"
        pass

     if searchterm:
         if lang=="English" :
                 query=(dblanguage.Dharug.Search_English==searchterm)|dblanguage.Dharug.Search_English.startswith(searchterm+' ;')|dblanguage.Dharug.Search_English.startswith(searchterm+',')|(dblanguage.Dharug.Search_English.contains("; "+searchterm+' ' ))|(dblanguage.Dharug.Search_English.endswith("; "+searchterm))
         words=[]
         page_id=dblanguage(dblanguage.Dharug.English==name).select()
         #logging.warn(page_id)
         wl=wordList(page_id[0].id)
         #logging.warn(wl)
         if wl:
                 for word in wl['words']:
 
                         words.append({"English":word.English,"Language":word.Language})
         else: wl=None
         wordlist=[]
         for row in words:
                 word_json=row
                 wordlist.append(word_json)
 
     return dict(wordlist=wordlist)


def dictionarysort():
    sort=request.args(0)
    if(sort==None):sort='English'
    wordlist=dblanguage(dblanguage.Dharug.Category==sort).select(dblanguage.Dharug.ALL, orderby=dblanguage.Dharug.Language_Word)
    for word in wordlist:
        read_word(word)
    top_message = language +" List sorted for "+sort
    return dict(words=wordlist, top_message=top_message)


def view_word():
    word_id=request.args(0)
    words=dblanguage.Dharug
    word, examples=read_word(dblanguage.Dharug(dblanguage.Dharug.id==word_id))
    word=fix_word(word)
    link=None
    if not auth.has_membership(auth.id_group('student')):

        link = URL(r=request, c='language' ,f='edit_word', args=word_id)

    related = []
    if word.RelatedWord:

        relates=word.RelatedWord.split(',')
        for relate in relates:
                relate=relate.strip()
                relateid=dblanguage.Dharug(dblanguage.Dharug.Language_Word.like( "%%%s%%" %relate, case_sensitive=False))
                if relateid:
                        relateid=relateid.id
                        relate=A(relate,_target="_blank",_href="/language/view_word/"+str(relateid))
                related.append(relate)
    relatenew=dblanguage(dblanguage.Dharug.English.like( "%%%s%%" %word.English, case_sensitive=False))
    if relatenew:
            related.append(BR()+"With similar English translation:")
            for relate in relatenew.select():
                if str(relate.id)!=word_id:
                    relateid=relate.id
                    relate=A(relate.Language_Word,_target="_blank",_href="/language/view_word/"+str(relateid))
                    related.append(relate)
    logging.warn(word.Sound)
    return dict(link = link, word=word, related=related,exampleSentences=examples, language=language )

def view_word_popup():
    word_id=request.args(0)
    words=dblanguage.Dharug
    word,examples =read_word(dblanguage.Dharug(dblanguage.Dharug.id==word_id))
    word=fix_word(word)

    link = URL(r=request, c='language' ,f='edit_word', args=word_id)
    return dict(link = link, word=word)



def category():

    word = request.args(0) or ''
    if not request.args:
        redirect(URL(r=request, c='language' ,f='index'))
    category= request.args(1)

    if languagewords:
        words=(languagewords.id>0)(languagewords.Category==category).select( orderby=languagewords.language)

    return  dict(words=words)

@auth.requires_login()
def create_word():
    if not request.args:
        redirect(URL(r=request,c='language', f='index'))
    create_word = request.args(0)
    name=create_word.replace('_',' ')

    word=languageword(Search_English==name)
    word=languageword(Search_English==name)
    form = crud.create(dblanguageword)
    return dict(word=word, form=form)

    
# edit clws
@auth.requires_login()
def edit_word():
    word_id=request.args(0)
    try:
        integer=True
        word_id=int(word_id)
    except :
        integer=False
        word_id=0
    try:
        name=word_id.replace('_',' ')
    except:
        name = ""
    w = dblanguage.Dharug
    if integer:
        word = w(id=word_id)
    else:
        word = w(Language_Word=name)
    if not word:
        word = w.insert(Language_Word=name)
    word, examples =read_word(word)
    if word: 
        word_id=word.id
        if auth.has_membership(auth.id_group('developer')):

            form = crud.update(w, word, deletable=True, onaccept=crud.archive,
                       next=URL(r=request,c='language', f='view_word',args=word_id))
        else:
            form = crud.update(w, word, deletable=False, onaccept=crud.archive,
                       next=URL(r=request,c='language', f='view_word',args=word_id))
    return dict(form=form,word=word,examples=examples)

def read_word(word):
    #call from all word processing - collects all information on word
    try:
        if word.Sound:
            pass
    except:
        word.Sound=""
    wordTypes=['male','female']
    if word.SoundFile: word.Sound=word.SoundFile
    if (not word.SoundFile or word.SoundFile==''or word.SoundFile==" "):
        for link in wordTypes:
            parts= word.Language_Word.split(',')
            word.Soundfile=parts[0]+".mp3"
            if os.path.exists('applications/'+language+'/uploads/media/sounds/'+link+'/'+word.Soundfile):
                        word.Sound+=link+'; '+URL(r=request, c='default',f='sounds/'+link, args=word.Soundfile)+";"
            else:
#if exists wav and mp3 use one
                word.Soundfile=parts[0]+".wav"
                if os.path.exists('applications/'+language+'/uploads/media/sounds/'+link+'/'+word.Soundfile):
                    word.Sound+=link+'; '+URL(r=request, c='default',f='sounds/'+link, args=word.Soundfile)+";"
    if word.Sound=="":
        word.Sound=";"  #add the voice as empty
    if (word.Image): word.Image=word.Image.strip()
    word.ImageLink=word.Image
    if word.Image==None or word.Image=="":word.Image=word.Search_English
    end=word.Image.find(';');
    if end>0:word.Image=word.Image[0:end]
    word.Image=word.Image.strip('(generic)')
    word.Image.strip()
    word.Image=word.Image.replace(', ','_')

    word.Image=word.Image.replace(' ','_')
    word.Image.strip()
    word.ImageLink=""
    if(os.path.exists('applications/'+language+'/uploads/media/images/'+word.Image+'.gif')):
                word.ImageLink = URL(r=request, c='default',f='images', args=word.Image+'.gif')
    elif(word.ImageLink==""):
        if(os.path.exists('applications/'+language+'/uploads/media/images/'+word.Image+'.jpg')):
            word.ImageLink = URL(r=request, c='default',f='images', args=word.Image+'.jpg')
        else: word.Image=""
    condition = dblanguage.DharugExamples.language_id==word.id
    examplelist=dblanguage(condition).select(dblanguage.DharugExamples.ALL)
    colour="black"
#remove ','
    if word.dialect.strip()=="": word.dialect="All"
# if only one dialect
    if word.dialect!="" and word.dialect.find(',')<0:
        colour=db(db.dialect.name==word.dialect).select()
        if colour: word.color=colour[0].color
        else: word.color='black'
    else:
        word.color='black'
    return word, examplelist
