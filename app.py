import streamlit as st
import time
import random
import os
import requests
import json

# 设置页面配置
st.set_page_config(page_title="NutriSnap AI", layout="wide", initial_sidebar_state="expanded")

# 模拟健身冷知识库
TIPS = [
    "你知道吗？100g 熟鸡胸肉约含有 30g 蛋白质。",
    "减脂期间,摄入足够的纤维可以显著增加饱腹感。",
    "补剂只是辅助,整体饮食结构才是增肌的关键。",
    "训练后 30 分钟内摄入快速吸收的碳水有助于糖原恢复。",
    "每日饮水量建议: 体重(kg) × 30-40ml",
    "优质脂肪来源: 鱼油、坚果、牛油果、橄榄油"
]

# ============= 营养计算工具函数 =============

def calculate_bmi(weight_kg, height_cm):
    """计算BMI"""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """BMI分类"""
    if bmi < 18.5:
        return "偏瘦", "🔵"
    elif 18.5 <= bmi < 24:
        return "正常", "🟢"
    elif 24 <= bmi < 28:
        return "偏重", "🟡"
    else:
        return "肥胖", "🔴"

def calculate_bmr(weight_kg, height_cm, age, gender):
    """计算基础代谢率 (Mifflin-St Jeor公式)"""
    if gender == "男":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:  # 女
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return round(bmr)

def calculate_tdee(bmr, activity_level):
    """计算每日总消耗 (TDEE)"""
    activity_factors = {
        "久坐 (几乎不运动)": 1.2,
        "轻度活动 (每周1-3次)": 1.375,
        "中度活动 (每周3-5次)": 1.55,
        "高度活动 (每周6-7次)": 1.725,
        "专业运动员": 1.9
    }
    return round(bmr * activity_factors[activity_level])

def calculate_macros(weight_kg, tdee, goal):
    """根据目标计算宏量营养素"""
    if goal == "增肌 💪":
        # 增肌: TDEE + 300-500, 高蛋白高碳水
        calories = tdee + 400
        protein = round(weight_kg * 2.2)  # 2.2g/kg
        fat = round((calories * 0.25) / 9)  # 25%来自脂肪
        carbs = round((calories - protein * 4 - fat * 9) / 4)
    elif goal == "减脂 🔥":
        # 减脂: TDEE - 300-500, 高蛋白低碳水
        calories = tdee - 400
        protein = round(weight_kg * 2.4)  # 2.4g/kg (保护肌肉)
        fat = round((calories * 0.25) / 9)  # 25%来自脂肪
        carbs = round((calories - protein * 4 - fat * 9) / 4)
    else:  # 维持 ⚖️
        calories = tdee
        protein = round(weight_kg * 1.8)  # 1.8g/kg
        fat = round((calories * 0.28) / 9)  # 28%来自脂肪
        carbs = round((calories - protein * 4 - fat * 9) / 4)
    
    return {
        "calories": calories,
        "protein": max(protein, 0),
        "carbs": max(carbs, 0),
        "fat": max(fat, 0)
    }

# ============= AI助手函数 =============

def call_ai_assistant(user_message, context):
    """调用AI助手 (使用Groq免费API或Mock)"""
    api_key = os.getenv("GROQ_API_KEY", "")
    
    # 如果没有API key,使用Mock响应
    if not api_key or api_key == "your_api_key_here":
        return mock_ai_response(user_message, context)
    
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = f"""你是一个专业的营养师助手。用户当前信息：
- 今日目标: 蛋白质{context['protein_goal']}g, 碳水{context['carbs_goal']}g, 脂肪{context['fat_goal']}g
- 已摄入: 蛋白质{context['protein_current']}g, 碳水{context['carbs_current']}g, 脂肪{context['fat_current']}g
- 还需: 蛋白质{context['protein_gap']}g, 碳水{context['carbs_gap']}g, 脂肪{context['fat_gap']}g

请提供实用、具体的食物建议,包括食物名称和大致营养含量。回答要简洁、友好、中文。"""

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    except Exception as e:
        return f"AI助手暂时不可用。错误: {str(e)}\n\n使用Mock建议: {mock_ai_response(user_message, context)}"

