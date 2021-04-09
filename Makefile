
DATA = data.csv
TWEETS = clean_tweets.csv orig_tweets.csv preprocessed_tweets.csv no_emojis_tweets.csv
SENTI_OUTPUT = clean_tweets0_out.txt orig_tweets0_out.txt preprocessed_tweets0_out.txt no_emojis_tweets0_out.txt

backup: $(FILES) $(DATA)
	cp clean_tweets.csv clean_tweets.csv.bak
	cp orig_tweets.csv orig_tweets.csv.bak
	cp data.csv data.csv.bak
	cp preprocessed_tweets.csv preprocessed_tweets.csv.bak
	cp no_emojis_tweets.csv no_emojis_tweets.csv.bak
	tar -cf $(shell date +%s).tar data.csv.bak orig_tweets.csv.bak clean_tweets.csv.bak preprocessed_tweets.csv.bak no_emojis_tweets.csv.bak
	rm data.csv.bak orig_tweets.csv.bak clean_tweets.csv.bak preprocessed_tweets.csv.bak no_emojis_tweets.csv.bak

senti: sentiment process_sentiment

results: senti
	mkdir results
	mv data.csv results/data.csv
	mv clean_tweets.csv results/clean_tweets.csv 
	mv orig_tweets.csv results/orig_tweets.csv
	mv data.csv results/data.csv
	mv preprocessed_tweets.csv results/preprocessed_tweets_sentimentq.csv
	mv no_emojis_tweets.csv results/no_emojis_tweets_sentiment.csv
	mv clean_tweets_sentiment.csv results/clean_tweets_sentiment.csv 
	mv orig_tweets_sentiment.csv results/orig_tweets_sentiment.csv
	mv data_sentiment.csv results/data_sentiment.csv
	mv preprocessed_tweets_sentiment.csv results/preprocessed_tweets_sentiment.csv
	mv no_emojis_tweets_sentiment.csv results/no_emojis_tweets_sentiment.csv

sentiment: $(TWEETS)
	java -jar ./SentiStrength/SentiStrengthCom.jar sentidata ./SentiStrength/SentiStrength_Data/ input orig_tweets.csv
	java -jar ./SentiStrength/SentiStrengthCom.jar sentidata ./SentiStrength/SentiStrength_Data/ input clean_tweets.csv
	java -jar ./SentiStrength/SentiStrengthCom.jar sentidata ./SentiStrength/SentiStrength_Data/ input preprocessed_tweets.csv
	java -jar ./SentiStrength/SentiStrengthCom.jar sentidata ./SentiStrength/SentiStrength_Data/ input no_emojis_tweets.csv

process_sentiment: $(SENTI_OUTPUT)
	python3 process_sentiment.py clean_tweets0_out.txt clean_tweets_sentiment.csv
	rm clean_tweets0_out.txt
	python3 process_sentiment.py orig_tweets0_out.txt orig_tweets_sentiment.csv
	rm orig_tweets0_out.txt
	python3 process_sentiment.py preprocessed_tweets0_out.txt preprocessed_tweets_sentiment.csv
	rm preprocessed_tweets0_out.txt
	python3 process_sentiment.py no_emojis_tweets0_out.txt no_emojis_tweets_sentiment.csv
	rm no_emojis_tweets0_out.txt

.PHONY: clean process_tweets

clean:
	rm -f clean_tweets.csv orig_tweets.csv data.csv no_emojis_tweets.csv preprocessed_tweets.csv

process_tweets:
	python3 scrape_data_and_analyze_tweets.py ./data/deduplicated_tweets.csv.clean data.csv orig_tweets.csv clean_tweets.csv no_emojis_tweets.csv preprocessed_tweets.csv
