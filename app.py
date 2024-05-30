import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def cashless_reimbursement_table(data_df):
    """Calculates and displays the Cashless vs Reimbursement table."""
    cashless_df=data_df.copy()
    # Group by Claim Type and calculate sum of Claimed Amount
    claim_amt_summary = cashless_df.groupby("Claim_Type")["Claimed_Amount"].sum().reset_index()

   
    total_claimed_amount = claim_amt_summary["Claimed_Amount"].sum()

    
    claim_amt_summary["As a % total Amt."] = (claim_amt_summary["Claimed_Amount"] / total_claimed_amount) * 100

    
    claim_count_summary = cashless_df.groupby("Claim_Type").size().reset_index(name="No. of Claims (Settled & Underprocess)")

    # Calculate total number of claims
    total_claims = claim_count_summary["No. of Claims (Settled & Underprocess)"].sum()

    claim_count_summary["As a % of total No."] = (claim_count_summary["No. of Claims (Settled & Underprocess)"] / total_claims) * 100    
    claim_count_summary["Avg Claim Size"] = claim_amt_summary["Claimed_Amount"] / claim_count_summary["No. of Claims (Settled & Underprocess)"]
    final_summary = pd.merge(claim_amt_summary, claim_count_summary, on="Claim_Type")

  
    total_row = pd.DataFrame({
        "Claim_Type": ["Total Claims"],
        "Claimed_Amount": [total_claimed_amount],
        "As a % total Amt.": [100],
        "No. of Claims (Settled & Underprocess)": [total_claims],
        "As a % of total No.": [100],
        "Avg Claim Size": [total_claimed_amount / total_claims]
    })

    final_summary = pd.concat([final_summary, total_row], ignore_index=True)

    
    final_summary = final_summary.rename(columns={"Claim_Type": "Claim Mode"})

    
    st.table(final_summary.style.format({"Claimed_Amount": "{:,.0f}", 
                                         "As a % total Amt.": "{:.0f}%",
                                         "As a % of total No.": "{:.0f}%",# 
                                         "Avg Claim Size": "{:,.0f}"}))

    
    return final_summary


