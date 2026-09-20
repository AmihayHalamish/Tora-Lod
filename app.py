import streamlit as st
import pandas as pd
import os

# הגדרות בסיסיות לעמוד
st.set_page_config(page_title="מאגר דברי תורה", layout="wide")
st.title("📚 מאגר דברי תורה")

# פונקציה לטעינת הנתונים מקובץ ה-CSV
@st.cache_data
def load_data():
    if os.path.exists("database.csv"):
        return pd.read_csv("database.csv")
    else:
        st.error("קובץ הנתונים database.csv לא נמצא.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.sidebar.header("חיפוש וסינון")

    # 1. שליפת כל הנושאים הקיימים ויצירת תיבת בחירה
    topics = df['נושא'].unique().tolist()
    selected_topic = st.sidebar.selectbox("בחר נושא:", ["הכל"] + topics)

    # סינון ראשוני לפי הנושא שנבחר
    if selected_topic != "הכל":
        filtered_df = df[df['נושא'] == selected_topic]
    else:
        filtered_df = df

    # 2. שליפת הכותבים *רק* מתוך הנושא שנבחר (סינון דינמי)
    authors = filtered_df['כותב'].unique().tolist()
    selected_author = st.sidebar.selectbox("בחר כותב:", ["הכל"] + authors)

    # סינון שני לפי הכותב שנבחר
    if selected_author != "הכל":
        filtered_df = filtered_df[filtered_df['כותב'] == selected_author]

    # הצגת התוצאות
    st.write(f"**נמצאו {len(filtered_df)} מסמכים מתאימים:**")
    st.markdown("---")

    # מעבר על כל התוצאות שסוננו והצגתן
    for index, row in filtered_df.iterrows():
        col1, col2 = st.columns([3, 1]) # חלוקת המסך לעמודות לעיצוב נקי
        
        with col1:
            st.subheader(row['כותרת'])
            st.write(f"**נושא:** {row['נושא']} | **כותב:** {row['כותב']}")
        
        with col2:
            file_path = os.path.join("documents", row['שם_קובץ'])
            
            # בדיקה אם קובץ ה-PDF באמת קיים בתיקייה
            if os.path.exists(file_path):
                with open(file_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 הורד קובץ PDF",
                        data=pdf_file,
                        file_name=row['שם_קובץ'],
                        mime="application/pdf",
                        key=f"download_{index}"
                    )
            else:
                st.warning("הקובץ חסר במערכת")
        
        st.markdown("---")
