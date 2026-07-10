# Agent Town

## 项目目标

构建一个像素风格的 **Agent 协作社区**，多个 AI Agent 在一个共享的像素办公室场景中实时协作、展示状态、互动。

## 技术栈

| 层       | 选型                               | 说明                          |
| -------- | ---------------------------------- | ----------------------------- |
| 框架     | Next.js 16 + React 19 + TypeScript | 全栈 JS/TS，前后端统一        |
| UI 组件  | Tailwind CSS 4 + 自定义 pixel HUD  | 控制面板、配置界面等非游戏 UI |
| 游戏引擎 | Phaser 3                           | 像素场景渲染、精灵动画、交互  |
| 实时通信 | WebSocket 或 SSE                   | 不用轮询                      |
| 后端 API | Next.js API Routes                 | 状态管理、Agent 生命周期      |
| 包管理   | pnpm                               | 已配置                        |

## 素材资源

素材应放在本仓库可引用路径下（例如 `agent-town/public/` 下的 tilesets/sprites）。若从 itch.io **LimeZu Modern** 等包导入，请在本地解压并重新导出 Tiled，使 JSON 中的 `image` 指向 `public/` 相对路径（勿提交指向其他用户主目录的绝对路径）。

### 素材清单

| 素材包                      | 路径                                   | 用途                                |
| --------------------------- | -------------------------------------- | ----------------------------------- |
| Modern Office Revamped v1.2 | `Modern_Office_Revamped_v1.2/`         | 核心办公室素材                      |
| Modern Interiors 完整版     | `moderninteriors-win/`                 | 309 个动画物件 + 室内家具/地板/墙壁 |
| Modern Exteriors            | `modernexteriors-win/`                 | 室外场景（备用）                    |
| Modern tiles Free           | `Modern tiles_Free/`                   | 免费角色素材 + 基础室内             |
| Character Generator 2.0     | `Character Generator 2.0 Linux Build/` | 角色生成器                          |

### 推荐尺寸

使用 **48x48** tile，画布 1280x720。

### 关键素材路径

```
# 房间骨架 tileset（墙壁/地板/门窗）
Modern_Office_Revamped_v1.2/1_Room_Builder_Office/Room_Builder_Office_48x48.png

# 办公家具 tileset
Modern_Office_Revamped_v1.2/Modern_Office_48x48.png

# 办公家具单件透明 PNG
Modern_Office_Revamped_v1.2/4_Modern_Office_singles/48x48/

# 设计参考（完整办公室布局示例）
Modern_Office_Revamped_v1.2/6_Office_Designs/Office_Design_1.gif
Modern_Office_Revamped_v1.2/6_Office_Designs/Office_Design_2.gif

# 通用室内 tileset
moderninteriors-win/1_Interiors/48x48/

# 动画物件精灵表（309 个）
moderninteriors-win/3_Animated_objects/48x48/spritesheets/

# 角色素材
moderninteriors-win/2_Characters/
```

### 素材使用须知

- 不需要 Aseprite — 所有精灵表、单件图、tileset 已切好
- 不需要 TexturePacker — spritesheet 现成可用
- 用 **Tiled Map Editor** 可视化拼装场景

## 场景拼装工作流

```
1. Tiled 里用 Room_Builder_Office_48x48.png 铺房间骨架
2. Tiled 对象层摆放家具（桌椅电脑装饰）
3. 导出 Tiled JSON → public/maps/
4. Phaser 加载 tilemap + 对象层
5. 代码加载 animated spritesheets（动态物件）
6. 加 Agent 逻辑
```

## 项目结构（与仓库一致，2026-07）

```
agent-town/
├── app/
│   ├── page.tsx
│   ├── layout.tsx
│   ├── globals.css
│   └── api/
│       ├── agents/discover/route.ts   # GET 发现 agent / 配置（path-safety）
│       └── internal/seat-sync/route.ts
├── server.ts                    # 开发：Next + WebSocket 代理到 Gateway
├── server.prod.mjs              # 生产：standalone（attachWsProxy(server, url) / attachAuggieBridge(server)）
├── lib/
│   ├── ws-proxy.ts / ws-proxy.mjs     # pnpm build:ws-proxy
│   ├── auggie-bridge.ts / .mjs        # pnpm build:auggie-bridge
│   ├── ws-origin.ts, path-safety.ts   # helpers testeables
│   ├── gateway.ts, store.ts, hooks/, …
│   └── __tests__/               # 6 suites Vitest（+ path-safety, ws-origin）
├── components/
│   ├── game/                    # Phaser（PhaserGame.tsx, scenes/, …）
│   ├── hud/, panel/, …
├── public/maps/
├── docs/THREAT_MODEL_GATEWAY_TOKEN.md
└── types/
```

WebSocket 浏览器 → `/api/gateway`（见 `lib/ws-proxy.ts`），非旧版 `app/api/ws/route.ts`。
`pnpm build` = `next build` + `build:ws-proxy` + `build:auggie-bridge`。

## Phaser 集成要点

- Phaser 依赖浏览器 API，必须用 `next/dynamic` + `ssr: false`
- 在 `useEffect` 中创建 Phaser.Game 实例，return 中销毁
- 场景逻辑写在独立 .ts 文件，不混入 React 组件

## 编码规范

- TypeScript 严格模式（已启用）
- 场景状态用 class 或模块封装，禁止全局变量和 window.\* 挂载
- 动画帧数、时间间隔等参数统一放配置文件，不散布在代码中
- 环境变量管理密钥，不硬编码
- React 组件天然防 XSS，不使用 dangerouslySetInnerHTML

## 开发顺序

1. 集成 Phaser 到 Next.js — 跑通空白 canvas
2. 加载 Tiled 地图 — 渲染基础办公室场景
3. Agent 状态 API — Next.js API Routes
4. 实时推送 — WebSocket/SSE
5. 角色动画 — Agent 在场景中移动、状态切换
6. 控制面板 — pixel HUD 管理界面
