import wx

class MainPanel(wx.Panel):
    def __init__(self, parent, switch_panel_callback):
        super(MainPanel, self).__init__(parent)
        
        self.switch_panel_callback = switch_panel_callback
        
        # Create the title
        titleFont = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.title = wx.StaticText(self, label="NyaaSec")
        self.title.SetFont(titleFont)
        self.subtitle = wx.StaticText(self, label="GUI-based security and hardening application")
        self.button_title = wx.StaticText(self, label="Security Utilities")

        # Load an image
        image = wx.Bitmap("./Nyaa.png", wx.BITMAP_TYPE_PNG)
        
        # Create a StaticBitmap to display the image
        self.kitty_ctrl = wx.StaticBitmap(self, bitmap=image)
        
        # Create buttons
        self.crypt_button = wx.Button(self, label='Encrypt a Device or Partition', size=(200, 40))
        self.hardening_button = wx.Button(self, label='Run Hardening Script', size=(200, 40))
        self.firejail_button = wx.Button(self, label='Setup Firejail', size=(200, 40))
        self.lock_button = wx.Button(self, label='Lock Root Account', size=(200, 40))
        self.firewall_button = wx.Button(self, label='Configure Firewall', size=(200, 40))

        # Bind buttons to switch panel events
        self.crypt_button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('encryption_panel'))
        self.hardening_button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('hardening_panel'))
        self.firejail_button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('firejail_panel'))
        self.lock_button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('lock_panel'))
        self.firewall_button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('firewall_panel'))
        
        # Create a vertical box sizer
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Add widgets to the sizer with flag to center them
        vbox.Add(self.title, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(self.subtitle, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        vbox.Add(self.kitty_ctrl, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(self.button_title, 0, wx.ALIGN_CENTER | wx.TOP, 40)
        vbox.Add(self.crypt_button, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(self.hardening_button, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(self.firejail_button, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(self.lock_button, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(self.firewall_button, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        # Set the sizer for the panel
        self.SetSizer(vbox)

class EncryptionPanel(wx.Panel):
    def __init__(self, parent, switch_panel_callback):
        super(EncryptionPanel, self).__init__(parent)
        self.switch_panel_callback = switch_panel_callback
        
        label = wx.StaticText(self, label="Encryption")
        
        button = wx.Button(self, label="Back")
        button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('main_panel'))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.ALL, 10)
        sizer.Add(button, 0, wx.ALL, 10)
        
        self.SetSizer(sizer)

class HardeningPanel(wx.Panel):
    def __init__(self, parent, switch_panel_callback):
        super(HardeningPanel, self).__init__(parent)
        self.switch_panel_callback = switch_panel_callback
        
        label = wx.StaticText(self, label="Hardening Script")
        
        button = wx.Button(self, label="Back")
        button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('main_panel'))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.ALL, 10)
        sizer.Add(button, 0, wx.ALL, 10)
        
        self.SetSizer(sizer)

class FirejailPanel(wx.Panel):
    def __init__(self, parent, switch_panel_callback):
        super(FirejailPanel, self).__init__(parent)
        self.switch_panel_callback = switch_panel_callback
        
        label = wx.StaticText(self, label="Setup Firejail")
        
        button = wx.Button(self, label="Back")
        button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('main_panel'))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.ALL, 10)
        sizer.Add(button, 0, wx.ALL, 10)
        
        self.SetSizer(sizer)

class LockPanel(wx.Panel):
    def __init__(self, parent, switch_panel_callback):
        super(LockPanel, self).__init__(parent)
        self.switch_panel_callback = switch_panel_callback
        
        label = wx.StaticText(self, label="Lock Root Account")
        
        button = wx.Button(self, label="Back")
        button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('main_panel'))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.ALL, 10)
        sizer.Add(button, 0, wx.ALL, 10)
        
        self.SetSizer(sizer)

class FirewallPanel(wx.Panel):
    def __init__(self, parent, switch_panel_callback):
        super(FirewallPanel, self).__init__(parent)
        self.switch_panel_callback = switch_panel_callback
        
        label = wx.StaticText(self, label="Configure Firewall")
        
        button = wx.Button(self, label="Back")
        button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('main_panel'))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.ALL, 10)
        sizer.Add(button, 0, wx.ALL, 10)
        
        self.SetSizer(sizer)

class MenuFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MenuFrame, self).__init__(parent, title=title, size=(400, 800))
        
        # Set the icon
        # icon = wx.Icon("./nyaa.ico", wx.BITMAP_TYPE_ICO)
        # self.SetIcon(icon)
        
        # Initialize panels
        self.main_panel = MainPanel(self, self.switch_panel)
        self.encryption_panel = EncryptionPanel(self, self.switch_panel)
        self.hardening_panel = HardeningPanel(self, self.switch_panel)
        self.firejail_panel = FirejailPanel(self, self.switch_panel)
        self.lock_panel = LockPanel(self, self.switch_panel)
        self.firewall_panel = FirewallPanel(self, self.switch_panel)
        
        # Use a dictionary to store panels
        self.panels = {
            'main_panel': self.main_panel,
            'encryption_panel': self.encryption_panel,
            'hardening_panel': self.hardening_panel,
            'firejail_panel': self.firejail_panel,
            'lock_panel': self.lock_panel,
            'firewall_panel':self.firewall_panel
        }
        
        # Set the frame sizer and show the main panel
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.switch_panel('main_panel')
        
        self.Show(True)
    
    def switch_panel(self, panel_name):
        # Hide and remove all panels from sizer
        for panel in self.panels.values():
            self.sizer.Detach(panel)
            panel.Hide()
        
        # Add and show the selected panel
        self.current_panel = self.panels[panel_name]
        self.sizer.Add(self.current_panel, 1, wx.EXPAND)
        self.current_panel.Show()
        self.Layout()

class App(wx.App):
    def OnInit(self):
        frame = MenuFrame(None, title="NyaaSec: Security and Hardening")
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()

