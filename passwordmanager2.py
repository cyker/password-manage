#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author:ciker
#version:1.0.1
'''
功能介绍：
    1、可以添加站点名称，url，用户名、密码，以及一系列备注信息
    2、已经实现删除，更新，增加操作
    3、需要完善的功能：
        （1）数据库没有加密
        （2）搜索列表没有完善，应该能实现，只显示主域名，比如www.baidu.com，应该将所有的baidu.com域名下的账号为一个名称，而不是每个账号都显示
            这个在插入账号时候就应该修改了。
        （3）管理功能还未实现
        （4）代码还有很多需要优化的地方
        


'''



import os, sys
import sqlite3
import random
import string

try:
    import win32clipboard as wc
    import win32con
except:
    pass

try:
    from tkinter import *
except ImportError:  #Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    PythonVersion = 3
    import tkinter.filedialog as fl
    import tkinter.messagebox as mb
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

inpdic = {}
inpflag = False         #防止意外关闭添加窗口造成的错误


class PASSWORDMANAGER:
    def __init__(self,datepath = os.getcwd() + "/dat.db"):
        self.datepath = datepath
        self.conn = sqlite3.connect(self.datepath)
        self.initDB()

    def excutesql(self,sql):
        cu = self.conn
        cu.execute(sql)
        self.conn.commit()

    def fetchsql(self,sql):
        cu = self.conn
        t = cu.execute(sql)
        return t.fetchall()

    def initDB(self):
        createsitesql ='''
        CREATE TABLE IF NOT EXISTS `site`
        ( `sid` INTEGER PRIMARY KEY,
        `title` VARCHAR(50) NOT NULL,
        `url` VARCHAR(50) NOT NULL
        );
        '''

        createuserpwdsql = '''
        CREATE TABLE IF NOT EXISTS `userpwd`
        ( `uid` INTEGER PRIMARY KEY,
        `sid` INT NOT NULL,
        `name` VARCHAR(50) NOT NULL,
        `pwd` VARCHAR(50) NOT NULL
        );
        '''

        createinfosql = '''
        CREATE TABLE IF NOT EXISTS `info`
        ( `iid` INTEGER PRIMARY KEY,
        `uid` INT NOT NULL ,
        `key` VARCHAR(50) NOT NULL,
        `value` VARCHAR(50) NOT NULL
        );
        '''

        self.excutesql(createsitesql)
        self.excutesql(createuserpwdsql)
        self.excutesql(createinfosql)

class MESSAGEBOX:
    def __init__(self,root):
        self.name = "message box type"
        self.root = root

    def cancelok(self,title,message):
        return mb.askokcancel(title=title,message=message)

    def msgbox(self,title,message):
        mb.showinfo(title=title,message=message)

    def fileOpenDialog(self,title,expname):
        return fl.askopenfilename(title=title,filetypes=[("%s格式"%expname,expname)])

class SYSTTEMCONTROL:
    def __init__(self):
        self.name = "系统操作函数"

    def getText(self):  # 读取剪切板
        wc.OpenClipboard()
        d = wc.GetClipboardData(win32con.CF_TEXT)
        wc.CloseClipboard()
        return d

    def setText(self,aString):  # 写入剪切板
        wc.OpenClipboard()
        wc.EmptyClipboard()
        # wc.SetClipboardData(win32con.CF_TEXT, str(aString))
        wc.SetClipboardText(aString,win32con.CF_TEXT)
        wc.CloseClipboard()
        print(aString)

class BASEFUNCTION:
    def __init__(self):
        self.name = "基本函数"

    def randomstrmain(self,lenth = 4,what='pwd'):
        if what == 'pwd':
            return self.randomstr()
        elif what == 'name':
            return self.randomstr(lenth,string.ascii_letters)

    def randomstr(self,lenth=8,stringl = string.ascii_letters+"!@#$%^&*();:<>,./?"):
        a = list(stringl)
        random.shuffle(a)
        t = ''.join(a[:lenth])
        return t

