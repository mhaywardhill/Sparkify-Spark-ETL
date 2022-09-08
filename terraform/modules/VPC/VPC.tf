resource "aws_vpc" "my-vpc" {
	cidr_block = var.vpc-cidr
}

resource "aws_internet_gateway" "IGW" {
	vpc_id =  aws_vpc.my-vpc.id
}


resource "aws_subnet" "mypublicsubnet" {  
   vpc_id =  aws_vpc.my-vpc.id
   cidr_block = var.pubsubcidr
 }


# Creating RT for Public Subnet
resource "aws_route_table" "publRT" {
	vpc_id =  aws_vpc.my-vpc.id
     	route {
    		cidr_block = "0.0.0.0/0"
    		gateway_id = aws_internet_gateway.IGW.id
     	}
}

#Associating the Public RT with the Public Subnets
resource "aws_route_table_association" "PubRTAss" {
	subnet_id = aws_subnet.mypublicsubnet.id
	route_table_id = aws_route_table.publRT.id
}
