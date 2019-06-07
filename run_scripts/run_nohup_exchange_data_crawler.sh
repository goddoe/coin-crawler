CURR_FILE_DIR=$(dirname "$0")
cd $CURR_FILE_DIR/../app/exchange_data_crawler/
nohup ./run_exchange_data_crawler.sh &