def cashless_reimbursement_charts(final_summary):
    """Creates and displays the Cashless vs Reimbursement bar charts."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    
    claim_types = final_summary["Claim Mode"][:-1] 
    claim_amounts = final_summary["Claimed_Amount"][:-1]
    ax1.bar(claim_types, claim_amounts, color="#5F8D8E", edgecolor="grey")
    ax1.set_title("Cashless Vs Reimbursement (In Value)")
    ax1.set_ylabel("Amount")
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,.0f}".format(x)))
    ax1.grid(axis='y')

    
    for i, v in enumerate(claim_amounts):
        ax1.text(i, v - 2000000, "{:,.0f}".format(v), ha='center', va='bottom', color='black', fontweight='bold')

    
    claim_counts = final_summary["No. of Claims (Settled & Underprocess)"][:-1]
    ax2.bar(claim_types, claim_counts, color="#5F8D8E", edgecolor="grey")
    ax2.set_title("Cashless Vs Reimbursement (In Nos)")
    ax2.set_ylabel("No. of Claims")
    ax2.grid(axis='y')

    
    for i, v in enumerate(claim_counts):
        ax2.text(i, v - 5, str(int(v)), ha='center', va='bottom', color='black', fontweight='bold')

    plt.tight_layout()
    st.pyplot(fig)
    




def relationship_wise_claims(data_df):
    """Calculates and displays the Relationship-wise Settled & Underprocess Claims Break Up table."""

    
    relationship_mapping = {
        'Self': 'Employee',
        'Spouse': 'Spouse',
        'Son': 'Child',
        'Daughter': 'Child',
        'Mother': 'Parents',
        'Father': 'Parents'
    }
    data_df["Relation"] = data_df["Relation"].map(relationship_mapping)

    # Group by Relation and calculate sum of Claimed Amount
    claim_amt_summary = data_df.groupby("Relation")["Incurred_Amount"].sum().reset_index()
    claim_amt_summary = claim_amt_summary.rename(columns={"Incurred_Amount": "Claim Amt"})

    # Calculate total claimed amount
    total_claimed_amount = claim_amt_summary["Claim Amt"].sum()

    # Calculate percentage of total amount
    claim_amt_summary["As a % total Amt."] = (claim_amt_summary["Claim Amt"] / total_claimed_amount) * 100

    # Count claims by Relation
    claim_count_summary = data_df.groupby("Relation").size().reset_index(name="No of Claims")

    # Calculate total number of claims
    total_claims = claim_count_summary["No of Claims"].sum()

    # Calculate percentage of total claims
    claim_count_summary["As a % of total No.s"] = (claim_count_summary["No of Claims"] / total_claims) * 100

    # Calculate average claim size
    claim_count_summary["Avg Claim Size"] = claim_amt_summary["Claim Amt"] / claim_count_summary["No of Claims"]

    # Merge the two summaries based on Relation
    final_summary1 = pd.merge(claim_amt_summary, claim_count_summary, on="Relation")

    # Add a row for total claims
    total_row = pd.DataFrame({
        "Relation": ["Total"],
        "Claim Amt": [total_claimed_amount],
        "As a % total Amt.": [100],
        "No of Claims": [total_claims],
        "As a % of total No.s": [100],
        "Avg Claim Size": [total_claimed_amount / total_claims]
    })

    final_summary1 = pd.concat([final_summary1, total_row], ignore_index=True)

    # Display the table with formatting
    st.table(final_summary1.style.format({"Claim Amt": "{:,.0f}", 
                                         "As a % total Amt.": "{:.0f}%",
                                         "As a % of total No.s":"{:.0f}%",
                                         "Avg Claim Size": "{:,.0f}"}))
    
    
    
    return final_summary1


def relationship_wise_charts(final_summary1):
    """Creates and displays the Relationship-wise pie charts."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    relations = final_summary1["Relation"][:-1]  # Exclude "Total"

    # Pie Chart 1: Claim Amount
    amounts = final_summary1["Claim Amt"][:-1]
    explode = [0.1 if r == "Parents" else 0 for r in relations]  # Explode "Parents" slice

    ax1.pie(amounts, explode=explode, labels=relations, autopct="%1.0f%%", 
            shadow=True, startangle=90, colors=["#ADD8E6", "#5F8D8E", "#5F8D8E", "#5F8D8E"])
    ax1.axis("equal")  # Equal aspect ratio ensures a circular pie chart
    ax1.set_title("Relationship Wise (In Value)")

    # Pie Chart 2: No of Claims
    counts = final_summary1["No of Claims"][:-1]
    explode = [0.1 if r == "Parents" else 0 for r in relations]  # Explode "Parents"

    ax2.pie(counts, explode=explode, labels=relations, autopct="%1.0f%%", 
            shadow=True, startangle=90, colors=["#ADD8E6", "#5F8D8E", "#5F8D8E", "#5F8D8E"])
    ax2.axis("equal")
    ax2.set_title("Relationship Wise (In Nos)")

    plt.tight_layout()
    st.pyplot(fig)




