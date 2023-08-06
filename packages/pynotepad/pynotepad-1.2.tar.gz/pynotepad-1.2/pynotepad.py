"""说明 Instructions:
A simple text editor written in Python.It supports editing text files,
binary files ,encodings and changing font size.
When you edit a binary file, the contents of the file are
displayed as escape sequences.
And code highlighting is supported when editing Python code files,like IDLE.

一款使用tkinter编写的文本编辑器, 支持编辑文本文件、二进制文件、改变字体大小。
支持ansi、gbk和utf-8编码。编辑二进制文件时, 文件内容以转义序列形式显示。
编辑python代码文件时, 支持代码高亮显示, 类似IDLE。

作者:qfcy (七分诚意)
版本:1.2
"""
import sys,os,time
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import tkinter.filedialog as dialog

try:
    from idlelib.colorizer import ColorDelegator
    from idlelib.percolator import Percolator
except ImportError:
    ColorDelegator=Percolator=None


__all__=["directories","search"]
__email__="3416445406@qq.com"
__author__="七分诚意 qq:3076711200 邮箱:%s"%__email__
__version__="1.2"

#_REPLACE_CHARS=['\x00','\r']
def view_hex(bytes):
    result=''
    for char in bytes:
        result+= hex(char)[2:] + ' '
    return result
def to_escape_str(bytes):
    # 将字节(bytes)转换为转义字符串
    return repr(bytes)[2:-1]
def to_bytes(escape_str):
    # 将转义字符串转换为字节
    try:
        return eval('b"""'+escape_str+'"""')
    except SyntaxError:
        return eval("b'''"+escape_str+"'''")

class SearchDialog(Toplevel):
    #查找对话框
    instances=[]
    def __init__(self,master):
        if not isinstance(master,Editor):
            raise TypeError("The master must be an Editor object, not %r."%(type(master).__name__))
        self.master=master
        self.coding=self.master.coding.get()
        cls=self.__class__
        cls.instances.append(self)
    def init_window(self,title="查找"):
        Toplevel.__init__(self,self.master)
        self.title(title)
        self.attributes("-toolwindow",True)
        self.attributes("-topmost",True)
        self.bind("<Destroy>",self.onquit)
    def show(self):
        self.init_window()
        frame=Frame(self)
        ttk.Button(frame,text="查找下一个",command=self.search).pack()
        ttk.Button(frame,text="退出",command=self.destroy).pack()
        frame.pack(side=RIGHT,fill=Y)
        inputbox=Frame(self)
        Label(inputbox,text="查找内容:").pack(side=LEFT)
        self.keyword=StringVar()
        keyword=ttk.Entry(inputbox,textvariable=self.keyword)
        keyword.pack(side=LEFT,expand=True,fill=X)
        keyword.bind("<Key-Return>",self.search)
        keyword.focus_force()
        inputbox.pack(fill=X)
        options=Frame(self)
        self.create_options(options)
        options.pack(fill=X)
    def create_options(self,master):
        Label(master,text="选项: ").pack(side=LEFT)
        self.use_regexpr=IntVar()
        ttk.Checkbutton(master,text="使用正则表达式",variable=self.use_regexpr)\
        .pack(side=LEFT)
        self.match_case=IntVar()
        ttk.Checkbutton(master,text="区分大小写",variable=self.match_case)\
        .pack(side=LEFT)
        self.use_escape_char=IntVar()
        self.use_escape_char.set(self.master.isbinary)
        ttk.Checkbutton(master,text="转义字符",variable=self.use_escape_char)\
        .pack(side=LEFT)
    
    def search(self,event=None,mark=True,bell=True):
        text=self.master.contents
        key=self.keyword.get()
        if not key:return
        if self.use_escape_char.get():
            key=str(to_bytes(key),encoding=self.coding)
        text.tag_remove("sel","1.0",END)
        pos=text.search(key,INSERT,END,
                        regexp=self.use_regexpr.get(),
                        nocase=not self.match_case.get())
        if pos:
            newpos="%s+%dc"%(pos,len(key))
            text.mark_set(INSERT,newpos)
            if mark:self.mark_text(pos,newpos)
            return pos,newpos
        elif bell:self.bell()
    def mark_text(self,start_pos,end_pos):
        text=self.master.contents
        text.tag_add("sel",start_pos,end_pos)
        text.focus_force()
        self.master.update_status()
    def onquit(self,event):
        cls=self.__class__
        if self in cls.instances:
            cls.instances.remove(self)

