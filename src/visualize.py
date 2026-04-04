import sqlite3
import pandas as pd
import plotly.express as px
import os

def generate_dashboard():
    print("📊 Generating interactive price dashboard...")
    
    # Connect to DB
    conn = sqlite3.connect('data/tracker.db')
    
    # Query the data: Join price_history with games to get names and stores
    query = """
    SELECT ph.date_checked, ph.price, g.name, g.store 
    FROM price_history ph
    JOIN games g ON ph.app_id = g.app_id
    ORDER BY ph.date_checked ASC
    """
    
    try:
        df = pd.read_sql_query(query, conn)
        
        if df.empty:
            print("⚠️ Not enough data to generate a graph yet.")
            return
            
        # Combine Name and Store for the legend
        df['Game & Store'] = df['name'] + ' (' + df['store'].str.upper() + ')'
        
        # Create the interactive line chart
        fig = px.line(
            df, 
            x='date_checked', 
            y='price', 
            color='Game & Store', 
            markers=True,
            title='🎮 Game Price Tracker Evolution',
            labels={'date_checked': 'Date', 'price': 'Price (€)'},
            template='plotly_dark' # A sleek dark mode theme
        )
        
        # Save to a static HTML file inside the data folder
        os.makedirs('data', exist_ok=True)
        fig.write_html('data/dashboard.html')
        print("✅ Dashboard saved to data/dashboard.html")
        
    except Exception as e:
        print(f"❌ Error generating dashboard: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    generate_dashboard()