def age_wise_claims_breakup(data_df):
    """Calculates and displays the Age-wise Claims Break Up table."""
    age_data = data_df.copy()
    age_bins = [0, 19, 26, 36, 46, 56, 66, 71, 76, 81, float('inf')]
    age_labels = ['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '66-70', '71-75', '76-80', 'Above 80']

    # Create age group column
    age_data['Age Group'] = pd.cut(age_data['Age'], bins=age_bins, labels=age_labels, right=False)

    # Calculate claim statistics for each age group
    age_table = age_data.groupby('Age Group').agg(
        Claim_Amt=('Incurred_Amount', 'sum'),
        No_of_Claims=('Claim_No', 'count')
    ).reset_index() # Reset the index to make 'Age Group' a column

    # Calculate grand totals
    grand_total_amt = age_table["Claim_Amt"].sum()
    grand_total_claims = age_table["No_of_Claims"].sum()

    # Calculate percentages
    age_table['As a % total Amt.'] = (age_table["Claim_Amt"] / grand_total_amt * 100).round(0).astype(int).astype(str) + "%"
    age_table['As a % of total Nos.'] = (age_table["No_of_Claims"] / grand_total_claims * 100).round(0).astype(int).astype(str) + "%"

    # Handle potential NaN or inf in Avg Claim Size
    age_table["Avg Claim Size"] = age_table["Claim_Amt"] / age_table["No_of_Claims"]
    age_table["Avg Claim Size"] = age_table["Avg Claim Size"].replace([np.inf, -np.inf], np.nan).fillna(0).round(0).astype(int)

    # Add grand total row
    grand_total_row = pd.DataFrame({
        "Age Group": ["Grand Total"],
        "Claim_Amt": [grand_total_amt],
        "As a % total Amt.": ["100%"],
        "No_of_Claims": [grand_total_claims],
        "As a % of total Nos.": ["100%"],
        "Avg Claim Size": [grand_total_amt / grand_total_claims]
    })

    age_table = pd.concat([age_table, grand_total_row], ignore_index=True)

    # Display the table with formatting
    st.table(age_table.style.format({"Claim_Amt": "{:,.0f}", "Avg Claim Size": "{:,.0f}"}))

    return age_table







def plot_age_wise_claims(age_table):
    """Plots the age-wise claims breakup graphs for claim amount and claim count."""

    # Exclude 'Grand Total' row
    age_table_plot = age_table[age_table['Age Group'] != 'Grand Total']

    fig, axs = plt.subplots(1, 2, figsize=(15, 5))  # 1 row, 2 columns for the plots

    # Plot 1: Claim Amount
    axs[0].barh(age_table_plot['Age Group'], age_table_plot['Claim_Amt'], color='#66664D')
    axs[0].set_title('Age-wise Claims (In Value)')
    axs[0].set_xlabel('')  # No x-axis label
    axs[0].invert_yaxis()  # Reverse the order of age groups

    # Add data labels to the bars in Plot 1
    for i, v in enumerate(age_table_plot['Claim_Amt']):
        axs[0].text(v + 50000, i, "{:,.0f}".format(v), color='black', va='center')

    # Plot 2: Number of Claims
    axs[1].barh(age_table_plot['Age Group'], age_table_plot['No_of_Claims'], color='#66664D')
    axs[1].set_title('Age-wise Claims (In Nos)')
    axs[1].set_xlabel('')  # No x-axis label
    axs[1].invert_yaxis()  # Reverse the order of age groups
    axs[1].set_xlim(0, 30)  # Adjust x-axis limit

    # Add data labels to the bars in Plot 2
    for i, v in enumerate(age_table_plot['No_of_Claims']):
        axs[1].text(v + 1, i, str(v), color='black', va='center')

    plt.tight_layout()  # Adjust layout for better spacing
    st.pyplot(fig)  # Display the plot in Streamlit
    
    
    


def amount_band_wise_claims_breakup(data_df):
    """Calculates and displays the Amount Band Wise Claims Break Up table."""
    data = data_df.copy()

    # Define amount bands and labels
    amount_bins = [0, 1, 25001, 50001, 75001, 100001, 150001, 200001, 300001, float('inf')]
    amount_labels = ["0", "1-25000", "25001-50000", "50001-75000", "75001-100000", 
                   "100001-150000", "150001-200000", "200001-300000", ">300000"]

    # Create amount band column
    data["Amount Band"] = pd.cut(data["Incurred_Amount"], bins=amount_bins, labels=amount_labels, right=False)

    # Calculate claim statistics for each amount band
    amount_band_data = data.groupby("Amount Band").agg(
        Claim_Amt=("Incurred_Amount", "sum"),
        No_of_Claims=("Claim_No", "count")
    ).reset_index()

    # Calculate percentages and average claim size
    grand_total_amt = amount_band_data["Claim_Amt"].sum()
    grand_total_claims = amount_band_data["No_of_Claims"].sum()

    amount_band_data["As a % total Amt."] = (amount_band_data["Claim_Amt"] / grand_total_amt * 100).round(0).astype(int).astype(str) + "%"
    amount_band_data["As a % of total Nos."] = (amount_band_data["No_of_Claims"] / grand_total_claims * 100).round(0).astype(int).astype(str) + "%"
    
    # Handle potential NaN or inf in Avg Claim Size
    amount_band_data["Avg Claim Size"] = amount_band_data["Claim_Amt"] / amount_band_data["No_of_Claims"]
    amount_band_data["Avg Claim Size"] = amount_band_data["Avg Claim Size"].replace([np.inf, -np.inf], np.nan).fillna(0).round(0).astype(int)
    

    # Add grand total row
    grand_total_row = pd.DataFrame({
        "Amount Band": ["Grand Total"],
        "Claim_Amt": [grand_total_amt],
        "As a % total Amt.": ["100%"],
        "No_of_Claims": [grand_total_claims],
        "As a % of total Nos.": ["100%"],
        "Avg Claim Size": [grand_total_amt / grand_total_claims]
    })

    amount_band_data = pd.concat([amount_band_data, grand_total_row], ignore_index=True)

    # Display the table
    #st.table(amount_band_data.style.format({"Claim_Amt": "{:,.0f}", "Avg Claim Size": "{:,.0f}"}))
    st.write(amount_band_data.style.format({"Claim_Amt": "{:,.0f}", "Avg Claim Size": "{:,.0f}"}))
    return amount_band_data


def plot_amount_band_charts(amount_band_data):
    """Generates two bar charts for Amount Band: one for Value and one for Number of Claims."""

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1 row, 2 columns of charts

    # Chart 1: Amount Band (In Value)
    axes[0].bar(amount_band_data["Amount Band"], amount_band_data["Claim_Amt"], color="#1A5259")
    axes[0].set_title("Amount Band (In Value)")
    axes[0].set_xlabel("Amount Band")
    axes[0].set_ylabel("Claim Amount")
    axes[0].tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
    
    # Annotate bars with values (optional)
    for i, v in enumerate(amount_band_data["Claim_Amt"]):
        axes[0].text(i, v, "{:,.0f}".format(v), ha='center', va='bottom')

    # Chart 2: Amount Band (In Nos)
    axes[1].bar(amount_band_data["Amount Band"], amount_band_data["No_of_Claims"], color="#1A5259")
    axes[1].set_title("Amount Band (In Nos)")
    axes[1].set_xlabel("Amount Band")
    axes[1].set_ylabel("No of Claims")
    axes[1].tick_params(axis='x', rotation=45)
    
    # Annotate bars with values (optional)
    for i, v in enumerate(amount_band_data["No_of_Claims"]):
        axes[1].text(i, v, str(v), ha='center', va='bottom')

    st.pyplot(fig)




def day_stay_wise_claims_breakup(data_df):
    """Calculates and displays the No of Day Stay wise Claims Break Up table."""
    data = data_df.copy()

    # Calculate the number of days stay
    data["Date_of_Discharge"] = pd.to_datetime(data["Date_of_Discharge"])
    data["Date_of_Admission"] = pd.to_datetime(data["Date_of_Admission"])
    data["No of Days"] = (data["Date_of_Discharge"] - data["Date_of_Admission"]).dt.days
    
    # data["Day Stay Group"] = pd.cut(data["No of Days"], bins=day_stay_bins, labels=day_stay_labels, right=False,include_lowest=True)
    def categorize_day_stay(days):
        if days < 1:
            return "<1"
        elif days == 1:
            return "1"
        elif days == 2:
            return "2"
        elif days == 3:
            return "3"
        elif 4 <= days <= 7:
            return "4-7"
        else:
            return "Above 7"

    data["Day Stay Group"] = data["No of Days"].apply(categorize_day_stay)
    
    # Calculate claim statistics for each day stay group
    day_stay_data = data.groupby("Day Stay Group").agg(
        Claim_Amt=("Incurred_Amount", "sum"),
        No_of_Claims=("Claim_No", "count")
    ).reset_index()

    grand_total_amt = day_stay_data["Claim_Amt"].sum()
    grand_total_claims = day_stay_data["No_of_Claims"].sum()

    day_stay_data["As a % total Amt."] = (day_stay_data["Claim_Amt"] / grand_total_amt * 100).round(0).astype(int).astype(str) + "%"
    day_stay_data["As a % of total Nos."] = (day_stay_data["No_of_Claims"] / grand_total_claims * 100).round(0).astype(int).astype(str) + "%"
    
    # Handle potential NaN or inf in Avg Claim Size
    day_stay_data["Avg Claim Size"] = day_stay_data["Claim_Amt"] / day_stay_data["No_of_Claims"]
    day_stay_data["Avg Claim Size"] = day_stay_data["Avg Claim Size"].replace([np.inf, -np.inf], np.nan).fillna(0).round(0).astype(int)

    # Add grand total row
    grand_total_row = pd.DataFrame({
        "Day Stay Group": ["Grand Total"],
        "Claim_Amt": [grand_total_amt],
        "As a % total Amt.": ["100%"],
        "No_of_Claims": [grand_total_claims],
        "As a % of total Nos.": ["100%"],
        "Avg Claim Size": [grand_total_amt / grand_total_claims]
    })

    day_stay_data = pd.concat([day_stay_data, grand_total_row], ignore_index=True)

    # Display the table
    st.table(day_stay_data.style.format({"Claim_Amt": "{:,.0f}", "Avg Claim Size": "{:,.0f}"}))

    return day_stay_data



def plot_day_stay_charts(day_stay_data):
    """Generates two charts for No of Days: one for Value and one for Number of Claims."""

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1 row, 2 columns of charts

    # Chart 1: No of Days (In Value)
    axes[0].bar(day_stay_data["Day Stay Group"], day_stay_data["Claim_Amt"], color="#B8B086")
    axes[0].set_title("No of Days (In Value)")
    axes[0].set_xlabel("No of Days")
    axes[0].set_ylabel("Claim Amount")
    axes[0].tick_params(axis='x', rotation=45)  # Rotate x-axis labels 

    # Annotate bars with values
    for i, v in enumerate(day_stay_data["Claim_Amt"]):
        axes[0].text(i, v, "{:,.0f}".format(v), ha='center', va='bottom')

    # Line plot for average claim size
    ax2 = axes[0].twinx()  # Create a second y-axis
    ax2.plot(day_stay_data["Day Stay Group"], day_stay_data["Avg Claim Size"], color="#962D3E", marker='^')
    ax2.set_ylabel("Avg Claim Size")
    ax2.tick_params(axis='y')

    # Annotate line plot points
    for i, v in enumerate(day_stay_data["Avg Claim Size"]):
        ax2.text(i, v, "{:,.0f}".format(v), ha='center', va='bottom')

    # Chart 2: No of Days (In Nos)
    axes[1].bar(day_stay_data["Day Stay Group"], day_stay_data["No_of_Claims"], color="#B8B086")
    axes[1].set_title("No of Days (In Nos)")
    axes[1].set_xlabel("No of Days")
    axes[1].set_ylabel("No of Claims")
    axes[1].tick_params(axis='x', rotation=45)

    # Annotate bars with values
    for i, v in enumerate(day_stay_data["No_of_Claims"]):
        axes[1].text(i, v, str(v), ha='center', va='bottom')

    st.pyplot(fig)




def top_10_city_wise_claims(data_df):
    """Calculates and displays the Top 10 City-wise Claims Analysis table."""
    data = data_df.copy()

    # Calculate claim statistics for each city
    city_data = data.groupby("City_Name").agg(
        Claim_Amt=("Incurred_Amount", "sum"),
        No_of_Claims=("Claim_No", "count")
    ).reset_index()

    # Sort by Claim Amount in descending order
    city_data = city_data.sort_values(by="Claim_Amt", ascending=False)

    # Get top 10 cities
    top_10_cities = city_data.head(10)

    # Calculate 'Others' data
    other_claim_amt = city_data.iloc[10:]["Claim_Amt"].sum()
    other_claims = city_data.iloc[10:]["No_of_Claims"].sum()

    # Create 'Others' row
    others_row = pd.DataFrame({
        "City_Name": ["Others"],
        "Claim_Amt": [other_claim_amt],
        "No_of_Claims": [other_claims]
    })

    # Concatenate top 10 cities and 'Others' row
    city_data = pd.concat([top_10_cities, others_row], ignore_index=True)

    # Calculate percentages and average claim size
    grand_total_amt = city_data["Claim_Amt"].sum()
    grand_total_claims = city_data["No_of_Claims"].sum()

    city_data["As a % total Amt."] = (city_data["Claim_Amt"] / grand_total_amt * 100).round(0).astype(int).astype(str) + "%"
    city_data["As a % of total Nos."] = (city_data["No_of_Claims"] / grand_total_claims * 100).round(0).astype(int).astype(str) + "%"
    city_data["Avg Claim Size"] = (city_data["Claim_Amt"] / city_data["No_of_Claims"]).round(0).astype(int)

    # Add Grand Total row
    grand_total_row = pd.DataFrame({
        "City_Name": ["Grand Total"],
        "Claim_Amt": [grand_total_amt],
        "As a % total Amt.": ["100%"],
        "No_of_Claims": [grand_total_claims],
        "As a % of total Nos.": ["100%"],
        "Avg Claim Size": [grand_total_amt / grand_total_claims]
    })

    city_data = pd.concat([city_data, grand_total_row], ignore_index=True)

    # Display the table
    st.table(city_data.style.format({"Claim_Amt": "{:,.0f}", "Avg Claim Size": "{:,.0f}"}))

    return city_data

def plot_city_wise_charts(city_data):
    """Generates two bar charts for City Wise data: one for Value and one for Number of Claims."""

    # Get the top 5 cities excluding "Others" and "Grand Total"
    top_5_cities = city_data[~city_data["City_Name"].isin(["Others", "Grand Total"])].head(5)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # 1 row, 2 columns

    # Chart 1: City Wise (In Value)
    axes[0].bar(top_5_cities["City_Name"], top_5_cities["Claim_Amt"], color="#4682B4")
    axes[0].set_title("City Wise (In Value)")
    axes[0].set_xlabel("City Name")
    axes[0].set_ylabel("Claim Amount")
    axes[0].tick_params(axis='x', rotation=45)

    for i, v in enumerate(top_5_cities["Claim_Amt"]):
        axes[0].text(i, v, "{:,.0f}".format(v), ha='center', va='bottom')

    # Chart 2: City Wise (In Nos)
    axes[1].bar(top_5_cities["City_Name"], top_5_cities["No_of_Claims"], color="#4682B4")
    axes[1].set_title("City Wise (In Nos)")
    axes[1].set_xlabel("City Name")
    axes[1].set_ylabel("No of Claims")
    axes[1].tick_params(axis='x', rotation=45)

    for i, v in enumerate(top_5_cities["No_of_Claims"]):
        axes[1].text(i, v, str(v), ha='center', va='bottom')

    st.pyplot(fig)



def top_10_hospitals_utilization(data_df):
    """Calculates and displays the Top 10 Hospitals Utilization table."""
    data = data_df.copy()

    # Calculate claim statistics for each hospital
    hospital_data = data.groupby("Hospital_Name").agg(
        Claim_Amt=("Incurred_Amount", "sum"),
        No_of_Claims=("Claim_No", "count")
    ).reset_index()

    hospital_data = hospital_data.sort_values(by="Claim_Amt", ascending=False)

    top_10_hospitals = hospital_data.head(10)
    other_claim_amt = hospital_data.iloc[10:]["Claim_Amt"].sum()
    other_claims = hospital_data.iloc[10:]["No_of_Claims"].sum()

    # Create 'Others' row
    others_row = pd.DataFrame({
        "Hospital_Name": ["Others"],
        "Claim_Amt": [other_claim_amt],
        "No_of_Claims": [other_claims]
    })

    # Concatenate top 10 hospitals and 'Others' row
    hospital_data = pd.concat([top_10_hospitals, others_row], ignore_index=True)

    # Calculate percentages and average claim size
    grand_total_amt = hospital_data["Claim_Amt"].sum()
    grand_total_claims = hospital_data["No_of_Claims"].sum()

    hospital_data["Expressed As a % total Amt."] = (hospital_data["Claim_Amt"] / grand_total_amt * 100).round(0).astype(int).astype(str) + "%"
    hospital_data["As a % of total Nos."] = (hospital_data["No_of_Claims"] / grand_total_claims * 100).round(0).astype(int).astype(str) + "%"
    
    # Handle potential NaN or inf in Avg Claim Size
    hospital_data["Avg Claim Size"] = hospital_data["Claim_Amt"] / hospital_data["No_of_Claims"]
    hospital_data["Avg Claim Size"] = hospital_data["Avg Claim Size"].replace([np.inf, -np.inf], np.nan).fillna(0).round(0).astype(int)
    
    # Add Grand Total row
    grand_total_row = pd.DataFrame({
        "Hospital_Name": ["Grand Total"],
        "Claim_Amt": [grand_total_amt],
        "Expressed As a % total Amt.": ["100%"],
        "No_of_Claims": [grand_total_claims],
        "As a % of total Nos.": ["100%"],
        "Avg Claim Size": [grand_total_amt / grand_total_claims]
    })

    hospital_data = pd.concat([hospital_data, grand_total_row], ignore_index=True)

    # Display the table
    st.table(hospital_data.style.format({"Claim_Amt": "{:,.0f}", "Avg Claim Size": "{:,.0f}"}))

    return hospital_data



def plot_hospital_wise_charts(hospital_data):
    """Generates two charts for Hospital Wise data: one for Value and one for Number of Claims."""

    hosp_data_for_chart = hospital_data[~hospital_data["Hospital_Name"].isin(["Others", "Grand Total"])]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Chart 1: Hospital Wise (In Value) with Average line
    axes[0].bar(hosp_data_for_chart["Hospital_Name"], hosp_data_for_chart["Claim_Amt"], color="#4682B4")
    axes[0].set_title("Hospital Wise (In Value)")
    axes[0].set_xlabel("Hospital Name")
    axes[0].set_ylabel("Claim Amount")
    axes[0].tick_params(axis='x', rotation=45, labelright=True) # Corrected tick_params

    # Annotate bars with values
    for i, v in enumerate(hosp_data_for_chart["Claim_Amt"]):
        axes[0].text(i, v, "{:,.0f}".format(v), ha='center', va='bottom')

    # Line plot for average claim size
    ax2 = axes[0].twinx()
    ax2.plot(hosp_data_for_chart["Hospital_Name"], hosp_data_for_chart["Avg Claim Size"], 
             color="#962D3E", marker='^', markersize=8)
    ax2.set_ylabel("Average Claim Size")

    # Annotate line plot points
    for i, v in enumerate(hosp_data_for_chart["Avg Claim Size"]):
        ax2.text(i, v, "{:,.0f}".format(v), ha='center', va='bottom', fontsize=8, 
                 bbox=dict(facecolor='white', alpha=0.8))

    # Chart 2: Hospital Wise (In Nos)
    axes[1].bar(hosp_data_for_chart["Hospital_Name"], hosp_data_for_chart["No_of_Claims"], color="#4682B4")
    axes[1].set_title("Hospital Wise (In Nos)")
    axes[1].set_xlabel("Hospital Name")
    #axes[1].set_ylabel("No of Claims")
    axes[1].tick_params(axis='x', rotation=45, labelright=True) # Corrected tick_params

    # Annotate bars with values
    for i, v in enumerate(hosp_data_for_chart["No_of_Claims"]):
        axes[1].text(i, v, str(v), ha='center', va='bottom')
    #plt.tight_layout()
    st.pyplot(fig)
    




def main():
    st.title("CSV File Processor")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the CSV file into a DataFrame
        data_df = pd.read_csv(uploaded_file)

        # Display the original DataFrame
        st.subheader("Original DataFrame")
        st.write(data_df)
        st.title("Cashless vs Reimbursement Analysis")
        #cashless_reimbursement_table(data_df)
        
        
        final_summary = cashless_reimbursement_table(data_df)
        cashless_reimbursement_charts(final_summary)
        
        st.title("Claim Status Report")

        #claim_status_report(data_df)
        
        st.title("Relationship Wise Settled & Underprocess Claims Break Up")

        final_summary1 = relationship_wise_claims(data_df)
        st.title("Charts")
        relationship_wise_charts(final_summary1)
        # """
        # there are some errors in the logic revisit
        st.title("Age-wise Claims Break Up")
        age_table=age_wise_claims_breakup(data_df)
        plot_age_wise_claims(age_table)
        # """
        st.title("Amount Bandwise Claims Breakup")
        amount_band_data=amount_band_wise_claims_breakup(data_df)
        plot_amount_band_charts(amount_band_data)
        
        st.title("Stay wise claims breakup")
        day_stay_data=day_stay_wise_claims_breakup(data_df)
        plot_day_stay_charts(day_stay_data)
        
        
        
        st.title("Hospital Wise Claims Analysis")
        hospital_data=top_10_hospitals_utilization(data_df)
        plot_hospital_wise_charts(hospital_data)
        
        st.title("City Wise Claims Data")
        city_data = top_10_city_wise_claims(data_df)
        plot_city_wise_charts(city_data)
        
if __name__ == "__main__":
    main()
