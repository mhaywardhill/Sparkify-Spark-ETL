resource "aws_security_group" "master-sg" {
 name 			= "sparkify-ElasticMapReduce-master"

 revoke_rules_on_delete = true
 vpc_id    			= var.vpc_id

 egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

 ingress {
    protocol = "tcp"
    from_port = 0
    to_port = 22
    cidr_blocks = ["${var.my_public_ip}/32"]
  }
}

resource "aws_security_group" "worker-sg" {
 name 			= "sparkify-ElasticMapReduce-worker"
 
 vpc_id    			= var.vpc_id
 revoke_rules_on_delete = true

 egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}