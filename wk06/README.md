STEPS TO CREATE NEW IMAGE AND LAUNCH JUPYTER NOTEBOOK
======================================================

Create your sshkey
	`ssh-keygen -t rsa`
Upload your sshkey to ibmcloud
Make sure you have removed knownhosts, since it will fail because of new key and old cache
Find your key id using `ibmcloud sl security sshkey-list`
Create new VSI using below commands
	To create a v100
	==================
	`ibmcloud sl vs create --datacenter=lon04 --hostname=v100a --domain=vebs1.com --image=2263543 --billing=hourly  --network 1000 --key=1834866 --flavor AC2_8X60X100 --san`

	To create a P100
	==================
	`ibmcloud sl vs create --datacenter=lon06 --hostname=p100a --domain=veb2.com --image=2263543 --billing=hourly  --network 1000 --key=1834866 --flavor AC1_8X60X100 --san`


Find public IP address of new VSI (p100 or v100 through IBM online console)
Connect to new VSI using
  `ssh -i ~/.ssh/id_rsa <public_ip_address> -l root`
  `ssh -i ~/.ssh/id_rsa 158.176.106.149 -l root`

Once connected -- follow instructions to load docker and start a JupyterNotebook
Once docker is done:
  `docker ps --> get container id`
  `docker logs <container_id>`
Get the URL for JupyterNotebook  (e.g. `http://(93a40d9fa8d6 or 127.0.0.1):8888/?token=6c0879c7fdb0e28d9797fbb7a31f2d20de590ad882251d96`)
  Replace the IP address with the public IP of the VSI (e.g. 158.176.106.149 here in P100)

Final Jupyeter Notebook URL becomes something like: 
	`http://158.176.106.149:8888/?token=6c0879c7fdb0e28d9797fbb7a31f2d20de590ad882251d96`
