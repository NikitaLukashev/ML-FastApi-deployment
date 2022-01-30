import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


class Processor:

    @staticmethod
    def process_predict(payload, couleur_map, categorie_map, description_tfidf, nom_tfidf):

        resource = pd.DataFrame(payload, index=[0])

        ###################################################################
        # process categorical and text feature by mapping encoded label and trained tfidf
        ###################################################################
        resource['couleur'] = resource['couleur'].map(couleur_map)
        resource['categorie'] = resource['categorie'].map(categorie_map)

        tfidf = description_tfidf.transform(resource['description_produit'])
        tfidf_cols = description_tfidf.get_feature_names()
        tmp = pd.DataFrame(data=tfidf.todense(),
                           columns=['tfidf_' + 'description_produit' + '_' + i for i in tfidf_cols])
        df = pd.concat([resource, tmp], axis=1)

        tfidf = nom_tfidf.transform(resource['nom_produit'])
        tfidf_cols = nom_tfidf.get_feature_names()
        tmp = pd.DataFrame(data=tfidf.todense(), columns=['tfidf_' + 'nom_produit' + '_' + i for i in tfidf_cols])
        df = pd.concat([df, tmp], axis=1)

        df = df.drop(['description_produit', 'nom_produit'], axis=1)

        ###################################################################
        # filling nan andtype casting
        ###################################################################
        for col in ['nb_images', 'longueur_image', 'largeur_image', 'annee', 'couleur',
                    'prix', 'categorie']:
            df[col] = df[col].astype(float).fillna(-999)
        return df

    @staticmethod
    def process_train(data: pd.DataFrame):
        def get_tfidf_vectorizer(df, field, vectorizer):
            vec = vectorizer.fit(df[field])
            tfidf_ = vectorizer.fit_transform(df[field])
            tfidf_cols = vectorizer.get_feature_names()
            temp = pd.DataFrame(data=tfidf_.todense(), columns=['tfidf_' + field + '_' + i for i in tfidf_cols])
            df = pd.concat([df, temp], axis=1)
            return df, vec

        def map_categorie(df):
            my_map_reversed = dict()
            for col in ['couleur', 'categorie']:
                my_map = dict(enumerate(df[col].astype('category').cat.categories))
                my_map_reversed[col] = {v: k for k, v in my_map.items()}
                df[col] = df[col].astype('category').cat.codes
            return df, my_map_reversed

        ###################################################################
        # process categorical and text feature by label encoding and tfidf
        ###################################################################
        data = data.drop(['id'], axis=1)
        tfidf = TfidfVectorizer(analyzer='word',
                                ngram_range=(1, 1),
                                lowercase=True,
                                max_features=20,
                                binary=True,
                                norm=None,
                                use_idf=False)

        data['description_produit'] = data['description_produit'].astype(str)
        data, description_produit_tfidf = get_tfidf_vectorizer(data, 'description_produit', tfidf)
        data.drop('description_produit', inplace=True, axis=1)

        data['nom_produit'] = data['nom_produit'].astype(str)
        data, nom_produit_tfidf = get_tfidf_vectorizer(data, 'nom_produit', tfidf)
        data.drop('nom_produit', inplace=True, axis=1)

        data, mapper = map_categorie(data)

        ###################################################################
        # replace nan value
        ###################################################################
        data.fillna(value=-999, inplace=True)

        ###################################################################
        # split train and target
        ###################################################################
        target = data['delai_vente']
        train = data.drop(['delai_vente'], axis=1)

        return train, target, mapper, description_produit_tfidf, nom_produit_tfidf
