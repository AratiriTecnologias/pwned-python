while true
do
        sleep 5
	curl -X POST -d @../json/upload.json -H "Content-type: application/json" https://api.pwned-2017.ml/upload
        sleep 5
	curl -X POST -d @../json/question.json -H "Content-type: application/json" https://api.pwned-2017.ml/question
        sleep 5
	curl -X POST -d @../json/message.json -H "Content-type: application/json" https://api.pwned-2017.ml/message
done
