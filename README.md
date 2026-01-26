# Weather Monitor
This a hobby project utilizing Raspberry Pi based temperature sensors around my home to capture weather data and commit it to an AWS SNS topic for storage in DynamoDB, alerting via SMS/SES and display in an web dashboard hosted in AWS Amplify.

# Architecture
![Architecture](/docs/architecture.png)

# Repo Structure

## cloud
- Contains all cloud related code

### dashboard
- Contains a GUI application for viewing device status and historical temperature data
- Expect this to be a Flutter or Angular web application

### database
- Will contain any schema related files (migrations etc)

### lambdas
- Contains the lambdas deployed to AWS that are responsbile for ingesting temperature data

## docs
- Contains project documentation

## tests
- Contains unit tests for the varous compnents

