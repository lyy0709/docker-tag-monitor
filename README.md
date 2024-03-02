# 蟑螂以及xyhelper大佬其他应用的docker监控

## 对接微信企业机器人防止连不上tg导致漏掉更新

## 部署方法

- docker一键部署

```bash
version: '3.8'
services:
  tag-monitor:
    image: lyy0709/docker-tag-monitor:latest
    volumes:
      - ./data:/data
    environment:
      - API_URLS=https://registry.hub.docker.com/v2/repositories/xyhelper/cockroachai/tags/,https://registry.hub.docker.com/v2/repositories/xyhelper/cdn-oaistatic/tags/
      - WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=企业微信机器人的token
    restart: unless-stopped
  
```

## API_URLS

- 对于Docker Hub上的公共镜像，Registry API的基本URL格式如下：

```bash
https://registry.hub.docker.com/v2/repositories/{username}/{imagename}/tags/
```

- 此脚本仅会获取最新版镜像tag为latest的更新，每半个小时监测一次，有更新则推送没有则继续循环
