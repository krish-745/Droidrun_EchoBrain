import streamlit as st
import sqlite3
import pandas as pd
import time

st.set_page_config(
    page_title="Echo Brain Admin",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="InputInstructions"] { display: none; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp {
        background: #0a0a0a;
    }
    
    .main .block-container {
        padding: 1.5rem 1rem;
        max-width: 1200px;
        background: #1a1a1a;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        margin: 1.5rem auto;
        border: 1px solid #2a2a2a;
    }
    
    h1 {
        color: #ffffff;
        font-weight: 700;
        margin-bottom: 0.3rem;
        margin-top: 0;
        text-align: center;
    }
    
    h2, h3 {
        color: #e0e0e0;
        font-weight: 600;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .stButton>button {
        background: #2a2a2a;
        color: white;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: #3a3a3a;
        border-color: #4a4a4a;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background-color: #2a2a2a;
        border-radius: 8px;
        border: 1px solid #3a3a3a;
        color: #ffffff;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #4a4a4a;
        background-color: #2d2d2d;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0f0f0f;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        background-color: transparent;
        color: #888888;
    }
    
    .stTabs [aria-selected="true"] {
        background: #2a2a2a;
        color: white;
        border: 1px solid #3a3a3a;
    }
    
    .streamlit-expanderHeader {
        background-color: #2a2a2a;
        border-radius: 8px;
        border: 1px solid #3a3a3a;
        font-weight: 600;
        color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #2d2d2d;
        border-color: #4a4a4a;
    }
    
    hr {
        margin: 1rem 0;
        border: none;
        height: 1px;
        background: #2a2a2a;
    }
    
    [data-testid="stSidebar"] {
        background: #0f0f0f;
        border-right: 1px solid #2a2a2a;
    }
    
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stButton>button {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        color: white;
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background: #2a2a2a;
        border-color: #3a3a3a;
    }
    
    .order-card, .query-card {
        background: #2a2a2a;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #4a4a4a;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .order-card:hover, .query-card:hover {
        background: #2d2d2d;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transform: translateX(4px);
        border-left-color: #5a5a5a;
    }
    
    .stSuccess {
        border-radius: 8px;
        border-left: 3px solid #48bb78;
        background-color: #1a2e1a;
        color: #90ee90;
    }
    
    .stInfo {
        border-radius: 8px;
        border-left: 3px solid #4299e1;
        background-color: #1a2a3a;
        color: #87ceeb;
    }
    
    .stWarning {
        border-radius: 8px;
        border-left: 3px solid #ed8936;
        background-color: #2e2a1a;
        color: #ffa500;
    }
    
    .stError {
        border-radius: 8px;
        border-left: 3px solid #f56565;
        background-color: #2e1a1a;
        color: #ff6b6b;
    }
    
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .welcome-header {
        text-align: center;
        padding: 2rem 0;
    }
    
    .welcome-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    p, span, label {
        color: #b0b0b0;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff;
    }
    
    [data-testid="stMetricLabel"] {
        color: #888888;
    }
    
    .stCaption {
        color: #666666 !important;
    }
    
    .element-container {
        margin-bottom: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        max-height: 60vh;
        overflow-y: auto;
        padding-right: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab-panel"]::-webkit-scrollbar {
        width: 6px;
    }
    
    .stTabs [data-baseweb="tab-panel"]::-webkit-scrollbar-track {
        background: #1a1a1a;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab-panel"]::-webkit-scrollbar-thumb {
        background: #3a3a3a;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab-panel"]::-webkit-scrollbar-thumb:hover {
        background: #4a4a4a;
    }
</style>
""", unsafe_allow_html=True)

def get_db_connection():
    conn = sqlite3.connect('brain.db')
    conn.row_factory = sqlite3.Row
    return conn

def run_query(query, params=()):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def get_data(query, params=()):
    conn = get_db_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_owner_profile():
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM owner LIMIT 1")
        return c.fetchone()
    except sqlite3.OperationalError:
        return None 
    finally:
        conn.close()

def setup_shop(shop_name, mobile_number):
    try:
        run_query("""
            CREATE TABLE IF NOT EXISTS owner (
                name TEXT,
                mobile_number TEXT UNIQUE
            )
        """)
        run_query("""CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, price TEXT, info TEXT)""")
        run_query("""CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            customer TEXT, description TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
            completed INTEGER DEFAULT 0)""")
        run_query("""CREATE TABLE IF NOT EXISTS queries (
            query_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            customer TEXT, info TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
            completed INTEGER DEFAULT 0)""")
            
        run_query("INSERT INTO owner (name, mobile_number) VALUES (?, ?)", (shop_name, mobile_number))
        return True
    except Exception as e:
        st.error(f"Error: {e}")
        return False

def render_onboarding():
    st.markdown('<div class="welcome-header">', unsafe_allow_html=True)
    st.markdown('<div class="welcome-icon"></div>', unsafe_allow_html=True)
    st.title("Welcome to Echo Brain")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem; color: #888888;'>
            Let's set up your business profile to get started.<br>
            Your intelligent business companion awaits!
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    with st.form("setup_form"):
        st.markdown("### Business Information")
        shop_name = st.text_input("Shop Name", placeholder="e.g., My Awesome Store")
        mobile = st.text_input("Mobile Number", placeholder="Used for secure login")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("Start My Business", use_container_width=True)
        
        if submitted:
            if shop_name and mobile:
                if setup_shop(shop_name, mobile):
                    st.success("Setup Complete! Redirecting to your dashboard...")
                    time.sleep(1.5)
                    st.rerun()
            else:
                st.warning("Please fill in both fields to continue.")

def render_login(owner_name):
    st.markdown('<div class="welcome-header">', unsafe_allow_html=True)
    st.markdown('<div class="welcome-icon"></div>', unsafe_allow_html=True)
    st.title(f"Welcome back, {owner_name}!")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem; color: #888888;'>
            Please verify your identity to access your dashboard
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("### Secure Login")
        mobile = st.text_input("Mobile Number", placeholder="Enter your registered mobile number")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_btn = st.form_submit_button("Login", use_container_width=True)
        
        if login_btn:
            saved_owner = get_owner_profile()
            if saved_owner and str(saved_owner['mobile_number']) == str(mobile):
                st.session_state.logged_in = True
                st.session_state.user = dict(saved_owner)
                st.success("Login Successful! Redirecting...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Incorrect mobile number. Please try again.")

def render_dashboard(user):
    st.sidebar.markdown(f"### {user['name']}")
    st.sidebar.markdown("---")
    
    pending_orders = get_data("SELECT COUNT(*) as count FROM orders WHERE completed = 0")
    pending_queries = get_data("SELECT COUNT(*) as count FROM queries WHERE completed = 0")
    total_products = get_data("SELECT COUNT(*) as count FROM products")
    
    st.sidebar.markdown("#### Quick Stats")
    st.sidebar.metric("Pending Orders", int(pending_orders['count'].iloc[0]) if not pending_orders.empty else 0)
    st.sidebar.metric("Pending Queries", int(pending_queries['count'].iloc[0]) if not pending_queries.empty else 0)
    st.sidebar.metric("Products", int(total_products['count'].iloc[0]) if not total_products.empty else 0)
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("Refresh Data", use_container_width=True):
        st.rerun()
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    st.title("Command Center")
    
    tab1, tab2, tab3 = st.tabs(["Inventory", "Orders", "Queries"])
    
    with tab1:
        st.header("Inventory Manager")
        
        with st.expander("Add New Product", expanded=False):
            with st.form("add_product", clear_on_submit=True):
                st.markdown("##### Product Details")
                c1, c2 = st.columns(2)
                name = c1.text_input("Product Name", placeholder="e.g., Premium Coffee")
                price = c2.text_input("Price", placeholder="e.g., $4.99")
                info = st.text_area("Description", placeholder="Add product details...")
                
                col1, col2, col3 = st.columns([2, 1, 2])
                with col2:
                    if st.form_submit_button("Add Item", use_container_width=True):
                        if name and price:
                            run_query("INSERT INTO products (name, price, info) VALUES (?, ?, ?)", (name, price, info))
                            st.success(f"Added {name} to inventory!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.warning("Please fill in name and price.")

        df = get_data("SELECT * FROM products")
        
        if not df.empty:
            st.markdown("#### Current Inventory")
            st.caption("Edit details or check 'Delete' to remove items")
            
            df['Delete'] = False
            
            edited_df = st.data_editor(
                df, 
                use_container_width=True, 
                hide_index=True, 
                key="inv_editor",
                column_config={
                    "product_id": st.column_config.NumberColumn("ID", disabled=True),
                    "name": st.column_config.TextColumn("Product Name", required=True),
                    "price": st.column_config.TextColumn("Price", required=True),
                    "info": st.column_config.TextColumn("Description"),
                    "Delete": st.column_config.CheckboxColumn("Delete?", default=False)
                }
            )
            
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("Save Changes", use_container_width=True):
                    for index, row in edited_df.iterrows():
                        if row['Delete']:
                            run_query("DELETE FROM products WHERE product_id = ?", (row['product_id'],))
                        else:
                            run_query(
                                "UPDATE products SET name = ?, price = ?, info = ? WHERE product_id = ?",
                                (row['name'], row['price'], row['info'], row['product_id'])
                            )
                    st.success("Inventory updated successfully!")
                    time.sleep(1)
                    st.rerun()
        else:
            st.info("No products in inventory. Add your first product above!")

    with tab2:
        st.subheader("Pending Orders")
        pending = get_data("SELECT * FROM orders WHERE completed = 0 ORDER BY timestamp DESC")
        
        if not pending.empty:
            for _, row in pending.iterrows():
                st.markdown('<div class="order-card">', unsafe_allow_html=True)
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{row['customer']}** • {row['description']}")
                with c2:
                    if st.button("Complete", key=f"ord_{row['order_id']}", use_container_width=True):
                        run_query("UPDATE orders SET completed = 1 WHERE order_id = ?", (row['order_id'],))
                        st.success("Order completed!")
                        time.sleep(0.5)
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("All caught up! No pending orders.")

        with st.expander("Show Completed Orders"):
            history = get_data("SELECT * FROM orders WHERE completed = 1 ORDER BY timestamp DESC")
            if not history.empty:
                st.dataframe(
                    history, 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={
                        "order_id": "Order ID",
                        "customer": "Customer",
                        "description": "Description",
                        "timestamp": "Completed At",
                        "completed": None
                    }
                )
            else:
                st.info("No completed orders yet.")

    with tab3:
        st.subheader("Pending Queries")
        pending_q = get_data("SELECT * FROM queries WHERE completed = 0 ORDER BY timestamp DESC")
        
        if not pending_q.empty:
            for _, row in pending_q.iterrows():
                st.markdown('<div class="query-card">', unsafe_allow_html=True)
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{row['customer']}** • *{row['info']}*")
                with c2:
                    if st.button("Resolve", key=f"q_{row['query_id']}", use_container_width=True):
                        run_query("UPDATE queries SET completed = 1 WHERE query_id = ?", (row['query_id'],))
                        st.success("Query resolved!")
                        time.sleep(0.5)
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("All caught up! No pending queries.")

        with st.expander("Show Resolved Queries"):
            q_history = get_data("SELECT * FROM queries WHERE completed = 1 ORDER BY timestamp DESC")
            if not q_history.empty:
                st.dataframe(
                    q_history, 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={
                        "query_id": "Query ID",
                        "customer": "Customer",
                        "info": "Question",
                        "timestamp": "Resolved At",
                        "completed": None
                    }
                )
            else:
                st.info("No resolved queries yet.")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

existing_shop = get_owner_profile()

if not existing_shop:
    render_onboarding()
elif not st.session_state.logged_in:
    render_login(existing_shop['name'])
else:
    render_dashboard(st.session_state.user)