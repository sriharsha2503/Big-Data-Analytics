from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, udf
from pyspark.sql.types import ArrayType, StringType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Data Preprocessing for Entity Resolution") \
    .getOrCreate()

# Sample DataFrame (Replace this with your actual data source)
data = [("John Doe", "1234 Main St", "johndoe@example.com"),
        ("Jane Smith", "5678 Oak St", "janesmith@example.com")]

columns = ["name", "address", "email"]
df = spark.createDataFrame(data, columns)

# Define UDF for tokenization
def tokenize(text):
    return text.split()

tokenize_udf = udf(tokenize, ArrayType(StringType()))

# Data cleaning and preprocessing
df_cleaned = df.withColumn("name_cleaned", lower(col("name"))) \
    .withColumn("address_cleaned", lower(col("address"))) \
    .withColumn("email_cleaned", lower(col("email"))) \
    .withColumn("name_tokens", tokenize_udf(col("name_cleaned"))) \
    .withColumn("address_tokens", tokenize_udf(col("address_cleaned"))) \
    .withColumn("email_tokens", tokenize_udf(col("email_cleaned")))

df_cleaned.show(truncate=False)

from pyspark.sql.functions import udf
from pyspark.sql.types import FloatType

# Define Jaccard Similarity UDF
def jaccard_similarity(set1, set2):
    set1 = set(set1)
    set2 = set(set2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

jaccard_similarity_udf = udf(jaccard_similarity, FloatType())

# Compute similarity scores
df_similarities = df_cleaned.alias("a").crossJoin(df_cleaned.alias("b")) \
    .filter(col("a.email") < col("b.email")) \
    .withColumn("similarity", jaccard_similarity_udf(col("a.email_tokens"), col("b.email_tokens")))

df_similarities.show(truncate=False)
