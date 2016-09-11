# -*- coding: utf-8 -*-
"""
Created on Sat Sep 03 13:49:24 2016
@author: q2git
"""
from tkfactory import TkFactory
import tkMessageBox as msgbox
import copy

class Gui(TkFactory):
    def __init__(self, filename):
        super(Gui, self).__init__(filename)
        self.config_cmd()
        self.update_tree()
        
    def config_cmd(self):
        self.b1.config(command = self.show_toplevel)
  
        self.rdbt1.config(command=lambda: self.show_var(self.rdbt1))
        self.ckbt1.config(command=lambda: self.show_var(self.ckbt1))
        
        self.mn1.entryconfig(0,command=lambda: self.menu_cmd(0))
        self.mn1.entryconfig(1,command=lambda: self.menu_cmd(1))
        self.mn1.entryconfig(2,command=lambda: self.menu_cmd(2))
        
        #self.widgets['s1'].config(command=lambda x=0:self.textvariables['ls1'].set(self.widgets['s1'].get()))
        #self.widgets['pg1'].start(50)
        
        self.b2.config(command=self.show_hide_f5)
        self.e1.bind('<FocusOut>', lambda _: self.show_var(self.e1))
        self.cb1.bind("<<ComboboxSelected>>", lambda _: self.show_var(self.cb1))
        self.tree1.bind('<<TreeviewSelect>>', self.sel_tree)
                
    def update_tree(self): 
        self.tree1.delete(*self.tree1.get_children())
        for name in self.widgetNames:
            widget = getattr(self, name)
            self.tree1.insert('', 0, iid=name,text=name.upper(), 
                values=tuple(widget.keys()))
    
    def show_hide_f5(self):
        if self.f5.grid_info():
            self.f5.grid_remove()
            self.b2.var.set('Show f5')
        else:
            self.f5.grid()
            self.b2.var.set('Hide f5')
    
    def show_var(self, widget):
        if hasattr(widget, 'var'):
            message = widget.var.get()
        else:
            message = 'No var'
        msgbox.showinfo(message = message)
        
    def menu_cmd(self, index):
        label = self.mn1.entrycget(index,'label')
        self.mn1.entryconfig(index, label= label+'-X')

    def sel_tree(self,event):
        val= self.tree1.item(self.tree1.selection()[0],'values')
        self.txt1.insert('end', val)
        self.txt1.insert('end', '\n')
        
    def show_toplevel(self):
        top = copy.deepcopy(self.topWindows['TOP_WINDOW1'])
        self.createWidgets(top)
        self.top1.transient(self.root)
        self.top1.grab_set() #modal window
        self.top1.focus() 

    def run(self):
        self.root.mainloop()           
            
if __name__ == '__main__':
    gui = Gui('gui.ini')
    gui.run()
