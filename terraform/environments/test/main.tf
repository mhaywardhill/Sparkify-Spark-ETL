provider "aws" {
	region = "us-west-2"
}

module "VPC" {
	source	= "../../modules/VPC"
	vpc-cidr	= var.vpc-cidr
	pubsubcidr	= var.pubsubcidr
}

module "securitygroups" {
	source	= "../../modules/securitygroups"
	vpc_id	= module.VPC.vpc_id
	depends_on 	= [module.VPC]
}

module "EMR" {
	source		= "../../modules/EMR"
	subnet_id		= module.VPC.subnet_id
	master_sg_id	= module.securitygroups.master_sg_id
	worker_sg_id	= module.securitygroups.worker_sg_id
	key_name		= var.key_name
	depends_on 		= [module.securitygroups]
					
}

