# -*- coding: utf-8 -*-
"""
update: 20160917
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
        #bind_all
        self.bind_all('<Control-KeyPress-q>', self.stop)
        #menu
        self.config_menu_cmd()
        #button
        self.b1.config(command=lambda: self.showMsg(self.b1.var.get()))        
        self.bt1.config(command= self.show_toplevel)
        self.bt2.config(command= self.show_hide_tree)
        #entry
        self.e1.bind('<Any-KeyRelease>', lambda _: self.showMsg(self.e1.var.get()))
        #radio group -bind to the shared variable
        self.rdgp1.trace('w', lambda *_: self.showMsg(self.rdgp1.get()) )               
        #checkbutton        
        self.ckbt1.config(command=lambda:self.showMsg(
            self.ckbt1.var.get() + ': ' + str(self.ckbt1.intvar.get()))
            )
        #spinbox
        self.spb1.config(command=lambda: self.showMsg(self.spb1.get()))
        #optionmenu
        self.opmn1.var.trace('w',lambda *_: self.showMsg(self.opmn1.var.get()))
        #scale                
        self.sc2.config(command=lambda _:self.showMsg(self.sc2.get()))
        self.sc1.config(command=lambda _:self.showMsg(self.sc1.get()))       
        #menu button
        self.mnbt1_s.entryconfig('cmd1', command=lambda: self.showMsg('cmd1'))
        self.mnbt1_s.entryconfig('cmd2', command=lambda: self.showMsg('cmd2'))
        #listbox
        self.list1.bind("<<ListboxSelect>>", self.get_list) 
        #text
        self.txt1.bind('<Double-1>',lambda _:self.txt1.delete('1.0', 'end'))
        #progressbar
        self.pg1.start(50)
        self.pg1.bind('<1>', lambda _:self.showMsg(self.pg1.intvar.get()))
        #combobox
        self.cb1.bind("<<ComboboxSelected>>", lambda _: self.showMsg(self.cb1.get()))
        #treeview
        self.tree1.bind('<<TreeviewSelect>>', self.sel_tree)
        #canvas
        self.cv1.bind("<Button-1>", self.xy)
        self.cv1.bind("<B1-Motion>", self.addLine)
        self.cv1.bind("<Double-Button-1>", lambda _: self.cv1.delete('all'))
      
    def show_toplevel(self):
        self.wm_state('withdrawn')
        g = Gui('gui.ini',self)
        self.top = g
        self.top.grab_set() #modal window
        self.top.focus() 
        g.bt1.var.set('top level window')
        g.bt1.config(command=lambda: self.bt1.var.set('changed by toplevel'))
        self.top.protocol('WM_DELETE_WINDOW', self.close_top )
    
    def close_top(self):
        self.wm_state('normal')
        self.focus()
        self.top.destroy()
        
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
            self.bt2.var.set('Show Treeview')
        else:
            self.tree1.master.grid()
            self.bt2.var.set('Hide Treeview')
    
    def showMsg(self, msg):
        self.nb1.select(0)
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
        self.txt1.insert('1.0', '\n') #'end'
        self.txt1.insert('1.0', val) 
        self.nb1.select(self.txt1)

    def run(self):
        self.mainloop()           
    
    def stop(self, event):
        print 'Event:', event.keycode
        self.destroy()
            
if __name__ == '__main__':
    gui = Gui('gui.ini')
    #print gui.__dict__
    gui.run()