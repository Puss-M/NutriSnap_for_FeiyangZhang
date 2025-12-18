# NutriSnap PWA 安装指南

## 🎉 恭喜！NutriSnap 现已支持 PWA

NutriSnap 已经成功转换为 Progressive Web App (PWA)。你现在可以将它安装到设备的主屏幕上，像使用原生应用一样使用它！

## 📱 如何安装

### Android (Chrome/Edge)

1. 在 Chrome 或 Edge 浏览器中打开 NutriSnap
2. 点击地址栏右侧的**安装**图标 (📥)
3. 或者在浏览器菜单中选择 "**添加到主屏幕**" 或 "**安装应用**"
4. 确认安装，应用图标会出现在主屏幕上

### iOS (Safari)

1. 在 Safari 浏览器中打开 NutriSnap
2. 点击底部的**分享**按钮 (□↑)
3. 滚动找到 "**添加到主屏幕**"
4. 点击 "**添加**"，应用图标会出现在主屏幕上

### Windows/Mac (Chrome/Edge)

1. 在 Chrome 或 Edge 浏览器中打开 NutriSnap
2. 点击地址栏右侧的**安装**图标 (⊕)
3. 或者在浏览器菜单中选择 "**安装 NutriSnap AI**"
4. 应用会作为独立窗口打开，并出现在开始菜单/应用程序中

## ✨ PWA 功能

- ✅ **快速访问**: 从主屏幕直接启动，无需打开浏览器
- ✅ **独立窗口**: 应用在独立窗口中运行，提供类原生应用体验
- ✅ **离线缓存**: 静态资源自动缓存，加载速度更快
- ✅ **推送通知**: (未来功能) 接收营养目标提醒
- ✅ **自动更新**: Service Worker 自动更新，始终使用最新版本

## 🚀 启动应用

### 本地开发

```bash
streamlit run app.py
```

然后在浏览器中打开 `http://localhost:8501`

### 部署到 Streamlit Cloud

1. 推送代码到 GitHub
2. 在 Streamlit Cloud 连接你的仓库
3. 部署后访问你的应用 URL
4. 按照上面的安装步骤将应用添加到主屏幕

## 📂 PWA 文件结构

```
NutriSnap/
├── app.py                      # 主应用 (已添加 PWA 支持)
├── manifest.json               # PWA 清单文件
├── sw.js                       # Service Worker 脚本
├── .streamlit/
│   └── config.toml            # Streamlit 配置 (主题颜色)
└── static/
    └── icons/
        ├── icon-192x192.png   # Android/Chrome 小图标
        ├── icon-512x512.png   # Android/Chrome 大图标
        └── apple-touch-icon.png  # iOS 图标
```

## 🔧 技术细节

- **Manifest**: 定义应用名称、图标、主题颜色等
- **Service Worker**: 缓存策略 (静态资源 Cache-First，动态内容 Network-First)
- **Meta 标签**: 支持 iOS Safari 和其他浏览器的 PWA 功能
- **主题颜色**: 清新绿色 (#10b981) 代表健康营养

## ⚠️ 注意事项

1. **网络依赖**: Streamlit 应用依赖 WebSocket 连接，完全离线时功能会受限
2. **HTTPS 要求**: PWA 需要 HTTPS (本地开发时除外)
3. **浏览器支持**: 最佳体验推荐 Chrome、Edge 或 Safari
4. **静态资源**: Service Worker 会缓存静态资源，更新图标时可能需要手动清除缓存

## 🐛 故障排除

### Service Worker 未注册

- 打开浏览器开发者工具 → Application → Service Workers
- 检查是否有错误信息
- 尝试取消注册并重新注册

### 安装按钮未显示

- 确保使用支持 PWA 的浏览器
- 确保应用通过 HTTP/HTTPS 访问 (不是 file://)
- 检查 manifest.json 是否正确加载

### 离线不工作

- 检查 Service Worker 是否正在运行
- 查看缓存存储是否包含必要的资源
- 刷新页面让 Service Worker 更新缓存

## 📞 反馈

如有问题或建议，请提交 Issue 或 Pull Request！
