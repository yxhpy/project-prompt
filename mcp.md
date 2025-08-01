# Model Context Protocol (MCP) 文档

## 什么是 MCP？

Model Context Protocol（模型上下文协议）是一种开放协议，旨在标准化大型语言模型（LLM）与外部数据源、工具和服务之间的交互方式。<mcreference link="https://zhuanlan.zhihu.com/p/29001189476" index="1">1</mcreference> <mcreference link="https://www.runoob.com/np/mcp-protocol.html" index="2">2</mcreference>

## MCP 的主要作用

### 1. 统一接口标准
MCP 就像 USB-C 一样，为不同设备提供统一的连接接口。<mcreference link="https://www.runoob.com/np/mcp-protocol.html" index="2">2</mcreference> 它使得开发者能够以一致的方式将各种数据源、工具和功能连接到 AI 模型，创建一个通用标准，使 AI 应用程序的开发和集成变得更加简单和统一。<mcreference link="https://zhuanlan.zhihu.com/p/29001189476" index="1">1</mcreference>

### 2. 解决数据孤岛问题
在没有 MCP 之前，我们需要人工从数据库中筛选信息，手动粘贴到 prompt 中。<mcreference link="https://zhuanlan.zhihu.com/p/29001189476" index="1">1</mcreference> MCP 通过标准化模型与外部资源的交互方式，提升 LLM 应用的功能性、灵活性和可扩展性。<mcreference link="https://www.runoob.com/np/mcp-protocol.html" index="2">2</mcreference>

### 3. 核心优势
- **生态丰富**：MCP 提供很多现成的插件，AI 可以直接使用
- **统一性**：不限制于特定的 AI 模型，任何支持 MCP 的模型都可以灵活切换
- **数据安全**：敏感数据留在本地，不必全部上传
- **功能扩展**：通过集成外部资源，显著扩展 LLM 应用的功能<mcreference link="https://zhuanlan.zhihu.com/p/29001189476" index="1">1</mcreference>

## MCP 架构

MCP 采用客户端-服务器架构，由三个核心组件构成：<mcreference link="https://blog.csdn.net/ZYC88888/article/details/146414158" index="3">3</mcreference>

### 1. Host（主机）
- 期望从服务器获取数据的 AI 应用（如 IDE、聊天机器人等）
- 负责初始化和管理客户端、处理用户授权、管理上下文聚合

### 2. Client（客户端）
- 主机与服务器之间的桥梁
- 与服务器保持一对一连接
- 负责消息路由、能力管理、协议协商和订阅管理

### 3. Server（服务器）
- 提供外部数据和工具的组件
- 通过工具、资源和提示模板为大型语言模型提供额外的上下文和功能

## 通信协议

MCP 使用 JSON-RPC 2.0 作为消息格式，定义了三种基本消息类型：<mcreference link="https://www.runoob.com/np/mcp-protocol.html" index="2">2</mcreference>

1. **请求（Requests）**：用于从客户端向服务器发起操作
2. **响应（Responses）**：对请求的答复
3. **通知（Notifications）**：单向消息，不需要接收方回复

## MCP 服务器配置示例

以下是一些常用的 MCP 服务器配置：

### 时间服务器
```json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": [
        "mcp-server-time"
      ]
    }
  }
}
```

### 顺序思考服务器
```json
{
  "mcpServers": {
    "Sequential Thinking": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ],
      "env": {}
    }
  }
}
```

### Context7 文档服务器
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": [
        "-y",
        "@upstash/context7-mcp@latest"
      ],
      "env": {
        "DEFAULT_MINIMUM_TOKENS": "10000"
      }
    }
  }
}
```

### Puppeteer 浏览器自动化服务器
```json
{
  "mcpServers": {
    "Puppeteer": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-puppeteer"
      ],
      "env": {}
    }
  }
}
```

## 总结

MCP 作为一种标准化协议，为 AI 模型与外部数据源和工具提供了统一的连接接口，简化了 AI 应用开发的复杂性，提高了开发效率。<mcreference link="https://blog.csdn.net/ZYC88888/article/details/146414158" index="3">3</mcreference> 通过模块化设计和标准化接口，MCP 支持多种传输方式和安全机制，适用于多种场景，是构建现代 AI 应用的重要基础设施。