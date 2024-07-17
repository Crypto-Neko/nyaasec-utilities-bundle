# NyaaSec Utilities Bundle v1.0.0

### Introduction

The NyaaSec Utilities Bundle is a collection of scripts that can serve to harden a GNU/Linux-based operating system. It currently supports distributions based on Ubuntu/Debian, Fedora, and Arch Linux.
My main motivation behind making this is to learn how to use wxWidgets (especially for Python) to make security software, which will help me create NyaaCrypt, a much bigger project I'll be starting now that this has been released.
Other than for practice, I hope this helps someone with less experience harden their Linux system: I'll be using it on future installs to quickly set my system up with just a few clicks.

### Features

1. **Encrypt a Device or Partition**: Allows the encryption of a block device in a few clicks using LUKS with 256-bit AES encryption.
2. **Hardening Script**: Runs a custom hardening script that sets secure kernel parameters and installs linux-hardened on supported distributions, along with some other security software.
3. **Setup Firejail**: Installs firejail and runs firecfg with the sound fix. Firejail is, in my opinion, the best sandboxing software available for Linux. Learn more about it [here](https://wiki.archlinux.org/title/Firejail).
4. **Lock Root Account**: Disable the root account login to prevent unauthorized access. This is an important attack vector to cover. Make sure you have a tool allowing you to gain root access like sudo or doas before running this.
5. **Check Firewall**: Identify the installed firewall application and display the current set of rules in use. It will warn you if the firewall is improperly configured.

### Download

You can run the .py file directly from the commandline on any supported Linux distribution, but for a better experience you can download the binary for v1.0.0 directly [at this link](https://github.com/Crypto-Neko/nyaasec-utilities-bundle/releases/tag/v1.0.0).

### Contact

If you want to ask me a question about the program, you can submit an issue here on GitHub. If you want to ask something privately, you can contact me on my Discord account with the username `crypto.kitty`.
