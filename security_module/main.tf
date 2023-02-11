data "aws_iam_policy_document" "lambda-assume-role-policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lexGptLambdaAccess" {
  statement {
    actions   = ["logs:*","s3:*","dynamodb:*","cloudwatch:*","sns:*","lambda:*","connect:*","secretsmanager:*","ds:*"]
    effect   = "Allow"
    resources = ["*"]
  }
}

resource "aws_iam_role" "lexgptlambda" {
    name               = "lexgptlambda"
    assume_role_policy = data.aws_iam_policy_document.lambda-assume-role-policy.json
    inline_policy {
        name   = "policy-86753011"
        policy = data.aws_iam_policy_document.lexGptLambdaAccess.json
    }

}