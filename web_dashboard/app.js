const CONFIG = {
    bots: [
        { id: 8080, name: "Bot 1", url: "http://127.0.0.1:8080/api/v1" },
        { id: 8081, name: "Bot 2", url: "http://127.0.0.1:8081/api/v1" },
        { id: 8082, name: "Bot 3", url: "http://127.0.0.1:8082/api/v1" },
        { id: 8083, name: "Bot 4", url: "http://127.0.0.1:8083/api/v1" },
        { id: 8084, name: "Bot 5", url: "http://127.0.0.1:8084/api/v1" },
        { id: 8085, name: "Bot 6 (Dip)", url: "http://127.0.0.1:8085/api/v1" },
        { id: 8086, name: "Bot 7 (MH)", url: "http://127.0.0.1:8086/api/v1" }
    ],
    auth: {
        username: "freqtrader",
        password: "freqtrade123"
    }
};

const state = {
    tokens: {}, // { 8080: "token_abc", ... }
    balances: {}, // { 8080: 123.45, ... }
    isRefreshing: false
};

// --- API Helpers ---

async function login(botId) {
    const bot = CONFIG.bots.find(b => b.id === botId);
    try {
        const credentials = btoa(`${CONFIG.auth.username}:${CONFIG.auth.password}`);
        const response = await fetch(`${bot.url}/token/login`, {
            method: 'POST',
            headers: { 'Authorization': `Basic ${credentials}` }
        });

        if (response.ok) {
            const data = await response.json();
            state.tokens[botId] = data.access_token;
            return true;
        }
    } catch (e) {
        console.error(`Login failed for ${botId}`, e);
    }
    return false;
}

