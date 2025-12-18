
import streamlit as st
import time
import random

# 设置页面配置，增加专业感
st.set_page_config(page_title="NutriSnap AI", layout="centered")

# 模拟健身冷知识库
TIPS = [
    "你知道吗？100g 熟鸡胸肉约含有 30g 蛋白质。",
    "减脂期间，摄入足够的纤维可以显著增加饱腹感。",
    "补剂只是辅助，整体饮食结构才是增肌的关键。",
    "训练后 30 分钟内摄入快速吸收的碳水有助于糖原恢复。"
]

def main():
    st.title("🍎 NutriSnap AI")
    st.caption("基于多模态 AI 的智能饮食分析系统")

    # 1. 模拟今日营养进度条（仪表盘）
    st.subheader("今日摄入进度")
    col1, col2, col3 = st.columns(3)
    # 模拟数据
    p_goal, c_goal, f_goal = 150, 200, 60
    p_current = 110 # 假设已经吃了一些
    
    col1.metric("蛋白质", f"{p_current}/{p_goal}g", f"-{p_goal-p_current}g")
    col2.metric("碳水", "120/200g", "-80g")
    col3.metric("脂肪", "45/60g", "-15g")

    # 2. 图片上传模块
    uploaded_file = st.file_uploader("拍摄或上传你的食物图片...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # 展示上传的图片
        st.image(uploaded_file, caption="待识别午餐", use_container_width=True)
        
        # 3. 异步加载效果：展示冷知识卡片
        with st.status("AI 正在解析图片语义...", expanded=True) as status:
            st.write("正在识别食物种类...")
            # 随机展示一条冷知识
            st.info(f"💡 健身小知识：{random.choice(TIPS)}")
            time.sleep(2) # 模拟 AI 运算时间
            st.write("正在估算营养密度...")
            time.sleep(1)
            status.update(label="识别完成！", state="complete", expanded=False)

        # 4. 识别结果与动态调整
        st.divider()
        st.success("识别结果：香煎鸡胸肉配西兰花")
        
        # 使用滑动条进行微调（装逼核心：交互感）
        weight = st.slider("估算重量 (g)", 50, 500, 200)
        
        # 动态计算逻辑
        protein = (weight / 100) * 30
        carbs = (weight / 100) * 5
        
        c1, c2 = st.columns(2)
        c1.markdown(f"**蛋白质:** {protein:.1f} g")
        c2.markdown(f"**碳水:** {carbs:.1f} g")

        # 5. 智能优化建议
        st.warning(f"🚀 **优化建议：** 你今日蛋白质缺口还有 {p_goal - (p_current + protein):.1f}g，建议下午加餐一份希腊酸奶。")

if __name__ == "__main__":
    main()
