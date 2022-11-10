import services.dao.dao as dao

if __name__ == "__main__":
    dao.instantiate_data()
    dao.instantiate_stopwords()
    dao.instantiate_unknown_responses()
    print("---Completed---")
