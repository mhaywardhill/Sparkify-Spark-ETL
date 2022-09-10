resource "aws_emr_cluster" "cluster" {
	name          = "mysparkcluster"
  	release_label = "emr-5.28.0"
  	applications  = ["Spark", "Zeppelin"]

  	ec2_attributes {
  		subnet_id					= var.subnet_id
		emr_managed_master_security_group 	= var.master_sg_id
    		emr_managed_slave_security_group  	= var.worker_sg_id
		key_name					= var.key_name
		instance_profile 				= "EMR_EC2_DefaultRole"
  	}

  	master_instance_group {
    		instance_type = "m5.xlarge"
  	}

  	core_instance_group {
    		instance_type  = "m5.xlarge"
    		instance_count = 2
  	}
	
	service_role = "EMR_DefaultRole"
}