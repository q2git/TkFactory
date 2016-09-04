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
    def __init__(self, filename):
        #None is for creating widget without specifying parent
        self.widgets = {None:None} 
        self.widgets['ROOT'] =  tk.Tk()
        self.root = self.widgets['ROOT'] 
        self.textvariables = {}
        root, styles, widgets = self.read_ini_file(filename)
        self.config_root(root) 
        self.config_styles(styles)
        self.__createWidgets(widgets)
        
    @staticmethod
    def read_ini_file(filename):
        """ Read gui configurations from the ini file 
        """
        with codecs.open(filename,'r','utf_8_sig') as f:
            cfg = ast.literal_eval(f.read())   
        root = cfg.pop('ROOT', {})
        styles = cfg.pop('STYLES', [])
        widgets = cfg.pop('WIDGETS', [])
        return (root, styles, widgets)
        
    def config_root(self, opts):
        """ Config the root window 
        """     
        geometry = opts.pop('GEOMETRY', None)
        resize = opts.pop('RESIZEABLE', None)
        iconbitmap = opts.pop('ICONBITMAP', None)
        title = opts.pop('TITLE', None)
        self.root.config(**opts)       
        self.root.geometry(geometry)
        self.root.resizable(width=resize[0],height=resize[1])
        self.root.iconbitmap(iconbitmap)
        self.root.title(title)    
                 
    def config_styles(self, styles):
        """ Config the ttk styles 
        """         
        self.root.s=ttk.Style()
        for name, opts in styles:
            if name == 'theme_use':
                self.root.s.theme_use(opts)
                continue #jump to next loop
            self.root.s.configure(name,**opts) 
            
    def __createWidgets(self, widgets):
        """ Create the widgets
        """
        for name, widget, parent, grid, opts in widgets:
            #get tk or ttk widget instance
            self.widgets[name] = getattr(
                                tk if widget.startswith('tk.') else ttk, 
                                widget[widget.find('.')+1:]
                                )(self.widgets[parent])                
            self.config_special_options(name, opts)           
            self.config_options(name, opts)  
            self.config_grid(name, grid)                                        

    def config_special_options(self, name, opts):
        """Config the widgets with some special options or some self-defined 
        options, the options with capitalized name are self-defined.
        """
        widget = self.widgets[name]        
        if isinstance(widget, ttk.Treeview):
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

        elif isinstance(widget, tk.Menu):
            label = opts.get('title')
            submenus = opts.pop('SUBMENUS', None)
            if isinstance(widget.master,tk.Menu): #for meunu
                widget.master.add_cascade(label=label,menu=widget,underline=0)
            elif 'menu' in widget.master.keys(): #for root,menubutton, etc.
                widget.master.config(menu=widget)
            if submenus: #add submenu
                for kind, coption in submenus:
                    widget.add(kind, **coption)
                    
        elif isinstance(widget, ttk.Notebook): 
            for child,kw in opts.pop('TABS', []):
                widget.add(self.widgets[child], **kw) 
                   
        elif isinstance(self.widgets[name],ttk.Panedwindow):
            for child,kw in opts.pop('PANES', []):
                widget.add(self.widgets[child], **kw)
                      
    def config_options(self, name, opts): 
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

    def config_grid(self, name, grid):
        """Config the grid and stretching options
        """
        if grid is not None:         
            widget = self.widgets[name]
            row,col,rowspan,colspan,sticky,stretch_row,stretch_col = grid
            widget.grid(row=row, column=col, rowspan=rowspan,
                        columnspan=colspan, sticky=sticky)                         
            if stretch_row!=0:  #enable stretching                      
                widget.master.rowconfigure(row, weight=stretch_row)           
            if stretch_col!=0:  #enable stretching     
                widget.master.columnconfigure(col, weight=stretch_col)  
                       
    def run(self):
        self.root.mainloop()
    
    def stop(self):
        self.root.destroy()
    
                                
if __name__ == '__main__':
    gui = TkFactory('gui.ini')
    gui.run()
