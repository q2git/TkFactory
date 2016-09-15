# -*- coding: utf-8 -*-
"""
update: 20160914
@author: q2git
"""

import Tkinter as tk
import ttk
import codecs
import ast

class TkFactory(object):    
    def __init__(self, filename, master=None):
        if master:
            self.ROOT = tk.Frame(master)
            config_grid(self.ROOT, {'sticky':'nsew'})
        else:
            self.ROOT = tk.Tk()
        self.createWidgets(get_cfgs(filename))
       
    def createWidgets(self, widgets_cnf): 
        w = {
                'TREEVIEW': _Tree, 'LISTBOX': _Listbox,
                'STYLE': _Style, 'MENU': _Menu,
                'ADD': add_children, 
            }

        for cnf in widgets_cnf:
            name, s_widget, parent = cnf.pop('ATTR')
            master = getattr(self, parent, None)
            
            if s_widget in w.keys():
                w[s_widget](self, name, master, cnf)
            else:
                setattr(self, name, 
                        getattr(
                                tk if s_widget.startswith('tk.') else ttk, 
                                s_widget[s_widget.find('.')+1:]
                                )(master)
                        )

                grid = cnf.pop('GRID', None)
                widget = getattr(self, name)
                config_grid(widget, grid)
                config_opts(widget, cnf) 

           
class _Menu(tk.Menu):
    """ Menu widget """
    def __init__(self, obj, name, master, cnf={}, **kwargs):
        tk.Menu.__init__(self, master, **kwargs)
        setattr(obj, name, self)
        self._configMe(cnf)
        
    def _configMe(self, cnf):
        label = cnf.get('title')
        submenus = cnf.pop('SUBMENUS', None)
        if isinstance(self.master, _Menu): #for meunu
            self.master.add_cascade(label=label,menu=self,underline=0)
        elif 'menu' in self.master.keys(): #for root,menubutton, etc.
            self.master.config(menu=self)
        if submenus: #add submenu
            for kind, coption in submenus:
                self.add(kind, **coption)              
        
    
class _Tree(ttk.Frame):
    """ framed treeview with scrollbars """
    def __init__(self, obj, name, master, cnf={}, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        self['padding'] = 1
        self.tree =ttk.Treeview(self)
        setattr(obj, name, self.tree)      
        self._configMe(cnf)
               
    def _configMe(self, cnf):
        grid = cnf.pop('GRID', None)
        columns = cnf.pop('COLUMNS',None)
        heading = cnf.pop('HEADING',None)
        col_width = cnf.pop('COL_WIDTH',None)
        icon_col = cnf.pop('ICON_COL',None) #(text,width)
        VSB = cnf.pop('VSB',True)
        HSB = cnf.pop('HSB',False)                    
        if icon_col: #The icon column
            self.tree.heading('#0',text=icon_col['text'])
            self.tree.column('#0',width=icon_col['width'])      
        if columns and heading and col_width:
            self.tree.config(columns=columns)
            for cid,text,width in zip(columns,heading,col_width):
                self.tree.heading(cid,text=text) 
                self.tree.column(cid,width=width)
        
        self.tree.config(**cnf)
        self.tree.grid(row=0, column=0, sticky='nsew') 
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)        
        add_scrollbar(self.tree, VSB, HSB)        
        config_grid(self, grid)


class _Listbox(ttk.Frame):
    """ framed listbox with scrollbars """
    def __init__(self, obj, name, master, cnf={}, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        self['padding'] = 1
        self.listbox =tk.Listbox(self)
        setattr(obj, name, self.listbox)   
        self._configMe(cnf)
        
    def _configMe(self, cnf):
        grid = cnf.pop('GRID', None)
        VSB = cnf.pop('VSB',True)
        HSB = cnf.pop('HSB',False) 
        setattr(self.listbox, 'listvar', tk.StringVar())
        self.listbox.config(listvariable=self.listbox.listvar)
        self.listbox.listvar.set(cnf.pop('listvariable', None)) 
        self.listbox.config(**cnf)
        self.listbox.grid(row=0, column=0, sticky='nsew') 
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        add_scrollbar(self.listbox, VSB, HSB)        
        config_grid(self, grid) 
        
    
class _Style(ttk.Style):
    """ ttk style """
    def __init__(self, obj, name, master, cnf={}):
          ttk.Style.__init__(self, master)
          setattr(obj, name, self)
          self._createStyles(cnf)
          
    def _createStyles(self, cnf): 
        self.theme_use(cnf.pop('THEME_USE', 'default'))
        for style_name, style_opts in cnf.items():
            self.configure(style_name, **style_opts)                 


def add_scrollbar(widget, vsb=True, hsb=True):
    """ adding scrollbar to the framed widgets, eg: treeview, listbox 
    """
    master = widget.master #master is a frame
    if vsb: #vertical scrollbar
        vsb = ttk.Scrollbar(master,orient="vertical", command=widget.yview)
        widget.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky='ns')                            
    if hsb: #horizontal scrollbar
        hsb = ttk.Scrollbar(master,orient="horizontal",command=widget.xview)
        widget.configure(xscrollcommand=hsb.set)   
        hsb.grid(row=1, column=0, sticky='ew')  
        

def add_children(obj, name, master, cnf={}):
    """ for panedwindow and notebook to add its children
    """
    children = cnf.pop('CHILDREN', [])
    for name, options in children:
        child = getattr(obj, name)
        master.add(child, **options)        


def config_grid(widget, grid):
    """config grid and stretching option for widget
    """
    if isinstance(grid, dict):
        weight_row = grid.pop('WEIGHT_ROW', 1)
        weight_col = grid.pop('WEIGHT_COL', 1)
        widget.grid(**grid)
        grid_info = widget.grid_info()      
        row = grid.get('row',grid_info.get('row',0))
        col = grid.get('column',grid_info.get('column',0))                                 
        widget.master.rowconfigure(row, weight=weight_row)           
        widget.master.columnconfigure(col,  weight=weight_col)  


def config_opts(widget, opts): 
    """config options for widget 
    """
    if hasattr(widget, 'keys'): #must be a widget
        if 'textvariable' in widget.keys():
            setattr(widget, 'var', tk.StringVar())
            widget.config(textvariable=widget.var)
            widget.var.set(opts.pop('text', None))                     
        #set the rest of options    
        widget.config(**opts)


def get_cfgs(filename):
    """ Read gui configurations from the ini file """       
    with codecs.open(filename,'r','utf_8_sig') as f:
        return ast.literal_eval(f.read())                       

                                
if __name__ == '__main__':
    gui = TkFactory('gui.ini')
    gui.ROOT.mainloop()