# 添加窗体
class ADDWINDOWS(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Form1')
        self.master.geometry('316x205')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('node.TLabel',anchor='w', font=('宋体',9))
        self.node = Label(self.top, text='target', style='node.TLabel')
        self.node.place(x=8, y=16,width=41,height=17)                                                                                   #, relwidth=0.13, relheight=0.083)

        self.nodeinputVar = StringVar(value='')
        self.nodeinput = Entry(self.top, textvariable=self.nodeinputVar, font=('宋体',9))
        self.nodeinput.place(x=72, y=12,width=153,height=25)                                                                    #, relwidth=0.484, relheight=0.122)

        self.style.configure('url.TLabel',anchor='w', font=('宋体',9))
        self.url = Label(self.top, text='url', style='url.TLabel')
        self.url.place(x=8, y=48, width=41, height=17)                      #, relwidth=0.13, relheight=0.083)

        self.style.configure('name.TLabel',anchor='w', font=('宋体',9))
        self.name = Label(self.top, text='name', style='name.TLabel')
        self.name.place(x=8, y=80, width=41, height=17)                              #, relwidth=0.13, relheight=0.083)

        self.style.configure('pwd.TLabel',anchor='w', font=('宋体',9))
        self.pwd = Label(self.top, text='pwd', style='pwd.TLabel')
        self.pwd.place(x=8, y=112, width=41, height=17)                                  #, relwidth=0.13, relheight=0.083)

        self.urlinputVar = StringVar(value='')
        self.urlinput = Entry(self.top, textvariable=self.urlinputVar, font=('宋体',9))
        self.urlinput.place(x =72, y =44, width =153, height =25)                         #, relwidth=0.484, relheight=0.122)

        self.nameinputVar = StringVar(value='')
        self.nameinput = Entry(self.top, textvariable=self.nameinputVar, font=('宋体',9))
        self.nameinput.place(x =72, y =76, width =153, height =25)                            #, relwidth=0.484, relheight=0.122)

        self.pwdinputVar = StringVar(value='')
        self.pwdinput = Entry(self.top, textvariable=self.pwdinputVar, font=('宋体',9))
        self.pwdinput.place(x =72, y =108, width =153, height =25)                                 #, relwidth=0.484, relheight=0.122)

        self.style.configure('nodebtn.TButton',font=('宋体',9))
        self.nodebtn = Button(self.top, text='get', command=self.nodebtn_Cmd, style='nodebtn.TButton')
        self.nodebtn.place(x =240, y =12, width =49, height =25)                                      #, relwidth=0.155, relheight=0.122)

        self.style.configure('urlbtn.TButton',font=('宋体',9))
        self.urlbtn = Button(self.top, text='get', command=self.urlbtn_Cmd, style='urlbtn.TButton')
        self.urlbtn.place(x =240, y =44, width =49, height =25)                           #, relwidth=0.155, relheight=0.122)

        self.style.configure('namebtn.TButton',font=('宋体',9))
        self.namebtn = Button(self.top, text='create', command=self.namebtn_Cmd, style='namebtn.TButton')
        self.namebtn.place(x =240, y =76, width =49, height =25)                                      #, relwidth=0.155, relheight=0.122)

        self.style.configure('pwdbtn.TButton',font=('宋体',9))
        self.pwdbtn = Button(self.top, text='create', command=self.pwdbtn_Cmd, style='pwdbtn.TButton')
        self.pwdbtn.place(x =240, y =108, width =49, height =25)                                   #, relwidth=0.155, relheight=0.122)

        self.style.configure('addbtn.TButton',font=('宋体',9))
        self.addbtn = Button(self.top, text='add', command=self.addbtn_Cmd, style='addbtn.TButton')
        self.addbtn.place(x =184, y =144, width =49, height =25)                                       #, relwidth=0.155, relheight=0.122)

        self.style.configure('submitbtn.TButton',font=('宋体',9))
        self.submitbtn = Button(self.top, text='submit', command=self.submitbtn_Cmd, style='submitbtn.TButton')
        self.submitbtn.place(x =240, y =144, width =49, height =25)                        #, relwidth=0.155, relheight=0.122)

class ADDWINDOWSAPP(ADDWINDOWS):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        ADDWINDOWS.__init__(self, master)
        self.keys = []
        self.values = []
        self.num = 1
        self.master = master
        self.basefunc = BASEFUNCTION()

    def nodebtn_Cmd(self, event=None):
        #TODO, Please finish the function here!
        pass

    def urlbtn_Cmd(self, event=None):
        #TODO, Please finish the function here!
        pass

    def namebtn_Cmd(self, event=None):
        #TODO, Please finish the function here!
        self.nameinputVar.set(self.basefunc.randomstrmain(6,'name'))
        pass

    def pwdbtn_Cmd(self, event=None):
        #TODO, Please finish the function here!
        self.pwdinputVar.set(self.basefunc.randomstrmain(10, 'pwd'))
        pass

    def addbtn_Cmd(self, event=None):
        #TODO, Please finish the function here!
        keyVar = StringVar(value='')
        keyinput = Entry(self.top, textvariable=keyVar, font=('宋体', 9))
        keyinput.place(x=8, y=144 + self.num*25 + 2, width=80, height=25)
        self.keys.append(keyVar)

        valVar = StringVar(value='')
        valinput = Entry(self.top, textvariable=valVar, font=('宋体', 9))
        valinput.place(x=100, y=144 + self.num*25 + 2, width=153, height=25)
        self.values.append(valVar)

        self.master.geometry('316x%s'%(str(205 + self.num*25 )))

        self.num = self.num + 1

    pass

    def submitbtn_Cmd(self, event=None):
        #TODO, Please finish the function here!
        global inpflag
        c = zip(self.keys, self.values)
        self.keyarr = []
        self.valarr = []
        inpflag = True

        for key, val in c:
            self.keyarr.append(str(key.get()))
            self.valarr.append(str(val.get()))
        # print("%s %s" % (key.get(), val.get()))

        inpdic['node'] = self.nodeinputVar.get()
        inpdic['url'] = self.urlinputVar.get()
        inpdic['username'] = self.nameinputVar.get()
        inpdic['password'] = self.pwdinputVar.get()

        inpdic['key'] = self.keyarr
        inpdic['val'] = self.valarr

        for key, val in inpdic.items():
            print("%s   %s" % (key, val))

        self.master.destroy()
        self.master.quit()
        pass

class DETAILWINDOWS(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Form1')
        self.master.geometry('316x605')
        # self.showDetailWindows()

    def showDetailWindows(self,infoDic):
        num = 0
        self.detailDic = {}
        iidKeyValue = {}

        self.Frame1 = self.winfo_toplevel()
        self.style = Style()
        self.style.configure('Label1.TLabel', anchor='w', font=('宋体', 4))
        self.style.configure('copy.TButton', font=('宋体', 9))

        for k, v in infoDic.items():
            if k != 'key' and k != 'value' and k != 'uid' and k!= 'iid':
                # self.keyLabelArr.append(keystr)
                label_temp = Label(self.Frame1, text=str(k), font='Label1.TLabel')
                label_temp.place(x=8, y=16 + num * 40, width=60, height=25)

                valuestr = StringVar(value=str(v))
                # self.valueEntryArr.append(valuestr)

                self.detailDic[str(k)] = valuestr

                entry_temp = Entry(self.Frame1, textvariable=valuestr, font=('宋体', 9))
                entry_temp.place(x=70, y=16 + num * 40, width=121, height=25)


                Button(self.Frame1, text='copy', command=lambda s=str(v): self.systemcontrol.setText(s),
                           style='copy.TButton').place(x=195, y=16 + num * 40, width=40, height=25)

                num = num + 1

        # 将用户info信息载入
        keyvalue = zip(infoDic['iid'],infoDic['key'],infoDic['value'])
        for iid,k,v in keyvalue:
            keyvalue_tmp = []
            keyvaluestr = StringVar(value=str(k))
            keyvalue_tmp.append(keyvaluestr)
            label_temp = Entry(self.Frame1, textvariable=keyvaluestr, font='Label1.TLabel')
            label_temp.place(x=8, y=16 + num * 40, width=60, height=25)

            valuestr = StringVar(value=str(v))
            keyvalue_tmp.append(valuestr)

            entry_temp = Entry(self.Frame1, textvariable=valuestr, font=('宋体', 9))
            entry_temp.place(x=70, y=16 + num * 40, width=121, height=25)

            Button(self.Frame1, text='copy', command=lambda s=str(v): self.systemcontrol.setText(s),
                       style='copy.TButton').place(x=195, y=16 + num * 40, width=40, height=25)

            iidKeyValue[iid] = keyvalue_tmp
            num = num + 1

        self.detailDic['keyValue'] = iidKeyValue

        updatebtn = Button(self.Frame1, text="更新", command=lambda uid=infoDic['uid'],dic=self.detailDic: self.updateacount(uid,dic))
        delbtn = Button(self.Frame1, text="删除", command=lambda uid=infoDic['uid']: self.deleteacount(uid))


        delbtn.place(x=170, y=16 + num * 40, width=60)
        updatebtn.place(x=8, y=16 + num * 40, width=60)


class DETAILWINDOWSAPP(DETAILWINDOWS):
    def __init__(self, master=None,detailInfoDic=''):
        DETAILWINDOWS.__init__(self, master)
        self.master = master
        self.detailInfoDic = detailInfoDic
        self.basefunc = BASEFUNCTION()
        self.showDetailMsg()

    def showDetailMsg(self):
        self.showDetailWindows(self.detailInfoDic)

    def updateacount(self,uid,dic):
        print('error')

    def deleteacount(self,uid):
        sidsql = '''
                SELECT `sid` FROM `userpwd` WHERE `uid`='{0}'
                '''.format(uid)

        sid = str(self.pwdmgr.fetchsql(sidsql)[0][0])

        # 删除用户名密码
        deluserpwdsql = '''
                DELETE FROM `userpwd` WHERE `uid`='{0}'
                '''.format(uid)
        # 删除用户注册其他信息
        delinfosql = '''
                DELETE FROM `info` WHERE `uid`='{0}'
                '''.format(uid)

        # 删除对应的站点信息
        delsitesql = '''
                DELETE FROM `site` WHERE `sid`='{0}'
                '''.format(sid)

        try:
            self.pwdmgr.excutesql(deluserpwdsql)
            self.pwdmgr.excutesql(delinfosql)
            self.msg.msgbox("成功", "删除{0}成功".format(uid))
        except:
            self.debug("删除{0}出现错误".format(uid), 2)
            pass

        # 判断站点信息是否为空
        selectSiteSql = '''
                    SELECT * FROM userpwd WHERE `sid`={0}
                '''.format(sid)

        try:
            sidIsNull = self.pwdmgr.fetchsql(selectSiteSql)
        except:
            self.debug("查询SID出错", 1)

        self.debug("sidIsNull:{0}".format(sidIsNull))
        if sidIsNull == []:
            check = self.msg.cancelok("CHECK", "该网站不存在用户相关信息，是否删除该站点信息")
            if check:
                try:
                    self.pwdmgr.excutesql(delsitesql)
                except:
                    self.msg.msgbox("错误", "删除站点信息出错")

# 主窗体
class MAINWINDOWS(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('pwdmanager')
        self.master.geometry('557x445')
        self.createWidgets()
        self.msg = MESSAGEBOX(master)
        self.dbpath = os.getcwd() + "/dat.db"

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.menu = Menu(self.top)
        self.configmenu = Menu(self.menu, tearoff=0)  # tearoff 为1的话可以独立出来
        self.managermenu = Menu(self.menu, tearoff=0)
        self.aboutmenu = Menu(self.menu, tearoff=0)
        self.configmenu.add_command(label="载入", command=self.loadDBFile)
        self.configmenu.add_command(label="初始化")
        self.menu.add_cascade(label="配置", menu=self.configmenu)
        self.managermenu.add_command(label="增加", command=self.addwinfuc)
        self.managermenu.add_command(label="管理")
        self.menu.add_cascade(label="管理", menu=self.managermenu)
        self.aboutmenu.add_command(label="关于..")
        self.menu.add_cascade(label="关于", menu=self.aboutmenu)
        self.top.config(menu=self.menu)

        self.style.configure('search.TLabel',anchor='w', font=('宋体',9))
        self.search = Label(self.top, text='search', style='search.TLabel')
        self.search.place(relx=0.014, rely=0.018, relwidth=0.117, relheight=0.074)

        self.searchinputVar = StringVar(value='')
        self.searchinput = Entry(self.top, text='', textvariable=self.searchinputVar, font=('宋体',9))
        self.searchinput.place(relx=0.158, rely=0.018, relwidth=0.318, relheight=0.074)
        self.searchinput.bind('<Key>',lambda event :self.searchbarfunc(self.searchinputVar.get()))

        # self.ListboxVar = StringVar(value='')
        self.ListboxFont = Font(font=('宋体',9))
        # self.Listbox = Listbox(self.top, listvariable=self.ListboxVar, font=self.ListboxFont)
        self.Listbox = Listbox(self.top, font=self.ListboxFont)
        self.Listbox.place(relx=0.014, rely=0.126, relwidth=0.461, relheight=0.818)
        self.Listbox.bind('<Double-Button-1>',self.listboxfunc)

        self.style.configure('Frame1.TLabelframe',font=('宋体',9))
        self.Frame1 = LabelFrame(self.top, style='Frame1.TLabelframe')
        self.Frame1.place(relx=0.503, rely=0.018, relwidth=0.49, relheight=0.937)

    def updateDetailFrame(self,infodic):
        num = 0
        # self.keyLabelArr = []
        # self.valueEntryArr = []
        self.btnArr = []
        self.detailDic = {}

        self.style.configure('Label1.TLabel', anchor='w', font=('宋体', 4))
        self.style.configure('copy.TButton', font=('宋体', 9))

        for k, v in infodic.items():
            if k != 'key' and k != 'value' and k != 'uid':
                # self.keyLabelArr.append(keystr)
                label_temp = Label(self.Frame1, text=str(k), font='Label1.TLabel')
                label_temp.place(x=8, y=16 + num * 40, width=60, height=25)

                valuestr = StringVar(value=str(v))
                # self.valueEntryArr.append(valuestr)

                self.detailDic[str(k)] = valuestr

                entry_temp = Entry(self.Frame1, textvariable=valuestr, font=('宋体', 9))
                entry_temp.place(x=70, y=16 + num * 40, width=121, height=25)

                self.btnArr.append(Button(self.Frame1, text='copy', command=lambda s=str(v): self.systemcontrol.setText(s),
                                     style='copy.TButton'))
                self.btnArr[num].place(x=195, y=16 + num * 40, width=40, height=25)
                num = num + 1

        updatebtn = Button(self.Frame1,text="更新",command=lambda uid=infodic['uid']:self.updatecount(uid))
        delbtn = Button(self.Frame1, text="删除", command=lambda uid=infodic['uid']:self.deletecount(uid))
        detailbtn = Button(self.Frame1,text="详细",command=lambda uid=infodic['uid']:self.detailmassage(uid))

        delbtn.place(x=170,y=16 + num * 40, width=60)
        updatebtn.place(x=8,y=16 + num * 40,width=60)
        detailbtn.place(x=90,y=16 + num * 40,width=60)


class MAINWINDOWSAPP(MAINWINDOWS):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None,debugLevel=1):
        MAINWINDOWS.__init__(self, master)
        self.initconfig()
        self.master = master
        self.systemcontrol = SYSTTEMCONTROL()
        self.debugLevel = debugLevel

    def debug(self,msg,level=1):
        if level <= self.debugLevel:
            print("[debug:%s]"%(msg))

    def copy_Cmd(self, event=None):
        #TODO, Please finish the function here!
        print('ok')
        pass

    def initconfig(self):
        if os.path.exists(self.dbpath) != True:
            check = self.msg.cancelok("数据文件不存在，是否初始化", "数据文件不存在，是否初始化")
            if check:
                self.pwdmgr = PASSWORDMANAGER()
                self.msg.msgbox("OK", "数据初始化成功")
            else:
                self.loadDBFile()
        else:
            self.pwdmgr = PASSWORDMANAGER()

    def searchbarfunc(self, searchstr):
        if searchstr.strip() != "":
            searchsql = '''
    			SELECT `title`,`url`,`sid` FROM `site` WHERE `title` LIKE '%{0}%' OR `url` LIKE '%{0}%' COLLATE NOCASE;
    		'''.format(str(searchstr))
            print(searchsql)
            rt = self.pwdmgr.fetchsql(searchsql)
            print(rt)
            if rt != None:
                self.showsearchresult(rt)

    def showsearchresult(self, titlelist):
        self.Listbox.delete(0, END)
        self.listboxdic = {}
        num = 0
        for title,url,sid in titlelist:
            if title == '':
                self.Listbox.insert(END,url)
            else:
                self.Listbox.insert(END, title)
            self.listboxdic[num] = sid
            num = num + 1

    def loadDBFile(self):
        self.dbpath = self.msg.fileOpenDialog("请选择数据文件", "db")
        self.pwdmgr = PASSWORDMANAGER(self.dbpath)
        self.msg.msgbox("载入文件成功", "OK")

    def addwinfuc(self):
        top = Toplevel()
        ADDWINDOWSAPP(top).mainloop()

        global inpflag
        if inpflag == False:
            return
        inpflag = False

        # try:
        sitesql = '''
            INSERT INTO `site` (`title`,`url`)
            VALUES ('%s','%s')
        ''' % (inpdic['node'], inpdic['url'])

        print(sitesql)
        self.pwdmgr.excutesql(sitesql)

        getsidsql = '''
        SELECT last_insert_rowid();
        '''
        sqlrt = self.pwdmgr.fetchsql(getsidsql)
        sid = str(sqlrt[0][0])

        usersql = '''
        INSERT INTO `userpwd` (`sid`,`name`,`pwd`)
            VALUES ('{0}','{1}','{2}');
        '''.format(sid,inpdic['username'],inpdic['password'])
        self.pwdmgr.excutesql(usersql)
        uidsql = "SELECT last_insert_rowid();"
        uid = str(self.pwdmgr.fetchsql(uidsql)[0][0])
        # print(uid)

        if 'key' in inpdic:
            for key,val in zip(inpdic['key'],inpdic['val']):
                infosql = '''
                INSERT INTO `info` (`uid`,`key`,`value`)
                VALUES ('{0}','{1}','{2}')
                '''.format(uid,key,val)
                print(infosql)
                self.pwdmgr.excutesql(infosql)

        # except:
        #     pass


    def getinfo(self,sid):
        rt = {}
        sitesql = '''
        SELECT `title`,`url` FROM `site` WHERE `sid` = '{}'
        '''.format(sid)

        sqlrt = self.pwdmgr.fetchsql(sitesql)
        rt['title'] = sqlrt[0][0]
        rt['url'] = sqlrt[0][1]

        userinfosql = '''
        SELECT `uid`,`name`,`pwd` FROM `userpwd` WHERE `sid` = '{0}'
        '''.format(sid)
        sqlrt = self.pwdmgr.fetchsql(userinfosql)
        rt['uid'] = sqlrt[0][0]
        rt['name'] = sqlrt[0][1]
        rt['pwd'] = sqlrt[0][2]

        infosql = '''
        SELECT `key`,`value` FROM `info` WHERE `uid` = '{0}'
        '''.format(rt['uid'])
        sqlrt = self.pwdmgr.fetchsql(infosql)
        keyarr = []
        valuearr = []
        for key,value in sqlrt:
            keyarr.append(key)
            valuearr.append(value)
        rt['key'] = keyarr
        rt['value'] = valuearr
        self.updateDetailFrame(rt)
        print(rt)

    def deletecount(self,uid):
        sidsql = '''
        SELECT `sid` FROM `userpwd` WHERE `uid`='{0}'
        '''.format(uid)

        sid = str(self.pwdmgr.fetchsql(sidsql)[0][0])

        # 删除用户名密码
        deluserpwdsql = '''
        DELETE FROM `userpwd` WHERE `uid`='{0}'
        '''.format(uid)
        # 删除用户注册其他信息
        delinfosql = '''
        DELETE FROM `info` WHERE `uid`='{0}'
        '''.format(uid)

        # 删除对应的站点信息
        delsitesql = '''
        DELETE FROM `site` WHERE `sid`='{0}'
        '''.format(sid)

        try:
            self.pwdmgr.excutesql(deluserpwdsql)
            self.pwdmgr.excutesql(delinfosql)
            self.msg.msgbox("成功","删除{0}成功".format(uid))
        except:
            self.debug("删除{0}出现错误".format(uid),2)
            pass

        # 判断站点信息是否为空
        selectSiteSql = '''
            SELECT * FROM userpwd WHERE `sid`={0}
        '''.format(sid)

        try:
            sidIsNull = self.pwdmgr.fetchsql(selectSiteSql)
        except:
            self.debug("查询SID出错",1)

        self.debug("sidIsNull:{0}".format(sidIsNull))
        if sidIsNull==[]:
            check = self.msg.cancelok("CHECK","该网站不存在用户相关信息，是否删除该站点信息")
            if check:
                try:
                    self.pwdmgr.excutesql(delsitesql)
                except:
                    self.msg.msgbox("错误","删除站点信息出错")


    def updatecount(self,uid):
        updatesql = '''
            UPDATE userpwd set `name`='{0}',`pwd`='{1}' WHERE `uid`={2}
        '''.format(self.detailDic['name'].get(),self.detailDic['pwd'].get(),uid)
        self.debug("sql: {0}".format(updatesql),2)
        try:
            self.pwdmgr.excutesql(updatesql)
            self.msg.msgbox('SUCCECE','用户名密码更新成功')
        except sqlite3.Error:
            self.msg.msgbox('ERROR','数据库更新失败')
            self.debug('update error:{0}'.format(sqlite3.Error.args[0]),2)

        # for k in self.keyLabelArr:
        #     self.debug("{0} label".format(k.get()),1)



    def detailmassage(self,uid):
        rt = {}
        sidsql = '''
                        SELECT `sid` FROM `userpwd` WHERE `uid`='{0}'
                        '''.format(uid)

        sid = str(self.pwdmgr.fetchsql(sidsql)[0][0])

        sitesql = '''
                        SELECT `title`,`url` FROM `site` WHERE `sid` = '{}'
                        '''.format(sid)

        sqlrt = self.pwdmgr.fetchsql(sitesql)
        rt['title'] = sqlrt[0][0]
        rt['url'] = sqlrt[0][1]

        userinfosql = '''
                        SELECT `uid`,`name`,`pwd` FROM `userpwd` WHERE `uid` = '{0}'
                        '''.format(uid)
        sqlrt = self.pwdmgr.fetchsql(userinfosql)
        rt['uid'] = sqlrt[0][0]
        rt['name'] = sqlrt[0][1]
        rt['pwd'] = sqlrt[0][2]

        infosql = '''
                        SELECT `key`,`value`,`iid` FROM `info` WHERE `uid` = '{0}'
                        '''.format(rt['uid'])
        sqlrt = self.pwdmgr.fetchsql(infosql)
        keyarr = []
        valuearr = []
        iidarr = []
        for key, value, iid in sqlrt:
            keyarr.append(key)
            valuearr.append(value)
            iidarr.append(iid)
        rt['key'] = keyarr
        rt['value'] = valuearr
        rt['iid'] = iidarr

        top = Toplevel()
        DETAILWINDOWSAPP(top,detailInfoDic=rt).mainloop()


        # sidsql = '''
        #         SELECT `sid` FROM `userpwd` WHERE `uid`='{0}'
        #         '''.format(uid)
        # sid = str(self.pwdmgr.fetchsql(sidsql)[0][0])
        #
        #
        # self.msg.msgbox("哈哈哈","有待完善")

    def listboxfunc(self,event):
        selectnum = int(self.Listbox.curselection()[0])
        sid = self.listboxdic[selectnum]
        self.getinfo(sid)


if __name__ == "__main__":
    top = Tk()

    MAINWINDOWSAPP(top).mainloop()
    try: top.destroy()
    except: pass
