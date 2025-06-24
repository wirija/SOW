import splink.comparison_library as cl
from splink import DuckDBAPI, Linker,  SettingsCreator, block_on, splink_datasets
import pandas as pd

# Sample data
df = pd.DataFrame([
    {"unique_id": 1, "first_name": "John", "surname": "Smith", "dob": "1990-01-01"},
    {"unique_id": 2, "first_name": "Jon", "surname": "Smyth", "dob": "1990-01-01"},
    {"unique_id": 3, "first_name": "Jane", "surname": "Doe", "dob": "1985-05-05"},
])


settings = SettingsCreator(
    link_type="dedupe_only",
    blocking_rules_to_generate_predictions=[
        block_on("first_name", "surname"),
        block_on("dob")
    ],
    comparisons=[
        cl.NameComparison("first_name"),
        cl.NameComparison("surname"),
        cl.DateOfBirthComparison("dob", input_is_string = True)
        
    ]
)

linker = Linker(df, settings, db_api=DuckDBAPI())

linker.training.estimate_probability_two_random_records_match(
    deterministic_matching_rules=[
        block_on("first_name", "surname"),
        block_on("dob"),
    ],
    recall=0.7,
)


# Estimate parameters and predict matches
linker.training.estimate_u_using_random_sampling(max_pairs=1e6)
linker.training.estimate_parameters_using_expectation_maximisation(block_on("first_name", "surname"),block_on("dob"),)

# Predict and cluster
df_predict = linker.inference.predict()
df_clusters = linker.clustering.cluster_pairwise_predictions_at_threshold(df_predict, threshold_match_probability=0.9,)

# Show results
print(df_clusters)
