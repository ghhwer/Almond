# Almond
This is a full hadoop docker enviroment for data platform development.

it is inspired by https://github.com/big-data-europe/docker-spark. The main difference is that the base images, (java and python base images) are built dependent of each other, thus, making version control easier.

# How to run
Build instructions are provided in a Makefile, once `make build` was compleated, run it by using `docker-compse up`.

This is a helper project.
