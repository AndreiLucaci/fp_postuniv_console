from src.repo.db_repo import DbRepository

try:
	repo = DbRepository()
	print(repo.Destinations)

except Exception as ex:
	print(ex)
