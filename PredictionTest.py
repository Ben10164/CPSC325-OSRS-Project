import Predictor
import pandas as pd

import DateTimeHelper

MAX_EPOCHS=1000
PATIENCE = MAX_EPOCHS/10
MODEL = "Conv1D"


# ITEM="Tumeken's shadow (uncharged)"
# ITEM="Scythe of vitur (uncharged)"
ITEM="Twisted bow"

DELTA = '1h'
# DELTA = '6h'


test_df = DateTimeHelper.getDT(ITEM, DELTA)[-30:]

# test_df = pd.read_json('temp.json')


model = Predictor.get_model(MAX_EPOCHS=MAX_EPOCHS,
                            PATIENCE=PATIENCE,
                            ITEM=ITEM,
                            MODEL=MODEL,
                            DELTA=DELTA)


te = Predictor.predict(model, test_df)
print(te)

#------#

# ITEM="Tumeken's shadow (uncharged)"
# ITEM="Scythe of vitur (uncharged)"
ITEM="Twisted bow"

# DELTA = '1h'
DELTA = '6h'

test_df = DateTimeHelper.getDT(ITEM, DELTA)[-30:]

# test_df = pd.read_json('temp.json')


model = Predictor.get_model(MAX_EPOCHS=MAX_EPOCHS,
                            PATIENCE=PATIENCE,
                            ITEM=ITEM,
                            MODEL=MODEL,
                            DELTA=DELTA)


te = Predictor.predict(model, test_df)
print(te)

#------#

# ITEM="Tumeken's shadow (uncharged)"
ITEM="Scythe of vitur (uncharged)"
# ITEM="Twisted bow"

DELTA = '1h'
# DELTA = '6h'

test_df = DateTimeHelper.getDT(ITEM, DELTA)[-30:]

# test_df = pd.read_json('temp.json')


model = Predictor.get_model(MAX_EPOCHS=MAX_EPOCHS,
                            PATIENCE=PATIENCE,
                            ITEM=ITEM,
                            MODEL=MODEL,
                            DELTA=DELTA)


te = Predictor.predict(model, test_df)
print(te)

#------#

# ITEM="Tumeken's shadow (uncharged)"
ITEM="Scythe of vitur (uncharged)"
# ITEM="Twisted bow"

# DELTA = '1h'
DELTA = '6h'

test_df = DateTimeHelper.getDT(ITEM, DELTA)[-30:]

# test_df = pd.read_json('temp.json')


model = Predictor.get_model(MAX_EPOCHS=MAX_EPOCHS,
                            PATIENCE=PATIENCE,
                            ITEM=ITEM,
                            MODEL=MODEL,
                            DELTA=DELTA)


te = Predictor.predict(model, test_df)
print(te)

#------#

ITEM="Tumeken's shadow (uncharged)"
# ITEM="Scythe of vitur (uncharged)"
# ITEM="Twisted bow"

# DELTA = '1h'
DELTA = '6h'

test_df = DateTimeHelper.getDT(ITEM, DELTA)[-30:]

# test_df = pd.read_json('temp.json')


model = Predictor.get_model(MAX_EPOCHS=MAX_EPOCHS,
                            PATIENCE=PATIENCE,
                            ITEM=ITEM,
                            MODEL=MODEL,
                            DELTA=DELTA)


te = Predictor.predict(model, test_df)
print(te)

#------#

ITEM="Tumeken's shadow (uncharged)"
# ITEM="Scythe of vitur (uncharged)"
# ITEM="Twisted bow"

DELTA = '1h'
# DELTA = '6h'

test_df = DateTimeHelper.getDT(ITEM, DELTA)[-30:]

# test_df = pd.read_json('temp.json')


model = Predictor.get_model(MAX_EPOCHS=MAX_EPOCHS,
                            PATIENCE=PATIENCE,
                            ITEM=ITEM,
                            MODEL=MODEL,
                            DELTA=DELTA)


te = Predictor.predict(model, test_df)
print(te)






