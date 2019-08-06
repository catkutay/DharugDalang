# This file was developed by Massimo Di Pierro
# It is released under BSD, MIT and GPL2 licenses

###################################################
# required parameters set by default if not set
###################################################
tag=None

DEFAULT={
    'editor' : False,
    'mode'   : 'html',    # 'markmin' or 'html' for wysiwyg editor
    'level'  : 3,            # 1 - wiki only, 2 - widgets enables, 3 - remplate render enabled
    'migrate': False,         # set to False in production
    'theme'  : 'cupertino', # the jquery-ui theme, mapped into plugin_wiki/ui/%(theme)s/jquery-ui-1.8.1.custom.css
    'widgets' : 'all',       # list of widgets to be made available
    'authorize_attachments' : False # shoudl attachment be restricted to the page?

}
if auth.user:
   DEFAULT = {
    'editor' : auth.user and auth.user.Role_Name=='editor' or auth.user.Role_Name=='teacher' or auth.user_id==1, # if current user a editor?
    'mode'   : 'html',    # 'markmin' or 'html' for wysiwyg editor
    'level'  : 3,            # 1 - wiki only, 2 - widgets enables, 3 - remplate render enabled
    'migrate': False,         # set to False in production
    'theme'  : 'cupertino', # the jquery-ui theme, mapped into plugin_wiki/ui/%(theme)s/jquery-ui-1.8.1.custom.css
    'widgets' : 'all',       # list of widgets to be made available
    'authorize_attachments' : False # shoudl attachment be restricted to the page?
    }


def _():
    """
    the mambo jambo here makes sure that 
    PluginManager.wiki.xxx is also exposed as plugin_wiki_xxx
    this is to minimize Storage lookup
    """
    if not 'db' in globals() or not 'auth' in globals():
        raise HTTP(500,"plugin_wiki requires 'db' and 'auth'")
    from gluon.tools import PluginManager
    prefix='plugin_wiki_'
    keys=dict(item for item in DEFAULT.items() if not prefix+item[0] in globals())
    plugins = PluginManager('wiki',**keys)
    globals().update(dict((prefix+key,keys[key]) for key in keys))
_()


###################################################
# js and css modules required by the plugin
###################################################


##for _f in ['plugin_wiki/jqgrid/css/ui.jqgrid.css',
##           'plugin_wiki/jqgrid/js/i18n/grid.locale-en.js',              
##           'plugin_wiki/jqgrid/js/jquery.jqGrid.min.js',
##           'plugin_wiki/slideshow/jquery.cycle.min.js',
##	   'plugin_multiselect/jquery.dimensions.js',
##	   'plugin_multiselect/jquery.multiselect.js',
##	   'plugin_multiselect/jquery.multiselect.css',
# #          'plugin_wiki/rating/jquery.rating.css',
##           'plugin_wiki/rating/jquery.rating.js',
##           'plugin_wiki/markitup/skins/markitup/style.css',
##	   'plugin_wiki/markitup/sets/markitup/style.css',
##	   'plugin_wiki/elrte-1.3/js/jquery-1.6.1.min.js',
##	   'plugin_wiki/elrte-1.3/js/jquery-ui-1.8.13.custom.min.js',
##	   'plugin_wiki/elrte-1.3/css/smoothness/jquery-ui-1.8.13.custom.css',
##
##	   'plugin_wiki/elrte-1.3/css/elrte.full.css',
##	   'plugin_wiki/elrte-1.3/js/i18n/elrte.en.js',
##	   'plugin_wiki/elrte-1.3/css/elrte.full.css'
##

##]:          
##    response.files.append(URL('static',_f))


def multiselect_widget(f,v):
    import uuid
    d_id = "multiselect-" + str(uuid.uuid4())[:8]
    wrapper = DIV(_id=d_id)
    inp = SQLFORM.widgets.options.widget(f,v)
    inp['_multiple'] = 'multiple'
    inp['_style'] = 'min-width: %spx;' % (len(f.name) * 20 + 50)
    if v:
        v = str(v).split('|')
        opts = inp.elements('option')
        for op in opts:
            if op['_value'] in v:
                op['_selected'] = 'selected'            
    scr = SCRIPT('jQuery("#%s select").multiSelect({'\
                 '"Select Menu %s"});' % (d_id,f.name))
    wrapper.append(inp)
    wrapper.append(scr)
    if request.vars.get(inp['_id']+'[]',None):
        var = request.vars[inp['_id']+'[]']
        var = [var]
        request.vars[f.name] = var
        del request.vars[inp['_id']+'[]']
    return wrapper


