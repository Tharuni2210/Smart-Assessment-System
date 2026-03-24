// 🌟 Auto apply animation
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".card, .dashboard-card, table, canvas")
        .forEach(el => el.classList.add("fade-in"));
});

// 🌟 Highlight top 3 leaderboard rows
const rows = document.querySelectorAll("table tr");

rows.forEach((row, index) => {
    if (index === 1) row.classList.add("gold");
    if (index === 2) row.classList.add("silver");
    if (index === 3) row.classList.add("bronze");
});

