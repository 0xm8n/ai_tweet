# AI Tweet

This is a simple Twitter bot that tweets about trending topics related to the subjects you specify.

## Requirements

* Docker
* Python 3.9
* Tweepy
* requests

## Installation

1. Clone this repository.
2. Create a `.env` file and add the required data
3. Build the Docker image:
```bash
docker-compose -f docker-compose.yml up --build 
```

4. Run the Docker container:
```bash
docker-compose -f docker-compose.yml up
```

## Usage
The bot will start tweeting about trending topics related to the subjects you specified in the .env file. You can stop the bot by pressing Ctrl+C.

## Customize
You can customize the bot by editing the ai_tweet.py file. For example, you can change the subjects that the bot tweets about, or you can change the frequency of the tweets.

## License
This project is licensed under the MIT License.
