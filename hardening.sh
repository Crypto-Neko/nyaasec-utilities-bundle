#!/bin/bash

# Get the distro
. /etc/os-release
export distro=$ID

# Update repositories and install relevant packaged
if [[ "$distro" == "ubuntu" || "$distro" == "debian" || "$distro" == "Ubuntu" || "$distro" == "Debian" ]]; then
	apt-get update
	apt-get install libpam-apparmor
	apt-get install sysctl-hardening
	sysctl -p
elif [[ "$distro" == "arch" || "$distro" == "Arch" ]]; then
	pacman -Syu
	pacman -Sy linux-hardened
	mkinitcpio -p linux-hardened
elif [[ "$distro" == "fedora" || "$distro" == "Fedora" ]]; then
	dnf update -y
	dnf install hardened-sources
	dnf install audit
	dnf install aide
fi

# Set secure kernel parameters
sysctl -w kernel.kptr_restrict=2
sysctl -w kernel.dmesg_restrict=1
sysctl -w kernel.printk="3 3 3 3"
sysctl -w net.core.bpf_jit_harden=2
sysctl -w dev.tty.ldisc_autoload=0
sysctl -w kernel.sysrq=4
sysctl -w kernel.perf_event_paranoid=3

# Set network hardening parameters
sysctl -w net.ipv4.tcp_syncookies=1
sysctl -w net.ipv4.tcp_rfc1337=1
sysctl -w net.ipv4.conf.all.rp_filter=1
sysctl -w net.ipv4.conf.default.rp_filter=1
sysctl -w net.ipv4.conf.all.accept_redirects=0
sysctl -w net.ipv4.conf.default.accept_redirects=0
sysctl -w net.ipv4.conf.all.secure_redirects=0
sysctl -w net.ipv4.conf.default.secure_redirects=0
sysctl -w net.ipv6.conf.all.accept_redirects=0
sysctl -w net.ipv6.conf.default.accept_redirects=0
sysctl -w net.ipv4.conf.all.send_redirects=0
sysctl -w net.ipv4.conf.default.send_redirects=0
sysctl -w net.ipv4.icmp_echo_ignore_all=1
sysctl -w net.ipv4.conf.all.accept_source_route=0
sysctl -w net.ipv4.conf.default.accept_source_route=0
sysctl -w net.ipv6.conf.all.accept_source_route=0
sysctl -w net.ipv6.conf.default.accept_source_route=0
sysctl -w net.ipv6.conf.all.accept_ra=0
sysctl -w net.ipv6.conf.default.accept_ra=0

# Userspace kernel parameters
sysctl -w kernel.yama.ptrace_scope=2
sysctl -w vm.mmap_rnd_bits=32
sysctl -w vm.mmap_rnd_compat_bits=16
sysctl -w fs.protected_symlinks=1
sysctl -w fs.protected_hardlinks=1
sysctl -w fs.protected_fifos=2
sysctl -w fs.protected_regular=2

# Notify the user that the script has successfully exited.
echo "***"
echo "Script completed successfully. You may hit \"Back\" now."
