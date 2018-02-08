import numpy as np
import pickle
import click
from misc import Similarity_model

MODEL_FILE = '../epicurious-recipes-with-rating-and-nutrition/model.pkl'
N_RESULT = 10

with open(MODEL_FILE, 'rb') as f:
	model = pickle.load(f)

@click.command()
@click.option('--operation',
	prompt='What operation do you want to do? "feat" to list features (ingredients), "recipes" to list recipes, "sim_rec" to get similar recipes, "best_match_ingredient" to get the best matching ingredients/feat',
	help='The operation to be performed. "feat" to list features (ingredients), "recipes" to list recipes, "sim_recipes" to get similar recipes, "best_match_ingredient" to get the best matching ingredients/feat'
)
@click.option('--n',
	prompt='N-th feature/recipe',
	default=-1,
	help='The index of the base feature/recipe for which you want to get similar items'
)
def main(operation, n):

	if operation == "feat":
		print model.ingredient_names
	elif operation == "recipes":
		print model.recipe_names
	elif operation == "sim_rec":
		if n is None or n < 0:
			print 'Please use --n to specify the base item'
		else:
			print model.recipe_names[n]
			print '\n'

			most_similar = np.argsort(model.recipe_similarity[n])[::-1]
			
			for similar_idx in most_similar[0:N_RESULT]:
				print model.recipe_names[similar_idx]

	elif operation == "best_match_ingredient":
		if n is None or n < 0:
			print 'Please use --n to specify the base item'
		else:
			print model.ingredient_names[n]
			print '\n'

			most_similar = np.argsort(model.ingredient_similarity[n])[::-1]
			
			for similar_idx in most_similar[0:N_RESULT]:
				print model.ingredient_names[similar_idx]
	else:
		print 'Please select a valid operation'

if __name__ == "__main__":
	main()