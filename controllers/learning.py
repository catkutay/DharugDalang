#################
#Interface to nltk for languages
#
#################
# -*- coding: utf-8 -*-
# try something like

import urllib
import nltk, re, pprint # NLTK and related modules -- are these all needed?
from nltk.corpus import abc

import os, sys
from  nltk.tokenize.punkt import PunktSentenceTokenizer
from worksheet import wsread_page

def translate_word(word, lang, ws, wd):
				reduced_word = ws.stem(word, hide_suffixes = False, show_translation = True, show_pos=True)

				stem = reduced_word[0]
				translated_stem = translate_stem(stem, lang, wd)

				translated_suffixes = reduced_word[1]
				# if translated_stem[0]=="": return (translated_stem, translated_suffixes)

				reduced_word_part = ws.stem(translated_stem[0], hide_suffixes = False, show_translation = True)

				translated_stem = translated_stem + translate_stem(reduced_word_part[0],lang, wd)
				translated_suffixes = translated_suffixes + reduced_word_part[1]

				return (translated_stem, translated_suffixes)

def translate_stem(stem, lang, wd):

	if lang!="English":
		if wd.has_word(stem):

			return (stem, wd.getEnglish(stem), wd.getPartEng(stem))
	else:

		if wd.has_eng_word(stem):
				return (stem, wd.getLanguage(stem), wd.getPartLang(stem))
	return (stem, stem, 'Unknown')

def print_words(words):
	AboriginalLanguage = ""
	english = ""
	pos=""
	for word in words:
        printed_word = print_word(word)
    AboriginalLanguage += printed_word[0] +" "
						english +=  printed_word[1] +" "
						pos+= printed_word[2]+" "

				return [AboriginalLanguage, english, pos]

def print_word(word):
	stem = word[0]
	suffixes = word[1]

	printed_stem = print_stem(stem)
	AboriginalLanguage = printed_stem[0]
	english = printed_stem[1]
	pos=printed_stem[2]
	for suffix in suffixes:
		printed_suffix = print_suffix(suffix)
		AboriginalLanguage +=  printed_suffix[0]
		english += printed_suffix[1]
		pos+=printed_suffix[2]
	return [AboriginalLanguage, english,pos]

def print_stem(stem):

				AboriginalLanguage = stem[0]
				english = stem[1]
				#create array
				pos=stem[2]
				w_length = len(AboriginalLanguage)
				e_length = len(english)

				length = max(w_length, e_length)
				AboriginalLanguage = AboriginalLanguage.center(length)
				english = english.center(length)
				if pos: pos = pos.center(length)
				return [AboriginalLanguage, english, pos]

def print_suffix(suffix):
				AboriginalLanguage = "-" + suffix[0]
				english = " " + suffix[1]
				pos = " "+suffix[2]
				w_length = len(AboriginalLanguage)
				e_length = len(english)

				length = max(w_length, e_length)
				AboriginalLanguage = AboriginalLanguage.center(length)
				english = english.center(length)
				pos= pos.center(length)
				return [AboriginalLanguage, english, pos]


def parser():
	words=None
	searchterm=request.vars.query
	lang=request.vars.lang
	#null searches
	if not(request.vars):
		return dict(wordlist=True, words=words)
	elif not(searchterm):
		return dict(wordlist=False, words=None, query=searchterm)

	### add reference to example sentences
	if lang=="English":

		query= dblanguage.DharugExamples.English.contains(searchterm.split(), all=True)
	else:
		query= dblanguage.DharugExamples.Language.contains(searchterm.split(),all=True)
	words=dblanguage(query)
	try:
		words=words.select()
		lastword=words[0]
		results=[]
		results.append(lastword)
		for word in words:
			if word.English!=lastword.English:
				results.append(word)
			lastword=word
		words=results
	except:
	### language/dictonary or learning/paerser
	#redirect (URL(r=request,c="learning",f="parser",vars={'query':searchterm, 'lang':lang}))
		redirect (URL(r=request,c="learning",f="parser"))
##else load dictionary
	wd = dictionary.AboriginalLanguageDictionary()
	ws = stemmer.AboriginalLanguageStemmer()
	if (words):
		return dict(wordlist=False, words=words, query=searchterm)
	else:
		newwords = PunktSentenceTokenizer().tokenize(searchterm)
		words = []

		for word in newwords:
			words+= [translate_word(word, lang, ws, wd)]
		lang=[]
		english=[]
		pos=[]
		for word in words:
			printed_word = print_word(word)
			lang.append(printed_word[0])
			english.append(printed_word[1])
			pos.append(printed_word[2])
		leng=len(lang)

		words=[lang,english,pos]
	return dict(wordlist=True, words=words, query=request.vars.query)


def pages():
	w = db.plugin_wiki_page
	t=db.plugin_wiki_tag
	taglist=db(t.id>0).select(orderby=t.id)
	words=None
	if plugin_wiki_editor:
			pages = db(w.worksheet==True).select(orderby=w.title)
	else:
				pages = db(w.worksheet==True)(w.is_public==True).select(orderby=w.title)

	if plugin_wiki_editor:
				form=SQLFORM.factory(Field('title',requires=db.plugin_wiki_page.title.requires))
				if form.accepts(request.vars):
						title=request.vars.title
						page =db(w.title==title).select().first()
						if not page:
								page = w.insert(slug=title.replace(' ','_'),
								title=title,worksheet="T",
								body=request.vars.template and w(slug=request.vars.template).body or '')
						redirect(URL(r=request,c="plugin_wiki",f='edit_page',args=form.vars.title,vars=dict(template=request.vars.from_template or '')))
	else:
				form=''
	return dict(query=request.vars.query, taglist=taglist, pages=pages, form=form)

