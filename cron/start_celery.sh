#!/usr/bin/env bash
# flower 用于监视和管理celery集群的web工具
celery flower --broker=redis://localhost:6379
