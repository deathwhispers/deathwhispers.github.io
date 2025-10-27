---
layout: post
title: "常用的 Docker 命令"
date: 2025-10-25
tags:
  - Docker
categories:
  []
comments: true
math: true
mermaid: true
author: deathwhispers
---

# Docker 常用命令大全

## Docker 基础命令

- 新装 Docker 环境后，执行 docker run hello-world 验证运行是否正常；

- 使用 docker info | grep "Storage Driver" 检查存储驱动（overlay2 / aufs）；

- 使用 docker system df 检查镜像和卷的磁盘占用。

## 镜像（Image）管理

```bash
# 拉取常用镜像
docker pull ubuntu:20.04
docker pull nginx:latest

# 构建自定义镜像
docker build -t myapp:1.0 .

# 查看镜像分层信息
docker history myapp:1.0
```

- 构建企业内网镜像：

- 清理老旧镜像：

- 对比镜像大小与缓存层，定位构建优化点。

## 容器（Container）管理

```bash
# 运行容器（后台 + 端口映射 + 命名）
docker run -d -p 8080:80 --name web nginx

# 实时进入容器终端
docker exec -it web bash

# 查看容器日志（实时滚动）
docker logs -f web

# 停止、启动、删除容器
docker stop web
docker start web
docker rm web
```

实战场景：

1️⃣ 部署一个测试环境：

```bash
docker run -d --name mysql-dev \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -p 3306:3306 \
  mysql:8.0
```

👉 用于本地开发测试数据库。

2️⃣ 启动前端 + 后端容器：

```bash
docker run -d --name api -p 8080:8080 my-api:v1
docker run -d --name web -p 80:80 -e API_URL=http://localhost:8080 my-web:v1
```

3️⃣ 容器故障排查：

```bash
docker exec -it api bash
cat /var/log/app/error.log
```

## 数据卷（Volumes）与挂载

- 持久化数据库：容器删除后数据仍保留；

- 开发映射：

- 备份卷数据：

## 网络（Networks）

实战场景：

1️⃣ 自定义网络实现容器互通：

```bash
docker network create backend_net

docker run -d --name db --network backend_net mysql:8.0
docker run -d --name app --network backend_net -e DB_HOST=db myapp:v1
```

> 👉 app 可直接通过主机名 db 访问数据库，无需暴露端口。

2️⃣ 快速排查网络问题：

```bash
docker exec -it app ping db
docker exec -it app curl http://db:3306
```

## 容器文件与交互调试

## 🧩 七、Docker Compose 常用命令

docker-compose.yml 示例

```yaml
version: "3.9"
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: 123456
    volumes:
      - dbdata:/var/lib/mysql
  web:
    image: nginx
    ports:
      - "8080:80"
    depends_on:
      - db
volumes:
  dbdata:
```

常用命令：

```bash
docker compose up -d
docker compose down
docker compose logs -f
docker compose exec web bash
```

- 一键启动完整开发环境：docker compose up -d

- 在 CI/CD 流程中部署测试服务；

- 自动清理旧网络与卷：docker compose down -v

## 系统级清理命令（慎用）

```bash
# 清理未使用资源
docker system prune -a

# 删除所有停止的容器
docker rm $(docker ps -aq -f status=exited)

# 删除所有悬空镜像
docker rmi $(docker images -q -f dangling=true)
```

实战技巧：

- 每次构建大镜像前执行 docker system df 查看磁盘空间；

- 在 CI 环境中可自动清理临时镜像，避免 runner 宕机。

> 💀 提示： 这些命令不可逆，请务必确认后再执行！

## 🧭 九、实用技巧与组合命令

```bash
# 查看最近启动的容器日志
docker logs $(docker ps -lq)

# 删除所有已退出的容器
docker rm $(docker ps -aq -f status=exited)

# 删除所有悬空镜像
docker rmi $(docker images -q -f dangling=true)

# 一键停止所有容器
docker stop $(docker ps -q)

# 一键删除所有容器
docker rm $(docker ps -aq)
```

## 参考文档

- Docker 官方文档

- Docker Compose 规范

- Docker 命令手册 (cheat sheet)