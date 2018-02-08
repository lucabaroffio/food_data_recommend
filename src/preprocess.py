import csv
import numpy as np
from sklearn.preprocessing import normalize
from scipy import sparse
import pickle
import gzip
from misc import similarity_model

INPUT_FILE = '../epicurious-recipes-with-rating-and-nutrition/epi_r.csv'
INGREDIENT_START_COL = 6

def compute_similarity(mat):
	similarity = np.matmul(mat, np.transpose(mat))
	return similarity - np.identity(len(similarity))

def main():

	recipe_names = []

	print 'loading data...'
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
		if idx % 5000 == 0:
			print '{}%'.format(idx*100.0/row_count)
	print 'done'

	print 'normalizing data...'
	recipe_to_ingredient_mat = normalize(ingredient_matrix)
	ingredient_to_recipe_mat = normalize(np.transpose(ingredient_matrix))
	print 'done'

	print 'computing similarity matrix...'
	recipe_similarity = compute_similarity(recipe_to_ingredient_mat)
	ingredient_similarity = compute_similarity(ingredient_to_recipe_mat)
	print 'done'

	print recipe_similarity

	# model = similarity_model(
	# 	recipe_similarity,
	# 	ingredient_similarity,
	# 	recipe_names,
	# 	ingredient_names
	# )

	# print 'saving data...'
	# with open('../epicurious-recipes-with-rating-and-nutrition/model.pkl.gz', 'wb') as output:
	# 	pickle.dump(model, output)
	# print 'done'

	for idx in xrange(50):
		print recipe_names[idx]
		print '\n'
		most_similar = np.argsort(recipe_similarity[idx])[::-1]

		for similar_idx in most_similar[0:5]:
			print recipe_names[similar_idx]

		print '\n\n\n'

	print 'most similar items\n\n'

	# recipe_similarity[recipe_similarity > 0.99] = 0
	# most_similar_indexed = np.dstack(
	# 	np.unravel_index(
	# 		np.argsort(
	# 			recipe_similarity.ravel()
	# 		),
	# 		recipe_similarity.shape
	# 	)
	# )[::-1]

	# for idx in xrange(20):
	# 	print recipe_names[most_similar_indexed[idx][0]]
	# 	print recipe_names[most_similar_indexed[idx][1]]
	# 	print '\n' 

if __name__ == "__main__":
	main()