###################################################
# required tables
###################################################

db.define_table('plugin_wiki_page',
                Field('slug',
                      requires=(IS_SLUG())),
                Field('title',default='',
                      requires=(IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'plugin_wiki_page.title'))),
                Field('is_public','boolean',default=True),
                Field('worksheet','boolean',default=False),
                Field('summary','text' , default=""),
		Field('body','text',default=''),
                Field('role',db.auth_group,
                      requires=IS_EMPTY_OR(IS_IN_DB(db,'auth_group.id','%(role)s'))),
                Field('tags','text'),
                Field('changelog',default=''),
		Field("is_active", 'boolean', default=True),
                auth.signature,
                format = '%(slug)s', migrate=False)

db.plugin_wiki_page.slug.requires = [IS_NOT_EMPTY(), SlugValidator()]
db.plugin_wiki_page.tags.requires = IS_IN_DB(db, 'plugin_wiki_tag.id', '%(name)s', multiple=True)
db.plugin_wiki_page.created_by.represent = represent_author
db.plugin_wiki_page.tags.widget=multiselect_widget
db.plugin_wiki_page.body.requires=IS_LENGTH(1000000)

db.define_table('plugin_wiki_page_archive',
                Field('current_record',db.plugin_wiki_page),
                db.plugin_wiki_page,
                format = '%(slug) %(modified_on)s', migrate=plugin_wiki_migrate)

db.define_table('plugin_wiki_transcript',
                Field('slug',
                      requires=(IS_SLUG())),
                Field('title',default='',
                      requires=(IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'plugin_wiki_transcript.title'))),
                Field('is_public','boolean',default=True),
		Field('summary',length=500),
                Field('body','text',default=''),
                Field('role',db.auth_group,
                      requires=IS_EMPTY_OR(IS_IN_DB(db,'auth_group.id','%(role)s'))),
                Field('changelog',default=''),
		Field('is_active', 'boolean', default=True),
                auth.signature,
                format = '%(slug)s', migrate=False)

db.plugin_wiki_transcript.slug.requires = [IS_NOT_EMPTY(), SlugValidator()]
db.plugin_wiki_transcript.created_by.represent = represent_author
db.plugin_wiki_transcript.body.requires=IS_LENGTH(1000000)

db.define_table('plugin_wiki_transcript_archive',
                Field('current_record',db.plugin_wiki_transcript),
                db.plugin_wiki_transcript,
                format = '%(slug) %(modified_on)s', migrate=plugin_wiki_migrate)

db.define_table('plugin_wiki_attachment',
                Field('tablename',writable=False,readable=False),
                Field('record_id','integer',writable=False,readable=False),
                Field('name',requires=IS_NOT_EMPTY()),
                Field('filename','upload',requires=IS_NOT_EMPTY(),autodelete=True),
                auth.signature,
                format='%(name)s', migrate=plugin_wiki_migrate)

db.define_table('resources',
                Field('id', 'integer',writable=False,readable=False),
                Field('slug','string',length=50),

                Field('name','upload',requires=IS_NOT_EMPTY(),autodelete=True),
                Field('title','string',length=50),
                Field('file','string',length=100),

                Field('Collected_by','string',length=100),
		        Field('description','string', length=500),
		        Field('type', 'string', length=10),
		        Field('Public','boolean', default=False),
                Field('Active','boolean', default=False),
                Field('Teaching','boolean', default=False),
                migrate=plugin_wiki_migrate)

db.define_table('elan',
                Field('id', 'integer',writable=False,readable=False),
                Field('resource_id','integer',length=11,requires=IS_IN_DB(db,'resources.id')),

                Field('speech','string',length=500),
                Field('translation','string',length=500),
                Field('start','float',length=100),

                Field('end','float',length=100),
                migrate=plugin_wiki_migrate)


db.define_table('plugin_wiki_comment',
                Field('tablename',
                      writable=False,readable=False),
                Field('record_id','integer',
                      writable=False,readable=False),
                Field('body',requires=IS_NOT_EMPTY(),label='Your comment'),
                auth.signature,
                migrate=plugin_wiki_migrate)

db.define_table('plugin_wiki_images',
                Field('id','integer',writable=False,readable=False),
		        Field('name',requires=IS_NOT_EMPTY()),
                Field('filename','upload',requires=IS_NOT_EMPTY(),autodelete=True),
                auth.signature,
                format='%(name)s', migrate=plugin_wiki_migrate)


