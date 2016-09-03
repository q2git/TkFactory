# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 13:29:02 2016

@author: q2git
"""

import Tkinter as tk
import ttk
import codecs
import ast

class TkFactory:
    def __init__(self,ini_file):
        tk_ini = ast.literal_eval(codecs.open(ini_file,'r','utf_8_sig').read())
        self.widgets = {}
        self.textvariables = {}
        self._config_root(tk_ini['WIDGETS'].pop(0)) #config root
        if tk_ini.has_key('STYLES'): self._config_styles(tk_ini['STYLES']) #config style
        self._createWidgets(tk_ini['WIDGETS']) #config widget
        
    def _config_root(self, cfg):
        "config root window"
        name, opts = cfg
        self.widgets[name] =  tk.Tk()
        self.root = self.widgets[name]
        if opts.has_key('geometry'):self.root.geometry(opts['geometry'])
        if opts.has_key('resizable'):self.root.resizable(width=opts['resizable'][0],height=opts['resizable'][1])
        if opts.has_key('iconbitmap'):self.root.iconbitmap(opts['iconbitmap'])
        if opts.has_key('title'):self.root.title(opts['title'])
                 
    def _config_styles(self,cfg_styles):
        "config styles"
        self.root.s=ttk.Style()
        for name, opts in cfg_styles:
            if name == 'theme_use':
                self.root.s.theme_use(opts)
                continue #jump to next loop
            self.root.s.configure(name,**opts) 
            
    def _createWidgets(self,cfg_widgets):
        "name,widget,parent,(grid),{options}"
        tk_ttk = {'tk':tk, 'ttk':ttk}
        for name,widget,parent,grid,opts in cfg_widgets:
            obj, widget_name = widget.split('.')            
            if parent == None:
                self.widgets[name] = getattr(tk_ttk[obj],widget_name)()              
            else:
                self.widgets[name] = getattr(tk_ttk[obj],widget_name)(self.widgets[parent]) 
                
            if widget_name == 'Treeview': #config treeview
                self._config_treeview(name, opts)
            if widget_name == 'Menu': #config treeview
                self._config_menu(name, opts)
            if widget_name == 'Notebook' and opts.has_key('TABS'): #config notebook
                for child,kw in opts.pop('TABS'):
                    self.widgets[name].add(self.widgets[child], **kw)
            if widget_name == 'PanedWindow' and opts.has_key('PANES'): #config notebook
                for child,kw in opts.pop('PANES'):
                    self.widgets[name].add(self.widgets[child], **kw)
                    
            self._config_widget(name, opts) #config options
            if grid is not None:
                self._config_grid(name, grid)      
    
    def _config_grid(self, name, grids):
        "config grid"
        row_id,col_id,row_span,col_span,sticky,stretch_row,stretch_col = grids        
        self.widgets[name].grid(row=row_id,column=col_id,rowspan=row_span,
                           columnspan=col_span,sticky=sticky)        
        if stretch_row!=0:  #enable stretching                      
            self.widgets[name].master.rowconfigure(row_id,weight=stretch_row)
        if stretch_col!=0:  #enable stretching     
            self.widgets[name].master.columnconfigure(col_id,weight=stretch_col)                                    
                      
    def _config_widget(self,name,opts): 
        "config the widget with specified option"
        if self.widgets[name].config().has_key('textvariable'):
            self.textvariables[name] = tk.StringVar()
            self.widgets[name].config(textvariable=self.textvariables[name])
            if opts.has_key('text'):
                self.textvariables[name].set(opts['text'])
                opts.pop('text')
        #set the rest options    
        self.widgets[name].config(**opts)
        
    def _config_menu(self, name, opts):
        "config menu"
        if isinstance(self.widgets[name].master,tk.Menu):
            self.widgets[name].master.add_cascade(label=opts['title'],menu=self.widgets[name],underline=0)
        elif self.widgets[name].master.config().has_key('menu'):
            self.widgets[name].master.config(menu=self.widgets[name])
        if opts.has_key('SUBMENUS'):
            for kind, coption in opts.pop('SUBMENUS'):
                self.widgets[name].add(kind, **coption)
                
    def _config_treeview(self, name, opts):
        vsb = ttk.Scrollbar(self.widgets[name].master,orient="vertical", command=self.widgets[name].yview)
        hsb = ttk.Scrollbar(self.widgets[name].master,orient="horizontal", command=self.widgets[name].xview)
        self.widgets[name].configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew') 
        if opts.has_key('columns'):self.widgets[name].config(columns=opts['columns'])
        if opts.has_key('#0'): #The icon column
            self.widgets[name].heading('#0',text=opts['#0']['text'])
            self.widgets[name].column('#0',width=opts['#0']['width'])
            opts.pop('#0')
        for cid,text,width in zip(opts['columns'],opts['heading'],opts['col_width']):
            self.widgets[name].heading(cid,text=text) #heading column
            self.widgets[name].column(cid,width=width) #column width 
        opts.pop('heading')
        opts.pop('col_width')
        opts.pop('columns')        
            
    def run(self):
        self.root.mainloop()
    
    def stop(self):
        self.root.destroy()
        
                                
if __name__ == '__main__':
    gui = TkFactory('gui.ini')
    gui.widgets['b1'].config(command=lambda x=0:gui.textvariables['e1'].set('Hello'))
    gui.widgets['rdbt1'].config(command=lambda x=0:gui.textvariables['ckbt1'].set('CheckButton1'))
    gui.widgets['ckbt1'].config(command=lambda x=0:gui.textvariables['ckbt1'].set(gui.textvariables['rdbt1'].get()))
    gui.widgets['mn2'].entryconfig(1,command=gui.stop)
    def fun(i):
        gui.widgets['mn1'].entryconfig(1,label='title{}'.format(i))
        gui.widgets['mn2'].entryconfig(1,label='hello{}'.format(i))
    gui.widgets['mn3'].entryconfig(0,command=lambda :fun(1))
    gui.widgets['mn3'].entryconfig(1,command=lambda :fun(2))
    gui.widgets['mn3'].entryconfig(2,command=lambda :fun(3))    
    gui.widgets['tree1'].insert('', 0, iid=11,text='hello', values=('a','b',234,324,'c','你好',),)
    gui.widgets['s1'].config(command=lambda x=0:gui.textvariables['ls1'].set(gui.widgets['s1'].get()))
    gui.widgets['pg1'].start(50)

    gui.run()


    #print ast.literal_eval(codecs.open('gui.ini','r','utf_8_sig').read())
