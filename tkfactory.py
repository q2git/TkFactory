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
        #None is for creating widget without specifying parent
        self.widgets = {None:None} 
        self.textvariables = {}
        root, styles, widgets = read_ini(ini_file)
        
        self._create_root(root) 
        self._config_styles(styles)
        self._createWidgets(widgets)
        
    def _create_root(self, opts):
        """ Create the root window 
        """     
        self.widgets['ROOT'] =  tk.Tk()
        geometry = opts.pop('geometry', None)
        resize = opts.pop('resizable', None)
        iconbitmap = opts.pop('iconbitmap', None)
        title = opts.pop('title', None)
        self.widgets['ROOT'].config(**opts)       
        if geometry:
            self.widgets['ROOT'].geometry(geometry)
        if resize:
            self.widgets['ROOT'].resizable(width=resize[0],height=resize[1])
        if iconbitmap:
            self.widgets['ROOT'].iconbitmap(iconbitmap)
        if title:
            self.widgets['ROOT'].title(title)    
                 
    def _config_styles(self, styles):
        """ Config the ttk styles 
        """         
        self.widgets['ROOT'].s=ttk.Style()
        for name, opts in styles:
            if name == 'theme_use':
                self.widgets['ROOT'].s.theme_use(opts)
                continue #jump to next loop
            self.widgets['ROOT'].s.configure(name,**opts) 
            
    def _createWidgets(self, widgets):
        """ Create the widgets
        """
        tk_ttk = {'tk':tk, 'ttk':ttk}
        for name, widget, parent, grid, opts in widgets:
            obj, w = widget.split('.')            
            #create tk or ttk widgets instance
            self.widgets[name] = getattr(tk_ttk[obj], w)(self.widgets[parent]) 
                
            if w == 'Treeview':
                config_treeview(self.widgets[name], opts)          
            if w == 'Menu':
                config_menu(self.widgets[name], opts)                
            if w == 'Notebook': 
                for child,kw in opts.pop('TABS', []):
                    self.widgets[name].add(self.widgets[child], **kw)                    
            if w == 'PanedWindow':
                for child,kw in opts.pop('PANES', []):
                    self.widgets[name].add(self.widgets[child], **kw)
                    
            self._config_options(name, opts) #config options
            config_grid(self.widgets[name], grid)                                        
                      
    def _config_options(self,name,opts): 
        """Config the rest of options
        """
        if 'textvariable' in self.widgets[name].keys():
            self.textvariables[name] = tk.StringVar()
            self.widgets[name].config(textvariable=self.textvariables[name])
            text = opts.pop('text', None)
            if text:
                self.textvariables[name].set(text)              
        #set the rest of options    
        self.widgets[name].config(**opts)
       
    def run(self):
        self.widgets['ROOT'].mainloop()
    
    def stop(self):
        self.widgets['ROOT'].destroy()


def read_ini(ini_file):
    """ 
    Read gui configurations from the ini file 
    """
    with codecs.open(ini_file,'r','utf_8_sig') as f:
        cfg = ast.literal_eval(f.read())   
    root = cfg.pop('ROOT', {})
    styles = cfg.pop('STYLES', [])
    widgets = cfg.pop('WIDGETS', [])
    
    return (root, styles, widgets)
    

def config_grid(widget, grid):
    """
    Config the grid and stretching options
    """
    if grid is not None: 
        row,col,rowspan,colspan,sticky,stretch_row,stretch_col = grid
        widget.grid(row=row, column=col, rowspan=rowspan,
                    columnspan=colspan, sticky=sticky)                         
        if stretch_row!=0:  #enable stretching                      
            widget.master.rowconfigure(row, weight=stretch_row)           
        if stretch_col!=0:  #enable stretching     
            widget.master.columnconfigure(col, weight=stretch_col)  
            

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