class ReplaceDialog(SearchDialog):
    #替换对话框
    instances=[]
    def show(self):
        self.init_window(title="替换")
        frame=Frame(self)
        ttk.Button(frame,text="替换",command=self.replace).pack()
        ttk.Button(frame,text="全部替换",command=self.replace_all).pack()
        ttk.Button(frame,text="退出",command=self.destroy).pack()
        frame.pack(side=RIGHT,fill=Y)
        
        inputbox=Frame(self)
        Label(inputbox,text="查找内容:").pack(side=LEFT)
        self.keyword=StringVar()
        keyword=ttk.Entry(inputbox,textvariable=self.keyword)
        keyword.pack(side=LEFT,expand=True,fill=X)
        keyword.focus_force()
        inputbox.pack(fill=X)
        
        replace=Frame(self)
        Label(replace,text="替换为:  ").pack(side=LEFT)
        self.text_to_replace=StringVar()
        replace_text=ttk.Entry(replace,textvariable=self.text_to_replace)
        replace_text.pack(side=LEFT,expand=True,fill=X)
        replace_text.bind("<Key-Return>",self.replace)
        replace.pack(fill=X)
        
        options=Frame(self)
        self.create_options(options)
        options.pack(fill=X)
    def replace(self,bell=True):
        text=self.master.contents
        result=self.search(mark=False,bell=bell)
        if not result:return -1 #-1标志已无文本可替换
        pos,newpos=result
        newtext=self.text_to_replace.get()
        text.delete(pos,newpos)
        text.insert(pos,newtext)
        end_pos="%s+%dc"%(pos,len(newtext))
        self.mark_text(pos,end_pos)
        
    def replace_all(self):
        self.master.contents.mark_set("insert","1.0")
        while self.replace(bell=False)!=-1:pass
     
