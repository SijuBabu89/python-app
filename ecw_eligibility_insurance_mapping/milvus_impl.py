from pymilvus import connections, FieldSchema, CollectionSchema, DataType, utility, Collection
import pandas as pd
from sentence_transformers import SentenceTransformer
from flask import Flask, jsonify
import json
import ast

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
connections.connect(
    db_name='default',
    alias='default',
    user='minioadmin',
    password='minioadmin',
    host='ec2-34-223-50-104.us-west-2.compute.amazonaws.com',
    port=19530
)


def initilize_connection():
    connections.connect(
        db_name='default',
        alias='default',
        user='minioadmin',
        password='minioadmin',
        host='ec2-34-223-50-104.us-west-2.compute.amazonaws.com',
        port=19530
    )


def upload_data(file):
    df = pd.read_csv(file)
    ids = []
    mapping_fields = []
    ecw_insurance = []

    for row, column in df.iterrows():
        mapping_fields.append(
            str(column['Payer Name']) + " " + str(column['Plan Name']) + " " + str(column['Insurance Type']))
        ecw_insurance.append(str(column['ECW Insurance']))
        ids.append(column['Ids'])
        return ids, mapping_fields, ecw_insurance


def vectorize_data(mapping_fields):
    # Sentences we want to encode. Example:
    ins_mapping_embeddings = []
    for field in mapping_fields:
        embeds = model.encode(field)
        ins_mapping_embeddings.append(embeds.tolist())
    return ins_mapping_embeddings


def create_collection(file):
    initilize_connection()
    ids, mapping_fields, ecw_insurance = upload_data(file)
    ins_mapping_embeddings = vectorize_data(mapping_fields)
    ins_id = FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, max_length=50)
    ecw_insurance_name = FieldSchema(name='ecw_insurance_name', dtype=DataType.VARCHAR, max_length=200)
    eligibility_insurance_attribute_vector = FieldSchema(name='eligibility_insurance_attribute_vector',
                                                         dtype=DataType.FLOAT_VECTOR, dim=384)
    ins_mapping_schema = CollectionSchema(fields=[ins_id, ecw_insurance_name, eligibility_insurance_attribute_vector],
                                          description='Insurance Mapping Collection')
    collection = Collection(name='ECWEligibilityInsurances', schema=ins_mapping_schema, using='aveta')

    entities = [ids, ecw_insurance, ins_mapping_embeddings]

    insert_result = collection.insert(entities)
    # After final entity is inserted, it is best to call flush to have no growing segments left in memory
    collection.flush()

    index_params = {"metric_type": "COSINE", "index_type": "IVF_FLAT", "params": {"nlist": 2048},
                    "index_name": "'eligibility_insurance_attribute_index"}

    collection.create_index(field_name="eligibility_insurance_attribute_vector", index_params=index_params)

    collection.create_index(
        field_name="ecw_insurance_name",
        index_name="scalar_index",
        index_params={"index_type": "marisa-trie"}
    )
    collection.load()


def search_insurance(query):
    initilize_connection()
    collection = Collection("ECWEligibilityInsurances")
    collection.load()
    query_embeddings = model.encode(query)
    query_embeddings_list = query_embeddings.tolist()
    result = collection.search(
        data=[query_embeddings_list],
        anns_field='eligibility_insurance_attribute_vector',
        param={"metric_type": "COSINE", "offset": 0, "params": {"nlist": 2048}},
        limit=5,
        expr=None,
        output_fields=['ecw_insurance_name'],
        consistency_level="Strong"
    )
    return result


def get_ecw_insurance(query):
    result = search_insurance(query)
    response = extract_list_output(result)
    if len(response) > 0:
        print(response[0])
        return response[0].get('insurance')
    return ''


def get_ecw_insurance_list(query):
    result = search_insurance(query)
    return extract_list_output(result)


def extract_list_output(result):
    inner_array_str = result[0]
    response = []
    try:
        for hits in result:
            # get the IDs of all returned hits
            # print(hits.ids)
            # get the distances to the query vector from all returned hits
            # print(hits.distances)
            for hit in hits:
                formatted_entity = {'id': hit.id, 'distance': hit.distance,
                                    'insurance': hit.entity.get('ecw_insurance_name')}
                response.append(formatted_entity)
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# get_ecw_insurance('Blue Cross Community MMAI (Medicare-Medicaid Plan) Blue Cross Community Health Plans Medicaid')
