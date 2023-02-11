resource "aws_lambda_function" "gpt_api_lambda" {
  function_name    = "gpt_api_lambda"
  filename         = "app.zip"
  handler          = "app.lambda_handler"
  source_code_hash = filebase64sha256("app.zip")
  role             = "${var.role_arn}"
  runtime          = "python3.9"
  memory_size      = 128
  timeout          = 30
  environment {
    variables = {
      GPT_API_KEY = "${var.gpt_key}"
    }
  }
}