class Editor(Tk):
    TITLE="PyNotepad"
    encodings="ansi","utf-8","utf-16","utf-32","gbk","big5"
    ICON="notepad.ico"
    NORMAL_CODING="utf-8"
    FONTSIZES=8, 9, 10, 11, 12, 14, 18, 20, 22, 24, 30
    NORMAL_FONT='宋体'
    NORMAL_FONTSIZE=11
    FILETYPES=[("所有文件","*.*")]
    windows=[]
    def __init__(self,filename=""):
        super().__init__()
        self.title(self.TITLE)
        self.bind("<Key>",self.window_onkey)
        self.bind("<FocusIn>",self.focus)
        self.bind("<FocusOut>",self.focus)
        self.protocol("WM_DELETE_WINDOW",self.ask_for_save)

        self.isbinary=self.file_changed=False
        self.bin_data=self.charmap=None
        self.colorobj=None
        self.coding=StringVar()
        self.coding.set(self.NORMAL_CODING)
        Editor.windows.append(self)

        self.load_icon()
        self.create_widgets()
        self.update()
        self.filename=''
        if filename:
            #self.filenamebox.insert(END,filename)
            self.load(filename)
    def load_icon(self):
        for path in sys.path:
            try:
                self.iconbitmap("{}\{}".format(path,self.ICON))
            except TclError:pass
            else:break
    def create_widgets(self):
        "创建控件"
        self.statusbar=Frame(self)
        self.statusbar.pack(side=BOTTOM,fill=X)
        self.status=Label(self.statusbar,justify=RIGHT)
        self.status.pack(side=RIGHT)

        frame=Frame(self)
        frame.pack(side=TOP,fill=X)

        ttk.Button(frame,text='新建', command=self.new,width=7).pack(side=LEFT)
        ttk.Button(frame,text='打开', command=self.open,width=7).pack(side=LEFT)
        ttk.Button(frame,text='打开二进制文件',
                   command=self.open_as_binary,width=13).pack(side=LEFT)
        ttk.Button(frame,text='保存', command=self.save,width=7).pack(side=LEFT)

        Label(frame,text="编码:").pack(side=LEFT)
        coding=ttk.Combobox(frame,textvariable=self.coding)
        coding["value"]=self.encodings
        coding.pack(side=LEFT)

        self.contents=ScrolledText(self,undo=True,width=75,height=24,
                                   font=(self.NORMAL_FONT,self.NORMAL_FONTSIZE,"normal"))
        self.contents.pack(expand=True,fill=BOTH)
        self.contents.bind("<Key>",self.text_change)
        self.contents.bind("<B1-ButtonRelease>",self.update_status)
        self.update_offset()

        self.create_menu()
    def create_binarytools(self):
        if self.isbinary:
            if not self.bin_data:
                self.bin_data=ScrolledText(self.statusbar,width=8,height=6)
            if not self.charmap:
                self.charmap=ScrolledText(self.statusbar,width=20,height=5)
            self.bin_data.pack(side=LEFT,expand=True,fill=BOTH)
            self.charmap.pack(fill=Y)
            self.status.pack_forget()
            self.status.pack(fill=X)
        else:
            if self.bin_data:
                self.bin_data.pack_forget()
            if self.charmap:
                self.charmap.pack_forget()
            self.status.pack(side=RIGHT)
    def create_menu(self):
        menu=Menu(self)
        filemenu=Menu(self,tearoff=False)
        filemenu.add_command(label="新建",
                             command=self.new,accelerator="Ctrl+N")
        filemenu.add_command(label="打开",
                             command=self.open,accelerator="Ctrl+O")
        filemenu.add_command(label="打开二进制文件",
                             command=self.open_as_binary)
        filemenu.add_command(label="保存",
                             command=self.save,accelerator="Ctrl+S")
        filemenu.add_command(label="另存为",command=self.save_as)
        filemenu.add_separator()
        filemenu.add_command(label="退出",command=self.ask_for_save)

        self.editmenu=Menu(self.contents,tearoff=False)
        master=self.contents
        self.editmenu.add_command(label="剪切  ",
                         command=lambda:self.text_change()==master.event_generate("<<Cut>>"))
        self.editmenu.add_command(label="复制  ",
                         command=lambda:master.event_generate("<<Copy>>"))
        self.editmenu.add_command(label="粘贴  ",
                         command=lambda:self.text_change()==master.event_generate("<<Paste>>"))
        self.editmenu.add_separator()
        self.editmenu.add_command(label="查找",accelerator="Ctrl+F",
                                  command=lambda:self.show_dialog(SearchDialog))
        self.editmenu.add_command(label="替换",
                                  command=lambda:self.show_dialog(ReplaceDialog))
        self.editmenu.add_separator()
        
        fontsize=Menu(self.contents,tearoff=False)
        fontsize.add_command(label="增大字体   ",accelerator='Ctrl+ "+"',
                             command=self.increase_font)
        fontsize.add_command(label="减小字体   ",accelerator='Ctrl+ "-"',
                             command=self.decrease_font)
        fontsize.add_separator()

        for i in range(len(self.FONTSIZES)):
            def resize(index=i):
                self.set_fontsize(index)
            fontsize.add_command(label=self.FONTSIZES[i],command=resize)

        self.editmenu.add_cascade(label="字体",menu=fontsize)
        self.contents.bind("<Button-3>",
                    lambda event:self.editmenu.post(event.x_root,event.y_root))


        helpmenu=Menu(self,tearoff=False)
        helpmenu.add_command(label="关于",command=self.about)

        menu.add_cascade(label="文件",menu=filemenu)
        menu.add_cascade(label="编辑",menu=self.editmenu)
        menu.add_cascade(label="帮助",menu=helpmenu)
        # 显示菜单
        self.config(menu=menu)


    def show_dialog(self,dialog_type):
        # dialog_type是对话框的类型
        for window in dialog_type.instances:
            if window.master is self:
                window.focus_force()
                return
        dialog_type(self).show()

    def set_fontsize(self,index):
        newsize=self.FONTSIZES[index]
        self.contents["font"]=(self.NORMAL_FONT,newsize,"normal")
    def increase_font(self):
        "增大字体"
        fontsize=int(self.contents["font"].split()[1])
        index=self.FONTSIZES.index(fontsize)+1
        if 0<=index<len(self.FONTSIZES): self.set_fontsize(index)
    def decrease_font(self):
        "减小字体"
        fontsize=int(self.contents["font"].split()[1])
        index=self.FONTSIZES.index(fontsize)-1
        if 0<=index<len(self.FONTSIZES): self.set_fontsize(index)


    def window_onkey(self,event):
        if event.state==4:#如果按下Ctrl键
            if event.keysym=='o':#按下Ctrl+O键
                self.open()
            elif event.keysym=='s':#Ctrl+S键
                self.save()
            elif event.keysym=='z':#Ctrl+Z
                try:self.contents.edit_undo()
                except TclError:self.bell()
                self.text_change()
            elif event.keysym=='y':
                try:self.contents.edit_redo()
                except TclError:self.bell()
                self.text_change()
            elif event.keysym=='f':
                self.show_dialog(SearchDialog)
            elif event.keysym=='equal':#Ctrl+ "+" 增大字体
                self.increase_font()
            elif event.keysym=='minus':#Ctrl+ "-" 减小字体
                self.decrease_font()
    def focus(self,event):
        #当窗口获得或失去焦点时,调用此函数
        for window in SearchDialog.instances + ReplaceDialog.instances:
            if window.master is self:
                if event.type==EventType.FocusIn:
                    if window.wm_state()=="iconic":
                        window.attributes("-toolwindow",True)
                    window.attributes("-topmost",True)
                    if not window.wm_state()=="normal":
                        window.deiconify()
                    self.contents.focus_force()
                else:
                    window.attributes("-topmost",False)
                    if self.wm_state()=="iconic":
                        window.withdraw()
                        #window.iconify()
                break

    def text_change(self,event=None):
        self.file_changed=True
        self.update_offset()
    def update_status(self,event=None):
        if self.isbinary:
            try:
                selected=self.contents.get(SEL_FIRST,SEL_LAST)
                data=eval("b'''"+selected+"'''")
                try:
                    text=str(data,encoding=self.coding.get(),
                             errors="backslashreplace")
                except TypeError:
                    text=''
                self.bin_data.delete("1.0",END)
                self.bin_data.insert(INSERT,text)
                self.charmap.delete("1.0",END)
                self.charmap.insert(INSERT,view_hex(data))
                self.status["text"]="选区长度: %d (Bytes)"%len(data)
            except (TclError,SyntaxError): #未选取内容
                self.update_offset()
        else:self.update_offset()
    def update_offset(self,event=None):
        if self.isbinary:
            selected=self.contents.get("1.0",INSERT)
            try:
                data=eval("b'''"+selected+"'''")
            except SyntaxError:
                sep='\\'
                selected=sep.join(selected.split(sep)[0:-1])
                data=eval("b'''"+selected+"'''")
            self.status["text"]="偏移量: {} ({})".format(len(data),hex(len(data)))
        else:
            offset=self.contents.index(CURRENT).split('.')
            self.status["text"]="Ln: {}  Col: {}".format(*offset)

    @classmethod
    def new(cls):
        window=cls()
        window.focus_force()
    def open(self):
        filename=dialog.askopenfilename(master=self,
                                        filetypes=self.FILETYPES)
        self.load(filename)
    def open_as_binary(self):
        filename=dialog.askopenfilename(master=self,
                                        filetypes=self.FILETYPES)
        self.load(filename,binary=True)
    def load(self,filename,binary=False):
        #加载一个文件
        if not filename.strip():
            return
        self.isbinary=binary
        if os.path.isfile(filename):
            self.filename=filename
            data=self._load_data(filename)
            if len(data)>10000:
                self.title(
                "%s - 加载中,请耐心等待..." % self.TITLE)
                self.update()
            self.contents.delete('1.0', END)
            if self.isbinary:
                self.contents.insert(INSERT,data)
            else:
                for char in data:
                    try:
                        self.contents.insert(INSERT,char)
                    except TclError:self.contents.insert(INSERT,' ')
            self.contents.mark_set(INSERT,"1.0")
            self.create_binarytools()
            self.change_title()
            self.change_mode()
            self.contents.focus_force()
        else:msgbox.showinfo("Error","文件未找到:"+repr(filename))
    def _load_data(self,filename):
        f=open(filename,"rb")#打开文件
        if self.isbinary:
            data=to_escape_str(f.read())
            return data
        else:
            try:
                #读取文件,并对文件内容进行编码
                data=str(f.read(),encoding=self.coding.get())
            except UnicodeDecodeError:
                f.seek(0)
                result=msgbox.askyesno("","""%s编码无法解码此文件,
是否使用二进制模式打开?"""%self.coding.get())
                if result:
                    self.isbinary=True
                    data=to_escape_str(f.read())
                else:
                    self.isbinary=False
                    data=str(f.read(),encoding=self.coding.get(),errors="replace")
        return data
    def change_title(self,running=False):
        newtitle="PyNotepad - "+os.path.split(self.filename)[1]+\
                  (" (二进制模式)" if self.isbinary else '')+\
                  (" (运行)" if running else '')
        self.title(newtitle)
    def change_mode(self):
        if ColorDelegator:
            if self.filename.lower().endswith((".py",".pyw"))\
                   and (not self.isbinary):
                self._codefilter=ColorDelegator()
                if not self.colorobj:
                    self.colorobj=Percolator(self.contents)
                self.colorobj.insertfilter(self._codefilter)
            elif self.colorobj and self._codefilter:
                self.colorobj.removefilter(self._codefilter)
    def ask_for_save(self,quit=True):
        if self.file_changed:## and self.filenamebox.get():
            retval=msgbox.askyesnocancel("文件尚未保存",
                              "是否保存{}的更改?".format(
                                  os.path.split(self.filename)[1] or "当前文件"))
            if not retval is None:
                if retval==True:self.save()
            else:return 0  #0:cancel
        if quit:
            Editor.windows.remove(self)
            self.destroy()
    def save(self):
        #保存文件
        if not self.filename:
            self.filename=dialog.asksaveasfilename(master=self.master,
                    filetypes=self.FILETYPES)
        filename=self.filename
        if filename.strip():
            text=self.contents.get('1.0', END)[:-1]
            if self.isbinary:
                data=to_bytes(text)
            else:data=bytes(text,encoding=self.coding.get())
            file=open(filename, 'wb')
            file.write(data)
            file.close()
            self.filename=filename
            self.file_changed=False
            self.change_title()
            self.change_mode()
    def save_as(self):
        self.filename=dialog.asksaveasfilename(master=self.master,
                    filetypes=self.FILETYPES)
        self.save()

    def about(self):
        msgbox.showinfo("关于",__doc__+"\n作者: "+__author__)

def main():
    def _mainloop():
        try:mainloop()
        # 忽略 ctrl+c
        except KeyboardInterrupt:_mainloop()
    if len(sys.argv)>1:
        for arg in sys.argv[1:]:
            try:
                Editor(arg)
            except OSError:pass
    else: Editor()
    _mainloop()

if __name__=="__main__":main()
