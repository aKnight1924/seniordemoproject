# Edit this configuration file to define what should be installed on
# your system. Help is available in the configuration.nix(5) man page, on
# https://search.nixos.org/options and in the NixOS manual (`nixos-help`).

{ config, lib, pkgs, ... }:

{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
    ];

  # Use the systemd-boot EFI boot loader.
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  networking.hostName = "nix-firewall"; # Define your hostname.
  # Pick only one of the below networking options.
  # networking.wireless.enable = true;  # Enables wireless support via wpa_supplicant.
  networking.networkmanager.enable = true;  # Easiest to use and most distros use this by default.

  # Set your time zone.
  time.timeZone = "US/Chicago";

  # Configure network proxy if necessary
  # networking.proxy.default = "http://user:password@proxy:port/";
  # networking.proxy.noProxy = "127.0.0.1,localhost,internal.domain";
  
  services.envfs.enable = false;
  services.xserver.enable = true;
  services.displayManager.ssdm.wayland.enable = true;
  services.desktopManager.plasma6.enable = true;

  # Configure keymap in X11
  # services.xserver.xkb.layout = "us";
  # services.xserver.xkb.options = "eurosign:e,caps:escape";

  # Enable CUPS to print documents.
  # services.printing.enable = true;

  # Enable sound.
  # hardware.pulseaudio.enable = true;
  # OR
  services.pipewire = {
    enable = true;
    pulse.enable = true;
  };

  # Enable touchpad support (enabled default in most desktopManager).
  services.libinput.enable = true;

  # Define a user account. Don't forget to set a password with ‘passwd’.
  users.users.admin = {
    isNormalUser = true;
    description = "admin"; # **parameter for user name
    extraGroups = [ "wheel" ]; # Enable ‘sudo’ for the user.
    shell = pkgs.bash;
    packages = with pkgs; [
    ];
    home = "/home/admin";
  };

  boot.loader.grub.device = "/dev/nvme0n1";  

  nixpkgs.config.allowUnfree = true;

  # List packages installed in system profile. To search, run:
  # $ nix search wget
  environment.systemPackages = with pkgs; [
    wget
    git
    python3
    nixos-generators
    devenv
  ]; # **parameter for including additional packages

  nix.settings.trusted-users = [
    "root" 
    "admin"
    ];

  services.openssh = {
  enable = true;  # **parameter for enable ssh
  ports = [ 22 ]; # **parameter for ssh port
  settings = {
    PasswordAuthentication = true;
    AllowUsers = null; # Allows all users by default. Can be [ "user1" "user2" ] # **parameter for allowed users
    UseDns = true;
    X11Forwarding = true;
    PermitRootLogin = "prohibit-password"; # "yes", "without-password", "prohibit-password", "forced-commands-only", "no" # **parameter for permit root log in
  };
};

networking.firewall = {
  enable = true;
  allowPing = false; # ** parameter to configure whether or not replying to ICMP requests is allowed
  allowedTCPPorts = [ 22 ]; # **parameter for allowed TCP ports
  #allowedUDPPorts = []; # **parameter for allowed UDP ports
  #extraCommands = []; # ** parameter for chain/state specific firewall rules or NAT
  #extraStopCommands = []; # removes the previous commands on shut down
};
  # Copy the NixOS configuration file and link it from the resulting system
  # (/run/current-system/configuration.nix). This is useful in case you
  # accidentally delete configuration.nix.
  # systemgit add.copySystemConfiguration = true;

  # This option defines the first version of NixOS you have installed on this particular machine,
  # and is used to maintain compatibility with application data (e.g. databases) created on older NixOS versions.
  #
  # Most users should NEVER change this value after the initial install, for any reason,
  # even if you've upgraded your system to a new NixOS release.
  #
  # This value does NOT affect the Nixpkgs version your packages and OS are pulled from,
  # so changing it will NOT upgrade your system - see https://nixos.org/manual/nixos/stable/#sec-upgrading for how
  # to actually do that.
  #
  # This value being lower than the current NixOS release does NOT mean your system is
  # out of date, out of support, or vulnerable.
  #
  # Do NOT change this value unless you have manually inspected all the changes it would make to your configuration,
  # and migrated your data accordingly.
  #
  # For more information, see `man configuration.nix` or https://nixos.org/manual/nixos/stable/options#opt-system.stateVersion .
  system.stateVersion = "24.11"; # Did you read the comment?
}
