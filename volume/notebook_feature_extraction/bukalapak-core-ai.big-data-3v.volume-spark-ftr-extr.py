# Copyright (c) 2019 PT Bukalapak.com
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


APP_NAME = "bukalapak-core-ai.big-data-3v.volume-spark-ftr-extr"


def extract_features(xs):
    import base64, pickle
    import numpy as np
    import tensorflow as tf
    # Extract input lists
    image_info_lists = []
    images_array = []
    for x in xs:
        image_info_lists.append([x.tid, x.iid])
        images_array.append(pickle.loads(base64.b64decode(x.i_ped.encode('UTF-8'))))
    images_np = np.array(images_array)
    # Load VGG16 model
    vgg = tf.keras.applications.vgg16.VGG16(weights='imagenet', include_top=True)
    # Construct medusa model
    vgg_input = vgg.input
    vgg_fc1_output = vgg.get_layer('fc1').output
    vgg_fc2_output = vgg.get_layer('fc2').output
    vgg_predictions_output = vgg.get_layer('predictions').output
    medusa = tf.keras.models.Model(inputs=vgg_input, 
                                   outputs=[vgg_fc1_output, 
                                            vgg_fc2_output, 
                                            vgg_predictions_output])
    # Extract features
    features = medusa.predict(images_np)
    # Add features to image table lists
    if len(image_info_lists) != len(features[0]):
        raise ValueError('The total of the image table lists is not ' +
                         'the same as the total of Medusa feature lists')
    for i in range(len(image_info_lists)):
        # append fc1
        image_info_lists[i].append(
            base64.b64encode(pickle.dumps(features[0][i])).decode('UTF-8')
        )
        # append fc2
        image_info_lists[i].append(
            base64.b64encode(pickle.dumps(features[1][i])).decode('UTF-8')
        )
        # append prediction
        image_info_lists[i].append(
            base64.b64encode(pickle.dumps(features[2][i])).decode('UTF-8')
        )

    return iter(image_info_lists)


def main(spark):
    from pyspark.sql import Row
    # Input
    image_ped_orc_pathfilename = \
        "file:/home/jovyan/work/" + \
        "data/images_ped.orc"
    # Output
    image_infr_orc_pathfilename = \
        "file:/home/jovyan/work/" + \
        "data/images_infr_ss.orc"
    # Read input file
    image_ped_dict_df = spark.read.orc(image_ped_orc_pathfilename)
    image_ped_dict_rdd = image_ped_dict_df.rdd
    print("        Number of Partitions:", image_ped_dict_rdd.getNumPartitions())
    # Extract features
    image_infr_list_rdd = image_ped_dict_rdd.mapPartitions(extract_features)
    # Write output file
    image_infr_dict_rdd = image_infr_list_rdd.map(lambda x: Row(tid=x[0],
                                                                iid=x[1],
                                                                fc1=x[2],
                                                                fc2=x[3],
                                                                pred=x[4]))
    image_infr_dict_df = spark.createDataFrame(image_infr_dict_rdd)
    image_infr_dict_df.write.save(image_infr_orc_pathfilename, format="orc")


if __name__ == "__main__":
    # Configure Spark
    spark = SparkSession \
        .builder \
        .appName(APP_NAME) \
        .getOrCreate()
    main(spark)
    spark.stop()
