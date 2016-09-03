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
        self.widgets = {None:None}
        self.textvariables = {}
        WIDGETS, STYLES = read_ini(ini_file)
        
        self._create_root(WIDGETS.pop(0)) #create root
        self._config_styles(STYLES) #config style
        self._createWidgets(WIDGETS) #create widget
        
    def _create_root(self, cfg):
        """ Create the root window """
        if cfg is None:
            return         
        name, opts = cfg
        self.widgets[name] =  tk.Tk()
        self.root = self.widgets[name]
        geometry = opts.pop('geometry', None)
        resizable = opts.pop('resizable', None)
        iconbitmap = opts.pop('iconbitmap', None)
        title = opts.pop('title', None)
        
        if geometry:
            self.root.geometry(geometry)
        if resizable:
            self.root.resizable(width=resizable[0],height=resizable[1])
        if iconbitmap:
            self.root.iconbitmap(iconbitmap)
        if title:
            self.root.title(title)
                 
    def _config_styles(self,cfg):
        """ Config the ttk styles """
        if cfg is None:
            return           
        self.root.s=ttk.Style()
        for name, opts in cfg:
            if name == 'theme_use':
                self.root.s.theme_use(opts)
                continue #jump to next loop
            self.root.s.configure(name,**opts) 
            
    def _createWidgets(self,cfg_widgets):
        """
        Create the widgets
        cfg_widgets = 
         ( name,widget, parent,
           (grid), -->(row,col,row-span,col-span,sticky,row-stretch,col-stretch)
           {options}
          )
        """
        tk_ttk = {'tk':tk, 'ttk':ttk}
        for name,widget,parent,grid,opts in cfg_widgets:
            obj, w = widget.split('.') 
            
            #create tk or ttk widgets instance
            self.widgets[name] = getattr(tk_ttk[obj],w)(self.widgets[parent]) 
                
            if w == 'Treeview': #config treeview
                config_treeview(self.widgets[name], opts)
                
            if w == 'Menu': #config treeview
                config_menu(self.widgets[name], opts)
                
            if w == 'Notebook' and opts.has_key('TABS'): #config notebook
                for child,kw in opts.pop('TABS'):
                    self.widgets[name].add(self.widgets[child], **kw)
                    
            if w == 'PanedWindow' and opts.has_key('PANES'): #config notebook
                for child,kw in opts.pop('PANES'):
                    self.widgets[name].add(self.widgets[child], **kw)
                    
            self._config_options(name, opts) #config options
            config_grid(self.widgets[name], grid)
            #if grid is not None:
            #    self._config_grid(name, grid)                                          
                      
    def _config_options(self,name,opts): 
        """
        Config the rest of options
        """
        if self.widgets[name].config().has_key('textvariable'):
            self.textvariables[name] = tk.StringVar()
            self.widgets[name].config(textvariable=self.textvariables[name])
            text = opts.pop('text', None)
            if text:
                self.textvariables[name].set(text)              
        #set the rest of options    
        self.widgets[name].config(**opts)
       
    def run(self):
        self.root.mainloop()
    
    def stop(self):
        self.root.destroy()


def read_ini(ini_file):
    """ 
    Read gui configurations from the ini file 
    """
    with codecs.open(ini_file,'r','utf_8_sig') as f:
        cfg = ast.literal_eval(f.read())   

    return (cfg.pop('WIDGETS', None) , cfg.pop('STYLES', None),)
    

def config_grid(widget, grid):
    """
    Config the grid and stretching options
    """
    if grid is None: 
        return
        
    row_id,col_id,row_span,col_span,sticky,stretch_row,stretch_col = grid
    
    widget.grid(row=row_id,column=col_id,rowspan=row_span,
                       columnspan=col_span,sticky=sticky) 
                       
    if stretch_row!=0:  #enable stretching                      
        widget.master.rowconfigure(row_id,weight=stretch_row)
        
    if stretch_col!=0:  #enable stretching     
        widget.master.columnconfigure(col_id,weight=stretch_col)  
            

def config_menu(widget, opts):
    """
    Config the menu widget
    """
    label = opts.get('title')
    submenus = opts.pop('SUBMENUS', None)
    if isinstance(widget.master,tk.Menu): #for meunu
        widget.master.add_cascade(label=label,menu=widget,underline=0)
    elif widget.master.config().has_key('menu'): #for menubutton, etc.
        widget.master.config(menu=widget)
    if submenus: #add submenu
        for kind, coption in submenus:
            widget.add(kind, **coption)


def config_treeview(widget, opts):
    """
    Config the treeview widget
    """        
    columns = opts.pop('columns',None)
    heading = opts.pop('heading',None)
    col_width = opts.pop('col_width',None)
    icon_col = opts.pop('#0',None) #(text,width)
    VSB = opts.pop('VSB',None)
    HSB = opts.pop('HSB',None)
    
    if VSB: #vertical scrollbar
        vsb = ttk.Scrollbar(widget.master,orient="vertical",
                            command=widget.yview)
        widget.configure(yscrollcommand=vsb.set)
        vsb.grid(row=VSB[0],column=VSB[1],rowspan=VSB[2],
                           columnspan=VSB[3], sticky='ns')                            
    if HSB: #horizontal scrollbar
        hsb = ttk.Scrollbar(widget.master,orient="horizontal",
                            command=widget.xview)
        widget.configure(xscrollcommand=hsb.set)   
        hsb.grid(row=HSB[0],column=HSB[1],rowspan=HSB[2],
                           columnspan=HSB[3], sticky='ew')  
    if icon_col: #The icon column
        widget.heading('#0',text=icon_col['text'])
        widget.column('#0',width=icon_col['width'])
    #heading and column width        
    if columns and heading and col_width:
        widget.config(columns=columns)
        for cid,text,width in zip(columns,heading,col_width):
            widget.heading(cid,text=text) #heading column
            widget.column(cid,width=width) #column width   

                                
if __name__ == '__main__':
    gui = TkFactory('gui.ini')
    gui.run()
