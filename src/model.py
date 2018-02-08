import numpy as np
import pickle

class Similarity_model(object):

	@staticmethod
	def load_model_from_file(file_path):
		with open(file_path, 'rb') as f:
			model = pickle.load(f)
		return model

	def init_indices(self):
		self.ingredient_index = {}
		for idx, ingredient_id in enumerate(self.ingredient_names) or []:
			self.ingredient_index[ingredient_id] = idx
		self.recipe_index = {}
		for idx, recipe_id in enumerate(self.recipe_names) or []:
			self.recipe_index[recipe_id] = idx

	def recommend_ingredients(self, input_ingredients):
		input_vector = np.zeros([len(self.ingredient_similarity), 1])
		indices = [self.ingredient_index[ingredient_id] for ingredient_id in input_ingredients if ingredient_id in self.ingredient_index]
		if len(indices) == 0:
			# probably this should raise an exception...
			return []
		input_vector[indices] = 1
		scores = np.squeeze(input_vector.transpose().dot(self.ingredient_similarity))
		# scores = self.ingredient_similarity.dot(input_vector)
		recom_indices = np.argsort(scores)[::-1]
		scores = np.array(scores)[recom_indices]
		recommendations = [{
			'ingredient': self.ingredient_names[index],
			'score': scores[n]
		} for n, index in enumerate(recom_indices)]
		return {
			'query': [self.ingredient_names[idx] for idx in indices],
			'recommendations': recommendations
		}

	@staticmethod
	def compute_similarity(mat):
		similarity = np.matmul(mat, np.transpose(mat))
		return (similarity - np.identity(len(similarity))).astype(np.float16)

	@staticmethod
	def symmetrize(mat):
		return (mat + mat.T - np.diag(mat.diagonal())).astype(np.float16)

	def set_recipe_similarity(self, mat):
		if mat != None:
			self._recipe_similarity = np.tril(mat).astype(np.float16) if self.store_triangular else mat.astype(np.float16)
		else:
			self._recipe_similarity = None

	def get_recipe_similarity(self):
		if self._recipe_similarity != None:
			return Similarity_model.symmetrize(self._recipe_similarity) if self.store_triangular else self._recipe_similarity
		else:
			return None

	recipe_similarity = property(get_recipe_similarity, set_recipe_similarity)

	def set_ingredient_similarity(self, mat):
		self._ingredient_similarity = np.tril(mat).astype(np.float16) if self.store_triangular else mat.astype(np.float16)

	def get_ingredient_similarity(self):
		return Similarity_model.symmetrize(self._ingredient_similarity) if self.store_triangular else self._ingredient_similarity

	ingredient_similarity = property(get_ingredient_similarity, set_ingredient_similarity)

	def __init__(self, 
		recipe_similarity,
		ingredient_similarity,
		recipe_names,
		ingredient_names,
		store_triangular=False
	):

		self.store_triangular = store_triangular
		self.recipe_similarity = recipe_similarity
		self.ingredient_similarity = ingredient_similarity
		self.recipe_names = recipe_names
		self.ingredient_names = ingredient_names

		self.init_indices()
