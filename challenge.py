import json
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from cli.chains.build_family_tree import build_tree_chain
from cli.controllers.normalize_format import listify_object
from sentence_transformers import SentenceTransformer
import igraph


def get_dataframes(
    items: list[dict] | dict, deities: list[dict], description_weight: int = 10
):
    """
    Returns dataframes with embedded descriptions for use in other challenge functions
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    items_df = pd.json_normalize(items)
    try:
        item_embedding = pd.DataFrame(
            model.encode(items_df["item_description"]) * description_weight
        )
        items_df = pd.concat([items_df, item_embedding], axis=1)
    except:
        pass
    deities_df = pd.json_normalize(deities)
    try:
        deity_embeddings = pd.DataFrame(
            model.encode(deities_df["deity_description"]) * description_weight
        )
        deities_df = pd.concat([deities_df, deity_embeddings], axis=1)
    except:
        pass
    return items_df, deities_df


def discover_most_likely_god(item: dict, description_weight: int = 3):
    """
    Discovers which god is most likely to have created an object based on a combination of the stats and vectors of the descriptions
    It does this by measuring the euclidean distance between the object's and the gods' stats, as well as the vector form of their descriptions
    Due to the nature of vector embeddings the stats have a pretty significant weight compared to the description
    This can be modified by adjusting the description_weight parameter, which is set to 3 as a baseline.
    This function will continue to work as long as the deities and item have a description or at least one stat in common
    Adding additional stats will not affect the results unless both the deities and items are updated with the new stats
    This is because we filter out all unnecessary data by using a set operation on the two DataFrames' columns
    which ensures only columns that exist in both data sets will be compared, and that those columns will be compared 1:1
    so even if the stats are in a different order, physical will be compared to physical, arcane to arcane, etc.
    """
    deities = json.load(open("deities.json"))
    if isinstance(deities, dict):
        deities = listify_object(deities)
    item_df, deities_df = get_dataframes(item, deities, description_weight)
    shared_columns = list(set(deities_df.columns) & set(item_df.columns))
    idx = euclidean_distances(
        item_df[shared_columns], deities_df[shared_columns]
    ).argmin()
    return deities[idx]


def make_family_tree(description_weight: int = 3, distance_cutoff: float = 8.0):
    graph = igraph.Graph()
    items = json.load(open("items.json"))
    deities = json.load(open("deities.json"))
    items_df, deities_df = get_dataframes(items, deities, description_weight)
    graph.add_vertices(
        items_df.shape[0],
        items_df[[x for x in items_df.columns if isinstance(x, str)]].to_dict(
            orient="list"
        ),
    )
    graph.add_vertices(
        deities_df.shape[0],
        deities_df[[x for x in deities_df.columns if isinstance(x, str)]].to_dict(
            orient="list"
        ),
    )
    shared_columns = list(set(deities_df.columns) & set(items_df.columns))
    distance_df = pd.DataFrame(
        euclidean_distances(items_df[shared_columns], deities_df[shared_columns])
    )
    relationships = []
    for i, item in enumerate(items):
        items_with_deities = (
            distance_df.loc[i, :]
            .where(lambda x: x < distance_cutoff)
            .dropna()
            .index.to_list()
        )
        item["relevant_deities"] = [
            {k: v for k, v in deities[x].items() if "deity" in k}
            for x in items_with_deities
        ]
    for item in sorted(items, key=lambda x: len(x["relevant_deities"]), reverse=True):
        relationships.append(build_tree_chain(item, relationships).model_dump())
    return relationships


if __name__ == "__main__":
    make_family_tree()