db.define_table('plugin_wiki_tag',
                Field('name',requires=IS_NOT_IN_DB(db,'plugin_wiki_tag.name')),
                Field('parent',requires=(IS_IN_DB(db,'plugin_wiki_tag.name') )),
		        auth.signature,
                format='%(name)s', migrate=plugin_wiki_migrate)


db.define_table('plugin_wiki_link', 
                Field('tag',db.plugin_wiki_tag),   
                Field('table_name'),
                Field('record_id','integer'), migrate=plugin_wiki_migrate)


db.define_table('plugin_wiki_rating',
                Field('tablename'),
                Field('record_id','integer'),
                Field('rating','double'),
                Field('counter','integer'))
   
   
db.define_table('plugin_wiki_rating_aux',
                Field('master',db.plugin_wiki_rating),
                Field('rating','double'),                
                Field('created_by',db.auth_user))
   
   
###################################################
# widgets embeddable in wiki pages
###################################################
class PluginWikiWidgets(object):    
    """
    todo:
    toc
    in-place-wiki-edit
    permission managemnt
    voting plugin
    """

    ###############################################
    # basic crud widgets (no ajax)
    ###############################################

    @staticmethod
    def read(table,record_id=None):
        """
        ## read and display a record
        - ``table`` is the name of a table
        - ``record_id`` is a record number
        """
        if not record_id: record_id=request.args(-1)
        #if not record_id.isdigit: return XML('no data')
        if (table!="ALC" and table !="CLW"):
            return crud.read(db[table],record_id)
        else:
            return crud.read(dblanguage[table],record_id)
    @staticmethod
    def _set_field_attributes(table,readonly_fields='',hidden_fields='',default_fields=''):
        if readonly_fields: 
            for f in readonly_fields.split(','):
                db[table][f.strip()].writable=False
        if hidden_fields: 
            for f in hidden_fields.split(','):
                db[table][f.strip()].writable=False
                db[table][f.strip()].readable=False                
        if default_fields:
            for f in default_fields.split(','):
                (key,value) = f.split('=')
                db[table][key.strip()].default=value.strip()

    @staticmethod
    def create(table,message='',next='',readonly_fields='',
               hidden_fields='',default_fields=''):
        """
        ## display a record create form
        - ``table`` is the name of a table
        - ``message`` is a the message to be displayed after record is created
        - ``next`` is where to redirect, example "page/index/[id]"
        - ``readonly_fields`` is a list of comma separated fields
        - ``hidden_fields`` is a list of comma separated fields 
        - ``default_fields`` is a list of comma separated "fieldname=value"
        """
        PluginWikiWidgets._set_field_attributes(table, readonly_fields,hidden_fields,default_fields)
        return crud.create(db[table],message=message,next=next)

    @staticmethod
    def update(table,record_id='',message='',next='',
               readonly_fields='',hidden_fields='',default_fields=''):
        """
        ## display a record update form
        - ``table`` is the name of a table
        - ``record_id`` is he record to be updated or {{=request.args(-1)}}
        - ``message`` is a the message to be displayed after record is created
        - ``next`` is where to redirect, example "page/index/[id]"
        - ``readonly_fields`` is a list of comma separated fields
        - ``hidden_fields`` is a list of comma separated fields
        - ``default_fields`` is a list of comma separated "fieldname=value"
        """

        PluginWikiWidgets._set_field_attributes(table, readonly_fields,hidden_fields,default_fields)
        if not record_id: record_id=request.args(-1)
        #if not record_id.isdigit(): record_id=None
        return crud.update(db[table],record_id,message=message,next=next)

    @staticmethod
    def select(table,query_field='',query_value='',fields=''):
        """
        ## Lists all records in the table
        - ``table`` is the name of a table
        - ``query_field`` and ``query_value`` if present will filter records by query_field==query_value 
        - ``fields`` is a list of comma separate fields to be displayed
        """
        query=None
        if query_field:
            query = db[table][query_field]==query_value
        if fields:
            fields=['%s.%s' % (table,f.strip()) for f in fields.split(',')]
        else:
            fields=None
        return crud.select(db[table],query=query,fields=fields,headers='fieldname:capitalize')

    @staticmethod
    def search(table,fields=''):
        """
        ## A Widgets for selecting records
        - ``table`` is the name of a table
        - ``fields`` is a list of comma separated fields to be displayed
        """
        if fields:
            fields=['%s.%s' % (table,f.strip()) for f in fields.split(',')]
        else:
            fields=None
        search, results = crud.search(db[table])
        if not results: results=T('no results')
        else: results=SQLTABLE(results,fields=fields,headers='fieldname:capitalize')
        return DIV(search,results)

    ###############################################
    # advanced crud (jqgrid with ajax search)
    ###############################################
    @staticmethod    
    def jqgrid(table,fieldname=None,fieldvalue=None,col_widths='',
               colnames=None,_id=None,fields='',
               col_width=80,width=700,height=300,id=None):
        """
        ## Embed a jqGrid plugin
        - ``table`` is the table name
        - ``fieldname``, ``fieldvalue`` are an optional filter (fieldname==fieldvalue)
        - ``_id`` is the "id" of the DIV that contains the jqGrid
        - ``fields`` is a list of columns names to be displayed
        - ``colnames`` is a list of column headers
        - ``col_width`` is the width of each column (default) 
        - ``height`` is the height of the jqGrid
        - ``width`` is the width of the jqGrid
        """
        from gluon.serializers import json
        _id = _id or 'jqgrid_%s' % table
        if not fields:
            fields = [x.strip() for x in db[table].fields if db[table][x.strip()].readable]
        elif isinstance(fields,str):
            fields = [x.strip() for x in fields.split(',')]
        else:
            fields = fields
        if col_widths:
            if isinstance(col_widths,(list,tuple)):
                col_widths = [str(x) for x in col_widths]
            else:
                col_widths = [x.strip() for x in col_widths.split(',')]
        if width=='auto':
            width=sum([int(x) for x in col_widths])
        elif not col_widths:
            col_widths = [col_width for x in fields]
        if isinstance(colnames,str):
            colnames = [x.strip() for x in colnames.split(',')]
        else:
            colnames = [(db[table][x].label or x) for x in fields]
        colmodel = [{'name':x,'index':x, 'width':col_widths[i], 'sortable':True}\
                        for i,x in enumerate(fields)]
        callback = URL('plugin_wiki','jqgrid',
                       vars=dict(tablename=table,
                                 columns=','.join(fields),
                                 fieldname=fieldname or '',
                                 fieldvalue=fieldvalue,
                                 ),
                       hmac_key=auth.settings.hmac_key,
                       salt=auth.user_id
                       )
        script="""
jQuery(document).ready(function(){jQuery("#%(id)s").jqGrid({ url:'%(callback)s', datatype: "json", colNames: %(colnames)s,colModel:%(colmodel)s, rowNum:10, rowList:[20,50,100], pager: '#%(id)s_pager', viewrecords: true,height:%(height)s});jQuery("#%(id)s").jqGrid('navGrid','#%(id)s_pager',{search:true,add:false,edit:false,del:false});jQuery("#%(id)s").setGridWidth(%(width)s,false);jQuery('select.ui-pg-selbox,input.ui-pg-input').css('width','50px');});
""" % dict(callback=callback,colnames=json(colnames),
           colmodel=json(colmodel),id=_id,height=height,width=width)
        return TAG[''](TABLE(_id=_id),
                       DIV(_id=_id+"_pager"),
                       SCRIPT(script))

    ###############################################
    # scientific widgets (latex, charting)
    ###############################################
    @staticmethod
    def latex(expression):
        """
        ## Uses Google charting API to embed LaTeX 
        """
        return XML('<img src="http://chart.apis.google.com/chart?cht=tx&chl=%s" align="center"/>' % expression.replace('"','\"'))

    @staticmethod
    def pie_chart(data='1,2,3',names='a,b,c',width=300,height=150,align='center'):
        """
        ## Uses Google charting API to embed a pie chart
        - ``data`` is a list of comma separated values 
        - ``names`` is a list of comma separated labels (one for data item)
        - ``width`` is the width of the image
        - ``height`` is the height of the image
        - ``align`` determines the alignment of the image
        """
        if isinstance(data,str):
            data = data.replace(' ','')
        elif isinstance(data,dict):
            data = '|'.join(','.join(str(y) for y in s) for s in data.values())
        elif isinstance(data,list):
            data = ','.join(str(y) for y in data)
        if isinstance(names,str):
            names = '|'.join(name.strip() for name in names.split(','))
        else:
            names = '|'.join(name for name in names)
        return XML('<img src="http://chart.apis.google.com/chart?cht=p3&chd=s:cEj9U&chs=%(width)sx%(height)s&chl=%(names)s&chd=t:%(data)s" align="%(align)s">' % dict(data=data,width=width,height=height,names=names,align=align))

    @staticmethod
    def bar_chart(data='1,2,3',names='a,b,c',width=300,height=150,align='center'):
        """
        ## Uses Google charting API to embed a bar chart
        - ``data`` is a list of comma separated values 
        - ``names`` is a list of comma separated labels (one for data item)
        - ``width`` is the width of the image
        - ``height`` is the height of the image
        - ``align`` determines the alignment of the image
        """
        if isinstance(data,str):
            data = data.replace(' ','')
        elif isinstance(data,dict):
            data = '|'.join(','.join(str(y) for y in s) for s in data.values())
        elif isinstance(data,list):
            data = ','.join(str(y) for y in data)
        if isinstance(names,str):
            names = '|'.join(name.strip() for name in names.split(','))
        else:
            names = '|'.join(name for name in names)
        height=int(width)/2
        return XML('<img src="http://chart.apis.google.com/chart?chxt=x,y&cht=bvs&chd=s:cEj9U&chls=2.0&chs=%(width)sx%(height)s&chxl=0:|%(names)s&chd=t:%(data)s" align="%(align)s">' % dict(data=data,width=width,height=height,names=names,align=align))

    ###############################################
    # media widgets
    ############################################### 
    @staticmethod
    def slideshow(links=None,table=None,field='image',transition='fade',width=200,height=200):
        """
        ## Embeds a slideshow
        It gets the images from a table

        - ``table`` is the table name
        - ``field`` is the upload field in the table that contains images
        - ``transition`` determines the type of transition, e.g. fade, etc.
        - ``width`` is the width of the image
        - ``height`` is the height of the image
        """

        import random
        id=str(random.random())[2:]
        if table:
            rows = db(db[table].id>0).select()
            if db[table][field].type=='upload':
                images = [IMG(_src=URL('default','download',args=row[field])) for row in rows]
            else:
                images = [IMG(_src=row[field]) for row in rows]
        elif links:
            images = [IMG(_src=link) for link in links.split(',')]
        else:
            images = []
        return DIV(SCRIPT("jQuery(document).ready(function() {jQuery('#slideshow%s').cycle({fx: '%s'});});" % (id,transition)),DIV(_id='slideshow'+id,*images))

    @staticmethod
    def youtube(code,width=400,height=250):
        """
        ## Embeds a youtube video (by code)
        - ``code`` is the code of the video
        - ``width`` is the width of the image
        - ``height`` is the height of the image
        """

        return XML("""<object width="%(width)s" height="%(height)s"><param name="movie" value="http://www.youtube.com/v/%(code)s&hl=en_US&fs=1&"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/%(code)s&hl=en_US&fs=1&" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="%(width)s" height="%(height)s"></embed></object>""" % dict(code=code, width=width, height=height))

    @staticmethod
    def vimeo(code,width=400,height=250):
        """
        ## Embeds a viemo video (by code)
        - ``code`` is the code of the video
        - ``width`` is the width of the image
        - ``height`` is the height of the image
        """
        return XML("""<object width="%(width)s" height="%(height)s"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=%(code)s&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=%(code)s&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="%(width)s" height="%(height)s"></embed></object>""" % dict(code=code, width=width, height=height))

    @staticmethod
    def mediaplayer(src,width=400,height=250):
        """
        ## Embeds a media file (such as flash video or an mp3 file)
        - ``src`` is the src of the video
        - ``width`` is the width of the image
        - ``height`` is the height of the image
        """
        return XML('<embed allowfullscreen="true" allowscriptaccess="always" flashvars="height=%(height)s&width=%(width)s&file=%(src)s" height="%(height)spx" src="%(url)s" width="%(width)spx"></embed>'%dict(url=URL('static','plugin_wiki/mediaplayer.swf'),src=src,width=width,height=height))

    ###############################################
    # social widgets (comments and tags)
    ###############################################
    @staticmethod
    def comments(table='None',record_id=None):
        """
        ## Embeds comments in the page
        Comments can be linked to a table and/or a record

        - ``table`` is the table name 
        - ``record_id`` is the id of the record
        """
        return LOAD('plugin_wiki','comment',
             args=(table,record_id or 0),ajax=True)

    @staticmethod
    def tags(table='None',record_id=None):
        """
        ## Embeds tags in the page
        tags can be linked to a table and/or a record

        - ``table`` is the table name 
        - ``record_id`` is the id of the record
        """

        return LOAD('plugin_wiki','tags',
                    args=(table,record_id or 0),ajax=True)

    @staticmethod
    def tag_cloud():
        """
        ## Embeds a tag cloud
        """

        return LOAD('plugin_wiki','cloud')


    @staticmethod
    def aggregator(feed, max_entries=5):
        """
        ## Embeds a feed aggregator
        - ``name`` is the aggregator name
        - ``feed`` is a list comma separated feed urls (http://rss.cbc.ca/lineup/topstories.xml)
        - ``max_entries`` is the max number of displayed entries (default=5)
        """
        import gluon.contrib.feedparser as feedparser
        lfeeds = isinstance(feeds,(str,unicode)) and feeds or feeds.split(",")
        content = DIV(A(d.channel.title,_href=d.channel.link,_rel=d.channel.description),
                      UL(),_id='web2py_aggregator')
        for feed in lfeeds:
            d = feedparser.parse(feed)
            for entry in d.entries[:max_entried]:
                content[1] += LI(A(entry.title,' ',SPAN(entry.updated),
                                   _href=entry.link,_rel=entry.descstiption,
                                   _class=web2py_aggregator_link))
        return content

    @staticmethod
    def map(  table='auth_user', width=400, height=200):
        """
        ## Embeds a Google map
        Gets points on the map from a table
        
        - ``table`` is the table name
        - ``width`` is the map width
        - ``height`` is the map height

        The table must have columns: latidude, longitude and map_popup.
        When clicking on a dot, the map_popup message will appear. 
        """

        import os
        import gluon.template
        content = open(os.path.join(request.folder,'views','plugin_wiki',
                                    'map.html'),'rb').read()
        context = dict(rows=db(db[table].id>0).select(),
                       width='%spx'%width,height='%spx'%height)
        return XML(gluon.template.render(content=content,context=context))

        

    @staticmethod
    def star_rating(table, record_id, splitstars=False):
        """            
        ## Create a star rating widget for a given record in given table.    
        if given table has a field called 'rating' average rating will also added to it.
        it will save ratings from logedin users only.                        
                       
        - ``table`` is the table name             
        - ``record_id`` is the id of record for which to show a rating widget.
        - ``splitstars`` if set to True will display split stars.            
        """
        import uuid
        id = uuid.uuid4()
        row=db(db.plugin_wiki_rating.tablename==table)(db.plugin_wiki_rating.record_id==record_id).select().first()
        rating = row.rating if row else 0
        callback = URL('plugin_wiki', 'star_rate', args = [table,record_id])
        incr = 0.5 if splitstars else 1
        return TAG[''](DIV(_id='star'+str(id),_class='rating'),
                       SCRIPT("jQuery(document).ready(function(){jQuery('%(uid)s').rating('%(callback)s',{increment:%(incr)s, maxvalue:5, curvalue:%(rating)s});});" % dict(uid='#star'+str(id), callback=callback,incr=incr, rating=rating)))

    @staticmethod
    def iframe(src, width=400, height=300):
        """
        embed a page in an <iframe></iframe>
        """
        return TAG.iframe(_src=src, _width=width, _height=height)

    @staticmethod
    def load_url(src):
        """
        loads the contenct of the url via ajax
        and traps forms
        """
        return LOAD(url=src)
    
    @staticmethod
    def load_action(action, controller='', ajax=True):
        """
        loads the content of URL(request.application, controller, action) via ajax
        and traps forms
        """
        return LOAD(controller, action, ajax=ajax)


