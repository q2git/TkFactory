# -*- coding: utf-8 -*-
"""
Created on Sat Sep 03 13:49:24 2016
@author: q2git
"""
from tkfactory import TkFactory

class Gui(TkFactory):
    def __init__(self, filename):
        super(Gui, self).__init__(filename)
        self.config_cmd()
        self.widgets['tp1'].grid_remove()
        
    def config_cmd(self):
        self.widgets['b1'].config(command=lambda: self.config_grid('rdbt1',(3, 1, 1, 1, 'ns', 1, 1)))
        self.widgets['rdbt1'].config(command=lambda: self.textvariables['ckbt1'].set('CheckButton1'))
        self.widgets['ckbt1'].config(command=lambda: self.textvariables['ckbt1'].set(self.textvariables['rdbt1'].get()))
        self.widgets['mn3'].entryconfig(0,command=self.stop)
        
        self.widgets['mn1'].entryconfig(0,command=self.switch)
        self.widgets['mn1'].entryconfig(1,command=lambda: self.fun(1))
        self.widgets['mn-3'].entryconfig(0,command=lambda: self.textvariables['mnbt1'].set('HELLO'))    
        self.widgets['s1'].config(command=lambda x=0:self.textvariables['ls1'].set(self.widgets['s1'].get()))
        self.widgets['pg1'].start(50)
        
        self.widgets['gui2_b1'].config(command=self.widgets['tp1'].grid_remove)
        self.widgets['gui2_e1'].bind('<FocusOut>', self.fun1)
        
        self.widgets['tree1'].bind('<<TreeviewSelect>>', self.tree_sel)
        for name in self.textvariables.keys():
            #self.textvariables[name].set(name)
            self.widgets['tree1'].insert('', 0, iid=name,text=name.upper(), 
                values=tuple(self.widgets[name].keys())#('a','b',234,324,'c','你好',),
                )
                
    def switch(self):
        self.widgets['tp1'].grid()

    
    def fun1(self, event):
        self.textvariables['e1'].set(self.textvariables['gui2_e1'].get())
        
    def fun(self,i):
        self.widgets['mn3'].entryconfig(1,label='title{}'.format(i))
        self.widgets['mn3'].entryconfig(1,label=self.widgets['mn3'].entrycget(i,'label'))            

    def tree_sel(self,event):
        widget=self.widgets['tree1']
        val= widget.item(widget.selection()[0],'values')
        self.widgets['cb1'].config(values=list(val))
        
            
            
if __name__ == '__main__':
    gui = Gui('gui.ini')
    gui.run()
