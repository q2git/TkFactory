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
    def __init__(self,ini_file,cmds):
        tk_ini = ast.literal_eval(codecs.open(ini_file,'r','utf_8_sig').read())
        self.widgets = {}
        self.textvariables = {}
        self.cmds = cmds
        if tk_ini.has_key('widgets'):
            self._createWidgets(tk_ini['widgets'])
        if tk_ini.has_key('styles'):
            self._config_styles(tk_ini['styles'])
            
    def _createWidgets(self,cfg_widgets):
        "name,type,parent,(grids),{options}"
        for name,w_type,parent,grids,opts in cfg_widgets:                
            if w_type == 'Tk': 
                self._config_root(name, opts)
                continue #the rest codes will not be excuted
            try: #get ttk widget instance
                self.widgets[name] =  getattr(ttk,w_type)(self.widgets[parent]) 
            except AttributeError: #get tk widget instance
                self.widgets[name] =  getattr(tk,w_type)(self.widgets[parent])

            if w_type == 'Treeview': #config treeview
                self._config_treeview(name, opts)
            if w_type == 'Menu': #config treeview
                self._config_menu(name, grids, opts)
                continue
                
            self._config_widget(name, opts) #config options
            self._config_grid(name, grids)      

    def _config_root(self, name, opts):
        "config root window"
        self.widgets[name] =  tk.Tk()
        self.root = self.widgets[name]
        if opts.has_key('geometry'):self.root.geometry(opts['geometry'])
        if opts.has_key('resizable'):self.root.resizable(width=opts['resizable'][0],height=opts['resizable'][1])
        if opts.has_key('iconbitmap'):self.root.iconbitmap(opts['iconbitmap'])
        if opts.has_key('title'):self.root.title(opts['title'])     
    
    def _config_grid(self, name, grids):
        "config grid"
        row_id,col_id,row_span,col_span,sticky,stretch_row,stretch_col = grids        
        self.widgets[name].grid(row=row_id,column=col_id,rowspan=row_span,
                           columnspan=col_span,sticky=sticky)        
        if stretch_row!=0:  #enable stretching                      
            self.widgets[name].master.rowconfigure(row_id,weight=stretch_row)
        if stretch_col!=0:  #enable stretching     
            self.widgets[name].master.columnconfigure(col_id,weight=stretch_col)     
                
    def _config_styles(self,cfg_styles):
        "config styles"
        self.root.s=ttk.Style()
        for name, opts in cfg_styles:
            if name == 'theme_use':
                self.root.s.theme_use(opts)
                continue #jump to next loop
            self.root.s.configure(name,**opts)                
                      
    def _config_widget(self,name,opts): 
        "config the widget with specified option"
        if self.widgets[name].configure().has_key('textvariable'):
            self.textvariables[name] = tk.StringVar()
            self.widgets[name].config(textvariable=self.textvariables[name])
            if opts.has_key('text'):
                self.textvariables[name].set(opts['text'])
                opts.pop('text')
        #set the rest options    
        self.widgets[name].config(**opts)
        
    def _config_menu(self, name, submenus, opts):
        "config menu"
        if isinstance(self.widgets[name].master,tk.Menu):
            self.widgets[name].master.add_cascade(label=opts['title'],menu=self.widgets[name],underline=0)
        elif self.widgets[name].master.config().has_key('menu'):
            self.widgets[name].master.config(menu=self.widgets[name])
        for kind, coption in submenus:
            self.widgets[name].add(kind, command=self.cmds[coption.pop('command')], **coption)
            
        self._config_widget(name, opts)      
            
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
        
                                
if __name__ == '__main__':
    def fun(event=None):
        print 'hh'
    gui = TkFactory('gui.ini',{'CMD1':fun,'CMD3':fun,'None':None})
    gui.widgets['bt_1'].config(command=lambda x=0:gui.textvariables['TestDataID'].set('Hello'))
    gui.widgets['ckbt1'].config(command=lambda x=0:gui.textvariables['ckbt1'].set(gui.textvariables['SampleRun'].get()))
    #gui.widgets['mn1'].add('cascade',label='test')
    #gui.widgets['mn2'].add('cascade',label='test2')

    gui.run()

    #print ast.literal_eval(codecs.open('gui.ini','r','utf_8_sig').read())
