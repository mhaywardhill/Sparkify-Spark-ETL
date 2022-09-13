# IP Address range assigned to the VPC, 216 assignable hosts
variable vpc-cidr {
	default = "10.16.0.0/24"
}

# IP Address range assigned to the Subnet, 30 assignable hosts
variable pubsubcidr {
	default = "10.16.0.0/27"
}

# The name of the EC2 Key (with the file extension)
variable key_name {
	sensitive   = true
}

# Used to add inbound rule to the EMR master node security group
variable my_public_ip {
	sensitive   = true
}
