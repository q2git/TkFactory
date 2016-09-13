# -*- coding: utf-8 -*-
"""
update: 20160911
@author: q2git
"""

import Tkinter as tk
import ttk
import codecs
import ast

class _Toplevel(tk.Toplevel):
    """ Toplevel window """
    def __init__(self, name, master, cnf={}, **kwargs):
        tk.Toplevel.__init__(self, master, **kwargs)
        setattr(master, name, self)
       
    
class _Tree(tk.Frame):
    """ ttk Treeview """
    def __init__(self, name, master, cnf={}, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.tree =ttk.Treeview(self)
        setattr(master, name, self.tree)      
        self._createWidgets(cnf)
               
    def _createWidgets(self, cnf={}):
        grid = cnf.pop('GRID', None)
        columns = cnf.pop('COLUMNS',None)
        heading = cnf.pop('HEADING',None)
        col_width = cnf.pop('COL_WIDTH',None)
        icon_col = cnf.pop('ICON_COL',None) #(text,width)
        VSB = cnf.pop('VSB',None)
        HSB = cnf.pop('HSB',None)            
        if VSB: #vertical scrollbar
            vsb = ttk.Scrollbar(self,orient="vertical",
                                command=self.tree.yview)
            self.tree.configure(yscrollcommand=vsb.set)
            vsb.grid(row=0, column=1, sticky='ns')                            
        if HSB: #horizontal scrollbar
            hsb = ttk.Scrollbar(self,orient="horizontal",
                                command=self.tree.xview)
            self.tree.configure(xscrollcommand=hsb.set)   
            hsb.grid(row=1, column=0, sticky='ew')  
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
        config_grid(self, grid)


class _Style(ttk.Style):
    """ ttk Styles """
    def __init__(self, name, master, cnf={}):
          ttk.Style.__init__(self, master)
          setattr(master, name, self)
          self._createStyles(cnf)
          
    def _createStyles(self, cnf={}):
        """ Config the ttk styles """  
        self.theme_use(cnf.pop('THEME_USE', 'default'))
        for style_name, style_opts in cnf.items():
            self.configure(style_name, **style_opts)                 

                
class TkFactory(tk.Frame):    
    def __init__(self, filename, master=None):
        tk.Frame.__init__(self, master)    
        self.createWidgets(get_cfgs(filename))
        config_grid(self, {'sticky':'nsew'})
        
    def createWidgets(self, widgets_cnf): 
        """ Create the widgets """
        w={'TREEVIEW': _Tree, 'STYLE': _Style, 'TOPLEVEL':_Toplevel}

        for cnf in widgets_cnf:
            name, s_widget, parent = cnf.pop('ATTR')

            if s_widget in w.keys():
                w[s_widget](name, self, cnf)
            else:
                setattr(self, name, 
                        getattr(
                                tk if s_widget.startswith('tk.') else ttk, 
                                s_widget[s_widget.find('.')+1:]
                                )(getattr(self, parent, self))
                        )

                grid = cnf.pop('GRID', None)
                widget = getattr(self, name)
                config_grid(widget, grid)
                config_opts(widget, cnf)  
          

def config_grid(widget, grid):
    """Config the grid and stretching options
    """
    if isinstance(grid, dict):
        weight_row = grid.pop('STRETCH_ROW', 1)
        weight_col = grid.pop('STRETCH_COL', 1)
        row = grid.get('row',0)
        col = grid.get('column',0)
        widget.grid(**grid)                                   
        widget.master.rowconfigure(row, weight=weight_row)           
        widget.master.columnconfigure(col,  weight=weight_col)  

def config_opts(widget, opts): 
    """Config the rest of options 
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
    #root = tk.Tk()
    gui = TkFactory('gui.ini')
    gui.tree1.insert('',0,text='hell', values=(1,2,43,5)) 
    
    gui.b1.config(command=gui.tree1.master.grid_remove)

    
    gui.mainloop()
