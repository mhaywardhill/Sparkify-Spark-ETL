
# Project: Spark and Data Lakes 

**Project Description**: A music streaming startup, Sparkify, has grown its user base and song database and wants to move its data from a data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, and a directory with JSON metadata on the songs. This ETL pipeline extracts their data from S3, processes them using Apache Spark, and writes the data back into S3 as a set of  parquet files for future use with analytical queries.

## Project Organization

```
    ├── README.md                               <- README file
    │
    ├── terraform                               <- Terraform config files to deploy EMR Apache Spark cluster
    │   ├── environments        
    │   │   └── test                            <- test environment folder, holds the Terraform state
    │   └── modules            
    │       ├── EMR                             <- Terraform config file to add EMR cluster 
    │       ├── securitygroups                  <- Terraform config file to add AWS security groups
    │       └── VPC                             <- Terraform config file to add networking components in AWS
    │
    ├── Read parquet files from AWS S3.ipynb    <- Jupyter notebook to read the parquet files
    │
    └── etl.py                                  <- script to process all JSON data in Spark and write into parquet files on S3
```

## Getting started

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

export TF_VAR_key_name="<key name>"

export TF_VAR_my_public_ip=$(curl -s http://whatismyip.akamai.com/)
```

Run the Terraform commands to build the AWS infrastructure:

```
./terraform init

./terraform plan

./terraform apply
```

### Topology of the AWS infrastructure

![VPC](/images/VPCDesign.png)