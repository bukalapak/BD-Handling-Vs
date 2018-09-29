# Copyright (c) 2018 PT Bukalapak.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pyspark.sql import SparkSession


APP_NAME = "bukalapak-core-ai.big-data-3v.volume-spark"


def tokenize(words):
    from tensorflow.keras.preprocessing.text import text_to_word_sequence
    return text_to_word_sequence(words['value'])


def main(spark):
    # Input
    product_names_text_filename = \
        "file:/home/jovyan/work/" + \
        "data/product_names_sample/" + \
        "product_names.rdd"
    # Output
    product_names_word_count_ss_orc_filename = \
        "file:/home/jovyan/work/" + \
        "data/product_names_sample/" + \
        "product_names_word_count_ss.orc"
    # Read input
    product_names_df = spark.read.text(product_names_text_filename)
    product_names_rdd = product_names_df.rdd
    # Perform tokenization and word count
    tokenized_product_names_rdd = \
        product_names_rdd.flatMap(lambda product_name: tokenize(product_name))
    word_count_product_names_rdd = \
        tokenized_product_names_rdd.map(lambda word: (word, 1)) \
                                   .reduceByKey(lambda a, b: a + b)
    # Write output
    word_count_product_names_df = spark.createDataFrame(word_count_product_names_rdd)
    word_count_product_names_df.write.save(product_names_word_count_ss_orc_filename, \
                                           format="orc")


if __name__ == "__main__":
    # Configure Spark
    spark = SparkSession \
        .builder \
        .appName(APP_NAME) \
        .getOrCreate()
    main(spark)
    spark.stop()