# -*- coding: utf-8 -*-
"""
update: 20160911
@author: q2git
"""

import Tkinter as tk
import ttk
import codecs
import ast

    
class TkFactory(object):    
    def __init__(self, filename):
        self.topWindows = {} #store configs of all toplevel windows
        self.widgetNames = set() #no duplication in widgetNames
        self.createWidgets(get_cfgs(filename))
        
    def createWidgets(self, widgets_cfgs):
        """ Create the widgets """
        
        funcs =  {'tk.Menu':self._menu, 
                  'ttk.Notebook':self._notebook,
                  'tk.PanedWindow':self._panedwindow, 
                  'ttk.Treeview': self._treeview,
                  'ttk.Style': self._styles,
                  'tk.Tk': self._toplevel,
                  'tk.Toplevel': self._toplevel,
                  'tk.Listbox': self._listbox,
                  }
                  
        for widget_cfgs in widgets_cfgs:
            
            if isinstance(widget_cfgs, list):
                self.topWindows[widget_cfgs.pop(0)] = widget_cfgs
                continue
            
            name, widget, parent = widget_cfgs.pop('ATTR')
            grid = widget_cfgs.pop('GRID', None)
            opts = widget_cfgs 
            
            setattr(self, name, 
                    getattr(
                            tk if widget.startswith('tk.') else ttk, 
                            widget[widget.find('.')+1:]
                            )(getattr(self, parent, None))
                    )
            
            self.config_grid(name, grid)      
            funcs.get(widget,lambda x,y: 0)(name, opts) #config special options
            self._config_opts(name, opts)
            
    def _config_opts(self, name, opts): 
        """Config the rest of options """
        widget = getattr(self, name)
        if hasattr(widget, 'keys'): #must be a widget not the style
            if 'textvariable' in widget.keys():
                setattr(widget, 'var', tk.StringVar())
                widget.config(textvariable=widget.var)
                widget.var.set(opts.pop('text', None))                     
            #set the rest of options    
            widget.config(**opts)
            #store all widgets name
            self.widgetNames.add(name)
        
    def config_grid(self, name, grid):
        """Config the grid and stretching options
        """
        if isinstance(grid, dict):
            widget = getattr(self, name)
            stretch_row = grid.pop('STRETCH_ROW', 0)
            stretch_col = grid.pop('STRETCH_COL', 0)
            widget.grid(**grid) 
                    
            if stretch_row:  #enable row stretching                   
                widget.master.rowconfigure(grid.get('row'), 
                                           weight=stretch_row)           
            if stretch_col:  #enable col stretching     
                widget.master.columnconfigure(grid.get('column'), 
                                              weight=stretch_col)  

    def _toplevel(self, name, opts):
        """ Config the root/toplevel window """ 
        widget = getattr(self, name)         
        widget.geometry(opts.pop('GEOMETRY', None))
        widget.resizable(**opts.pop('RESIZEABLE', {}))
        widget.iconbitmap( opts.pop('ICONBITMAP', None))
        widget.title(opts.pop('TITLE', None))    

        
    def _styles(self, name, opts):
        """ Config the ttk styles """  
        style = getattr(self, name)
        style.theme_use(opts.pop('THEME_USE', 'default'))
        for style_name, style_opts in opts.items():
            style.configure(style_name, **style_opts) 
            
    def _treeview(self, name, opts):
        """ config the notebook """
        widget = getattr(self, name) 
        
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
        if columns and heading and col_width:
            widget.config(columns=columns)
            for cid,text,width in zip(columns,heading,col_width):
                widget.heading(cid,text=text) 
                widget.column(cid,width=width) 
        
    def _menu(self, name, opts):
        """ config the menu """
        widget = getattr(self, name)
        label = opts.get('title')
        submenus = opts.pop('SUBMENUS', None)
        if isinstance(widget.master,tk.Menu): #for meunu
            widget.master.add_cascade(label=label,menu=widget,underline=0)
        elif 'menu' in widget.master.keys(): #for root,menubutton, etc.
            widget.master.config(menu=widget)
        if submenus: #add submenu
            for kind, coption in submenus:
                widget.add(kind, **coption)
                    
    def _notebook(self, name, opts):
        """ config the notebook """
        widget = getattr(self, name)
        for child, kw in opts.pop('TABS', []):
            widget.add(getattr(self, child), **kw) 
                  
    def _panedwindow(self, name, opts):
        """ config the panedwindow """
        widget = getattr(self, name)
        for child, kw in opts.pop('PANES', []):
            widget.add(getattr(self, child), **kw)

    def _listbox(self, name, opts):
        """Config the listbox """
        widget = getattr(self, name)
        setattr(widget, 'listvar', tk.StringVar())
        widget.config(listvariable=widget.listvar)
        widget.listvar.set(opts.pop('listvariable', None))           

def get_cfgs(filename):
    """ Read gui configurations from the ini file """       
    with codecs.open(filename,'r','utf_8_sig') as f:
        return ast.literal_eval(f.read())                       

                                
if __name__ == '__main__':
    gui = TkFactory('gui.ini')    
    gui.root.mainloop()
