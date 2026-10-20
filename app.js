// ============================================================
// LLM Database Explorer — frontend (data schema v2.0)
// Reads llm_pricing_data.json only. No hardcoded model data.
// ============================================================
'use strict';

const $ = (id) => document.getElementById(id);
const fmt = (n) => (n === null || n === undefined ? '—' : n.toLocaleString());
const money = (n) => (n === null || n === undefined ? '—' : '$' + n);
const yuan = (n) => (n === null || n === undefined ? '—' : '¥' + n);

let DATA = null;          // raw JSON
let MODELS = [];          // flattened model rows w/ provider info
let NEWS = [];            // flattened news rows
let activeGroup = '';

// ---------- 载入 ----------
async function load() {
    try {
        const r = await fetch('llm_pricing_data.json');
        DATA = await r.json();
        flatten();
        $('dataMeta').textContent =
            `schema v${DATA.schema_version} · 数据截至 ${DATA.data_as_of} · 生成于 ${DATA.generated_at.slice(0, 10)}`;
        $('methodology').textContent = DATA.methodology;
        renderHealth();
        buildFilters();
        renderModels();
        renderNews();
    } catch (e) {
        console.error(e);
        $('modelsArea').innerHTML =
            '<div class="empty">数据加载失败：' + escapeHtml(String(e)) + '</div>';
    }
}

function flatten() {
    MODELS = [];
    DATA.providers.forEach((p) => {
        p.models.forEach((m) => MODELS.push(Object.assign({
            provider: p.name, provider_en: p.en_name, region: p.region, group: p.group,
            china_access: p.china_access, docs_url: p.docs_url,
            has_official_cn_source: p.has_official_cn_source
        }, m)));
    });
    NEWS = [];
    (DATA.provider_news || []).forEach((g) => {
        (g.items || []).forEach((it) => NEWS.push(Object.assign({
            provider: g.provider, source_type: g.source_type,
            source_url: g.source_url, crawled_at: g.crawled_at, group_note: g.note
        }, it)));
    });
}

// ---------- 分组标签 ----------
function renderGroupTabs() {
    const nav = $('groupTabs');
    nav.innerHTML = '<button class="group-tab active" data-group="">全部</button>';
    Object.entries(DATA.taxonomy.groups).forEach(([k, v]) => {
        const b = document.createElement('button');
        b.className = 'group-tab';
        b.dataset.group = k;
        b.textContent = v.value;
        b.onclick = () => {
            activeGroup = k;
            nav.querySelectorAll('.group-tab').forEach((x) => x.classList.toggle('active', x.dataset.group === k));
            renderModels();
        };
        nav.appendChild(b);
    });
}

// ---------- 筛选器 ----------
function buildFilters() {
    const add = (sel, val, txt) => {
        const o = document.createElement('option');
        o.value = val; o.textContent = txt;
        sel.appendChild(o);
    };
    const pf = $('providerFilter');
    const byGroup = (a, b) =>
        (a.group < b.group ? -1 : a.group > b.group ? 1 : a.provider.localeCompare(b.provider));
    const provs = [];
    MODELS.forEach((m) => { if (!provs.some((x) => x.name === m.provider && x.group === m.group)) provs.push(m); });
    provs.sort(byGroup).forEach((m) => add(pf, m.provider, `${DATA.taxonomy.groups[m.group].value} · ${m.provider}`));

    const cf = $('categoryFilter');
    Object.entries(DATA.taxonomy.categories).forEach(([k, v]) => add(cf, k, v));

    const af = $('accessFilter');
    Object.entries(DATA.taxonomy.china_access).forEach(([k, v]) => add(af, k, v));

    const ctx = $('contextFilter');
    [0, 32768, 131072, 262144, 500000, 1000000, 2000000].forEach((c) => {
        add(ctx, c, c === 0 ? '不限' : c >= 1e6 ? c / 1e6 + 'M' : c / 1024 + 'K');
    });

    const np = $('newsProvider');
    [...new Set(NEWS.map((n) => n.provider))].sort().forEach((p) => add(np, p, p));
    const ns = $('newsSource');
    [...new Set(NEWS.map((n) => n.source_type))].sort().forEach((s) => add(ns, s, s));

    renderGroupTabs();

    ['providerFilter', 'categoryFilter', 'accessFilter', 'sourceFilter', 'priceSort',
     'contextFilter', 'minInputPrice', 'maxInputPrice', 'minOutputPrice', 'maxOutputPrice',
     'peakOnly', 'cnyOnly', 'newsProvider', 'newsSource'].forEach((id) => {
        $(id).addEventListener(id.endsWith('Price') ? 'input' : 'change', () => {
            if (id.startsWith('news')) renderNews(); else renderModels();
        });
    });
    $('searchInput').addEventListener('input', renderModels);
    $('searchBtn').addEventListener('click', renderModels);
    $('searchInput').addEventListener('keydown', (e) => { if (e.key === 'Enter') renderModels(); });
    $('clearBtn').addEventListener('click', clearFilters);
}

