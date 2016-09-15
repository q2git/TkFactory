# -*- coding: utf-8 -*-
"""
Created on Sat Sep 03 13:49:24 2016
@author: q2git
"""
from tkfactory import TkFactory
import tkMessageBox as msgbox

class Gui(TkFactory):
    def __init__(self, filename, master=None):
        super(Gui, self).__init__(filename, master)
        self.config_cmd()
        self.update_tree()
        
    def config_cmd(self):
        self.b1.config(command= self.show_toplevel)
        self.b2.config(command= self.show_hide_tree)
        self.b3.config(command= self.change_menu)        
        self.rdbt1.config(command=lambda: self.show_var(self.rdbt1))
        self.ckbt1.config(command=lambda: self.show_var(self.ckbt1))
        self.list1.bind("<<ListboxSelect>>", self.get_list)
        self.list1.bind("<FocusIn>",lambda _: self.list1.listvar.set(self.style.theme_names()))        
      
        self.sc1.config(command=lambda _:self.l1.var.set(self.sc1.get()))
        self.pg1.start(50)
        

        self.e1.bind('<FocusOut>', lambda _: self.show_var(self.e1))
        self.cb1.bind("<<ComboboxSelected>>", lambda _: self.show_var(self.cb1))
        self.tree1.bind('<<TreeviewSelect>>', self.sel_tree)

    def get_list(self, event):
        index = self.list1.curselection()[0]       
        var = self.list1.get(index)
        msgbox.showinfo(message='{0}-{1}'.format(index,var))
        self.style.theme_use(var)
        
    def update_tree(self): 
        self.tree1.delete(*self.tree1.get_children())
        for name, widget in self.__dict__.items():
            if hasattr(widget, 'keys'):
                self.tree1.insert('', 0, iid=name,text=name.upper(), 
                    values=tuple(widget.keys()))
    
    def show_hide_tree(self):
        if self.tree1.master.grid_info():
            self.tree1.master.grid_remove()
            self.b2.var.set('Show f5')
        else:
            self.tree1.master.grid()
            self.b2.var.set('Hide f5')
    
    def show_var(self, widget):
        if hasattr(widget, 'var'):
            message = widget.var.get()
        else:
            message = 'No var'
        msgbox.showinfo(message = message)
        
    def menu_cmd(self, name):
        txt = self.mn1.entrycget(name,'label')
        self.mn1.entryconfig(name, label= txt+'-X')
        
    def change_menu(self):
        self.b3.var.set('Change Menu')
        #self.mn0.entryconfig('Menu1', state="disabled")
        self.mn1.entryconfig('cmd1',command=lambda: self.menu_cmd('cmd1'))
        self.mn1.entryconfig(2,command=lambda: self.menu_cmd(2))
        self.mn1.entryconfig(3,command=lambda: self.menu_cmd(3))
        
    def sel_tree(self,event):
        val= self.tree1.item(self.tree1.selection()[0],'values')
        self.txt1.insert('end', val)
        self.txt1.insert('end', '\n')
        
    def show_toplevel(self):
        import Tkinter as tk
        top = tk.Toplevel()
        g = Gui('gui.ini', top)
        top.grab_set() #modal window
        top.focus() 
        g.b1.config(command=lambda: g.b1.var.set('this is toplevel'))

    def run(self):
        self.ROOT.mainloop()           
            
if __name__ == '__main__':
    gui = Gui('gui.ini')
    #print gui.__dict__
    gui.run()