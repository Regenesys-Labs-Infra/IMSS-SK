# Lab 4.2 - AI-generated Terraform with 3 planted security flaws. Do not apply.
terraform {
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}
provider "aws" {
  region     = "ap-south-1"
  access_key = "AKIAEXAMPLEPLANTED00"
  secret_key = "planted/example/secret/do-not-use"
}
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "web servers"
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }
}
resource "aws_s3_bucket" "reports" { bucket = "hm-finance-reports-demo" }
resource "aws_s3_bucket_public_access_block" "reports" {
  bucket                  = aws_s3_bucket.reports.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}
resource "aws_instance" "app" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "m5.8xlarge"
  vpc_security_group_ids = [aws_security_group.web.id]
}