# model = Predictor.get_model(MAX_EPOCHS=MAX_EPOCHS0,
#                             PATIENCE=10,
#                             normalize=False,
#                             # normalize=True,
#                             ITEM=ITEM,
#                             # ITEM="Twisted bow",
#                             # ITEM="Osmumten's fang",
#                             INPUT_WIDTH=30,
#                             LABEL_WIDTH=30,
#                             CONV_WIDTH=30,
#                             LABEL_COLUMNS=['average',
#                                            'avgHighPrice', 'avgLowPrice'],
#                             # MODEL="Linear",
#                             MODEL=MODEL,
#                             # MODEL="Multi_Step_Dense",
#                             DELTA='6h')


"""
OUTPUT:

Metal device set to: Apple M1 Pro

systemMemory: 16.00 GB
maxCacheSize: 5.33 GB

2023-04-11 09:50:20.763628: W tensorflow/tsl/platform/profile_utils/cpu_utils.cc:128] Failed to get CPU frequency: 0 Hz
WARNING:absl:Found untraced functions such as _jit_compiled_convolution_op while saving (showing 1 of 1). These functions will not be directly callable after loading.
                     avgHighPrice  avgLowPrice  highPriceVolume  lowPriceVolume       average
timestamp                                                                                    
2023-04-04 00:00:00   419452531.0    417092217               53              65  4.181524e+08
2023-04-04 06:00:00   422033002.0    418189843               29              36  4.199045e+08
2023-04-04 12:00:00   422052934.0    418586926               36              44  4.201466e+08
2023-04-04 18:00:00   421522480.0    418734043               50              64  4.199570e+08
2023-04-05 00:00:00   420748527.0    418458669               52              54  4.195820e+08
2023-04-05 06:00:00   420239469.0    417530445               24              35  4.186324e+08
2023-04-05 12:00:00   419604058.0    417103312               39              49  4.182116e+08
2023-04-05 18:00:00   419830587.0    416143069               53              82  4.175908e+08
2023-04-06 00:00:00   420427331.0    417235090               57              60  4.187903e+08
2023-04-06 06:00:00   420474463.0    418487095               19              29  4.192738e+08
2023-04-06 12:00:00   420585430.0    418140134               43              40  4.194070e+08
2023-04-06 18:00:00   427511457.0    423346541               61              73  4.252425e+08
2023-04-07 00:00:00   427273079.0    423700571               64              61  4.255297e+08
2023-04-07 06:00:00   427249970.0    424319218               31              38  4.256359e+08
2023-04-07 12:00:00   429269887.0    426233075               47              57  4.276055e+08
2023-04-07 18:00:00   435976326.0    430959594               78              80  4.334362e+08
2023-04-08 00:00:00   435503213.0    433180950               51              75  4.341209e+08
2023-04-08 06:00:00   436541576.0    433727433               40              44  4.350675e+08
2023-04-08 12:00:00   436519816.0    433264584               59              73  4.347196e+08
2023-04-08 18:00:00   437073682.0    433633330               64              73  4.352405e+08
2023-04-09 00:00:00   437892200.0    433522873               68              86  4.354522e+08
2023-04-09 06:00:00   436524265.0    434484423               38              40  4.354782e+08
2023-04-09 12:00:00   434721277.0    431577208               45              48  4.330985e+08
2023-04-09 18:00:00   433693220.0    429312588               69              79  4.313549e+08
2023-04-10 00:00:00   429252779.0    426777847               58              81  4.278106e+08
2023-04-10 06:00:00   430353063.0    425308930               45              33  4.282190e+08
2023-04-10 12:00:00   430885909.0    427056157               57              63  4.288753e+08
2023-04-10 18:00:00   428029074.0    424751858               77              71  4.264569e+08
2023-04-11 00:00:00   423967008.0    421295542               62              45  4.228435e+08
2023-04-11 06:00:00   422366364.0    418491980               30              31  4.203974e+08
1/1 [==============================] - 0s 287ms/step
[[4.18507e+08]]
"""
