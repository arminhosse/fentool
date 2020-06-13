"""Unittest wrapper for different feature engineering methods"""

from unittest import TestCase, skipUnless
import pytest
import os
import pandas as pd

from fentool.pre_process import Encoder, Minmax, Standard

RESOURCE_PATH = '%s/resources' % os.path.dirname(os.path.realpath(__file__))


class TestEncoder(TestCase):
    """ Unittest for the encoder method """
    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(RESOURCE_PATH + '/sample_data.csv')

    def test_auto_detect_categorical(self):

        enc = Encoder()

        col = enc.auto_detect_categorical(TestEncoder.df)

        self.assertTrue(col == 'ocean_proximity',
                    msg="auto category detection failed")

    def test_fit_transform(self):

        # test the ordinal
        enc = Encoder('ordinal')
        df_enc = enc.fit_transform(TestEncoder.df)

        self.assertTrue((TestEncoder.df.columns == df_enc.columns).all()
                        , msg="Mismatch in df columns after ordinal encoder")
        self.assertTrue(enc.cat_cols == 'ocean_proximity',
                        msg="Unexpected categorical column")

        self.assertTrue(df_enc[enc.cat_cols].min().values == 0,
                        msg="Unexpected categorical code")
        self.assertTrue(df_enc[enc.cat_cols].max().values == 3,
                        msg="Unexpected categorical code")

        # test the one-hot encoder
        enc = Encoder('one-hot')
        df_enc = enc.fit_transform(TestEncoder.df)
        self.assertTrue(df_enc.columns.shape == (15,),
                        msg="Mismatch in df columns after ordinal encoder")


class TestMinMax(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(RESOURCE_PATH + '/sample_data.csv')
        enc = Encoder()
        cls.df_enc = enc.fit(cls.df)

    def test_validate_inputs(self):

        prep = Minmax(input_range=(0, 1))

        self.assertTrue(prep.input_range == (0, 1),
                        msg="desired range not assigned properly")

    def test_fit(self):

        prep = Minmax()

        prep.fit(pd.get_dummies(TestMinMax.df_enc))

        print(prep)