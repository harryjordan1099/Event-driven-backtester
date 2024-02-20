# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3.9
#     language: python
#     name: py39
# ---

# %%
# %load_ext autoreload
# %autoreload 2

# %%
import queue


from backtester.data import HistoricCSVDataHandler

# %%
events = queue.Queue()
test_data_handler = HistoricCSVDataHandler(events, "/notebooks/Event-driven-backtester/data", ["BTC-USD"])

# %%
