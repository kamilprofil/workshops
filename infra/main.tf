resource "aws_security_group" "organizer-postgres" {
  name   = "organizer"
  vpc_id = var.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, { Name = "${var.env}" })
}


resource "aws_db_subnet_group" "organizer" {
  name       = "organizer"
  subnet_ids = var.subnet_ids

  tags = merge(var.tags, { Name = "${var.env}" })
}


resource "aws_db_parameter_group" "organizer" {
  name   = "organizer"
  family = "postgres11"

  parameter {
    name  = "log_connections"
    value = "1"
  }
 }

resource "aws_db_instance" "organizer" {
  identifier             = "organizer"
  instance_class         = "db.t2.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "11"
  username               = var.db_user
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.organizer.name
  vpc_security_group_ids = [aws_security_group.organizer-postgres.id]
  parameter_group_name   = aws_db_parameter_group.organizer.name
  publicly_accessible    = true
  skip_final_snapshot    = true
}
