# GPT Demo in Gradio

This is a demo inferencing of the [GPT](https://openai.com/blog/better-language-models/) model, trained on harry potter books dataset.
Inferencing was done using docker container, and the model was served using [Gradio](https://gradio.app/). Later model was deployed in ECS Fargate.

## How to run

To build the docker image, run the following command:
```
docker build -t gpt-demo .
```
To run the docker container locally, run the following command:
```
docker run -p 80:80 -it --rm gpt-demo
```
Now we can access the model at http://localhost:80 or if you rae working on a ec2 container, you can access it using the public ip of the ec2 instance.