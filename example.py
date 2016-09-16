# -*- coding: utf-8 -*-
"""
Created on Sat Sep 03 13:49:24 2016
@author: q2git
"""
from tkfactory import TkFactory
import tkMessageBox as msgbox

class Gui(TkFactory):
    def __init__(self, filename, master=None):
        #super(Gui, self).__init__(filename, master)
        TkFactory.__init__(self, filename, master)
        self.config_cmd()
        self.update_tree()
        self.list1.listvar.set(self.style.theme_names())
        
    def config_cmd(self):
        #menu
        self.config_menu_cmd()
        #button
        self.b1.config(command=lambda: self.showMsg(self.b1.get()))        
        self.bt1.config(command= self.show_toplevel)
        self.bt2.config(command= self.show_hide_tree)
        #radio group
        for n, w in self.__dict__.items(): 
            if n.startswith('rdgp1_'): 
                w.config(command=lambda: self.showMsg(self.rdgp1.get()))
        #checkbutton        
        self.ckbt1.config(command=lambda: self.showMsg(self.ckbt1.var.get()))
        #spinbox
        self.spb1.config(command=lambda: self.showMsg(self.spb1.get()))
        #optionmenu
        self.opmn1.bind('<Double-Button-1>',
                        lambda _: self.showMsg(self.opmn1.var.get())
                        )
        #scale                
        self.sc2.config(command=lambda _:self.showMsg(self.sc2.get()))
        self.sc1.config(command=lambda _:self.showMsg(self.sc1.get()))       
        #menu button
        self.mnbt1_s.entryconfig('cmd1', command=lambda: self.showMsg('cmd1'))
        self.mnbt1_s.entryconfig('cmd2', command=lambda: self.showMsg('cmd2'))
        #listbox
        self.list1.bind("<<ListboxSelect>>", self.get_list)     
        #progressbar
        self.pg1.start(50)
        self.pg1.bind('<Button-1>', lambda _:self.showMsg(self.pg1.intvar.get()))
        #entry, combobox
        self.e1.bind('<Any-KeyPress>', lambda _: self.showMsg(self.e1.var.get()))
        self.cb1.bind("<<ComboboxSelected>>", lambda _: self.showMsg(self.cb1.get()))
        #treeview
        self.tree1.bind('<<TreeviewSelect>>', self.sel_tree)
        #canvas
        self.cv1.bind("<Button-1>", self.xy)
        self.cv1.bind("<B1-Motion>", self.addLine)
        self.cv1.bind("<Double-Button-1>", lambda _: self.cv1.delete('all'))
        
    #from: http://www.tkdocs.com/tutorial/canvas.html
    lastx, lasty = 0, 0 
    def xy(self, event):
        global lastx, lasty
        lastx, lasty = event.x, event.y
    
    def addLine(self, event):
        global lastx, lasty
        self.cv1.create_line((lastx, lasty, event.x, event.y), fill='red')
        lastx, lasty = event.x, event.y
        
    def get_list(self, event):
        index = self.list1.curselection()[0]       
        var = self.list1.get(index)
        self.style.theme_use(var)
        self.showMsg('{0}-{1}'.format(index,var))
        
    def update_tree(self): 
        self.tree1.delete(*self.tree1.get_children())
        for name, widget in self.__dict__.items():
            if hasattr(widget, 'keys'):
                self.tree1.insert('', 0, iid=name,text=name.upper(), 
                    values=tuple(widget.keys()))
    
    def show_hide_tree(self):
        if self.tree1.master.grid_info():
            self.tree1.master.grid_remove()
            self.b2.var.set('Show Treeview')
        else:
            self.tree1.master.grid()
            self.b2.var.set('Hide Treeview')
    
    def showMsg(self, msg):
        self.msg1.var.set('{0:20}'.format(msg))
        
    def config_menu_cmd(self):
        s = self.mn1.entrycget(0,'label') #tearoff=0, so index starts from 0
        self.mn1.entryconfig(0, command=lambda: self.showMsg(s))
        self.mn1.entryconfig('cmd2', command=lambda: self.showMsg('cmd2'))
        self.mn1.entryconfig('cmd3', command=lambda: self.showMsg('cmd3'))
        
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
        self.wm_state('withdrawn')
        g = Gui('gui.ini',self)
        self.top = g
        self.top.grab_set() #modal window
        self.top.focus() 
        g.b1.var.set('top level window')
        g.b1.config(command=lambda: self.b1.var.set('changed by toplevel'))
        self.top.protocol('WM_DELETE_WINDOW', self.close_top )
    
    def close_top(self):
        self.wm_state('normal')
        self.focus()
        self.top.destroy()

    def run(self):
        self.mainloop()           

            
if __name__ == '__main__':
    gui = Gui('gui.ini')
    #print gui.__dict__
    gui.run()