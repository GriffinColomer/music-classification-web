# Running the Web App
1. Clone the repositoty
2. Download the model [here](https://drive.google.com/file/d/1DreyPFynxUjo4_RnMi1YBH-45776my4K/view?usp=sharing). Move the model into `backend/MachineLearning`
3. Start the web app with `docker-compose up`
4. Visit the site [here](http://localhost:3000)

# Developing the webapp

## How to run

After cloning repository make sure you have docker installed. You should run the environment in the docker container. Also download the file [here](https://drive.google.com/file/d/1DreyPFynxUjo4_RnMi1YBH-45776my4K/view?usp=sharing) and put it into `backend/MachineLearning`

To start the app use `docker-compose up --build --watch` This will run the webapp in a controled and repeatable environment. You will be able to edit any of the files just as when reguarly developing react [here](http://localhost:3000/). Or if you are working on the backend I built it using flask, the port it's using is 5000. Just edit whatever files you need in there. It will automatically be updated as well.

## Installing npm packages
If you need to install any packages you will need to rebuild the docker container and make sure you are in the correct directory. Before installing any make sure to change `cd frontend`. After you can install your package with `npm install <package name>`. Then rerun the command to build the docker container.

## Installing python packages
If you need to use any python packages add them to the requirements.txt and rebuild the docker containers. using the original command. It will look like they work fine in your environment but the docker contaainer has to install it seperately so be aware.

## API
Send a post request to `http://localhost:5000/api/sendmp3` it needs to be a `multipart/form-data`. It needs a file and user below is and example of a request.
#### Example Request
```const data = new FormData();
data.append("file", "<path to mp3 file>");

const xhr = new XMLHttpRequest();
xhr.withCredentials = true;

xhr.addEventListener("readystatechange", function () {
  if (this.readyState === this.DONE) {
    console.log(this.responseText);
  }
});

xhr.open("POST", "http://localhost:5000/api/sendmp3");
xhr.send(data);
```
#### Example Response
```
{
	"genre": "country"
}
```
