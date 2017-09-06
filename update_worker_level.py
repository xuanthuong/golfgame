# -*- coding: utf-8 -*-
# Description: update workers levels from CFD table
# By Thuong.Tran
# Date: 05 Sept. 2017


def get_finalized_process(today, worker):
  pass

def update_levels(worker):
  finalized_proc = get_finalized_process(today, worker)
  for proc in finalized_proc:
    update(worker, proc)

def update(worker):
  pass