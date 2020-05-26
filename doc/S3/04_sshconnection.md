
# OT-2 ssh connection setup guide

## Steps

1) Generate a ssh key:
```ssh-keygen```

2) Add your private key to your local IDs:
```ssh-add```

3) Now connect to your robot using the jupyter notebook, open a terminal and add your puclic key to the end of the file `/root/.ssh/authorized_keys`

4) Connect from your local machine as root:
```ssh root@yourrobothostname```

Now you also have `scp` enabled! Use it to copy and sync files between robots.
