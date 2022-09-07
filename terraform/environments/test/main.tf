provider "aws" {
	region = "us-west-2"
}


module "s3" {
	source	= "../../modules/s3"
	bucket_name	= var.bucket_name
}

module "VPC" {
	source	= "../../modules/VPC"
	vpc-cidr	= var.vpc-cidr
	prisubcidr 	= var.prisubcidr
}