def mock_ai_response(user_message, context):
    """Mock AI响应 (当API不可用时)"""
    protein_gap = context['protein_gap']
    location = ""
    
    # 简单的关键词检测
    if "红旗" in user_message or "在哪" in user_message:
        location = "红旗区域"
    
    suggestions = []
    
    if protein_gap > 100:
        suggestions.append("🥩 瘦牛肉200g (约42g蛋白质)")
        suggestions.append("🍗 鸡胸肉250g (约60g蛋白质)")
        suggestions.append("🥚 鸡蛋5个 (约30g蛋白质)")
    elif protein_gap > 50:
        suggestions.append("🐟 三文鱼150g (约30g蛋白质)")
        suggestions.append("🍗 鸡胸肉150g (约36g蛋白质)")
    elif protein_gap > 20:
        suggestions.append("🥛 希腊酸奶200g (约20g蛋白质)")
        suggestions.append("🥚 鸡蛋3个 (约18g蛋白质)")
    else:
        suggestions.append("✅ 你的蛋白质摄入已经接近目标!")
    
    response = f"基于你还需{protein_gap}g蛋白质的情况,我建议:\n\n"
    response += "\n".join(suggestions)
    
    if location:
        response += f"\n\n📍 在{location},你可以去附近超市或健身餐店购买这些食材。"
    
    return response

# ============= 主应用 =============

