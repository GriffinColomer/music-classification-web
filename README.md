# Developing the webapp

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## How to run

After cloning repository make sure you have docker installed. You should run the environment in the docker container.

To start the app use `docker-compose up --build --watch` This will run the webapp in a controled and repeatable environment. You will be able to edit any of the files just as when reguarly developing react at [here](http://localhost:3000/)

## Installing packages
If you need to install any packages you will need to rebuild the docker container and make sure you are in the correct directory. Before installing any make sure to change `cd frontend`. After you can install your package with `npm install <package name>`. Then rerun the command to build the docker container.

