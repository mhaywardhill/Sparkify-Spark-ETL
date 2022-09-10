variable vpc-cidr {
	default = "172.168.0.0/16"
}

variable pubsubcidr {
	default = "172.168.0.0/24"
}

variable key_name {
	sensitive   = true
}

variable my_public_ip {
	sensitive   = true
}
