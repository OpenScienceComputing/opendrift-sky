# opendrift-sky
SkyPilot files for running OpenDrift
#### Install skypilot 
```
mkdir sky
cd sky
conda create -y -n sky python=3.10
conda activate sky
pip install "skypilot-nightly[aws]"
```
#### Create sky cluster
on existing Nebari kubernetes deployment
```
pip install kubernetes
pip install ray
sudo apt install socat
export AWS_PROFILE=esiplab2   # credentials for ESIP Nebari (so we can access k8s)
sky check # should come back with `Kubernetes:enabled`
```
#### Create conda environment on Cluster
```
sky launch -c opendrift-rsignell opendrift_sky.yaml
```
#### Run an Opendrift simulation
make sure to export OSN_SECRET_ACCESS_KEY and OSN_ACCESS_KEY_ID, setting the to the OSN S3 keys so Sky can write to OSN object storage
```
sky exec opendrift-rsignell --env AWS_SECRET_ACCESS_KEY={OSN_SECRET_ACCESS_KEY} --env AWS_ACCESS_KEY_ID={OSN_ACCESS_KEY_ID} opendrift_sky.yaml
```
The resulting NetCDF files show up on OSN here:
```
aws s3 ls s3://rsignellbucket2/rsignell/CNAPS/output/ --no-sign-request --endpoint-url=https://renc.osn.xsede.org
```
