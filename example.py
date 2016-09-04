# -*- coding: utf-8 -*-
"""
Created on Sat Sep 03 13:49:24 2016

@author: q2git
"""
from tkfactory import TkFactory


gui = TkFactory('gui.ini')
gui.widgets['b1'].config(command=lambda: gui.config_grid('rdbt1',(3, 1, 1, 1, 'ns', 1, 1)))
gui.widgets['rdbt1'].config(command=lambda: gui.textvariables['ckbt1'].set('CheckButton1'))
gui.widgets['ckbt1'].config(command=lambda: gui.textvariables['ckbt1'].set(gui.textvariables['rdbt1'].get()))
gui.widgets['mn3'].entryconfig(0,command=gui.stop)
def fun(i):
    gui.widgets['mn3'].entryconfig(1,label='title{}'.format(i))
    gui.widgets['mn3'].entryconfig(1,label=gui.widgets['mn3'].entrycget(i,'label'))
gui.widgets['mn1'].entryconfig(0,command=lambda: fun(0))
gui.widgets['mn1'].entryconfig(1,command=lambda: fun(1))
gui.widgets['mn-3'].entryconfig(0,command=lambda: gui.textvariables['mnbt1'].set('HELLO'))    
gui.widgets['s1'].config(command=lambda x=0:gui.textvariables['ls1'].set(gui.widgets['s1'].get()))
gui.widgets['pg1'].start(50)
def fun2(widget):
    val= widget.item(widget.selection()[0],'values')
    gui.widgets['cb1'].config(values=list(val))
gui.widgets['tree1'].bind('<<TreeviewSelect>>',lambda x: fun2(gui.widgets['tree1']))
for name in gui.textvariables.keys():
    #gui.textvariables[name].set(name)
    gui.widgets['tree1'].insert('', 0, iid=name,text=name.upper(), 
        values=tuple(gui.widgets[name].keys())#('a','b',234,324,'c','你好',),
        )
    
gui.run()
