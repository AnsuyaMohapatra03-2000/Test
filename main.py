import streamlit as st

# --- Poker Hand Evaluation Helper ---
def evaluate_hand(hand):
    """Evaluate a 5-card poker hand and return a numeric rank (lower is better)."""
    ranks_order = '23456789TJQKA'
    rank_map = {r: i for i, r in enumerate(ranks_order)}
    values = sorted([rank_map[card[0]] for card in hand], reverse=True)
    suits = [card[1] for card in hand]
    is_flush = len(set(suits)) == 1
    is_straight = all(values[i] - 1 == values[i+1] for i in range(4))

    counts = {v: values.count(v) for v in set(values)}
    sorted_counts = sorted(counts.values(), reverse=True)

    if is_straight and is_flush:
        return (1, values)  # Straight flush
    elif sorted_counts == [4, 1]:
        return (2, values)  # Four of a kind
    elif sorted_counts == [3, 2]:
        return (3, values)  # Full house
    elif is_flush:
        return (4, values)  # Flush
    elif is_straight:
        return (5, values)  # Straight
    elif sorted_counts == [3, 1, 1]:
        return (6, values)  # Three of a kind
    elif sorted_counts == [2, 2, 1]:
        return (7, values)  # Two pair
    elif sorted_counts == [2, 1, 1, 1]:
        return (8, values)  # One pair
    else:
        return (9, values)  # High card

# --- UI Config ---
st.set_page_config(page_title="Team Card Assignment", layout="centered")

st.title("🎴 Team Card Assignment")
st.markdown("Select 5 cards per player, evaluate their poker hands, then rank the team members!")

# --- Setup ---
players = ["Player 1", "Player 2", "Player 3"]
ranks = list("23456789TJQKA")
suits = ["♠", "♥", "♦", "♣"]

# --- Session State Initialization ---
for p in players:
    if p not in st.session_state:
        st.session_state[p] = []

# --- Card Input for Each Player ---
for p in players:
    st.subheader(p)
    cols = st.columns(3)
    with cols[0]:
        rank = st.selectbox(f"Rank", ranks, key=f"rank_{p}")
    with cols[1]:
        suit = st.selectbox(f"Suit", suits, key=f"suit_{p}")
    with cols[2]:
        if st.button(f"Add {rank}{suit}", key=f"add_{p}"):
            card = (rank, suit)
            # 🔧 Fix: Only extract from actual player hands
            used = {c for k, hand in st.session_state.items() if k in players for c in hand}
            if card in used:
                st.error("🛑 Card already taken!")
            elif len(st.session_state[p]) >= 5:
                st.warning("✋ Hand already has 5 cards.")
            else:
                st.session_state[p].append(card)

    # Display current hand
    st.write("Current Hand:", st.session_state[p])

# --- Evaluate and Rank Players ---
if st.button("🏆 Evaluate & Rank"):
    hands = {}
    for p in players:
        if len(st.session_state[p]) != 5:
            st.warning(f"{p} does not have 5 cards yet.")
        else:
            hands[p] = st.session_state[p]

    if len(hands) == len(players):  # All hands are ready
        scores = [(p, evaluate_hand(h)) for p, h in hands.items()]
        scores.sort(key=lambda x: x[1])  # Lower rank is better

        st.success("✅ Poker Hands Ranked:")
        for i, (p, score) in enumerate(scores, 1):
            st.write(f"**#{i} - {p}** → Hand: {st.session_state[p]}")

# --- Reset Button ---
if st.button("🔁 Reset Game"):
    for p in players:
        st.session_state[p] = []
