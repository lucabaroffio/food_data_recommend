import csv
import numpy as np
from sklearn.preprocessing import normalize

INPUT_FILE = '../epicurious-recipes-with-rating-and-nutrition/epi_r.csv'
INGREDIENT_START_COL = 6

def main():

	recipe_names = []

	row_count = sum(1 for row in csv.reader(open(INPUT_FILE), delimiter=','))
	csvReader = csv.reader(open(INPUT_FILE), delimiter=',')
	for idx, row in enumerate(csvReader):
		if idx == 0:
			column_names = row
			ingredient_names = column_names[INGREDIENT_START_COL:]
			ingredient_matrix = np.empty([row_count-1, len(ingredient_names)])
		else:
			recipe_names.append(row[0])
			x = np.array(row[INGREDIENT_START_COL:])
			ingredient_matrix[idx-1] = x
			# print ingredient_matrix[idx-1]
			# raw_input()

		# print percentage of completion
		if idx % 1000 == 0:
			print '{}%'.format(idx*100.0/row_count)

	print 'normalizing data'
	ingredient_matrix = normalize(ingredient_matrix)
	print 'done'

	print 'computing similarity matrix...'
	recipe_similarity = np.matmul(ingredient_matrix, np.transpose(ingredient_matrix))
	recipe_similarity = recipe_similarity - np.identity(len(recipe_similarity))
	print 'done'

	for idx in xrange(10):
		print recipe_names[idx]
		print '\n'
		most_similar = np.argsort(recipe_similarity[idx])[::-1]

		for similar_idx in most_similar[0:5]:
			print recipe_names[similar_idx]

		print '\n\n\n'

if __name__ == "__main__":
	main()