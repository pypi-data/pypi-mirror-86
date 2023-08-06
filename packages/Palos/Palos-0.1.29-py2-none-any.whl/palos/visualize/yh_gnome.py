# -*- coding: future_fstrings -*-
"""
2008-01-21
    module for some custom gnome functions
"""
#for Python2&3 compatibility
from __future__ import absolute_import, division, print_function
from builtins import (bytes, str, open, super, range,
    zip, round, input, int, pow, object)

import os, sys
import traceback

def get_chr_pos_from_x_axis_pos(x_axis_pos, chr_gap, chr_id2cumu_size, chr_id_ls):
    """
    2008-02-04
        split out from variation.src.GenomeBrowser.py
    2008-02-03
        get chromosome, position from the x axis position
        chr_id_ls is the sorted version of the keys of chr_id2cumu_size
    """
    chr_id_chosen = None
    position = -1
    for i in range(1, len(chr_id_ls)):
        #the 1st in chr_id_ls is fake chromosome 0
        prev_chr_id = chr_id_ls[i-1]
        chr_id = chr_id_ls[i]
        if chr_id2cumu_size[chr_id]>=x_axis_pos:
            chr_id_chosen = chr_id
            position = x_axis_pos - chr_id2cumu_size[prev_chr_id]
            break
    return chr_id_chosen, position

def foreach_cb(model, path, iter, pathlist):
    """
    Example:
        
        pathlist = []
        self.tree_nodes_selection.selected_foreach(yh_gnome.foreach_cb, pathlist)
        if len(pathlist) >0:
            for i in range(len(pathlist)):
                node_id = self.liststore_nodes[pathlist[i][0]][0]
                self.backend_ins.log_into_node(node_id)
    
    2008-01-21 copied from annot.bin.codense.common
    04-17-05
        used in gui listview, pathfinding.
    """
    pathlist.append(path)	

def edited_cb(cell, path, new_text, user_data):
    """
    2008-02-05
        call back for editable CellRendererText in create_columns()
    """
    liststore, column = user_data
    liststore[path][column] = new_text
    return
    
def create_columns(treeview, label_list, editable_flag_ls=None, liststore=None):
    """
    Examples:
        
        yh_gnome.create_columns(self.treeview1, self.backend_ins.display_job_label_ls)
        self.liststore = gtk.ListStore(*self.backend_ins.display_job_label_type_ls)
        list_2d = self.backend_ins.refresh(username, update_node_info,
            jobs_since, only_running, \
            update_job_info=update_job_info)
        yh_gnome.fill_treeview(self.treeview1, self.liststore, list_2d,
            reorderable=True, multi_selection=True)
    
    2008-02-05
        add editable_flag_ls and liststore
    2008-01-21 copied from annot.bin.codense.common
    04-17-05
        create columns in the treeview in the first refresh
    04-21-05
        remove the old columns and reset the model of treeview
    """
    import gtk
    tvcolumn_dict = {}
    cell_dict = {}
    #remove old columns
    old_column_list = treeview.get_columns()
    for column in old_column_list:
        treeview.remove_column(column)
    treeview.set_model()
        
    for i in range(len(label_list)):
        tvcolumn_dict[i] = gtk.TreeViewColumn(label_list[i])
        # create the TreeViewColumn to display the data
        treeview.append_column(tvcolumn_dict[i])
        # add tvcolumn to treeview
        cell_dict[i] = gtk.CellRendererText()
        # create a CellRendererText to render the data
        if editable_flag_ls and liststore:
            if editable_flag_ls[i]:
                cell_dict[i].set_property('editable', True)
                cell_dict[i].connect('edited', edited_cb, (liststore, i))
        tvcolumn_dict[i].pack_start(cell_dict[i], True)
        # add the cell to the tvcolumn and allow it to expand
        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in liststore
        tvcolumn_dict[i].add_attribute(cell_dict[i], 'text', i)
        tvcolumn_dict[i].set_sort_column_id(i)	# Allow sorting on the column

def fill_treeview(treeview, liststore, list_2d, reorderable=True, multi_selection=True):
    """
    2008-11-07
        put "liststore.append(data)" into try... except ... to handle wrong types in liststore
        fix a bug when list_2d is totally empty
    2008-02-05 add flag multi_selection
    2008-01-21 copied from annot.bin.codense.common
    04-17-05
    05-20-05
        expand the data in list_2d if it's too short
    """
    import gtk
    length_of_treeview = len(treeview.get_columns())
    no_of_rows = len(list_2d)
    for i in range(no_of_rows):
        ls = list_2d[i]
        data = ls[:]
        #copy the list to avoid change the content in ls, 'data=ls' changes the content of ls
        for i in range(length_of_treeview-len(data)):
            data.append('')
        try:
            liststore.append(data)
        except:
            sys.stderr.write("Exception happened for data=%s.\n vs previous data=%s.\n"%\
                (repr(data), repr(list_2d[max(0,i-1)])))
            traceback.print_exc()
            sys.stderr.write('%s.\n'%repr(sys.exc_info()))
    # set the TreeView mode to be liststore
    treeview.set_model(liststore)

    if reorderable:
        if len(list_2d)>0:	#2008-11-07 soemtimes, it's all empty
            for i in range(len(list_2d[0])):
                # make it searchable
                treeview.set_search_column(i)
            
        # Allow drag and drop reordering of rows
        treeview.set_reorderable(True)
    if multi_selection:
        #setting the selection mode
        treeselection = treeview.get_selection()
        treeselection.set_mode(gtk.SELECTION_MULTIPLE)

