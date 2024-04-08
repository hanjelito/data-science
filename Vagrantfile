Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "juan-gon"

  config.vm.provider "virtualbox" do |v|
      v.memory    = "4096"
      v.cpus      = "2"
      # v.customize ["modifyvm", :id, "--basefolder", "/sgoinfre/students/juan-gon/vm-ds"]

  end

  config.vm.synced_folder "./projects", "/vagrant/projects"
  config.vm.synced_folder "./scripts", "/vagrant/scripts"

  config.vm.network "forwarded_port", guest: 5432, host: 5433
  # config.vm.network "forwarded_port", guest: 5432, host: 5432


  config.vm.provision "shell", privileged: false, path: "scripts/python_setup.sh"
  config.vm.provision "shell", privileged: false, path: "scripts/postgres_setup.sh"

  config.vm.define "python_env" do |python_env|
    python_env.vm.network "private_network", type: "dhcp"
  end
end


# ps aux | grep 'VirtualBox'