variable "env" {
  type = string
  description = "Environment name"
}
variable "vpc_id" {
  type        = string
  description = "Id of the VPC"
}

variable "db_password" {
  type        = string
  description = "Postgres password"
  sensitive = true
}

variable "subnet_ids" {
  type        = list(any)
  description = "List of subnet ids for Postgres"
}

variable "tags" {
  type        = map(string)
  description = "List of tags attached to resources"
}
