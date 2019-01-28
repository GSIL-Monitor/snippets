#!/bin/bash
set -ex
ROOT=$(cd $(dirname $0) > /dev/null; pwd)

# 更新代码
if [[ ! -d "$ROOT/diablo" ]]; then
  git clone ssh://git@git.corp.qianka.com/v4/diablo
fi
cd $ROOT/diablo
git fetch --all --prune
git reset --hard origin/master
rev=$(git rev-parse --short HEAD)

# 安装依赖
npm install yarn
node_modules/.bin/yarn

# 打包
npm run build

# TODO: 清理历史数据
# 思路：
# 0x00 每次打包完回去当前版本，并记录到某个历史文件中
# 0x01 根据保留的份数等配置，遍历并删除多余的文件
# 0x02 最后更新版本历史记录文件

# 制作docker镜像
cd $ROOT
docker build -t diablo:$rev .
docker tag diablo:$rev registry.cn-hangzhou.aliyuncs.com/qianka/diablo:$rev
docker tag diablo:$rev registry.cn-hangzhou.aliyuncs.com/qianka/diablo:latest
docker push registry.cn-hangzhou.aliyuncs.com/qianka/diablo:$rev
docker push registry.cn-hangzhou.aliyuncs.com/qianka/diablo:latest