class Dummy_File:
    """
    2008-01-24
        copied from http://www.daa.com.au/pipermail/pygtk/attachments/20031004/dbb34c38/Py_Shell.py
    """
    def __init__(self, buffer, tag=None):
        """Implements a file-like object for redirect the stream to the buffer"""
        self.buffer = buffer
        self.tag = tag
    
    def write(self, text):
        """Write text into the buffer and apply self.tag"""
        iter=self.buffer.get_end_iter()
        if self.tag:
            self.buffer.insert_with_tags(iter, text, self.tag)
        else:
            self.buffer.insert(iter, text)
    
    def writelines(self, l):
        map(self.write, l)
    
    def flush(self):
        pass
    
    def isatty(self):
        return 1

def subwindow_hide(widget, event, data=None):
    widget.hide()
    return True

#2008-04-21 movied from variation.src.common
#2008-02-04 custom NavigationToolbar
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg
class Cursors:  #namespace
    HAND, POINTER, SELECT_REGION, MOVE = range(4)
cursors = Cursors()

class NavigationToolbar2GTKAgg_chromosome(NavigationToolbar2GTKAgg):
    """
    2008-02-04 NavigationToolbar with custom mouse_move()
    """
    def __init__(self, canvas, window):
        NavigationToolbar2GTKAgg.__init__(self, canvas, window)
        self.chr_id2size = {}
        self.chr_id2cumu_size = {}
        self.chr_gap = None
        self.chr_id_ls = None
    
    def update_chr_info(self, chr_id2size, chr_id2cumu_size, chr_gap, chr_id_ls):
        """
        2008-02-04
            fill up the chromosome info
        """
        self.chr_id2size = chr_id2size
        self.chr_id2cumu_size = chr_id2cumu_size
        self.chr_gap = chr_gap
        self.chr_id_ls = chr_id_ls
    
    def mouse_move(self, event):
        """
        2008-02-04
            custom the label shown for 'motion_notify_event'
            self._idDrag=self.canvas.mpl_connect('motion_notify_event', self.mouse_move)
        """
        #print 'mouse_move', event.button

        if not event.inaxes or not self._active:
            if self._lastCursor != cursors.POINTER:
                self.set_cursor(cursors.POINTER)
                self._lastCursor = cursors.POINTER
        else:
            if self._active=='ZOOM':
                if self._lastCursor != cursors.SELECT_REGION:
                    self.set_cursor(cursors.SELECT_REGION)
                    self._lastCursor = cursors.SELECT_REGION
                if self._xypress:
                    x, y = event.x, event.y
                    lastx, lasty, a, ind, lim, trans= self._xypress[0]
                    self.draw_rubberband(event, x, y, lastx, lasty)
            elif (self._active=='PAN' and
                  self._lastCursor != cursors.MOVE):
                self.set_cursor(cursors.MOVE)

                self._lastCursor = cursors.MOVE

        if event.inaxes and event.inaxes.get_navigate():

            try:
                #2008-02-04 custom here
                if self.chr_id2size and self.chr_id2cumu_size and \
                    self.chr_gap!=None and self.chr_id_ls:
                    x_axis_pos_int = int(round(event.xdata))
                    chr_id, position = get_chr_pos_from_x_axis_pos(
                        x_axis_pos_int, self.chr_gap,
                        self.chr_id2cumu_size, self.chr_id_ls)
                    chr_perc = -1	#default
                    if chr_id in self.chr_id2size:
                        chr_perc = position/float(self.chr_id2size[chr_id])*100
                        if chr_perc>100 or chr_perc<0:	#out of range
                            chr_perc = -1
                    if position==-1:	#not within any chromosome
                        position = x_axis_pos_int
                    s = 'chr=%s, pos=%i(%.1f%%), y=%s'%(chr_id, position,
                        chr_perc, event.ydata)
                else:
                    s = event.inaxes.format_coord(event.xdata, event.ydata)
            except ValueError: pass
            except OverflowError: pass
            else:
                if len(self.mode):
                    self.set_message('%s : %s' % (self.mode, s))
                else:
                    self.set_message(s)
        else: self.set_message(self.mode)

def getDataOutOfTextEntry(widget, data_type=None, filter_func=None, default=None):
    """
    2010-6-14
        add argument default
    2010-4-27
        This function fetches the data present in a text widget.
        
        widget could be text_entry, combobox, ComboBoxEntry
        
        Example for filter_func
            filter_func = lambda x: x.split('_')[0]
    """
    if hasattr(widget, 'get_text'):
        text = widget.get_text()
    elif hasattr(widget, 'get_active_text'):	# combobox or ComboBoxEntry
        text = widget.get_active_text()
    else:
        text = ''
    if text and filter_func:
        text = filter_func(text)
    if data_type:
        if text:
            text = data_type(text)
        else:
            text = None
    if default is not None and text is None:
        text = default
    return text