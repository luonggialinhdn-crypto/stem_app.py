import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

st.set_page_config(
    page_title="STEM: Thiết kế sân thể thao tối ưu",
    layout="wide",
    page_icon="🏟️"
)

st.markdown("""
<style>
.main { background-color: #f5f7f9; }
h1 { color: #1E3A8A; font-weight: bold; }
.stMetric { background-color: #ffffff; border-radius: 10px; padding: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Cấu hình thiết kế")
    P = st.number_input("Nhập tổng chu vi sân (m):", min_value=10, max_value=500, value=100)
    st.info("💡 Chu vi cố định giúp tối ưu chi phí vật liệu làm hàng rào.")
    
    L_test = st.slider("Điều chỉnh chiều dài L (m)", 1.0, float(P/2 - 1.0), float(P/4))
    W_test = P/2 - L_test
    S_test = L_test * W_test

st.title("🏟️ Thiết kế Sân Thể thao Tối ưu")
st.caption("Dự án STEM - Trường THCS Trưng Vương | Năm học 2025-2026")

tab1, tab2, tab3 = st.tabs(["📊 Mô phỏng & Tối ưu", "📖 Cơ sở khoa học", "💰 Dự toán chi phí"])

with tab1:
    L_opt = P / 4
    S_max = L_opt ** 2
    col1, col2, col3 = st.columns(3)

    col1.metric("Chiều dài (L)", f"{L_test:.2f} m")
    col2.metric("Chiều rộng (W)", f"{W_test:.2f} m")
    col3.metric("Diện tích", f"{S_test:.2f} m²", delta=f"{S_test - S_max:.2f} m²")

    if abs(S_test - S_max) < 0.1:
        st.success("🎯 Tuyệt vời! Kích thước này đạt diện tích tối ưu (Hình vuông).")
    
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Biến thiên diện tích")
        x_graph = np.linspace(0, P/2, 200)
        y_graph = x_graph * (P/2 - x_graph)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_graph, y_graph, color="#3b82f6", linewidth=2, label="Diện tích S")
        ax.scatter([L_test], [S_test], color="#f59e0b", s=100, zorder=5, label="Điểm đang chọn")
        ax.scatter([L_opt], [S_max], color="#ef4444", marker="*", s=200, zorder=5, label="Điểm tối ưu")

        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '' if x == 0 else f'{x:g}'))
        
        ax.set_xlabel("Chiều dài (m)", loc='right', fontsize=9)
        ax.set_ylabel("Diện tích (m²)", loc='top', fontsize=9)
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.legend(
            loc='upper right', 
            fontsize=9, 
            labelspacing=1.2, 
            handletextpad=0.8, 
            markerscale=0.8,  
            borderpad=0.6       
        )
        st.pyplot(fig)

    with c2:
        st.subheader("Bản vẽ mô phỏng sân")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        
        rect = plt.Rectangle((0, 0), L_test, W_test, color="#10b981", alpha=0.7, ec="#064e3b", lw=2)
        ax2.add_patch(rect)

        ax2.axis('off') 
        
        margin = max(L_test, W_test) * 0.25
        ax2.set_xlim(-margin, L_test + margin)
        ax2.set_ylim(-margin, W_test + margin)
        ax2.set_aspect("equal")

        ax2.text(L_test/2, -margin/4, f"L = {L_test:.1f}m", ha='center', fontweight='bold', color="#1e3a8a")
        ax2.text(-margin/4, W_test/2, f"W = {W_test:.1f}m", va='center', rotation='vertical', fontweight='bold', color="#1e3a8a")
        
        plt.title(f"Mô hình sân thực tế", fontsize=10, pad=10)
        st.pyplot(fig2)

with tab2:
    st.subheader("Cơ sở lý thuyết Toán học")
    st.markdown("Dựa trên kiến thức về hàm số bậc hai và bất đẳng thức:")
    st.latex(r"S = L \times (\frac{P}{2} - L) = -\left(L - \frac{P}{4}\right)^2 + \frac{P^2}{16}")
    st.info(f"Kết luận: Diện tích đạt giá trị cực đại khi $L = P/4 = {L_opt:.2f}$ m.")

with tab3:
    st.subheader("Dự toán kinh phí hoàn thiện")
    gia_co = st.number_input("Giá cỏ nhân tạo (VNĐ/m²):", min_value=0, value=150000, step=10000)
    phi_co = S_test * gia_co
    st.write(f"### 💵 Tổng chi phí vật liệu: {phi_co:,.0f} VNĐ")
    st.caption("* Chi phí chưa bao gồm công thợ và các phụ kiện khác.")