def main():
    st.title("🍎 NutriSnap AI")
    st.caption("基于多模态 AI 的智能饮食分析系统")
    
    # 初始化session state
    if 'profile_set' not in st.session_state:
        st.session_state.profile_set = False
    if 'protein_current' not in st.session_state:
        st.session_state.protein_current = 0
    if 'carbs_current' not in st.session_state:
        st.session_state.carbs_current = 0
    if 'fat_current' not in st.session_state:
        st.session_state.fat_current = 0
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # 创建标签页
    tab1, tab2, tab3 = st.tabs(["👤 个人资料", "📊 营养追踪", "🤖 AI助手"])
    
    # ========== Tab 1: 个人资料 ==========
    with tab1:
        st.header("个人信息")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox("性别", ["男", "女"])
            age = st.number_input("年龄", min_value=10, max_value=100, value=25)
            weight = st.number_input("体重 (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
        
        with col2:
            height = st.number_input("身高 (cm)", min_value=100, max_value=250, value=170)
            activity = st.selectbox("活动水平", 
                ["久坐 (几乎不运动)", "轻度活动 (每周1-3次)", "中度活动 (每周3-5次)", 
                 "高度活动 (每周6-7次)", "专业运动员"])
            goal = st.selectbox("健身目标", ["增肌 💪", "减脂 🔥", "维持 ⚖️"])
        
        # 实时BMI计算
        st.divider()
        st.subheader("健康指标")
        
        bmi = calculate_bmi(weight, height)
        category, emoji = get_bmi_category(bmi)
        
        col_bmi1, col_bmi2, col_bmi3 = st.columns(3)
        col_bmi1.metric("BMI指数", f"{bmi}", help="体重指数")
        col_bmi2.metric("体型分类", f"{emoji} {category}")
        
        # 计算营养目标
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, activity)
        macros = calculate_macros(weight, tdee, goal)
        
        col_bmi3.metric("每日消耗", f"{tdee} kcal", help="TDEE")
        
        st.divider()
        st.subheader("每日营养目标")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("总热量", f"{macros['calories']} kcal")
        col_m2.metric("🥩 蛋白质", f"{macros['protein']} g")
        col_m3.metric("🍚 碳水", f"{macros['carbs']} g")
        col_m4.metric("🥑 脂肪", f"{macros['fat']} g")
        
        # 保存到session
        if st.button("✅ 保存个人资料", type="primary", use_container_width=True):
            st.session_state.profile_set = True
            st.session_state.weight = weight
            st.session_state.height = height
            st.session_state.age = age
            st.session_state.gender = gender
            st.session_state.activity = activity
            st.session_state.goal = goal
            st.session_state.macros = macros
            st.session_state.tdee = tdee
            st.session_state.bmi = bmi
            st.success("✅ 个人资料已保存!")
    
    # ========== Tab 2: 营养追踪 ==========
    with tab2:
        if not st.session_state.profile_set:
            st.warning("⚠️ 请先在 **个人资料** 标签页设置你的信息")
        else:
            st.header("今日营养摄入")
            
            # 获取目标
            macros = st.session_state.macros
            p_goal = macros['protein']
            c_goal = macros['carbs']
            f_goal = macros['fat']
            
            # 当前摄入
            p_current = st.session_state.protein_current
            c_current = st.session_state.carbs_current
            f_current = st.session_state.fat_current
            
            # 进度条
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🥩 蛋白质", f"{p_current}/{p_goal}g", 
                         delta=f"{p_current - p_goal}g" if p_current >= p_goal else f"-{p_goal - p_current}g")
                st.progress(min(p_current / p_goal, 1.0))
            
            with col2:
                st.metric("🍚 碳水", f"{c_current}/{c_goal}g",
                         delta=f"{c_current - c_goal}g" if c_current >= c_goal else f"-{c_goal - c_current}g")
                st.progress(min(c_current / c_goal, 1.0))
            
            with col3:
                st.metric("🥑 脂肪", f"{f_current}/{f_goal}g",
                         delta=f"{f_current - f_goal}g" if f_current >= f_goal else f"-{f_goal - f_current}g")
                st.progress(min(f_current / f_goal, 1.0))
            
            st.divider()
            
            # 食物识别模块
            st.subheader("📸 拍摄或上传食物")
            uploaded_file = st.file_uploader("选择图片...", type=["jpg", "png", "jpeg"])
            
            if uploaded_file is not None:
                # 展示上传的图片
                st.image(uploaded_file, caption="待识别食物", use_container_width=True)
                
                # 模拟AI识别
                with st.status("AI 正在解析图片语义...", expanded=True) as status:
                    st.write("正在识别食物种类...")
                    st.info(f"💡 健身小知识: {random.choice(TIPS)}")
                    time.sleep(1.5)
                    st.write("正在估算营养密度...")
                    time.sleep(1)
                    status.update(label="✅ 识别完成!", state="complete", expanded=False)
                
                # 识别结果
                st.divider()
                st.success("🍗 识别结果: 香煎鸡胸肉配西兰花")
                
                # 重量调整
                weight_food = st.slider("估算重量 (g)", 50, 500, 200)
                
                # 动态计算 (假设鸡胸肉: 100g = 30g蛋白, 5g碳水, 3g脂肪)
                protein_food = round((weight_food / 100) * 30, 1)
                carbs_food = round((weight_food / 100) * 5, 1)
                fat_food = round((weight_food / 100) * 3, 1)
                
                col_n1, col_n2, col_n3 = st.columns(3)
                col_n1.markdown(f"**🥩 蛋白质:** {protein_food} g")
                col_n2.markdown(f"**🍚 碳水:** {carbs_food} g")
                col_n3.markdown(f"**🥑 脂肪:** {fat_food} g")
                
                # 添加到今日摄入
                if st.button("➕ 添加到今日摄入", type="primary"):
                    st.session_state.protein_current += protein_food
                    st.session_state.carbs_current += carbs_food
                    st.session_state.fat_current += fat_food
                    st.success("✅ 已添加到今日摄入!")
                    st.rerun()
                
                # 智能建议
                p_gap = p_goal - st.session_state.protein_current
                if p_gap > 0:
                    st.warning(f"💡 **优化建议:** 你今日蛋白质缺口还有 {p_gap:.1f}g,建议下午加餐一份希腊酸奶或蛋白粉。")
                else:
                    st.success(f"🎉 **太棒了!** 你今日蛋白质摄入已达标!")
    
    # ========== Tab 3: AI助手 ==========
    with tab3:
        st.header("🤖 AI营养助手")
        
        if not st.session_state.profile_set:
            st.warning("⚠️ 请先在 **个人资料** 标签页设置你的信息")
        else:
            # 显示当前营养缺口
            macros = st.session_state.macros
            p_gap = max(macros['protein'] - st.session_state.protein_current, 0)
            c_gap = max(macros['carbs'] - st.session_state.carbs_current, 0)
            f_gap = max(macros['fat'] - st.session_state.fat_current, 0)
            
            st.info(f"📊 **当前营养缺口:** 蛋白质 {p_gap:.0f}g | 碳水 {c_gap:.0f}g | 脂肪 {f_gap:.0f}g")
            
            # 聊天界面
            st.subheader("💬 与AI助手对话")
            
            # 显示聊天历史
            for msg in st.session_state.chat_history:
                if msg['role'] == 'user':
                    st.markdown(f"**🧑 你:** {msg['content']}")
                else:
                    st.markdown(f"**🤖 AI:** {msg['content']}")
                st.divider()
            
            # 输入框
            user_input = st.text_input("输入你的问题...", 
                                      placeholder="例如: 我在红旗,今天差150g蛋白质,你建议我要买点什么吃?",
                                      key="user_input")
            
            col_send1, col_send2 = st.columns([1, 5])
            with col_send1:
                send_button = st.button("发送", type="primary", use_container_width=True)
            with col_send2:
                if st.button("清除对话", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
            
            if send_button and user_input:
                # 添加用户消息
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input
                })
                
                # 准备上下文
                context = {
                    'protein_goal': macros['protein'],
                    'carbs_goal': macros['carbs'],
                    'fat_goal': macros['fat'],
                    'protein_current': st.session_state.protein_current,
                    'carbs_current': st.session_state.carbs_current,
                    'fat_current': st.session_state.fat_current,
                    'protein_gap': p_gap,
                    'carbs_gap': c_gap,
                    'fat_gap': f_gap
                }
                
                # 调用AI
                with st.spinner("AI思考中..."):
                    ai_response = call_ai_assistant(user_input, context)
                
                # 添加AI响应
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response
                })
                
                st.rerun()
            
            # 快捷问题
            st.divider()
            st.subheader("💡 快捷提问")
            
            quick_questions = [
                f"我今天还差{p_gap:.0f}g蛋白质,推荐吃什么?",
                "增肌期间晚上可以吃什么?",
                "减脂可以吃哪些零食?",
                "训练后应该吃什么?"
            ]
            
            cols = st.columns(2)
            for i, q in enumerate(quick_questions):
                if cols[i % 2].button(q, use_container_width=True, key=f"quick_{i}"):
                    # 模拟用户输入快捷问题
                    st.session_state.chat_history.append({'role': 'user', 'content': q})
                    context = {
                        'protein_goal': macros['protein'],
                        'carbs_goal': macros['carbs'],
                        'fat_goal': macros['fat'],
                        'protein_current': st.session_state.protein_current,
                        'carbs_current': st.session_state.carbs_current,
                        'fat_current': st.session_state.fat_current,
                        'protein_gap': p_gap,
                        'carbs_gap': c_gap,
                        'fat_gap': f_gap
                    }
                    ai_response = call_ai_assistant(q, context)
                    st.session_state.chat_history.append({'role': 'assistant', 'content': ai_response})
                    st.rerun()

if __name__ == "__main__":
    main()
