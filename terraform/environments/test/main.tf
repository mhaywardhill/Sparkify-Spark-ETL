provider "aws" {
	region = "us-west-2"
}

module "VPC" {
	source	= "../../modules/VPC"
	vpc-cidr	= var.vpc-cidr
	pubsubcidr	= var.pubsubcidr
}