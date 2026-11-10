"""Pipeline hoàn chỉnh; mọi thống kê chỉ fit trong fold/train."""
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from .config import FEATURES, NUMERIC, CATEGORICAL, SPEC
from .validation import normalize_features

class FeatureNormalizer(TransformerMixin, BaseEstimator):
    def fit(self, X, y=None):
        missing = set(FEATURES) - set(X.columns)
        if missing:
            raise ValueError(f"Missing required features: {sorted(missing)}")
        self.feature_names_in_ = FEATURES.copy()
        self.n_features_in_ = len(FEATURES)
        return self

    def transform(self, X):
        return normalize_features(X)

    def get_feature_names_out(self, input_features=None):
        return FEATURES.copy()

def build_pipeline(name):
    numeric_steps = [("imputer", SimpleImputer(strategy="median", add_indicator=True))]
    if name == "logistic_regression":
        numeric_steps.append(("scaler", StandardScaler()))
    prep = ColumnTransformer([
        ("numeric", Pipeline(numeric_steps), NUMERIC),
        ("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False, drop=None)),
        ]), CATEGORICAL),
    ], remainder="drop", verbose_feature_names_out=True)
    if name == "baseline":
        estimator = DummyClassifier(strategy="most_frequent")
    elif name == "logistic_regression":
        estimator = LogisticRegression(**SPEC["experiments"]["models"][name]["fixed"])
    elif name == "random_forest":
        estimator = RandomForestClassifier(**SPEC["experiments"]["models"][name]["fixed"])
    else:
        raise ValueError(name)
    return Pipeline([("normalize", FeatureNormalizer()), ("preprocess", prep), ("model", estimator)])

def churn_probability(pipeline, X):
    """Không giả định cột thứ 2 luôn là lớp churn."""
    classes = list(pipeline.classes_)
    if 1 not in classes:
        raise ValueError("Pipeline không có lớp churn=1.")
    return pipeline.predict_proba(X)[:, classes.index(1)]

