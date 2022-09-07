resource "aws_vpc" "my-vpc" {
	cidr_block = var.vpc-cidr
}


resource "aws_subnet" "myprivatesubnet" {  
   vpc_id =  aws_vpc.my-vpc.id
   cidr_block = var.prisubcidr
}

