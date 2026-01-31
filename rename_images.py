# -*- coding: utf-8 -*-
"""
إعادة تسمية صور التصنيفات والمنتجات إلى أسماء إنجليزية (category-1.jpg, product-1.jpg)
شغّل مرة واحدة: python rename_images.py
"""
import os
import shutil

BASE = os.path.abspath(os.path.dirname(__file__))
CAT_DIR = os.path.join(BASE, 'static', 'images', 'categories')
PROD_DIR = os.path.join(BASE, 'static', 'images', 'products')
NUM_CATEGORIES = 15
NUM_PRODUCTS = 8


def rename_category_images():
    jpgs = sorted([f for f in os.listdir(CAT_DIR) if f.lower().endswith('.jpg') and not f.startswith('_tmp_')])
    for i, f in enumerate(jpgs):
        src = os.path.join(CAT_DIR, f)
        tmp = os.path.join(CAT_DIR, f'_tmp_{i}.jpg')
        os.rename(src, tmp)
    for i in range(len(jpgs)):
        src = os.path.join(CAT_DIR, f'_tmp_{i}.jpg')
        dst = os.path.join(CAT_DIR, f'category-{i + 1}.jpg')
        os.rename(src, dst)
    # إذا كان عدد الملفات أقل من 15 ننسخ صورة افتراضية للباقي
    for i in range(len(jpgs) + 1, NUM_CATEGORIES + 1):
        src = os.path.join(CAT_DIR, 'category-1.jpg')
        dst = os.path.join(CAT_DIR, f'category-{i}.jpg')
        if os.path.isfile(src) and not os.path.isfile(dst):
            shutil.copy2(src, dst)
    print(f'Categories: category-1.jpg .. category-{NUM_CATEGORIES}.jpg ready.')


def rename_product_images():
    jpgs = sorted([f for f in os.listdir(PROD_DIR) if f.lower().endswith('.jpg') and not f.startswith('_tmp_')])
    jpgs = jpgs[:NUM_PRODUCTS]
    for i, f in enumerate(jpgs):
        src = os.path.join(PROD_DIR, f)
        tmp = os.path.join(PROD_DIR, f'_tmp_{i}.jpg')
        os.rename(src, tmp)
    for i in range(len(jpgs)):
        src = os.path.join(PROD_DIR, f'_tmp_{i}.jpg')
        dst = os.path.join(PROD_DIR, f'product-{i + 1}.jpg')
        os.rename(src, dst)
    # إذا كان عدد الملفات أقل من 8 ننسخ صورة افتراضية للباقي
    for i in range(len(jpgs) + 1, NUM_PRODUCTS + 1):
        src = os.path.join(PROD_DIR, 'product-1.jpg')
        dst = os.path.join(PROD_DIR, f'product-{i}.jpg')
        if os.path.isfile(src) and not os.path.isfile(dst):
            shutil.copy2(src, dst)
    print(f'Products: product-1.jpg .. product-{NUM_PRODUCTS}.jpg ready.')


if __name__ == '__main__':
    rename_category_images()
    rename_product_images()
    print('Done.')