###################################################
# main class to intantiate the widget
###################################################
class PluginWiki(object):

    def __init__(self):
        import re
        regex = re.compile('(?P<s> *)(?P<t>.+) +(?P<k>\S+)')
        menu_page = db(db.plugin_wiki_page.slug=='meta-menu').select().first()
        code_page = db(db.plugin_wiki_page.slug=='meta-code').select().first()
        if code_page and request.controller=='plugin_wiki' and not request.function in ('page_edit', 'page_history'):
            try:
                exec(re.sub('\r\n|\n\r|\r','\n',code_page.body.strip()),globals())
            except:
                import traceback
                if plugin_wiki_editor:
                    response.flash = DIV(H4('Execution error in page _proc'),              
                                         PRE(traceback.format_exc()))
                else:
                    response.flash = 'Internal error, please contact the administrator'
        if menu_page:
            response.menu=[]
            parents = [(-1,response.menu)]
            for line in menu_page.body.split('\n'):
                match = regex.match(line)
                if not match: continue
                indent=len(match.group('s'))
                title=match.group('t')
                url=match.group('k')
                if url.lower()=='none':
                    url=URL('plugin_wiki','page',args=request.args)
                elif url.startswith('page:'):
                    url=URL('plugin_wiki','page',args=url[5:])
                while indent<=parents[-1][0]:
                    parents.pop()
                newtree=[]
                parents[-1][1].append((title,False,url,newtree)) 
                parents.append((indent,newtree))
        self.extra = self.extra_blocks()

    # this embeds page attachments
    class attachments(object):   
        def __init__(self,tablename,record_id=0,
                     caption='Attachments',close="Close",
                     id=None,width=70,height=70,
                     source=None):
            import uuid
            self.tablename=tablename
            self.record_id=record_id
            self.caption=caption
            self.close=close
            self.id=id or str(uuid.uuid4())
            self.width=width
            self.height=height
            if not source:
                source=URL('plugin_wiki','attachments',args=(tablename,record_id))
            self.source = source
        def xml(self):
            return '<div id="%(id)s" style="display:none"><div style="position:fixed;top:0%%;left:0%%;width:100%%;height:100%%;background-color:black;z-index:1001;-moz-opacity:0.8;opacity:.80;opacity:0.8;"></div><div style="position:fixed;top:%(top)s%%;left:%(left)s%%;width:%(width)s%%;height:%(height)s%%;padding:16px;border:2px solid black;background-color:white;opacity:1.0;z-index:1002;overflow:auto;-moz-border-radius: 10px; -webkit-border-radius: 10px;"><span style="font-weight:bold">%(title)s</span><span style="float:right">[<a href="#" onclick="jQuery(\'#%(id)s\').hide();return false;">%(close)s</a>]</span><hr/><div style="width:100%%;height:90%%;" id="c%(id)s"><iframe id="attachments_modal_content" style="width:100%%;height:100%%;border:0">%(loading)s</iframe></div></div></div><a href="#" onclick="jQuery(\'#attachments_modal_content\').attr(\'src\',\'%(source)s\');jQuery(\'#%(id)s\').fadeIn(); return false" id="plugin_wiki_open_attachments"">%(title)s</a>' % dict(title=self.caption,source=self.source,close=self.close,id=self.id,left=(100-self.width)/2,top=(100-self.height)/2,width=self.width,height=self.height,loading=T('loading...'))

    class widget_builder(object):   
        def __init__(self,
                     caption='Widget Builder',close="Close",
                     id=None,width=70,height=70):
            import uuid
            self.caption=caption
            self.close=close
            self.id=id or str(uuid.uuid4())
            self.width=width
            self.height=height
            self.source=URL('plugin_wiki','widget_builder')
        def xml(self):
            return '<div id="%(id)s" style="display:none"><div style="position:fixed;top:0%%;left:0%%;width:100%%;height:100%%;background-color:black;z-index:1001;-moz-opacity:0.8;opacity:.80;opacity:0.8;"></div><div style="position:fixed;top:%(top)s%%;left:%(left)s%%;width:%(width)s%%;height:%(height)s%%;padding:16px;border:2px solid black;background-color:white;opacity:1.0;z-index:1002;overflow:auto;-moz-border-radius: 10px; -webkit-border-radius: 10px;"><span style="font-weight:bold">%(title)s</span><span style="float:right">[<a href="#" onclick="jQuery(\'#%(id)s\').hide();return false;">%(close)s</a>]</span><hr/><div style="width:100%%;height:90%%;" id="c%(id)s"><iframe id="widget_builder_modal_content" style="width:100%%;height:100%%;border:0">%(loading)s</iframe></div></div></div><a href="#" onclick="jQuery(\'#widget_builder_modal_content\').attr(\'src\',\'%(source)s\');jQuery(\'#%(id)s\').fadeIn(); return false" id="plugin_wiki_open_attachments"">%(title)s</a>' % dict(title=self.caption,source=self.source,close=self.close,id=self.id,left=(100-self.width)/2,top=(100-self.height)/2,width=self.width,height=self.height,loading=T('loading...'))

    def pdf(self,text):
        if not plugin_wiki_mode=='markmin':
            raise Exception( "Not supported")

        response.headers['content-type'] = 'application/pdf'
        return "Not implemented"

    def render(self,text,level=plugin_wiki_level,page_url=URL()):
        import re
        if plugin_wiki_mode=='html':
            return self.render_html(text,page_url)        
        elif plugin_wiki_mode=='markmin':
            return self.render_markmin(text,page_url)
        else:
            raise Exception("Not supported")

    def parse_value(self,code):
        code = code.replace('[page]',request.args(0))
        code = code.replace('[id]',request.args(1) or '')
        code = code.replace('[application]',request.application)
        code = code.replace('[client]',request.client)
        if plugin_wiki_level>2:
            import gluon.template
            return gluon.template.render(code,context=globals())
        return code

    def render_widget(self,code):        
        try:
            items = [x.strip().split(':',1) for x in code.split('\n')]
            args = dict((item[0].strip(), self.parse_value(item[1].strip())) for item in items)
            name = args.get('name','')
            if not name or name[0]=='_': return 'ERROR'
            del args['name']
            html = getattr(PluginWikiWidgets,name)(**args)
            if isinstance(html,str):
                return html
            elif html:
                return html.xml()
            else:
                ''
        except:
            if plugin_wiki_editor:
                import traceback
                return '<div class="error"><pre>%s</pre></div>' % traceback.format_exc()
            else:
                return '<div class="error">system error</div>'

    def render_template(self,code):
        import gluon.template
        try:
            return gluon.template.render(code,context=globals())
        except:
            if plugin_wiki_editor:
                import traceback
                return '<div class="error"><pre>%s</pre></div>' % traceback.format_exc()
            else:
                return '<div class="error">system error</div>'

    def extra_blocks(self):
        extra = {}
        LATEX = '<img src="http://chart.apis.google.com/chart?cht=tx&chl=%s" align="center"/>'
        extra['latex'] = lambda code: LATEX % code.replace('"','\"')
        extra['verbatim'] = lambda code: cgi.escape(code)
        extra['code'] = lambda code: CODE(code,language=None).xml()
        extra['code_python'] = lambda code: CODE(code,language='python').xml()
        extra['code_c'] = lambda code: CODE(code,language='c').xml()
        extra['code_cpp'] = lambda code: CODE(code,language='cpp').xml()
        extra['code_java'] = lambda code: CODE(code,language='java').xml()
        extra['code_html_plain'] = lambda code: CODE(code,language='html_plain').xml()
        extra['code_html'] = lambda code: CODE(code,language='html').xml()
        extra['code_web2py'] = lambda code: CODE(code,language='web2py').xml()
        if plugin_wiki_level>1:
            extra['widget'] = lambda code: self.render_widget(code)
        if plugin_wiki_level>2:
            extra['template'] = lambda code: self.render_template(code)
        return extra

    def render_markmin(self,text,page_url=URL()):
        import re
        att_url = URL(request.application,'plugin_wiki','attachment')
        session.plugin_wiki_attachments=[]
        def register(match):
            session.plugin_wiki_attachments.append(match.group('h'))
            return '[[%s %s/%s' % (match.group('t'),att_url,match.group('h'))
        text = re.sub('\[\[(?P<t>[^\[\]]+)\s+attachment:\s*(?P<h>[\w\-\.]+)',
                      register,text)
        text = re.sub('\[\[(?P<t>[^\[\]]+) page:','[[\g<t> %s/' % page_url,text)
        return MARKMIN(text,extra=self.extra)

    def render_html(self,text,page_url=URL()):
        import re
        logging.warn (page_url)
        text = text.replace('href="page:','href="%s/' % page_url) 
        att_url = URL(r=request,c='plugin_wiki',f='attachment')
        text = text.replace('src="attachment:', 'src="%s/' % att_url)
        regex_code = re.compile('``(?P<t>.*?)``:(?P<c>\w+)',re.S)
        while True:
            match=regex_code.search(text)
            if not match:
                break
            if match.group('c') in self.extra:
                code = match.group('t').strip().replace('<br>','')
                html = self.extra[match.group('c')](code)
                text = text[:match.start()]+html+text[match.end():]
        return XML(text,sanitize=plugin_wiki_level<2)

    def embed_page(self,slug):
        page=db(db.plugin_wiki_page.slug==slug).select().first()
        if not page: return page
        return XML(plugin_wiki.render(page.body))

    def widget(self,name,*args,**kargs):
        return getattr(PluginWikiWidgets,name)(*args,**kargs)

plugin_wiki=PluginWiki()
