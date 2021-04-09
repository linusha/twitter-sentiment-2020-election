
DATA = data.csv
TWEETS = clean_tweets.csv orig_tweets.csv preprocessed_tweets.csv no_emojis_tweets.csv

backup: $(FILES) $(DATA)
	cp clean_tweets.csv clean_tweets.csv.bak
	cp orig_tweets.csv orig_tweets.csv.bak
	cp data.csv data.csv.bak
	cp preprocessed_tweets.csv preprocessed_tweets.csv.bak
	cp no_emojis_tweets.csv no_emojis_tweets.csv.bak
	tar -cf $(shell date +%s).tar data.csv.bak orig_tweets.csv.bak clean_tweets.csv.bak preprocessed_tweets.csv.bak no_emojis_tweets.csv.bak
	rm data.csv.bak orig_tweets.csv.bak clean_tweets.csv.bak preprocessed_tweets.csv.bak no_emojis_tweets.csv.bak

sentiment: $(TWEETS)
	java -jar ./SentiStrength/SentiStrengthCom.jar sentidata ./SentiStrength/SentiStrength_Data/ input orig_tweets.csv
	java -jar ./SentiStrength/SentiStrengthCom.jar sentidata ./SentiStrength/SentiStrength_Data/ input clean_tweets.csv
	java -jar ./SentiStrength/SentiStrengthCom.jar sentidata ./SentiStrength/SentiStrength_Data/ input preprocessed_tweets.csv
	java -jar ./SentiStrength/SentiStrengthCom.jar sentidata ./SentiStrength/SentiStrength_Data/ input no_emojis_tweets.csv

.PHONY: clean process_tweets

clean:
	rm -f clean_tweets.csv orig_tweets.csv data.csv no_emojis_tweets.csv preprocessed_tweets.csv

process_tweets:
	python3 scrape_data_and_analyze_tweets.py ./data/deduplicated_tweets.csv.clean data.csv orig_tweets.csv clean_tweets.csv no_emojis_tweets.csv preprocessed_tweets.csv