def page():
	"""
	shows a page
	"""
	slug= request.args(0)
	import re
	if slug=="Index" or slug==None:
		redirect(URL(r=request, c='plugin_wiki', f='index.html'))
	if slug=="Admin_Help" and not auth.user:
		redirect(URL(r=request, c='plugin_wiki', f='pages'))


	w = db.plugin_wiki_page

	if plugin_wiki_editor:
			pages = db(w.worksheet==True).select(orderby=w.title)
	else:

			pages = db(w.worksheet==True)(w.is_public==True).select(orderby=w.title)

	page = w(slug=slug)

	#for template
	if (not page or not page.is_public or not page.is_active):
		 if plugin_wiki_editor:
				redirect(URL(r=request, c='plugin_wiki', f='edit_page', args=request.args))
		 if (session):session.flash=T("Page not available")

		 redirect(URL(r=request, c='plugin_wiki', f='pages'))
	elif page and page.role and not auth.has_membership(page.role):
		raise HTTP(404)
		# parse pages. First History
	if page.worksheet:
		page.questions=[]
	page.attachments=[]
	a=db.plugin_wiki_attachment
	query = (a.tablename=="page")&(a.record_id==page.id)
	page.attachments=db(query).select()
	page_body=page.body
	if (page.worksheet):

		page_body = wsread_page(page)
	#   page=wsread_question(page_body, page)
	else:
		page_body=page.body
		title=page.title
	print ('there')
	return dict(query=request.vars,form="", title=page.title, pages=pages, page=page, page_body=page_body, slug=slug)

def list():
	page_id=request.args(0)
	query=request.vars
#pickup a query of two dimension, not sure why FIXME
	#logging.warn(query)
#get# new word and add
	try:
		word_id=query["word_id"]

		word=dblanguage.Dharug(dblanguage.Dharug.id==word_id)
		db.topics.insert(page_id=page_id,English=word.English,Language=word.Language_Word)
		db.commit()
		newwords=None
	except:
		pass

	words=[]
	wl=wordlist(page_id)
	if wl:
		for word in wl['words']:

			words.append({"English":word.English,"Language":word.Language})
	else: wl=None
	#logging.warn(newwords)
	return dict(words=words,  page_id=page_id)

def addlist():
	#logging.warn("addlist")
	page_id=request.args(0)
	query=request.vars
#pickup a query of two dimension, not sure why FIXME
	#logging.warn(query)
#get new word and add
	newwords=None
	searchterm=None
	try:
		searchterm=query['query']
	except:
		pass
 
	if query['lang']=="English" :

				query=(dblanguage.Dharug.Search_English==searchterm)|dblanguage.Dharug.Search_English.startswith(searchterm+' ;')|dblanguage.Dharug.Search_English.startswith(searchterm+',')|(dblanguage.Dharug.Search_English.contains("; "+searchterm+' ' ))|(dblanguage.Dharug.Search_English.endswith("; "+searchterm))
	else:
				query= dblanguage.Dharug.Language_Word==searchterm

	#get new word and add
	newwords=[]
	newword=dblanguage(query).select()
	if newword:
		lastword=newword[0]
		#db.topics.insert(page_id=page_id,English=lastword["English"],Language=lastword["Language_Word"])
		newwords.append({"English":lastword.English,"Language":lastword.Language_Word, "id":lastword.id})
		for word in newword:
			if word.Language_Word!=lastword.Language_Word:
				newwords.append({"English":word.English,"Language":word.Language_Word, "id":word.id})
				lastword=word

   
	#logging.warn(newwords)
	return dict( newwords=newwords, page_id=page_id)



@auth.requires_login()
def edit_page_old():
	"""
	edit a page
	"""
	import os
	slug = request.args(0) or 'Index'
	tags=""
	if request.args(1): tags='|'+request.args(1)+'|'
	slug=slug.replace(' ','_')
	w = db.plugin_wiki_page
	w.role.writable = w.role.readable = plugin_wiki_level>1
	page = w(slug=slug)
	imgActions=[]
	imageAction=os.listdir("applications/Dharug/uploads/media/images/Actions")
	for image in imageAction:
		imgActions.append(image)

	imgNames=[]
	imageName=os.listdir("applications/Dharug/uploads/media/images/Names")
	for image in imageName:
		imgNames.append(image)
	imgAll=[]
	imageAll=os.listdir("applications/Dharug/uploads/media/images")
	for image in imageAll:
		imgAll.append(image)


	"""
	db.plugin_wiki_page.tag.default=""
	db.plugin_wiki_page.update.tags=db.plugin_wiki_page.tags
	"""
	if not page:
		db.plugin_wiki_page.tags.default=tags

		page = w.insert(slug=slug,
						title=slug.replace('_',' '),
						tags=tags,
						body=request.vars.template and w(slug=request.vars.template).body or '')
	else:
		tags = page.tags #in practice 'xyz' would be a variable
	if page.title=="Index":
		form = crud.update(w, page, deletable=True, onaccept=crud.archive,
					   next=URL(r=request, c='plugin_wiki', f='index'))
	else:
		form = crud.update(w, page, deletable=True, onaccept=crud.archive,
				next=URL(r=request,c='learning', f='page',args=slug))

	return dict(form=form,page=page,tags=tags, imageActions=imgActions, imageAll=imgAll,imageNames=imgNames)

