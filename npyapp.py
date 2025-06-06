import npyscreen

# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application

class MyTestApp(npyscreen.NPSAppManaged):
    #Gloval variables
    allowedThrough, allowedIn, allowedOut, mDHCPVar, icmpFragVar, icmpSmurfVar, icmpEchoVar, synFloodVar = None, None, None, None, None, None, None, None
    def onStart(self):
        self.registerForm("MAIN", MainForm())
        self.registerForm("AllowedIn", AllowedInForm())
        self.registerForm("AllowedOut", AllowedOutForm())
        self.registerForm("OtherOptions1", OtherOptions1Form())
        self.registerForm("OtherOptions2", OtherOptions2Form())
        self.registerForm("OtherOptions3", OtherOptions3Form())
    
class MainForm(npyscreen.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("AllowedIn")

    def create(self):
        self.allowedThrough = self.add(npyscreen.TitleMultiSelect, name='Select which services are allowed to be accessed through the firewall:', values=['SSH', 'HTTP', 'HTTPS', 'DNS'],scroll_exit=True)

    def on_ok(self):
        self.parentApp.allowedThrough = self.allowedThrough.value
        self.parentApp.switchForm("AllowedIn")


class AllowedInForm(npyscreen.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("AllowedOut")
        
    def create(self):
        self.allowedIn = self.add(npyscreen.TitleMultiSelect, name='Select which services are allowed to be accessed on the firewall:', values=['SSH', 'HTTP', 'HTTPS', 'DNS'],scroll_exit=True)

    def on_ok(self):
        self.parentApp.allowedIn = self.allowedIn.value
        self.parentApp.switchForm("AllowedOut")


class AllowedOutForm(npyscreen.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("OtherOptions1")
        
    def create(self):
        self.allowedOut = self.add(npyscreen.TitleMultiSelect, name='Select which services are allowed to be accessed from the firewall:', values=['SSH', 'HTTP', 'HTTPS', 'DNS'],scroll_exit=True)

    def on_ok(self):
        self.parentApp.allowedOut = self.allowedOut.value
        self.parentApp.switchForm("OtherOptions1")


class OtherOptions1Form(npyscreen.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("OtherOptions2")
    
    def create(self):
        self.mDHCP = self.add(npyscreen.TitleSelectOne, max_height=4, name='Block multicast DHCP?', values=['Yes', 'No'])
        self.icmpFrag = self.add(npyscreen.TitleSelectOne, max_height=4, name='Protect from ICMP Fragmentation attacks?', values=['Yes', 'No'])
        self.icmpSmurf = self.add(npyscreen.TitleSelectOne, max_height=4,name='Protect from ICMP Smurf attacks?', values=['Yes', 'No'])

    def on_ok(self):
        self.parentApp.mDHCPVar = self.mDHCP.value
        self.parentApp.icmpFragVar = self.icmpFrag.value
        self.parentApp.icmpSmurfVar = self.icmpSmurf.value
        self.parentApp.switchForm("OtherOptions2")


class OtherOptions2Form(npyscreen.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("OtherOptions3")
    
    def create(self):
        self.icmpEcho = self.add(npyscreen.TitleSelectOne, max_height=4, name='Block ICMP echo requests?', values=['Yes', 'No'])
        self.synFlood = self.add(npyscreen.TitleSelectOne, max_height=4, name='Protect from SYN flood attacks?', values=['Yes', 'No'])

    def on_ok(self):
        self.parentApp.icmpEchoVar = self.icmpEcho.value
        self.parentApp.synFloodVar = self.synFlood.value
        self.parentApp.switchForm("OtherOptions3")


class OtherOptions3Form(npyscreen.ActionForm):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm(None)
        
    def create(self):
        self.customSSHPort = self.add(npyscreen.TitleText, name='Set SSH server port:', value='22')
        self.public = self.add(npyscreen.TitleText, name='Set public interface name:', value='enp0s8')
        self.private = self.add(npyscreen.TitleText, name='Set public interface name:', value='enp0s9')
        self.fileName = self.add(npyscreen.TitleText, name='Set configuration file name:', value='configuration.nix')

    def on_ok(self):
        portsAllowedThroughUdp = []
        portsAllowedThroughTcp = []
        portsAllowedInUdp = []
        portsAllowedInTcp = []
        portsAllowedOutUdp = []
        portsAllowedOutTcp = []
        #dhcpIn, dhcpOut = None, None
        #ports allowed through firewall
        if 0 in self.parentApp.allowedThrough:
            portsAllowedThroughTcp.append(22)
        if 1 in self.parentApp.allowedThrough:
            portsAllowedThroughTcp.append(80)
        if 2 in self.parentApp.allowedThrough:
            portsAllowedThroughTcp.append(443)
        if 3 in self.parentApp.allowedThrough:
            portsAllowedThroughTcp.append(53)
            portsAllowedThroughUdp.append(53)
        #ports allowed coming in to firewall
        if 0 in self.parentApp.allowedIn:
            portsAllowedInTcp.append(self.customSSHPort.value)
        if 1 in self.parentApp.allowedIn:
            portsAllowedInTcp.append(80)
        if 2 in self.parentApp.allowedIn:
            portsAllowedInTcp.append(443)
        if 3 in self.parentApp.allowedIn:
            portsAllowedInTcp.append(53)
            portsAllowedInUdp.append(53)
        #ports allowed outgoing from firewall
        if 0 in self.parentApp.allowedOut:
            portsAllowedOutTcp.append(22)
        if 1 in self.parentApp.allowedOut:
            portsAllowedOutTcp.append(80)
        if 2 in self.parentApp.allowedOut:
            portsAllowedOutTcp.append(443)
        if 3 in self.parentApp.allowedOut:
            portsAllowedOutTcp.append(53)
            portsAllowedOutUdp.append(53)
        config_data = [
            '# Edit this configuration file to define what should be installed on',
            '# your system. Help is available in the configuration.nix(5) man page, on',
            '# https://search.nixos.org/options and in the NixOS manual (`nixos-help`).',
            '',
            '{ config, lib, pkgs, ... }:',
            '',
            '{',
            '  imports =',
            '    [ # Include the results of the hardware scan.',
            '      ./hardware-configuration.nix',
            '    ];',
            '',
            '  # Use the systemd-boot EFI boot loader.',
            '  boot.loader.systemd-boot.enable = true;',
            '  boot.loader.efi.canTouchEfiVariables = true;',
            '',
            '  networking.hostName = "nix-firewall"; # Define your hostname.',
            '  # Pick only one of the below networking options.',
            '  # networking.wireless.enable = true;  # Enables wireless support via wpa_supplicant.',
            '  networking.networkmanager.enable = true;  # Easiest to use and most distros use this by default.',
            '',
            '  # Set your time zone.',
            '  time.timeZone = "US/Chicago";',
            '',
            '  # Configure network proxy if necessary',
            '  # networking.proxy.default = "http://user:password@proxy:port/";',
            '  # networking.proxy.noProxy = "127.0.0.1,localhost,internal.domain";',
            '  ',
            '  services.envfs.enable = false;',
            '  services.xserver = {',
            '    enable = true;',
            '    displayManager.gdm.enable = true;',
            '    desktopManager.gnome.enable = true;',
            '  };',
            '',
            '  # Enable CUPS to print documents.',
            '  # services.printing.enable = true;',
            '',
            '  # Enable sound.',
            '  # hardware.pulseaudio.enable = true;',
            '  # OR',
            '  services.pipewire = {',
            '    enable = true;',
            '    pulse.enable = true;',
            '  };',
            '',
            '  # Enable touchpad support (enabled default in most desktopManager).',
            '  services.libinput.enable = true;',
            '',
            "  # Define a user account. Don't forget to set a password with ‘passwd’.",
            '  users.users.admin = {',
            '    isNormalUser = true;',
            '    description = "admin";',
            '    extraGroups = [ "wheel" ]; # Enable ‘sudo’ for the user.',
            '    shell = pkgs.bash;',
            '    packages = with pkgs; [',
            '    ];',
            '    home = "/home/admin";',
            '  };',
            '',
            '  boot.loader.grub.device = "/dev/nvme0n1";  ',
            '',
            '  nixpkgs.config.allowUnfree = true;',
            '',
            '  # List packages installed in system profile. To search, run:',
            '  # $ nix search wget',
            '  environment.systemPackages = with pkgs; [',
            '    wget',
            '    git',
            '    python3',
            '    nixos-generators',
            '    devenv',
            '  ]; # **parameter for including additional packages',
            '',
            '  nix.settings.trusted-users = [',
            '    "root" ',
            '    "admin"',
            '    ];',
            '',
            '  services.openssh = {'
            ]
        if 0 in self.parentApp.allowedIn:
            config_data.append('    enable = true;  # **parameter for enabling ssh')
        else:
            config_data.append('    enable = false;  # **parameter for enabling ssh')
        config_data.append(f'    ports = [ {self.customSSHPort.value} ]; # **parameter for ssh port')
        config_data.extend([
            '    settings = {',
            '       PasswordAuthentication = true;',
            '       AllowUsers = null; # Allows all users by default. Can be [ "user1" "user2" ] # **parameter for allowed users',
            '       UseDns = true;',
            '       X11Forwarding = true;',
            '       PermitRootLogin = "prohibit-password"; # "yes", "without-password", "prohibit-password", "forced-commands-only", "no" # **parameter for permit root log in',
            '  };',
            '};',
            '',
            'networking.firewall = {',
            '  enable = true;',
            "  extraCommands = ''",
            "    iptables -N nixos-fw-forward",
            "    iptables -N nixos-fw-output",
            "    iptables -A FORWARD -j nixos-fw-forward",
            "    iptables -A OUTPUT -j nixos-fw-output",
            "    iptables -A nixos-fw-output -o lo -j nixos-fw-accept"
            ])
        #Forward chain commands
        for x in portsAllowedThroughTcp:
            config_data.append(f"    iptables -A nixos-fw-forward -i {self.public.value} -p tcp --dport {x} -m state --state NEW,ESTABLISHED -j nixos-fw-accept")
        for x in portsAllowedThroughUdp:
            config_data.append(f"    iptables -A nixos-fw-forward -i {self.public.value} -p udp --dport {x} -m state --state NEW,ESTABLISHED -j nixos-fw-accept")
        config_data.append(f"    iptables -A nixos-fw-forward -i {self.private.value} -m state --state NEW,ESTABLISHED -j nixos-fw-accept")
        config_data.append(f"    iptables -A nixos-fw-forward -i {self.public.value} -m state --state RELATED,ESTABLISHED -j nixos-fw-accept")
        config_data.append("    iptables -A nixos-fw-forward -j nixos-fw-log-refuse")
        #Input chain commands 
        for x in portsAllowedInUdp:
            config_data.append(f"    iptables -I nixos-fw 2 -p udp --dport {x} -m state --state NEW,ESTABLISHED -j nixos-fw-accept")
        for x in portsAllowedInTcp:
            config_data.append(f"    iptables -I nixos-fw 2 -p tcp --dport {x} -m state --state NEW,ESTABLISHED -j nixos-fw-accept")
        if 0 in self.parentApp.icmpEchoVar:
            config_data.append("    iptables -I nixos-fw 2 -p icmp ! --icmp-type echo-request -j ACCEPT")
        else:
            config_data.append("    iptables -I nixos-fw 2 -p icmp -j ACCEPT")
        config_data.append("    iptables -I nixos-fw 2 -p udp --sport 67:68 --dport 67:68 -j nixos-fw-accept")
        if 0 in self.parentApp.synFloodVar:
            config_data.extend([
                "    iptables -N syn-limit",
                "    iptables -I nixos-fw 1 -p tcp --syn -j syn-limit",
                "    iptables -A syn-limit -m hashlimit --hashlimit-upto 4/sec --hashlimit-burst 3 --hashlimit-mode srcip --hashlimit-name conn_rate_limit -j nixos-fw-accept",
                "    iptables -A syn-limit -j nixos-fw-log-refuse"
                ])
        if 0 in self.parentApp.icmpSmurfVar:
            config_data.extend([
                "    iptables -N icmp-smurf",
                "    iptables -I nixos-fw 1 -p icmp -j icmp-smurf",
                "    iptables -A icmp-smurf -m hashlimit --hashlimit-upto 2/sec --hashlimit-burst 2 --hashlimit-mode srcip --hashlimit-name conn_rate_limit -j RETURN",
                "    iptables -A icmp-smurf -j nixos-fw-log-refuse"
                ])
        if 0 in self.parentApp.icmpFragVar:
            config_data.extend([
                "    iptables -N icmp-frag",
                "    iptables -I nixos-fw 1 -p icmp -j icmp-frag",
                "    iptables -A icmp-frag -m length --length 20:1492 -j RETURN",
                "    iptables -A icmp-frag -j nixos-fw-log-refuse"
                ])
        if 0 in self.parentApp.mDHCPVar:
            config_data.extend([
                "    iptables -N multicast-dhcp",
                "    iptables -I nixos-fw 1 -p udp -d 224.0.0.251 --sport 67:68 --dport 67:68 -j multicast-dhcp",
                "    iptables -A multicast-dhcp -j nixos-fw-log-refuse"
                ])
        #Output chain commands
        config_data.append("    iptables -A nixos-fw-output -p udp --sport 67:68 --dport 67:68 -j nixos-fw-accept")
        if 0 in self.parentApp.icmpEchoVar:
            config_data.append("    iptables -A nixos-fw-output -p icmp ! --icmp-type echo-reply -j nixos-fw-accept")
        for x in portsAllowedOutTcp:
            config_data.append(f"    iptables -A nixos-fw-output -p tcp --dport {x} -m state --state NEW,ESTABLISHED -j nixos-fw-accept")
        for x in portsAllowedOutUdp:
            config_data.append(f"    iptables -A nixos-fw-output -p udp --dport {x} -m state --state NEW,ESTABLISHED -j nixos-fw-accept")
        config_data.extend([
            "    iptables -A nixos-fw-output -m state --state RELATED,ESTABLISHED -j nixos-fw-accept",
            "    iptables -A nixos-fw-output -j nixos-fw-log-refuse",
            "  '';",
            "  extraStopCommands = ''",
            "    iptables -F",
            "    iptables -X",
            "  ''; #removes the previous commands on shut down",
            '};',
            '',
            '  # Copy the NixOS configuration file and link it from the resulting system',
            '  # (/run/current-system/configuration.nix). This is useful in case you',
            '  # accidentally delete configuration.nix.',
            '  # system.copySystemConfiguration = true;',
            '',
            '  # This option defines the first version of NixOS you have installed on this particular machine,',
            '  # and is used to maintain compatibility with application data (e.g. databases) created on older NixOS versions.',
            '  #',
            '  # Most users should NEVER change this value after the initial install, for any reason,',
            "  # even if you've upgraded your system to a new NixOS release.",
            '  #',
            '  # This value does NOT affect the Nixpkgs version your packages and OS are pulled from,',
            '  # so changing it will NOT upgrade your system - see https://nixos.org/manual/nixos/stable/#sec-upgrading for how',
            '  # to actually do that.',
            '  #',
            '  # This value being lower than the current NixOS release does NOT mean your system is',
            '  # out of date, out of support, or vulnerable.',
            '  #',
            '  # Do NOT change this value unless you have manually inspected all the changes it would make to your configuration,',
            '  # and migrated your data accordingly.',
            '  #',
            '  # For more information, see `man configuration.nix` or https://nixos.org/manual/nixos/stable/options#opt-system.stateVersion .',
            '  system.stateVersion = "24.11"; # Did you read the comment?',
            '}'
            ])
        file = open(f"{self.fileName.value}", 'w')
        for line in config_data:
                file.write(line + '\n')
        file.close()
        self.parentApp.switchForm(None)
    

if __name__ == '__main__':
    npyscreen.wrapper(MyTestApp().run())