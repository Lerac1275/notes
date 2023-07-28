This markdown files details how to set up Pyenv on a mac with virtualenv enabled. 

Done via `brew`.

1: Download and install Homebrew
By installing Homebrew you should have installed Xcode CLT
in case you want to install xocde separately, you can run the very first line
```
# xcode-select --install /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# update Homebrew and add formulae
brew update
# Check for broken dependencies and/or outdated packages
brew doctor
brew cleanup

# Setup Pyenv 
brew install pyenv
brew install pyenv-virtualenv

# after installing, update .zprofile accordingly
cd
echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
echo 'eval "$(pyenv init -)"' >> ~/.zprofile
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.zprofile

# (Optional) update your locale settings
#export LANG="en_US.UTF-8"
#export LC_ALL="en_US.UTF-8"
#export LC_CTYPE="en_US.UTF-8"
# If you see this error: Failing command: ['/home/float/test/t/bin/python3.6', '-Im', 'ensurepip', '--upgrade', '--default-pip']. This means that your locale has not been set up correctly. https://github.com/pypa/virtualenv/issues/1059

# set up the required python environments
# we use 3.9.11
pyenv install 3.9.11
# create a virtual environment 
pyenv virtualenv 3.9.11 python_3.9.11_env
```