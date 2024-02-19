# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3.10
#     language: python
#     name: py310
# ---

# %%
# %load_ext autoreload
# %autoreload 2

# %%
from backtester.event import MarketEvent, SignalEvent

# %%
event_test = MarketEvent()
print(event_test.type)

# %%
