import streamlit as st

# Set page layout
st.set_page_config(page_title="Team Card Assignment", layout="wide")

# Custom styles for cards and layout
st.markdown("""
    <style>
    .card-box {
        display: flex;
        gap: 10px;
        margin: 10px 0;
    }
    .card {
        width: 40px;
        height: 60px;
        border: 2px dashed #bbb;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 20px;
        background-color: #fff;
        color: #333;
    }
    .player-header {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🃏 Team Card Assignment")
st.write("Select cards for all team members and analyze their hands!")

# Card definitions
ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
suits = ['♠', '♥', '♦', '♣']

# Choose number of players
num_players = st.slider("Number of Players", min_value=2, max_value=6, value=3)

# Initialize session state for each player
for i in range(1, num_players + 1):
    if f"player_{i}_hand" not in st.session_state:
        st.session_state[f"player_{i}_hand"] = []

# Render player columns
player_cols = st.columns(num_players)

for i in range(num_players):
    player_id = f"player_{i+1}_hand"
    with player_cols[i]:
        st.markdown(f'<div class="player-header">🧑‍🤝‍🧑 Player {i+1}</div>', unsafe_allow_html=True)
        st.markdown(f"<b>Cards: {len(st.session_state[player_id])}/5</b>", unsafe_allow_html=True)

        # Show current cards
        st.markdown('<div class="card-box">' +
            ''.join(f'<div class="card">{r}{s}</div>' for r, s in st.session_state[player_id]) +
            '</div>', unsafe_allow_html=True)

        # Select new card
        st.markdown("##### Select Rank:")
        selected_rank = st.radio(f"rank_{i}", ranks, horizontal=True, key=f"rank_{i}")
        st.markdown("##### Select Suit:")
        selected_suit = st.radio(f"suit_{i}", suits, horizontal=True, key=f"suit_{i}")

        # Add button
        if st.button(f"➕ Add {selected_rank}{selected_suit}", key=f"add_{i}"):
            if len(st.session_state[player_id]) >= 5:
                st.warning("You already have 5 cards!")
            elif (selected_rank, selected_suit) in st.session_state[player_id]:
                st.warning("Card already added!")
            else:
                st.session_state[player_id].append((selected_rank, selected_suit))
