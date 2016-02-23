# slack-meme
Post memes to any of your Slack channels with a slash command.

## Usage

### Built-in Templates

`/meme success; we have; a meme bot;`

<img src="http://i.imgur.com/ns098uP.png">

`/meme templates` shows you the available built-in templates:

<img src="http://i.imgur.com/J3vvqFm.png">

### Custom Templates
Use your own image by passing its URL as the template:

`/meme https://pbs.twimg.com/profile_images/657199367556866048/EBEIl2ol.jpg; Hello; It's me`

<img src="http://i.imgur.com/QrfrZlZ.png">

### Preview

Hone your meme skills privately until you get it just right:

`/meme preview awesome-awkward; makes a meme; doesn't show anyone;`

<img src="http://i.imgur.com/Wz5UFXu.png">

## Setup

### Slash Command

Follow these steps to configure the slash command in Slack:

  1. Navigate to https://<your-team-domain>.slack.com/apps/manage/custom-integrations
  2. Select "Slash Commands" and click on "Add Configuration".
  3. Enter a name for your command (eg. `/meme`) and click "Add Slash Command Integration".
  4. Copy the token string from the integration settings and use it in the next section.
  5. You can configure additional settings here. We also edited the following settings:
    - Customize Name: we used "doge".
    - Customize Icon
    - Autocomplete Help text: We selected "Show this command in the autocomplete list" with "Create a meme" as the description and "\[preview\] meme-name; top text; bottom text;" as the useage text.
  5. After you complete the setup, enter the provided API endpoint URL in the URL field.

### KMS Setup
  1. Create a KMS key - http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html.
    - `aws kms create-key --description 'lambda secrets'`
    - `aws kms create-alias --alias-name alias/lambda-secrets --target-key-id <key id>`
  2. Encrypt the token using the AWS CLI= `aws kms encrypt --key-id alias/lambda-secrets --plaintext "<COMMAND_TOKEN>"`.
  3. Copy the base-64 encoded, encrypted key (CiphertextBlob) to the `ENCRYPTED_EXPECTED_TOKEN` variable.

### Deploying to lambda
  1. Use `pip install -r requirements.txt` to install the python dependencies.
  2. Run `create_package.sh` to create a deployment zip.
  3. Go to https://eu-west-1.console.aws.amazon.com/lambda/home?region=eu-west-1#/create?step=2 to create a new Lambda Function
  4. Fill in the name and description and select the "Python 2.7" runtime.
  5. Select "Upload a .ZIP file" and upload "slack-meme.zip"
  6. Leave the Handler on 'lambda_function.lambda_handler' and select 'Create new role > *basic execution role' as Role.
  7. On the new page select 'Create a new IAM role' as 'IAM Role'. and 'slack_meme' as Role Name. Use the following policy (Show Policy Document > Edit). You can get the ARN with `aws kms describe-key --key-id alias/lambda-secrets`
  ```
       {
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
              ],
              "Resource": "arn:aws:logs:*:*:*"
            },
            {
                     "Effect": "Allow",
             "Action": [
               "kms:Decrypt"
             ],
             "Resource": [
               "<your KMS key ARN>"
             ]
           }
         ]
       }
    ```
  8. Click on 'Next' and 'Create function' to create the lambda function.  


### API Gateway Setup

  1. Select the 'API endpoints' in the AWS Lambda configuration and Add an API endpoint. Use the following settings:
    - API endpoint type: API Gateway
    - API name: LambdaServices
    - Resource name: /slack-meme
    - Method: POST
    - Deployment stage: prod
    - Security: Open
  2. Update the URL for your Slack slash command with the API endpoint URL.
  3. Open the API Gateway console and go to the POST resource of /slack-meme
  4. Open 'Integration Request' settings. And add a mapping template:
    - Content-type: application/x-www-form-urlencoded
    - Mapping Template: `{ "body": $input.json("$") }`
  5. Click on 'Deploy api' and update the 'prod' stage.
  

## Update Your Deployment

To update the deployed version, edit the code in src, run `create_package.sh` and upload `slack-meme.zip` to the existing lambda function.

## Credits

- This is based on code written by [Nicole White](https://github.com/nicolewhite). Awesome work, Nicole!
- The KMS decription is based on an AWS lambda blueprint. Thank you, AWS!
- This uses [memegen](https://github.com/jacebrowning/memegen). Thanks memegen!
- This also uses [memeifier](http://memeifier.com). Thanks memeifier!
