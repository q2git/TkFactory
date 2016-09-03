# -*- coding: utf-8 -*-
"""
Created on Sat Sep 03 13:49:24 2016

@author: q2git
"""
from tkfactory import TkFactory

if __name__ == '__main__':
    gui = TkFactory('gui.ini')
    gui.widgets['b1'].config(command=lambda x=0:gui.textvariables['e1'].set('Hello'))
    gui.widgets['rdbt1'].config(command=lambda x=0:gui.textvariables['ckbt1'].set('CheckButton1'))
    gui.widgets['ckbt1'].config(command=lambda x=0:gui.textvariables['ckbt1'].set(gui.textvariables['rdbt1'].get()))
    gui.widgets['mn2'].entryconfig(1,command=gui.stop)
    def fun(i):
        gui.widgets['mn1'].entryconfig(1,label='title{}'.format(i))
        gui.widgets['mn2'].entryconfig(1,label=gui.widgets['mn3'].entrycget(i,'label'))
    gui.widgets['mn3'].entryconfig(0,command=lambda :fun(0))
    gui.widgets['mn3'].entryconfig(1,command=lambda :fun(1))
    gui.widgets['mn3'].entryconfig(2,command=lambda :fun(2))    
    gui.widgets['tree1'].insert('', 0, iid=11,text='hello', values=('a','b',234,324,'c','你好',),)
    gui.widgets['s1'].config(command=lambda x=0:gui.textvariables['ls1'].set(gui.widgets['s1'].get()))
    gui.widgets['pg1'].start(50)

    gui.run()