function clearFilters() {
    ['searchInput', 'providerFilter', 'categoryFilter', 'accessFilter', 'sourceFilter',
     'priceSort', 'minInputPrice', 'maxInputPrice', 'minOutputPrice', 'maxOutputPrice',
     'peakOnly', 'cnyOnly'].forEach((id) => {
        const el = $(id);
        el.value = el.type === 'checkbox' ? false : '';
    });
    activeGroup = '';
    renderGroupTabs();
    renderModels();
}

// ---------- 过滤 ----------
function filteredModels() {
    const q = $('searchInput').value.trim().toLowerCase();
    const prov = $('providerFilter').value;
    const cat = $('categoryFilter').value;
    const acc = $('accessFilter').value;
    const srcf = $('sourceFilter').value;
    const minCtx = parseInt($('contextFilter').value, 10) || 0;
    const mi = parseFloat($('minInputPrice').value);
    const ma = parseFloat($('maxInputPrice').value);
    const mo = parseFloat($('minOutputPrice').value);
    const mox = parseFloat($('maxOutputPrice').value);
    const peakOnly = $('peakOnly').checked;
    const cnyOnly = $('cnyOnly').checked;

    let out = MODELS.filter((m) => {
        if (activeGroup && m.group !== activeGroup) return false;
        if (prov && m.provider !== prov) return false;
        if (cat && m.category !== cat) return false;
        if (acc && m.china_access !== acc) return false;
        if (minCtx && (m.context_length || 0) < minCtx) return false;
        if (peakOnly && !m.peak_valley) return false;
        if (cnyOnly && m.currency !== 'CNY') return false;

        const inp = m.input_price_per_million;
        const outp = m.output_price_per_million;
        const hasIn = inp !== null && inp !== undefined;
        const hasOut = outp !== null && outp !== undefined;
        if (srcf === 'dual' && !(m.sources && m.sources.length >= 2)) return false;
        if (srcf === 'single' && !(m.sources && m.sources.length === 1)) return false;
        if (srcf === 'official' && !(m.sources || []).some((s) => String(s.kind || '').includes('official'))) return false;

        // 价格区间按 USD 等价值过滤（CNY 价已附 usd 换算），无价格的条目在区间筛选下不显示
        if (mi || ma || mo || mox) {
            const iv = hasIn ? (m.currency === 'CNY' ? m.input_price_usd_per_million : inp) : null;
            const ov = hasOut ? (m.currency === 'CNY' ? m.output_price_usd_per_million : outp) : null;
            if (mi && !(iv !== null && iv >= mi)) return false;
            if (ma && !(iv !== null && iv <= ma)) return false;
            if (mo && !(ov !== null && ov >= mo)) return false;
            if (mox && !(ov !== null && ov <= mox)) return false;
        }

        if (q) {
            const hay = [m.model_id, m.name, m.provider, m.provider_en,
                         m.category, m.note, m.cross_check, m.currency,
                         (m.sources || []).map((s) => s.name + ' ' + (s.note || '')).join(' ')].join(' ').toLowerCase();
            if (!hay.includes(q)) return false;
        }
        return true;
    });

    const s = $('priceSort').value;
    const key = s.startsWith('input') ? 'input_price_usd_per_million' : 'output_price_usd_per_million';
    const dir = s.endsWith('asc') ? 1 : -1;
    if (s) out.sort((a, b) => {
        const av = a[key], bv = b[key];
        if (av === null && bv === null) return 0;
        if (av === null) return 1;
        if (bv === null) return -1;
        return (av - bv) * dir;
    });
    return out;
}

