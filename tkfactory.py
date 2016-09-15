# -*- coding: utf-8 -*-
"""
update: 20160915
@author: q2git
"""

import Tkinter as tk
import ttk
import codecs
import ast

class TkFactory(tk.Tk, tk.Toplevel):    
    def __init__(self, filename, master=None):
        if master: #choose root widget
            tk.Toplevel.__init__(self,master)
        else:
            tk.Tk.__init__(self)
        cfgs = get_cfgs(filename)  
        self.configRoot(**cfgs.pop(0))
        self.createWidgets(cfgs)

    def configRoot(self, **kwargs):
        """ Config the root window """         
        self.geometry(kwargs.pop('GEOMETRY', None))
        self.resizable(**kwargs.pop('RESIZEABLE', {}))
        self.iconbitmap( kwargs.pop('ICONBITMAP', None))
        self.title(kwargs.pop('TITLE', None))    
        self.config(kwargs)
        
    def createWidgets(self, widgets_cnf): 
        f = {
            'TREEVIEW': create_Treeview, 'LISTBOX': create_Listbox,
            'STYLE': create_Style, 'MENU': create_Menu, 'ADD': add_Children, 
            }

        for cnf in widgets_cnf:
            name, kind, parent_ = cnf.pop('ATTR')
            parent = getattr(self, parent_, self)        
            fun = f.get(kind)
            try:
                if fun:
                    widget = fun(self, PARENT=parent, **cnf)
                else:
                    widget = create_basicWidget(self, PARENT=parent, 
                                                KIND=kind, **cnf)
                setattr(self, name, widget)
            except Exception as e:
                print name, e
       

def create_basicWidget(root, **kwargs):
    """ create basic widget """
    d = {'tk': tk, 'ttk': ttk}
    parent = kwargs.pop('PARENT', root) #parent widget
    cls, kind = kwargs.pop('KIND').split('.')
    grid = kwargs.pop('GRID', None)
    w = getattr(d[cls], kind)(parent)
    config_grid(w, grid)
    config_opts(w, kwargs)
    return w     
 
   
def create_Menu(root, **kwargs):
    """ create menu """
    parent = kwargs.pop('PARENT', root) #parent widget
    m = tk.Menu(parent)
    label = kwargs.get('title')
    submenus = kwargs.pop('SUBMENUS', None)
    if isinstance(m.master, tk.Menu): #for meunu
        m.master.add_cascade(label=label,menu=m,underline=0)
    elif 'menu' in m.master.keys(): #for root,menubutton, etc.
        m.master.config(menu=m)
    if submenus: #add submenu
        for kind, coption in submenus:
            m.add(kind, **coption) 
    return m
                               
    
def create_Treeview(root, **kwargs):
    """ framed treeview with scrollbars """   
    parent = kwargs.pop('PARENT', root) #parent widget
    frame = ttk.Frame(parent, padding=1)
    tree =ttk.Treeview(frame)
    
    grid = kwargs.pop('GRID', None)
    columns = kwargs.pop('COLUMNS',None)
    heading = kwargs.pop('HEADING',None)
    col_width = kwargs.pop('COL_WIDTH',None)
    icon_col = kwargs.pop('ICON_COL',None) #(text,width)
    VSB = kwargs.pop('VSB',True)
    HSB = kwargs.pop('HSB',False) 
                          
    if icon_col: #The icon column
        tree.heading('#0',text=icon_col['text'])
        tree.column('#0',width=icon_col['width'])      
    if columns and heading and col_width:
        tree.config(columns=columns)
        for cid,text,width in zip(columns,heading,col_width):
            tree.heading(cid,text=text) 
            tree.column(cid,width=width)

    tree.config(kwargs)
    add_scrollbar(tree, VSB, HSB) #add scrollbar for treeview  
    tree.grid(row=0, column=0, sticky='nsew')        
    config_grid(frame, grid) 
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)      
    return tree    


def create_Listbox(root, **kwargs):
    """ framed listbox with scrollbars """
    parent = kwargs.pop('PARENT', root) #parent widget
    frame = ttk.Frame(parent, padding=1)
    listbox = tk.Listbox(frame) 

    grid = kwargs.pop('GRID', None)
    VSB = kwargs.pop('VSB',True)
    HSB = kwargs.pop('HSB',False) 
    
    setattr(listbox, 'listvar', tk.StringVar())
    listbox.config(listvariable=listbox.listvar)
    listbox.listvar.set(kwargs.pop('listvariable', None)) 
    listbox.config(kwargs)
    add_scrollbar(listbox, VSB, HSB)     
    listbox.grid(row=0, column=0, sticky='nsew') 
    config_grid(frame, grid)    
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)            
    return listbox    
                 

def create_Style(master, **kwargs):
    """ create style """
    cnf = kwargs.pop('style', {})
    s = ttk.Style(master)
    s.theme_use(cnf.pop('THEME_USE', 'default'))
    for style_name, style_opts in cnf.items():
        s.configure(style_name, **style_opts) 
    return s
 

def add_Children(root, **kwargs):
    """ for panedwindow and notebook to add its children
    """
    parent = kwargs.pop('PARENT', root) #parent widget
    children = kwargs.pop('CHILDREN', [])
    for name, options in children:
        child = getattr(root, name)
        parent.add(child, **options)        


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
    gui.mainloop()