# EC2

## To connect:
- First provision an instance, make sure to select one with the free usage tier. 
- **Must** provision one **with** a keypair, either use one you already have saved somewhere or create a new one and save the private key file (`.pem` / `.cer`) somewhere on your local machine. You will need this to ssh in later on.
- Once provisioned and running, select the instance & go to the tab for ssh connection.
- Copy the command to ssh into the instance from the terminal. Replace the keypair cert path with the path to your saved private key file.

## To setup Python:
- For python installation you can follow [this guide](https://towardsthecloud.com/amazon-ec2-install-python-pip). Note that you can specify the version you would like to install (e.g. `sudo yum install python3.11 -y` will install python3.11)
    - Call it with `python3.11`
- If pip wasn't installed with the previous command you can check out [this thread](https://stackoverflow.com/a/55158505/13479945). 
    -  Look for the pip version available with `yum search pip`
    -  Find one that suits the version you need then install. e.g. `sudo yum install python3.11-pip`
    -  Invoke it with the exact python version behind the pip call; e.g. `pip3.11 list`  `pip3.11 install -r requirements.txt`