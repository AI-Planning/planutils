Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 3
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update && apt-get install --no-install-recommends -y \
        bison \
        build-essential \
        ca-certificates \
        cmake \
        cryptsetup \
        curl \
        flex \
        g++-multilib \
        gcc-multilib \
        git \
        libgpgme11-dev \
        libseccomp-dev \
        libssl-dev \
        locales \
        pkg-config \
        python3 \
        python3-dev \
        python3-pip \
        python3-venv \
        scons \
        software-properties-common \
        squashfs-tools \
        tzdata \
        unzip \
        uuid-dev \
        vim \
        wget

    pip3 install --upgrade pip

    # install go to build singularity
    export VERSION=1.13 OS=linux ARCH=amd64
    wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz
    tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz
    rm go$VERSION.$OS-$ARCH.tar.gz
    export GOPATH="${HOME}/go"
    export PATH="/usr/local/go/bin:${PATH}:${GOPATH}/bin"

    # get a recent version of singularity
    export VERSION=3.5.0
    wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-${VERSION}.tar.gz && \
    tar -xzf singularity-${VERSION}.tar.gz
    cd singularity
    ./mconfig
    make -C ./builddir
    make -C ./builddir install
    cd ..
    rm -rf singularity
    rm singularity-${VERSION}.tar.gz
    echo '. /usr/local/etc/bash_completion.d/singularity' >> /home/vagrant/.bashrc

    # install & setup the planutils for the vagrant user
    runuser -l vagrant -c "pip3 install --user planutils --trusted-host pypi.org --trusted-host files.pythonhosted.org"
    runuser -l vagrant -c "planutils --setup"
SHELL

  config.ssh.forward_x11 = true
  config.ssh.forward_agent = true
end
