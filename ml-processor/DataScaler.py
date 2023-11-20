from sklearn.preprocessing import PowerTransformer

class DataScaler:
    def __init__(self):
        self.transformer = PowerTransformer()

    def fit_transform(self, data):
        # Fit the transformer on the training data and transform it
        transformed_data = self.transformer.fit_transform(data)
        return transformed_data

    def transform(self, data):
        # Transform new data using the fitted transformer
        transformed_data = self.transformer.transform(data)
        return transformed_data