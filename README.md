
# Project: Spark and Data Lakes 

**Project Description**: A music streaming startup, Sparkify, has grown its user base and song database even more and wants to move its data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, and a directory with JSON metadata on the songs in their app.

In this project, we will build an ETL pipeline that extracts their data from the data lake hosted on S3, processes them using Apache Spark, which is deployed on an EMR cluster, and writes the data back into S3 as a set of dimensional tables in parquet file format.

From these tables, we can find insights into what songs their users are listening to.

## Project Organization

```
    ├── README.md                               <- README file
    │
    ├── images                                  <- topology diagram and screenshots
    │
    ├── terraform                               <- Terraform config files to deploy the EMR cluster
    │   ├── environments        
    │   │   └── test                            <- test environment folder, holds the Terraform state
    │   └── modules            
    │       ├── EMR                             <- Terraform config file to add EMR cluster 
    │       ├── securitygroups                  <- Terraform config file to add AWS security groups
    │       └── VPC                             <- Terraform config file to add networking components in AWS
    │
    ├── notebooks                               <- Jupyter notebooks for reading the parquet files and troubleshooting the etl 
    │
    └── etl.py                                  <- script to process all JSON data in Spark and write into parquet files on S3
```

# Getting started

## Prerequisites

* ### S3 Bucket

We require an S3 bucket to hold the output from the ETL. The S3 bucket is created separately from the Terraform configuration so we can tear down the EMR cluster without deleting the parquet files.

```
aws s3api create-bucket --bucket "<S3 bucket name>" --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2"
```

* ### EC2 Key Pair

An EC2 Key pair is specified in the Terraform configuration for the EMR cluster and is used to connect to the master node using the SSH protocol. 

* ### Default roles

The default roles EMR_EC2_DefaultRole and EMR_DefaultRole are required for the EMR cluster.

```
aws emr create-default-roles
```

##  Setup

Clone the repository locally:
```
git clone https://github.com/mhaywardhill/Sparkify-Spark-ETL.git
```

and go into the repository and navigate to the terraform environment folder:

```
cd Sparkify-Spark-ETL/terraform/environments/test/
```

We need to set the following environment variables used by Terraform:

```
export TF_VAR_bucket_name="<S3 bucket name>"

export TF_VAR_key_name="<EC2 key pair name (without the file extension)>"

export TF_VAR_my_public_ip=$(curl -s http://whatismyip.akamai.com/)
```

Run the Terraform init, plan, and apply commands to deploy the resources to build the AWS infrastructure:

```
./terraform init

./terraform plan

./terraform apply
```

### Topology of the AWS infrastructure

![VPC](/images/VPCDesign.png)


# How to run the ETL

Receive the IP address of the master node from the Terraform output:

```
export master_ip_addr=$(./terraform output -raw emr_cluster_dns)
```

Update the S3 bucket name in the ETL script:

```
sed -i "s/<bucket name>/$TF_VAR_bucket_name/g" ../../../etl.py
```

Copy the ETL script to the master node:

```
scp -i ~/.ssh/$TF_VAR_key_name.pem ../../../etl.py hadoop@$master_ip_addr:/home/hadoop
```

SSH to the master node:

```
ssh -i ~/.ssh/$TF_VAR_key_name.pem hadoop@$master_ip_addr
```

![emrmasternode](/images/EMRMasterNode.png)

Run the ETL script from the master node:

```
/usr/bin/spark-submit --master yarn etl.py 
```

## Clean Up Resources

Tear down the resources managed by Terraform, managed by the state file in the environment folder.

```
./terraform destroy
```

