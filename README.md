# Temperature Monitor

This a hobby project utilizing Raspberry Pi based temperature sensors around my home loud services to ingest and display temperature data from different locations around my house

# Architecture

# Repo Structure

## cloud

- Contains all cloud related code

### dashbord

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
