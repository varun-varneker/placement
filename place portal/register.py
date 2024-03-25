import streamlit as st
import pandas as pd

# Load data from CSV file
def load_data(filename):
    df = pd.read_csv(filename)
    return df

# Define admin password
ADMIN_PASSWORD = "admin123"

# Dictionary to store placement details with register numbers as keys
placement_details = load_data("Book11.csv")  # Load data from CSV file

def get_placement_details(identifier):
    """Function to get placement details by register number or name"""
    # Check if identifier is a register number
    reg_num_matches = placement_details[placement_details["REGISTER NUMBER"] == identifier]
    if not reg_num_matches.empty:
        return reg_num_matches
    # Check if identifier is a name
    name_matches = placement_details[placement_details["NAME"] == identifier]
    if not name_matches.empty:
        return name_matches
    # If neither register number nor name is found
    return None

# Streamlit app layout
def main():
    st.title("Placement Portal")

    page = st.sidebar.radio("Navigation", ["Home", "Placement Details", "Admin"])

    if page == "Home":
        st.header("Enter Your Details")
        name = st.text_input("Enter Your Name:")
        register_number = st.text_input("Enter Your Register Number:")
        if st.button("Search"):
            if name.strip() != "" or register_number.strip() != "":
                placement = get_placement_details(register_number)
                if placement is None:
                    placement = get_placement_details(name)
                if placement is not None:
                    st.session_state.placement = placement
                    st.sidebar.success("Details found! Click 'Placement Details' for more info.")
                else:
                    st.sidebar.error("Placement details not found for the given register number or name.")
            else:
                st.sidebar.warning("Please enter either your name or register number.")
    elif page == "Placement Details":
        st.header("Placement Details")
        if "placement" in st.session_state:
            placement = st.session_state.placement
            st.success(f"Congratulations {placement.iloc[0]['NAME']}!")
            st.write(f"You've been placed at {placement.iloc[0]['COMPANY']} with a package of {placement.iloc[0]['PACKAGE']} per annum.")
        else:
            st.error("No placement details available.")
    elif page == "Admin":
        st.header("Admin Portal")
        st.subheader("Authentication Required")
        password = st.text_input("Enter Admin Password:", type="password")
        if password == ADMIN_PASSWORD:
            st.subheader("All Student Details")
            st.dataframe(placement_details)
        elif password != "":
            st.error("Incorrect password. Please try again.")

if __name__ == "__main__":
    main()
