# Weather Monitor

A hobby project using Raspberry Pi-based temperature sensors placed around my home to capture weather data. Captured data is published to an AWS SNS topic, which drives storage in DynamoDB, SMS/email alerting via SES, and a live web dashboard hosted on AWS Amplify.

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

### iac (Infrastructure as Code)

- Will contain files to spin up cloud infrastructure from code

### lambdas

- Contains the lambdas deployed to AWS that are responsbile for ingesting temperature data

## docs

- Contains project documentation

## tests

- Contains unit tests for the varous compnents
