
FILES = clean_tweets.csv orig_tweets.csv data.csv

backup: $(FILES) 
	cp clean_tweets.csv clean_tweets.csv.bak
	cp orig_tweets.csv orig_tweets.csv.bak
	cp data.csv data.csv.bak
	tar -cf $(shell date +%s).tar data.csv.bak orig_tweets.csv.bak clean_tweets.csv.bak
	rm data.csv.bak orig_tweets.csv.bak clean_tweets.csv.bak


.PHONY: clean

clean:
	rm -f clean_tweets.csv orig_tweets.csv data.csv

