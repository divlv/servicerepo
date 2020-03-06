# In case of strage errors, enable GUI and see the live console log:
#Vagrant.configure("1") do |config|
#  config.vm.boot_mode = :gui
#end

Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"

  # Shared folder mounting error prevents execution of provision section (switch it off)
  config.vm.synced_folder '.', '/vagrant', disabled: true

  # Check "Cable connected" setting in VirtualBox (without it Vagrant could stuck at boot phase)
  config.vm.provider :virtualbox do |vm|
    vm.customize [
      "modifyvm", :id,
      "--cableconnected1", "on",
      "--memory", "4096"
    ]
  end

  # No shared folder is mounted, that's why - running provision commands here:
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get -y update
    sudo apt-get -y install docker.io
    sudo apt-get -y install docker-compose
    sudo service docker restart
    sudo systemctl enable docker
    sudo git clone https://github.com/divlv/servicerepo
  SHELL

  # AUTOEXEC.BAT :-)
  config.vm.provision "shell", run: 'always', inline: <<-SHELL
    cd servicerepo
    sudo docker-compose up -d
  SHELL

  config.vm.network :forwarded_port, guest: 18000, host: 18000
  config.vm.network :forwarded_port, guest: 5432, host: 15432
end