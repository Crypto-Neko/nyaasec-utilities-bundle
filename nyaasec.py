import os
import wx
import subprocess
import threading
import sys

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
        image_path = "./Nyaa.png"
        image = wx.Bitmap(image_path, wx.BITMAP_TYPE_PNG)
        
        # Create a StaticBitmap to display the image
        self.kitty_ctrl = wx.StaticBitmap(self, bitmap=image)
        
        # Create buttons
        self.crypt_button = wx.Button(self, label='Encrypt a Device or Partition', size=(200, 40))
        self.hardening_button = wx.Button(self, label='Run Hardening Script', size=(200, 40))
        self.firejail_button = wx.Button(self, label='Setup Firejail', size=(200, 40))
        self.lock_button = wx.Button(self, label='Lock Root Account', size=(200, 40))
        self.firewall_button = wx.Button(self, label='Check Firewall', size=(200, 40))

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

# Panel to encrypt block devices using LUKS
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

# Panel for running the hardening script
class HardeningPanel(wx.Panel):
    def __init__(self, parent, switch_panel_callback):
        super(HardeningPanel, self).__init__(parent)
        self.switch_panel_callback = switch_panel_callback
        
        # Set up the text
        label = wx.StaticText(self, label="Run Hardening Script")
        body = wx.StaticText(self, label="Runs a hardening script that sets secure kernel parameters and installs linux-hardened or equivalent security modules depending on your distribution. Good for basic security on any supported GNU/Linux system.")
        body.Wrap(350)

        # Set up the buttons
        button = wx.Button(self, label="Back")
        lock_button = wx.Button(self, label="Run script")
        button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('main_panel'))
        lock_button.Bind(wx.EVT_BUTTON, lambda event: self.on_hardening_click(event))
        
        # Output box to view the result
        self.output_box = wx.TextCtrl(self, size=(350, 450), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        # Create a vertical box sizer
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Add widgets to the sizer with flag to center them
        vbox.Add(label, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(body, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(lock_button, 0, wx.ALIGN_CENTER | wx.TOP, 40)
        vbox.Add(self.output_box, 0, wx.ALIGN_CENTER | wx.TOP, 40)
        vbox.Add(button, 0, wx.ALIGN_CENTER | wx.TOP, 30)

        # Set the sizer for the panel
        self.SetSizer(vbox)
    
    def on_hardening_click(self, event):
        # Define the command to run the script
        command = "chmod +x hardening.sh && ./hardening.sh"
        
        # Run the command in a separate thread
        threading.Thread(target=self.run_command, args=(command,)).start()

    def run_command(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in process.stdout:
            wx.CallAfter(self.append_output, line)
        for line in process.stderr:
            wx.CallAfter(self.append_output, line)
        
        process.stdout.close()
        process.stderr.close()
        process.wait()
    
    def append_output(self, text):
        self.output_box.AppendText(text)

# Class for the panel containing the Firejail script
class FirejailPanel(wx.Panel):
    def __init__(self, parent, switch_panel_callback):
        super(FirejailPanel, self).__init__(parent)
        self.switch_panel_callback = switch_panel_callback
        
        # Set up the text
        label = wx.StaticText(self, label="Setup Firejail")
        body = wx.StaticText(self, label="Firejail is state-of-the-art sandbox software for Linux that prevents applications from having access to files and processes unnecessary for their functioning. Using it is recommended for optimal security. This script will install Firejail if it is not present on your system and configure your applications to use it.")
        body.Wrap(350)

        # Set up the buttons
        button = wx.Button(self, label="Back")
        firejail_button = wx.Button(self, label="Setup Firejail")
        button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('main_panel'))
        firejail_button.Bind(wx.EVT_BUTTON, lambda event: self.on_firejail_click(event))
        
        # Output box to view the result
        self.output_box = wx.TextCtrl(self, size=(350, 250), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        # Distribution choice
        dist_label = wx.StaticText(self, label="Select your distribution:")
        self.dist_choice = wx.Choice(self, choices=["Ubuntu/Debian", "Fedora", "Arch Linux"])
        self.dist_choice.SetSelection(0)  # Default to the first option

        # Create a vertical box sizer
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Add widgets to the sizer with flag to center them
        vbox.Add(label, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(body, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(dist_label, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(self.dist_choice, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(firejail_button, 0, wx.ALIGN_CENTER | wx.TOP, 40)        
        vbox.Add(self.output_box, 0, wx.ALIGN_CENTER | wx.TOP, 40)
        vbox.Add(button, 0, wx.ALIGN_CENTER | wx.TOP, 100)

        # Set the sizer for the panel
        self.SetSizer(vbox)

    def on_firejail_click(self, event):
        # Get the selected distribution
        dist = self.dist_choice.GetString(self.dist_choice.GetSelection())
        
        # Define the command based on the selected distribution
        if dist == "Ubuntu/Debian":
            command = "apt-get update && apt-get install -y firejail && firecfg --fix-sound"
        elif dist == "Fedora":
            command = "dnf install -y firejail && firecfg --fix-sound"
        elif dist == "Arch Linux":
            command = "pacman -Syu --noconfirm firejail && firecfg --fix-sound"
        else:
            command = "echo 'Unsupported distribution selected'"
        
        # Run the command in a separate thread
        threading.Thread(target=self.run_command, args=(command,)).start()

    def run_command(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in process.stdout:
            wx.CallAfter(self.append_output, line)
        for line in process.stderr:
            wx.CallAfter(self.append_output, line)
        
        process.stdout.close()
        process.stderr.close()
        process.wait()
    
    def append_output(self, text):
        self.output_box.AppendText(text)

# Panel for locking the root account
class LockPanel(wx.Panel):
    def __init__(self, parent, switch_panel_callback):
        super(LockPanel, self).__init__(parent)
        self.switch_panel_callback = switch_panel_callback
        
        # Set up the text
        label = wx.StaticText(self, label="Lock Root Account")
        body = wx.StaticText(self, label="This will make the root account inaccessible via login, which can increase security. Make sure you have a utility like sudo or doas to run commands as root or your user is in the WHEEL group.")
        body.Wrap(350)

        # Set up the buttons
        button = wx.Button(self, label="Back")
        lock_button = wx.Button(self, label="Disable it")
        button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('main_panel'))
        lock_button.Bind(wx.EVT_BUTTON, lambda event: self.on_disable_click(event))
        
        # Output box to view the result
        self.output_box = wx.TextCtrl(self, size=(350, 450), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        # Create a vertical box sizer
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Add widgets to the sizer with flag to center them
        vbox.Add(label, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(body, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(lock_button, 0, wx.ALIGN_CENTER | wx.TOP, 40)
        vbox.Add(self.output_box, 0, wx.ALIGN_CENTER | wx.TOP, 40)
        vbox.Add(button, 0, wx.ALIGN_CENTER | wx.TOP, 30)

        # Set the sizer for the panel
        self.SetSizer(vbox)
    
    def on_disable_click(self, event):
        command = "sudo passwd -l root"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # Display the output in the TextCtrl
        self.output_box.SetValue(stdout.decode() + stderr.decode())

# Panel for getting firewall configuration information
class FirewallPanel(wx.Panel):
    def __init__(self, parent, switch_panel_callback):
        super(FirewallPanel, self).__init__(parent)
        self.switch_panel_callback = switch_panel_callback
        
        # Set up the text
        label = wx.StaticText(self, label="Check Firewall")
        body = wx.StaticText(self, label="Checks which firewall application is installed and prints the table of rules currently in use.")
        body.Wrap(350)

        # Set up the buttons
        button = wx.Button(self, label="Back")
        firewall_button = wx.Button(self, label="Check Firewall")
        button.Bind(wx.EVT_BUTTON, lambda event: self.switch_panel_callback('main_panel'))
        firewall_button.Bind(wx.EVT_BUTTON, lambda event: self.on_firewall_click(event))
        
        # Output box to view the result
        self.output_box = wx.TextCtrl(self, size=(350, 250), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        # Create a vertical box sizer
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Add widgets to the sizer with flag to center them
        vbox.Add(label, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(body, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        vbox.Add(firewall_button, 0, wx.ALIGN_CENTER | wx.TOP, 40)        
        vbox.Add(self.output_box, 0, wx.ALIGN_CENTER | wx.TOP, 40)
        vbox.Add(button, 0, wx.ALIGN_CENTER | wx.TOP, 270)

        # Set the sizer for the panel
        self.SetSizer(vbox)

    def on_firewall_click(self, event):
        # Get the selected distribution
        firewall_script = """
        #!/bin/bash
        
        # Check for iptables or nftables
        if command -v iptables > /dev/null 2>&1; then
            echo "iptables is installed."
            iptables -L
        elif command -v nft > /dev/null 2>&1; then
            echo "nftables is installed."
            nft list ruleset
        else
            echo "Neither iptables nor nftables is installed. Run hardening script to install."
            exit 1
        fi
        """
        
        # Run the command in a separate thread
        threading.Thread(target=self.run_command, args=(firewall_script,)).start()

    def run_command(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in process.stdout:
            wx.CallAfter(self.append_output, line)
        for line in process.stderr:
            wx.CallAfter(self.append_output, line)
        
        process.stdout.close()
        process.stderr.close()
        process.wait()
    
    def append_output(self, text):
        self.output_box.AppendText(text)

# Frame for the entire application
class MenuFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MenuFrame, self).__init__(parent, title=title, size=(400, 800))
        
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

