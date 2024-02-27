from sentence_transformers import SentenceTransformer
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, utility , Collection

def test_impl():
    connection = connections.connect(
        db_name='default',
        alias='default',
        user='minioadmin',
        password='minioadmin',
        host='ec2-34-223-50-104.us-west-2.compute.amazonaws.com',
        port=19530
    )
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    query = 'Blue Cross Community MMAI (Medicare-Medicaid Plan) Blue Cross Community Health Plans Medicaid'
    query_embeddings = model.encode(query)
    embd = query_embeddings.tolist()
    collection = Collection("ECWEligibilityInsurances")
    collection.load()
    result = collection.search(
        data=[embd],
        anns_field='eligibility_insurance_attribute_vector',
        param={"metric_type": "L2", "params": {"nlist": 1024}},
        limit=5,
        expr=None,
        output_fields=['ecw_insurance_name']

    )
    print(result)

test_impl()