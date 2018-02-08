import numpy as np

class Similarity_model(object):

	@staticmethod
	def compute_similarity(mat):
		similarity = np.matmul(mat, np.transpose(mat))
		return (similarity - np.identity(len(similarity))).astype(np.float16)

	@staticmethod
	def symmetrize(mat):
		return (mat + mat.T - np.diag(mat.diagonal())).astype(np.float16)

	def set_recipe_similarity(self, mat):
		self._recipe_similarity = np.tril(mat).astype(np.float16)

	def get_recipe_similarity(self):
		return Similarity_model.symmetrize(self._recipe_similarity)

	recipe_similarity = property(get_recipe_similarity, set_recipe_similarity)

	def set_ingredient_similarity(self, mat):
		self._ingredient_similarity = np.tril(mat).astype(np.float16)

	def get_ingredient_similarity(self):
		return Similarity_model.symmetrize(self._ingredient_similarity)

	ingredient_similarity = property(get_ingredient_similarity, set_ingredient_similarity)

	def __init__(self, 
		recipe_similarity,
		ingredient_similarity,
		recipe_names,
		ingredient_names
	):

		self.recipe_similarity = recipe_similarity
		self.ingredient_similarity = ingredient_similarity
		self.recipe_names = recipe_names
		self.ingredient_names = ingredient_names