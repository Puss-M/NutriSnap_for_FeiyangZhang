# 🍎 NutriSnap AI

基于多模态 AI 的智能饮食分析系统

## 功能特点

- 📸 **智能食物识别**：上传食物图片，AI 自动识别食物种类
- 📊 **营养分析**：实时计算蛋白质、碳水、脂肪含量
- 🎯 **每日追踪**：可视化展示今日营养摄入进度
- 💡 **健身小知识**：分析过程中展示专业健身营养知识
- ⚖️ **重量调整**：使用滑动条微调食物重量，动态更新营养数据

## 在线演示

🌐 部署在 Streamlit Cloud 上，无需本地安装即可使用！

访问链接：`https://your-app.streamlit.app`（部署后更新此链接）

## 本地运行

如果您想在本地运行此应用：

1. 克隆仓库：

   ```bash
   git clone https://github.com/your-username/nutrisnap-ai.git
   cd nutrisnap-ai
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 运行应用：

   ```bash
   streamlit run app.py
   ```

4. 在浏览器中访问 `http://localhost:8501`

## 技术栈

- **Framework**: Streamlit
- **Language**: Python 3.10+
- **Dependencies**: 见 `requirements.txt`

## 项目结构

```
nutrisnap-ai/
├── app.py              # 主应用文件
├── requirements.txt    # Python 依赖
└── README.md          # 项目说明
```

## 使用说明

1. 打开应用后，查看今日营养摄入进度
2. 点击 "拍摄或上传你的食物图片..." 上传食物照片
3. AI 会自动识别食物并显示冷知识
4. 查看识别结果和营养成分
5. 使用滑动条调整食物重量（如需要）
6. 获取智能优化建议

## License

MIT License

## 作者

NutriSnap AI Demo
