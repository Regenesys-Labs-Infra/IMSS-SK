# Firewall / security group change requested by APP-PORTAL-L2 for vendor support access
resource "aws_security_group_rule" "vendor_ssh" {
  type              = "ingress"
  from_port         = 22
  to_port           = 22
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = "sg-0portalapp000001"
  description       = "Vendor SSH access to portal app server"
}