// ---------- 渲染模型 ----------
function escapeHtml(s) {
    return String(s === null || s === undefined ? '' : s)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function renderModels() {
    const list = filteredModels();
    const area = $('modelsArea');
    $('resultCount').textContent = `${list.length} / ${MODELS.length} 条`;

    if (!list.length) { area.innerHTML = '<div class="empty">没有符合条件的模型，请放宽筛选条件。</div>'; }
    else { area.innerHTML = list.map(cardHtml).join(''); }

    $('totalCount').textContent = MODELS.length;
    $('providerCount').textContent = DATA.providers.length;
    $('dualCount').textContent = MODELS.filter((m) => (m.sources || []).length >= 2).length;
    $('peakCount').textContent = MODELS.filter((m) => m.peak_valley).length;
}

function cardHtml(m) {
    const g = DATA.taxonomy.groups[m.group].value;
    const c = DATA.taxonomy.categories[m.category] || m.category;
    const a = DATA.taxonomy.china_access[m.china_access] || m.china_access;
    const dual = (m.sources || []).length >= 2;
    const cur = m.currency === 'CNY' ? '¥' : '$';
    const pv = m.peak_valley;

    let pvHtml = '';
    if (pv) {
        pvHtml = `<div class="pv-box"><span class="pv-tag">波峰波谷</span>
          <p><b>峰：</b>${escapeHtml(pv.peak_windows)}<br><b>谷：</b>${escapeHtml(pv.valley_windows)}</p>
          <p class="pv-disc"><b>折扣：</b>${escapeHtml(pv.discount)}</p>
          ${pv.note ? `<p class="pv-note">${escapeHtml(pv.note)}</p>` : ''}
          <a href="${escapeHtml(pv.source_url)}" target="_blank" rel="noopener">来源 ↗</a></div>`;
    }

    return `<article class="model-card">
      <header>
        <h3>${escapeHtml(m.name)}<code>${escapeHtml(m.model_id)}</code></h3>
        <div class="tags">
          <span class="tag group">${escapeHtml(g)}</span>
          <span class="tag cat">${escapeHtml(c)}</span>
          <span class="tag access ${m.china_access}">${escapeHtml(a)}</span>
          ${dual ? '<span class="tag dual">双源已交叉</span>' : '<span class="tag single">单一来源</span>'}
        </div>
      </header>
      <p class="prov">${escapeHtml(m.provider)} · 上下文 <b>${fmt(m.context_length)}</b> tokens · <span title="${m.currency === 'CNY' ? '人民币计价，附约 USD 换算值' : '美元计价'}">${escapeHtml(m.currency)}</span></p>
      <table class="price-table">
        <thead><tr><th></th><th>原生计价</th><th>约 USD（仅对比）</th></tr></thead>
        <tbody>
          <tr><td>输入 /M</td><td>${m.input_price_per_million === null ? '—' : cur + m.input_price_per_million}</td><td>${money(m.input_price_usd_per_million)}</td></tr>
          <tr><td>输出 /M</td><td>${m.output_price_per_million === null ? '—' : cur + m.output_price_per_million}</td><td>${money(m.output_price_usd_per_million)}</td></tr>
          ${m.cache_hit_input_per_million !== null ? `<tr><td>缓存命中输入 /M</td><td>${cur + m.cache_hit_input_per_million}</td><td>${money(m.cache_hit_input_per_million * 0.1408)}</td></tr>` : ''}
        </tbody>
      </table>
      <p class="cross">${escapeHtml(m.cross_check)}</p>
      ${(m.sources || []).map((s) => `<p class="src"><a href="${escapeHtml(s.url)}" target="_blank" rel="noopener">${escapeHtml(s.name)}</a>${s.note ? ' <span class="src-note">' + escapeHtml(s.note) + '</span>' : ''}</p>`).join('')}
      ${m.note ? `<p class="note">${escapeHtml(m.note)}</p>` : ''}
      ${pvHtml}
      <p class="docs"><a href="${escapeHtml(m.docs_url)}" target="_blank" rel="noopener">厂商文档 ↗</a></p>
    </article>`;
}

// ---------- 峰谷区块 ----------
function renderPeakValley() {
    $('pvGrid').innerHTML = (DATA.peak_valley || []).map((v) => `
      <article class="pv-card">
        <h3>${escapeHtml(v.provider)} <small>${escapeHtml(v.scope)}</small></h3>
        <dl>
          <dt>峰时段</dt><dd>${escapeHtml(v.peak_windows)}</dd>
          <dt>谷时段</dt><dd>${escapeHtml(v.valley_windows)}</dd>
          <dt>折扣</dt><dd>${escapeHtml(v.discount)}</dd>
          ${v.tz ? `<dt>时区口径</dt><dd>${escapeHtml(v.tz)}</dd>` : ''}
        </dl>
        <p class="quote">${escapeHtml(v.evidence)}</p>
        ${v.note ? `<p class="pv-note">${escapeHtml(v.note)}</p>` : ''}
        <p class="src"><a href="${escapeHtml(v.source_url)}" target="_blank" rel="noopener">取数来源 ↗</a></p>
      </article>`).join('');
}

// ---------- 新闻区块 ----------
function renderNews() {
    const prov = $('newsProvider').value;
    const srcf = $('newsSource').value;
    const list = NEWS.filter((n) => (!prov || n.provider === prov) && (!srcf || n.source_type === srcf));
    const grid = $('newsGrid');
    if (!list.length) { grid.innerHTML = '<div class="empty">该条件下没有新闻条目。</div>'; return; }
    const byProv = {};
    list.forEach((n) => { (byProv[n.provider] = byProv[n.provider] || []).push(n); });
    grid.innerHTML = Object.keys(byProv).sort().map((p) => `
      <article class="news-card">
        <header><h3>${escapeHtml(p)}</h3></header>
        <ul>${byProv[p].map((n) => `<li>
          ${n.url ? `<a href="${escapeHtml(n.url)}" target="_blank" rel="noopener">${escapeHtml(n.title)}</a>` : escapeHtml(n.title)}
          <span class="news-meta">${n.date || '—'} · ${escapeHtml(n.source || n.source_type)}</span>
        </li>`).join('')}</ul>
        <p class="pv-note">${escapeHtml(byProv[p][0].group_note || '')}</p>
      </article>`).join('');
}

// ---------- 健康表 ----------
function renderHealth() {
    const okList = [];
    (DATA.source_health || []).forEach((h) => okList.push(h));
    const tb = $('healthTable').querySelector('tbody');
    tb.innerHTML = okList.map((h) => {
        const size = h.bytes ? fmt(h.bytes) + ' B' : (h.items ? h.items + ' 条' : '—');
        return `<tr class="${h.ok ? 'ok' : 'fail'}">
          <td>${h.ok ? '✓ 可达' : '✗ 不可达'}</td>
          <td><a href="${escapeHtml(h.url)}" target="_blank" rel="noopener">${escapeHtml(h.url)}</a></td>
          <td>${escapeHtml(h.kind || '')}</td>
          <td>${size}</td>
          <td>${escapeHtml(h.error || h.note || '')}${h.retry_count ? ` · 重试 ${h.retry_count} 次` : ''}</td>
        </tr>`;
    }).join('');
    $('unresolvedList').innerHTML = (DATA.unresolved || []).map((u) => `<li>${escapeHtml(u)}</li>`).join('');
    $('deprecatedList').innerHTML = (DATA.deprecated_paths || []).map((d) =>
      `<li>✗ ${escapeHtml(d.from)} <span class="err">${escapeHtml(d.error)}</span><br>
       → <a href="${escapeHtml(d.to)}" target="_blank" rel="noopener">${escapeHtml(d.to)}</a></li>`).join('');
}

load();
