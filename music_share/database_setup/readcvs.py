# -*- coding:utf-8 -*-

Artists_fname = "Artists.csv"
Albums_Create_fname="Albums_Create.csv"
Belong_fname="Belong.csv"
Contain_fname="Contain.csv"
Groups_fname="Groups.csv"
PersonalLists_Save_fname = "PersonalLists_Save.csv"
Singers_fname = "Singers.csv"
Artists=open(Artists_fname)

f = open(Artists_fname)
cur.copy_from(f, Artists_fname.rstrip('.csv'), sep=',')
f.close()



def readcvs(fname):
	fhandle=open(fname)
	for line in fhandle.readlines():
		print line.rstrip('\n').split(',')
	fhandle.close()
		
readcvs(Artists_fname)
readcvs(Albums_Create_fname)
readcvs(Belong_fname)
readcvs(Contain_fname)
readcvs(Groups_fname)
readcvs(PersonalLists_Save_fname)
readcvs(Singers_fname)