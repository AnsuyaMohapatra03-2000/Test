import streamlit as st
from collections import Counter

# ---------- Configuration ----------
st.set_page_config(page_title="Team Card Assignment", layout="wide")

ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
suits = ['♠', '♥', '♦', '♣']
rank_values = {r: i for i, r in enumerate(reversed(ranks), start=2)}

# ---------- Style ----------
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
        border: 2px solid #bbb;
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
    .rank-title {
        font-size: 28px;
        font-weight: 700;
        color: #333;
        margin-top: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.title("🃏 Team Card Assignment")
st.write("Select cards for all team members and analyze their hands!")

# ---------- Player Setup ----------
num_players = st.slider("Number of Players", 2, 6, 3)

# ---------- State Initialization ----------
for i in range(1, num_players + 1):
    if f"player_{i}_hand" not in st.session_state:
        st.session_state[f"player_{i}_hand"] = []

# ---------- UI for Each Player ----------
cols = st.columns(num_players)

for i in range(num_players):
    pid = f"player_{i+1}_hand"
    with cols[i]:
        st.markdown(f'<div class="player-header">P{i+1} - Player {i+1}</div>', unsafe_allow_html=True)
        st.markdown(f"Cards: {len(st.session_state[pid])}/5")

        # Current hand display
        st.markdown('<div class="card-box">' +
            ''.join(f'<div class="card">{r}{s}</div>' for r, s in st.session_state[pid]) +
            '</div>', unsafe_allow_html=True)

        # Card selection
        selected_rank = st.radio(f"Select Rank P{i+1}", ranks, horizontal=True, key=f"rank_{i}")
        selected_suit = st.radio(f"Select Suit P{i+1}", suits, horizontal=True, key=f"suit_{i}")

        if st.button(f"➕ Add {selected_rank}{selected_suit}", key=f"add_{i}"):
            if len(st.session_state[pid]) >= 5:
                st.warning("You already have 5 cards!")
            elif (selected_rank, selected_suit) in st.session_state[pid]:
                st.warning("Card already added!")
            else:
                st.session_state[pid].append((selected_rank, selected_suit))

# ---------- Poker Hand Evaluation ----------
def evaluate_hand(hand):
    rank_counts = Counter([r for r, _ in hand])
    suit_counts = Counter([s for _, s in hand])
    values = sorted([rank_values[r] for r, _ in hand], reverse=True)

    is_flush = max(suit_counts.values()) == 5
    is_straight = all(values[i] - 1 == values[i + 1] for i in range(4))

    if is_straight and is_flush:
        if values[0] == 14:
            return (1, "Royal Flush", values)
        return (2, "Straight Flush", values)
    if 4 in rank_counts.values():
        return (3, "Four of a Kind", values)
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        return (4, "Full House", values)
    if is_flush:
        return (5, "Flush", values)
    if is_straight:
        return (6, "Straight", values)
    if 3 in rank_counts.values():
        return (7, "Three of a Kind", values)
    if list(rank_counts.values()).count(2) == 2:
        return (8, "Two Pair", values)
    if 2 in rank_counts.values():
        return (9, "One Pair", values)
    return (10, "High Card", values)

# ---------- Show Rankings ----------
if all(len(st.session_state[f"player_{i+1}_hand"]) == 5 for i in range(num_players)):
    st.markdown("---")
    st.markdown('<div class="rank-title">🏆 Team Member Rankings</div>', unsafe_allow_html=True)

    results = []
    for i in range(num_players):
        pid = f"player_{i+1}_hand"
        hand = st.session_state[pid]
        score = evaluate_hand(hand)
        results.append((i + 1, score, hand))

    results.sort(key=lambda x: (x[1][0], -x[1][2][0]))

    for idx, (player_num, (rank, label, values), hand) in enumerate(results, start=1):
        card_display = ''.join(f'<div class="card">{r}{s}</div>' for r, s in hand)
        st.markdown(f"""
            <div style='padding:10px; margin:10px 0; border-radius:12px; background-color:#f9f9f9'>
                <h3 style='margin:0;'>#{idx} - Player {player_num}</h3>
                <strong>{label}</strong> - High Card: {hand[0][0]}
                <div class="card-box">{card_display}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("Please ensure all players select exactly 5 cards to evaluate rankings.")