async function apiCall(botId, endpoint, method = 'GET', body = null, isRetry = false) {
    const bot = CONFIG.bots.find(b => b.id === botId);
    if (!state.tokens[botId]) await login(botId);

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000); // 15s timeout

    try {
        const headers = { 'Authorization': `Bearer ${state.tokens[botId]}` };
        if (body) headers['Content-Type'] = 'application/json';

        const response = await fetch(`${bot.url}${endpoint}`, {
            method,
            headers,
            body: body ? JSON.stringify(body) : null,
            signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (response.status === 401 && !isRetry) {
            await login(botId);
            return apiCall(botId, endpoint, method, body, true);
        }
        return response.ok ? await response.json() : null;
    } catch (e) {
        clearTimeout(timeoutId);
        console.error(`API Error ${botId} ${endpoint}`, e);
        return null;
    }
}

// --- Actions ---

async function handleManualEntry(botId, side) {
    const card = document.getElementById(`bot-${botId}`);
    const input = card.querySelector(`.pair-input`);
    const pair = input.value.trim().toUpperCase();
    if (!pair) {
        showToast("Please enter a pair (e.g., BTC/USDT)", "error");
        return;
    }

    const actionText = side === 'buy' ? 'LONG' : 'SHORT';
    showToast(`Attempting to enter ${pair} ${actionText} on Bot ${botId}...`);

    const res = await apiCall(botId, '/forceenter', 'POST', {
        pair: pair,
        side: side
    });

    if (res && (res.trade_id || res.status === "ok")) {
        showToast(`Success! Entered ${pair} ${actionText}`, "success");
        input.value = "";
        refreshBot(botId);
    } else {
        showToast(`Failed: ${res ? res.message || JSON.stringify(res) : 'Network Error'}`, "error");
    }
}

async function handleSell(botId, tradeId) {
    if (!confirm("Are you sure you want to panic sell this trade?")) return;

    showToast(`Selling trade ${tradeId}...`);
    const res = await apiCall(botId, '/forceexit', 'POST', { trade_id: tradeId });

    if (res && (res.result === "success" || res.trade_id || res.status === "ok")) {
        showToast("Sell order placed successfully!", "success");
        refreshBot(botId);
    } else {
        showToast(`Sell failed: ${res ? res.message || JSON.stringify(res) : 'Error'}`, "error");
    }
}

// --- UI Updates ---

async function refreshAll() {
    if (state.isRefreshing) return;
    state.isRefreshing = true;

    try {
        // Run refreshes in parallel but DON'T wait for all to finish before updating UI
        const refreshPromises = CONFIG.bots.map(bot => refreshBot(bot.id));
        const results = await Promise.all(refreshPromises);
        const onlineCount = results.filter(r => r === true).length;

        const globalStatus = document.getElementById('global-status');
        if (onlineCount === CONFIG.bots.length) {
            globalStatus.textContent = "SYSTEM HEALTHY";
            globalStatus.style.color = "var(--success)";
        } else if (onlineCount > 0) {
            globalStatus.textContent = `PARTIAL: ${onlineCount}/${CONFIG.bots.length} ONLINE`;
            globalStatus.style.color = "var(--accent-3)";
        } else {
            globalStatus.textContent = "ALL BOTS OFFLINE";
            globalStatus.style.color = "var(--danger)";
        }

        // Update Global Total based on latest state.balances
        updateTotalBalance();

    } catch (e) {
        console.error("Refresh error", e);
    } finally {
        state.isRefreshing = false;
    }
}

function updateTotalBalance() {
    const total = Object.values(state.balances).reduce((sum, b) => sum + b, 0);
    const el = document.getElementById('total-balance');
    if (el) {
        el.textContent = `$${total.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }
}

async function refreshBot(botId) {
    const card = document.getElementById(`bot-${botId}`);
    if (!card) return false;

    const [statusData, profitData, balanceData] = await Promise.all([
        apiCall(botId, '/status'),
        apiCall(botId, '/profit'),
        apiCall(botId, '/balance')
    ]);

    const statusEl = card.querySelector('.status-indicator');
    if (!statusEl) return false;

    if (statusData) {
        card.classList.remove("offline-card");
        statusEl.textContent = "ONLINE";
        statusEl.classList.remove("offline");
        statusEl.classList.add("online");

        // Update Profit
        const profitValEl = card.querySelector('.profit-val');
        if (profitValEl && profitData) {
            const profitPct = profitData.profit_all_percent != null ? profitData.profit_all_percent.toFixed(2) : "0.00";
            profitValEl.textContent = `${profitPct}%`;
            profitValEl.style.color = parseFloat(profitPct) >= 0 ? 'var(--success)' : 'var(--danger)';
        }

        // Update Balance
        const balanceValEl = card.querySelector('.balance-val');
        if (balanceValEl && balanceData && balanceData.currencies) {
            const usdt = balanceData.currencies.find(c => c.currency === 'USDT');
            if (usdt) {
                const bal = usdt.balance || 0;
                balanceValEl.textContent = `$${bal.toFixed(2)}`;
                state.balances[botId] = bal;
            }
        }

        // Update Trades List
        const listEl = card.querySelector('.trades-list');
        if (listEl) {
            listEl.innerHTML = '';
            let trades = Array.isArray(statusData) ? statusData : (statusData.trades || []);

            if (trades.length === 0) {
                listEl.innerHTML = '<li style="color:var(--text-muted); font-size:0.9rem; text-align:center;">No active trades</li>';
            } else {
                trades.forEach(t => {
                    const li = document.createElement('li');
                    li.className = 'trade-item';
                    const profit = (t.profit_ratio * 100).toFixed(2);
                    const profitClass = parseFloat(profit) >= 0 ? 'pos' : 'neg';

                    li.innerHTML = `
                        <div class="trade-info">
                            <strong>${t.pair}</strong>
                            <span class="trade-profit ${profitClass}">${profit}%</span>
                        </div>
                        <button class="btn-sell" onclick="handleSell(${botId}, ${t.trade_id})">SELL</button>
                    `;
                    listEl.appendChild(li);
                });
            }
        }
        return true;
    } else {
        card.classList.add("offline-card");
        statusEl.textContent = "OFFLINE";
        statusEl.classList.remove("online");
        statusEl.classList.add("offline");
        state.balances[botId] = 0;
        return false;
    }
}

function showToast(msg, type = "info") {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    if (type === "error") toast.style.borderLeftColor = "var(--danger)";
    if (type === "success") toast.style.borderLeftColor = "var(--success)";

    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}

// --- Init ---
document.addEventListener('DOMContentLoaded', () => {
    refreshAll();
    setInterval(refreshAll, 5000);
});
