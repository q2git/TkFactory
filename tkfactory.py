# -*- coding: utf-8 -*-
"""
update: 20160917
@author: q2git
"""

import Tkinter as tk
import ttk
import codecs
import ast
import os.path

class TkFactory(tk.Tk, tk.Toplevel):    
    def __init__(self, filename, master=None):
        if master: #choose root widget
            tk.Toplevel.__init__(self,master)
        else:
            tk.Tk.__init__(self)
        self.cfgdir, cfgs = get_cfgs(filename)  
        self.configRoot(**cfgs.pop(0))
        self.createWidgets(cfgs)

    def configRoot(self, **kwargs):
        """ Config the root window """         
        self.geometry(kwargs.pop('GEOMETRY', None))
        self.resizable(**kwargs.pop('RESIZEABLE', {}))
        ico = kwargs.pop('ICONBITMAP', None)
        if ico: 
            self.iconbitmap(os.path.join(self.cfgdir, ico))
        self.title(kwargs.pop('TITLE', None))    
        self.config(kwargs)
        
    def createWidgets(self, widgets_cnf): 
        f = {
            'TREEVIEW':create_Treeview, 'LISTBOX':create_Listbox,
            'STYLE':create_Style, 'MENU':create_Menu, 'ADD':add_Children,
            'OPTIONMENU':create_OptionMenu, 'RADIOGROUP':create_RadioGroup,
            }

        for cnf in widgets_cnf:
            name, kind, parent_ = cnf.pop('ATTR')
            parent = getattr(self, parent_, self)        
            fun = f.get(kind)
            try:
                if fun:
                    widget = fun(self, PARENT=parent, **cnf)
                else:
                    widget = create_BasicWidget(self, PARENT=parent, 
                                                KIND=kind, **cnf)
                setattr(self, name, widget) #set attribution on root                    
            except Exception as e:
                print name, e


def create_BasicWidget(root, **kwargs):
    """ create basic widget """
    d = {'tk': tk, 'ttk': ttk}
    parent = kwargs.pop('PARENT', root) #parent widget
    cls, kind = kwargs.pop('KIND').split('.')
    grid = kwargs.pop('GRID', None)
    w = getattr(d[cls], kind)(parent)
    config_grid(w, grid)
    config_opts(w, kwargs)
    return w     
 
       
def create_OptionMenu(root, **kwargs):
    """ create OptionMenu widget """
    parent = kwargs.pop('PARENT', root) #parent widget
    oplist = kwargs.pop('OPLIST', ())
    grid = kwargs.pop('GRID', None)
    var = tk.StringVar()
    if oplist: var.set(oplist[0]) #set default option
    w = tk.OptionMenu(parent, var, *oplist)
    setattr(w, 'var', var)
    config_grid(w, grid)
    return w
 
   
def create_Menu(root, **kwargs):
    """ create menu """
    parent = kwargs.pop('PARENT', root) #parent widget
    w = tk.Menu(parent)
    copt = kwargs.pop('COPT',{}) #submenu,coption
    items = kwargs.pop('ITEMS', [])
    w.config(**kwargs)
    if isinstance(w.master, tk.Menu): #add submenu
        w.master.add_cascade(menu=w, **copt)
    elif 'menu' in w.master.keys(): #for root,menubutton, etc.
        w.master.config(menu=w)
    for kind, coption in items: #add menu items
        w.add(kind, **coption) 
    return w
                               
    
def create_Treeview(root, **kwargs):
    """ framed treeview with scrollbars """   
    parent = kwargs.pop('PARENT', root) #parent widget
    frms = kwargs.pop('FRMS', {}) #frame setting    
    frame = tk.Frame(parent, **frms)
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
    frms = kwargs.pop('FRMS', {}) #frame setting    
    frame = tk.Frame(parent, **frms)
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
  
               
def create_RadioGroup(root, **kwargs):
    """ create radio group with frame """
    grid = kwargs.pop('GRID', None)
    frms = kwargs.pop('FRMS', {}) #frame setting
    parent = kwargs.pop('PARENT', root) #parent widget
    frame = tk.LabelFrame(parent, **frms)
    config_grid(frame, grid)
    txts = kwargs.pop('TXTS', ())
    vals = kwargs.pop('VALS', ())
    var = tk.StringVar()
    for txt, val in zip(txts, vals):
        rd = tk.Radiobutton(frame, variable=var, text=txt, value=val)
        rd.config(**kwargs)
        rd.grid()
    var.set(None) #default no radiobox selected   
    return var #return the shared variable
 
 
def create_Style(root, **kwargs):
    """ create style """
    parent = kwargs.pop('PARENT', root)
    s = ttk.Style(parent)
    s.theme_use(kwargs.pop('THEME_USE', 'default'))
    for style_name, style_opts in kwargs.items():
        s.configure(style_name, **style_opts) 
    return s
 

def add_Children(root, **kwargs):
    """ for panedwindow and notebook to add its children
    """
    parent = kwargs.pop('PARENT', root) #parent widget
    children = kwargs.pop('CHILDREN', [])

    for name, options in children:
        child = getattr(root, name)
        if isinstance(child, (tk.Listbox,ttk.Treeview)):
            parent.add(child.master, **options)
        else:
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


def config_opts(widget, opts): 
    """config options for widget 
    """
    if hasattr(widget, 'keys'): #must be a widget
        if 'textvariable' in widget.keys():
            setattr(widget, 'var', tk.StringVar())
            widget.config(textvariable=widget.var)
            widget.var.set(opts.pop('text', None)) 
        if 'variable' in widget.keys():
            setattr(widget, 'intvar', tk.IntVar())
            widget.config(variable=widget.intvar)                    
        #set the rest of options    
        widget.config(**opts)
        
        
def config_grid(widget, grid):
    """config grid and stretching option for widget
    """
    if isinstance(grid, dict):
        weight_row = grid.pop('WEIGHT_ROW', 1)
        weight_col = grid.pop('WEIGHT_COL', 1)
        widget.grid(**grid)
        grid_info = widget.grid_info()      
        row = grid.get('row',grid_info.get('row'))
        col = grid.get('column',grid_info.get('column'))                                 
        widget.master.rowconfigure(row, weight=weight_row)           
        widget.master.columnconfigure(col,  weight=weight_col)  
 

def get_cfgs(filename):
    """ Read gui configurations from the ini file """
    cfgdir = os.path.dirname(os.path.abspath(filename))       
    with codecs.open(filename,'r','utf_8_sig') as f:
        cfg = ast.literal_eval(f.read()) 
    return (cfgdir, cfg)                      

                                
if __name__ == '__main__':
    gui = TkFactory('gui.ini')
    gui.mainloop()
