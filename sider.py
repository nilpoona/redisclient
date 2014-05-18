# -*- coding: utf-8 -*-
from attributeredis import AttributeRedis
import wx
import wx.grid
import wx.lib.gridmovers

class RedisData(AttributeRedis):
    pass

class SettingsPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        self._parent = parent
        self._redis_connect_button = wx.Button(self, -1, u'接続', (360, 15))

        self.st_host = wx.StaticText(self, -1, "Host Name:", pos=(20,20))
        self._host_name_box = wx.TextCtrl(self, wx.ID_ANY, 'localhost', pos=(100, 20))

        self.st_port = wx.StaticText(self, -1, "Port:", pos=(210,20))
        self._port_box  = wx.TextCtrl(self, wx.ID_ANY, '6379', pos=(245, 20))

        self._bind()

    def _bind(self):
        self.Bind(wx.EVT_BUTTON, self.redis_connect, id=self._redis_connect_button.GetId())

    def redis_connect(self, event):
        #TODO バリデーション
        if self._port_box.IsEmpty() or self._host_name_box.IsEmpty():
            wx.MessageBox('Host Name or Port Number is Empty.', 'Error')
            return

        port_number = self._port_box.GetValue()
        host_name = self._host_name_box.GetValue()

        RedisData(host_name, int(port_number))

class RedisDataGrid(wx.grid.Grid):
    def __init__(self, parent, id):
        wx.grid.Grid.__init__(self, parent, id, size=(1000, 500))
        self.CreateGrid(2,3)
        self.SetColLabelSize(0)
        self.SetRowLabelSize(0)
        self.SetCellValue(0, 0, "Key")
        self.SetCellValue(0, 1, "Data Type")
        self.SetCellValue(0, 2, "Value")
        
class RedisDataPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        grid = wx.GridBagSizer(hgap=5, vgap=5)

        grid.Add(RedisDataGrid(self, -1), pos=(0,0))
        self.SetSizerAndFit(grid)

class Sider(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title=title, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN, size=(1000, 800), pos=wx.DefaultPosition)
        self._redis = None

        panel = wx.Panel(self, -1)
        self._settings_panel = SettingsPanel(panel, -1)
        self.redis_data_panel = RedisDataPanel(panel, -1)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self._settings_panel, 1, wx.EXPAND | wx.ALL, 5)
        layout.Add(self.redis_data_panel, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(layout)

        self.Centre()
        self.Show(True)

    def set_redis_connection(self, redis):
        self._redis = redis

app = wx.App()
Sider(None, -1, 'Sider')
app.MainLoop()
