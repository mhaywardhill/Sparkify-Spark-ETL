resource "aws_security_group" "master-sg" {
 name 	= "ssparkify-ElasticMapReduce-master"
 vpc_id    = var.vpc_id

 egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

resource "aws_security_group" "worker-sg" {
 name 	= "sparkify-ElasticMapReduce-worker"
 vpc_id    = var.vpc_id
 
 egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}