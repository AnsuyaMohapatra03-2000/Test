import streamlit as st

# Constants
CARDS = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
SUITS = ['♠', '♥', '♦', '♣']
CARD_VALUES = {r: i for i, r in enumerate(reversed(CARDS), start=2)}

def evaluate_hand(hand):
    vals = sorted([CARD_VALUES[c[0]] for c in hand], reverse=True)
    suits = [c[1] for c in hand]
    counts = sorted({v: vals.count(v) for v in vals}.values(), reverse=True)
    is_flush = len(set(suits)) == 1
    is_straight = all(vals[i] - 1 == vals[i+1] for i in range(4)) or vals == [14,5,4,3,2]
    if is_flush and is_straight and vals[0] == 14: return ("Royal Flush", 10, vals)
    if is_flush and is_straight: return ("Straight Flush", 9, vals)
    if counts[0] == 4: return ("Four of a Kind", 8, vals)
    if counts[0] == 3 and counts[1] == 2: return ("Full House", 7, vals)
    if is_flush: return ("Flush", 6, vals)
    if is_straight: return ("Straight", 5, vals)
    if counts[0] == 3: return ("Three of a Kind", 4, vals)
    if counts[0] == 2 and counts[1] == 2: return ("Two Pair", 3, vals)
    if counts[0] == 2: return ("One Pair", 2, vals)
    return ("High Card", 1, vals)

st.set_page_config(page_title="Team Card Assignment", layout="wide")
st.title("🎴 Team Card Assignment")
st.markdown("Select 5 cards per player, evaluate their poker hands, then rank the team members!")

players = [f"Player {i+1}" for i in range(6)]

# Initialize hands state
for p in players:
    if p not in st.session_state:
        st.session_state[p] = []

# UI: input columns
cols = st.columns(3)
for idx, p in enumerate(players):
    col = cols[idx % 3]
    with col:
        st.subheader(p)
        hand = st.session_state[p]
        # Input selectors
        rank = st.selectbox("Rank", CARDS, key=f"rank_{p}")
        suit = st.selectbox("Suit", SUITS, key=f"suit_{p}")
        card = (rank, suit)
        if st.button(f"Add {rank}{suit}", key=f"add_{p}"):
            used = {c for hand in st.session_state.values() for c in hand}
            if card in used:
                st.error("🛑 Card already taken!")
            elif len(hand) >= 5:
                st.warning("✋ Hand already has 5 cards.")
            else:
                hand.append(card)
        # Display current hand
        if hand:
            st.markdown("**Selected Cards:** " + "  |  ".join(f"{r}{s}" for r, s in hand))
        if st.button("Clear Hand", key=f"clear_{p}"):
            st.session_state[p] = []

st.markdown("---")

# Actions
if st.button("🔍 Evaluate Hands"):
    complete = all(len(st.session_state[p]) == 5 for p in players)
    if not complete:
        st.warning("Each player needs exactly 5 cards!")
    else:
        results = []
        for p in players:
            ht, hr, tieb = evaluate_hand(st.session_state[p])
            results.append((p, ht, hr, tieb, st.session_state[p]))
        results.sort(key=lambda x: (x[3], x[2]), reverse=True)
        st.markdown("## 🏆 Rankings")
        for rank, (p, ht, hr, _, hand) in enumerate(results, start=1):
            st.markdown(f"**#{rank} – {p}**")
            st.markdown(f"- Hand Type: *{ht}*")
            st.markdown(f"- High Cards: {', '.join(map(str, hr))}")
            st.markdown(f"- Cards: {' | '.join(f'{r}{s}' for r, s in hand)}")
            
if st.button("🔄 Reset All Hands"):
    for p in players:
        st.session_state[p] = []
    st.experimental_rerun()
