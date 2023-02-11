terraform {
  required_version = ">= 0.14"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = ">= 4.9.0"
    }

    tls = {
      source = "hashicorp/tls"
      version = "3.4.0"
    }
  }

  

  backend "s3" {
    bucket = "<state_bucket>"
    key    = "lambdastate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"
}

module "security_module" {
    source = "./security_module"
}


module "gpt_api_lambda" {
    source = "./lambda_code"
    role_arn=module.security_module.lambda_role
}