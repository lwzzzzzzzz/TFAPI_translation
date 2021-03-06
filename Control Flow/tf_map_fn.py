"""
tf.map_fn(fn, elems)：接受一个函数对象，然后用该函数对象对集合（elems）中的每一个元素分别处理，

def preprocessing_image(image, training):
    image = ...
    return image

def preprocessing_images(images, training):
    images = tf.map_fn(lambda image: preprocessing_image(image, training), images)
    return images
"""
## tf.where

tf.where(condition, x=None, y=None, name=None)

功能：若x,y都为None，返回condition值为True的坐标;
    若x,y都不为None，返回condition值为True的坐标在x内的值，condition值为False的坐标在y内的值

输入：condition:bool类型的tensor

```python
a = tf.constant([True, False, False, True])
x = tf.constant([1, 2, 3, 4])
y = tf.constant([5, 6, 7, 8])
z = tf.where(a)
z2 = tf.where(a, x, y)

sess = tf.Session()
print(sess.run(z))
print(sess.run(z2))
sess.close()

# z==>[[0]
#      [3]]
# z2==>[ 1 6 7 4]
```
## 标签的匹配
```
train_labels = tf.map_fn(lambda l: tf.where(tf.equal(labels, l)
                                            )[0][0], label_batch, dtype=tf.int64)
```
## 注解：
label_batch是一个[batch_size,1]的张量，labels储存有所有的图片标签的信息，是一个[pictures_num,1]的张量。
很明显label_batch的行数比picture_num小得多，这时候如果我们直接使用tf.equal函数会出现维度不匹配的问题，使用map_fn主要是将定义的函数运用到后面集合中每个元素中。这里的l其实是label_batch标签张量中的一个秩相同的单个张量。

tf.equal(labels,l)会得到一个[Flase,True,Flase,True,False,False,False]的张量，tf.where会找到此布尔值数组的第一个为True的索引。由于函数返回的是一个二维数组，所以使用[0][0]提取出该值。

## Example
```python
"""主要测试tf.where的使用"""
import tensorflow as tf
import numpy as np


a = np.array([[5]])
a1 = np.array([[1], [2], [3]])
b = np.array([[1], [7], [8], [4], [5], [2], [3], [2], [3]])
# 对于[n,1]shape张量匹配必须使用map_fn函数，否则会出shape函数维度不匹配的错误
c1 = tf.map_fn(lambda l: tf.where(tf.equal(b, l))[0][0], a1, dtype=tf.int64)
c = tf.where(tf.equal(a, b))[0][0]

# c = tf.where(tf.equal(a1, b))[0][0] 这个语句就会出现下面维度不匹配的错误。
# Dimensions must be equal, but are 3 and 7 for 'Equal' (op: 'Equal') with input shapes: [3,1], [7,1].
sess = tf.Session()
print(sess.run(c))
print(sess.run(c1))

# 4
# [0 5 6]

```
