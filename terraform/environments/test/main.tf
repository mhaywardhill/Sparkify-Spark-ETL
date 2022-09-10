provider "aws" {
	region = "us-west-2"
}

module "VPC" {
	source	= "../../modules/VPC"
	vpc-cidr	= var.vpc-cidr
	pubsubcidr	= var.pubsubcidr
}

module "EMR" {
	source	= "../../modules/EMR"
	subnet_id	= module.VPC.subnet_id
	key_name	= var.key_name
	depends_on = [module.VPC]
}