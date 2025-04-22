from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

# Downloads to your-project/data/
api.dataset_download_files('robikscube/elden-ring-ultimate-dataset', path='./data', unzip=True)