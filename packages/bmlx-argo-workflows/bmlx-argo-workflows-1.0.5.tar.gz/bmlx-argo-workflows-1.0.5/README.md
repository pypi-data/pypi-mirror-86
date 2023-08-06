# Argo Workflows Python Client

Python client for Argo Workflows (bigo 内部使用版本)

![](https://github.com/argoproj-labs/argo-client-python/workflows/CI/badge.svg)


#### 为什么要维护bigo 内部的版本？  
    github上官方的版本的代码是使用官方的 openapi-generator-cli (https://github.com/OpenAPITools/openapi-generator)  自动生成  
    生成的代码中 openapi model 的 to_dict 函数产生的dict 如果直接去序列化到json，则无法被argo 的golang package 正确解析。  
    因此需要对官方版本的 to_dict 方法进行改写，从而可以让 bmlx client端产生的argo workflow的json 文件被bmlx api-server端正确解析。  

#### 开发  
  1. 本地需要在 /usr/local/openapi/ 目录下安装 openapi-generator-cli.jar (从 https://github.com/gtarcoder/openapi-generator 下载编译)  
  2. 本地修改代码之后，执行 make client 产生最新的sdk 代码  
  3. 修改 argo/workflows/client/__about__.py 中的 __version__ 为新的版本号  
  4. 将改动提交到远端，并触发CICD， CICD 会自动打包新的python package 并发布到私有 pypi 服务器  
   

#### 使用  
```bash
pip install bmlx-argo-workflows #(需要设置好私有pypi 源)  
```