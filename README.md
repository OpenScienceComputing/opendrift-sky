# opendrift-sky
SkyPilot files for running OpenDrift
#### install skypilot 
```
mkdir sky
cd sky
mamba create -y -n sky python=3.10
mamba activate sky
pip install "skypilot-nightly[aws]"
#### use existing Nebari kubernetes deployment
pip install kubernetes
pip install ray
sudo apt install socat
export AWS_PROFILE=esiplab2   # credentials for ESIP Nebari (so we can access k8s)
sky check # should come back with `Kubernetes:enabled`
#### create environment
```
sky launch -c opendrift-rsignell opendrift_sky.yaml
```
#### run an Opendrift simulation
make sure to export OSN_SECRET_ACCESS_KEY and OSN_ACCESS_KEY_ID, setting the to the OSN S3 keys so Sky can write to OSN object storage
```
sky exec opendrift-rsignell --env AWS_SECRET_ACCESS_KEY={OSN_SECRET_ACCESS_KEY} --env AWS_ACCESS_KEY_ID={OSN_ACCESS_KEY_ID} opendrift_sky.yaml
```
