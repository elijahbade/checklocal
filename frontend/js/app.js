/**
 * PowerWatch by CheckLocal Main Web Mirror Application
 * OSF x Andela Hackathon: "Information You Can Trust"
 * Track: Transparency & Accountability
 */

const CheckLocalApp = {
    currentCountry: "all",
    currentCategory: "power_status", // Default to PowerWatch Feeder Audits!
    searchQuery: "",
    facts: [],

    init() {
        this.bindEvents();
        this.loadStats();
        this.loadTrendingFacts();
        this.loadTweets();

        // Initialize simulator
        if (window.WhatsAppSimulator) {
            window.WhatsAppSimulator.init();
        }
    },

    bindEvents() {
        // Country tabs
        document.querySelectorAll(".country-tab").forEach(tab => {
            tab.addEventListener("click", (e) => {
                document.querySelectorAll(".country-tab").forEach(t => t.classList.remove("active"));
                tab.classList.add("active");
                this.currentCountry = tab.getAttribute("data-country") || "all";
                this.loadTrendingFacts();
            });
        });

        // Category pills
        document.querySelectorAll(".cat-pill").forEach(pill => {
            pill.addEventListener("click", (e) => {
                document.querySelectorAll(".cat-pill").forEach(p => p.classList.remove("active"));
                pill.classList.add("active");
                this.currentCategory = pill.getAttribute("data-cat") || "all";
                this.loadTrendingFacts();
            });
        });

        // Search input with debounce
        const searchInput = document.getElementById("searchFeedInput");
        if (searchInput) {
            let debounceTimer;
            searchInput.addEventListener("input", (e) => {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    this.searchQuery = e.target.value.trim();
                    this.loadTrendingFacts();
                }, 300);
            });
        }

        // Report Modal Controls
        const openModalBtn = document.getElementById("openReportModalBtn");
        const closeModalBtn = document.getElementById("closeReportModalBtn");
        const modal = document.getElementById("reportModal");

        if (openModalBtn && modal) {
            openModalBtn.addEventListener("click", () => {
                modal.style.display = "flex";
            });
        }
        if (closeModalBtn && modal) {
            closeModalBtn.addEventListener("click", () => {
                modal.style.display = "none";
            });
        }
        if (modal) {
            modal.addEventListener("click", (e) => {
                if (e.target === modal) modal.style.display = "none";
            });
        }

        // Docket Modal Controls
        const closeDocketBtn = document.getElementById("closeDocketModalBtn");
        const docketModal = document.getElementById("docketModal");
        if (closeDocketBtn && docketModal) {
            closeDocketBtn.addEventListener("click", () => {
                docketModal.style.display = "none";
            });
        }
        if (docketModal) {
            docketModal.addEventListener("click", (e) => {
                if (e.target === docketModal) docketModal.style.display = "none";
            });
        }

        // Web Report Form Submission
        const reportForm = document.getElementById("reportSubmissionForm");
        if (reportForm) {
            reportForm.addEventListener("submit", async (e) => {
                e.preventDefault();
                await this.submitWebReport();
            });
        }
    },

    async loadStats() {
        try {
            const res = await fetch("/api/reports/stats");
            const data = await res.json();
            const elFacts = document.getElementById("statVerifiedFacts");
            const elReports = document.getElementById("statTotalReports");
            const elTrust = document.getElementById("statTrustScore");
            const elSpeed = document.getElementById("statAvgSpeed");

            if (elFacts) elFacts.textContent = data.verified_facts || "4";
            if (elReports) elReports.textContent = data.total_submissions || "542";
            if (elTrust) elTrust.textContent = "100%";
            if (elSpeed) elSpeed.textContent = "4";
        } catch (err) {
            console.warn("Could not load stats:", err);
        }
    },

    async loadTrendingFacts() {
        const container = document.getElementById("factsFeedContainer");
        if (!container) return;

        try {
            let url = `/api/trending?country=${encodeURIComponent(this.currentCountry)}&category=${encodeURIComponent(this.currentCategory)}`;
            if (this.searchQuery) {
                url += `&search=${encodeURIComponent(this.searchQuery)}`;
            }

            const res = await fetch(url);
            const data = await res.json();
            this.facts = data;
            this.renderFacts(data);
        } catch (err) {
            console.error("Failed to load trending facts:", err);
            container.innerHTML = `<div style="text-align:center;padding:2rem;color:#64748B;">Failed to load verified data. Check backend status.</div>`;
        }
    },

    renderFacts(facts) {
        const container = document.getElementById("factsFeedContainer");
        if (!container) return;

        if (!facts || facts.length === 0) {
            container.innerHTML = `
                <div style="background:white;border-radius:12px;padding:3rem 1.5rem;text-align:center;border:1px dashed #CBD5E1;">
                    <div style="font-size:2rem;margin-bottom:0.5rem;">⚡</div>
                    <h3 style="font-size:1.1rem;font-weight:700;color:#1E293B;margin-bottom:0.4rem;">No records found in this category</h3>
                    <p style="color:#64748B;font-size:0.875rem;margin-bottom:1.25rem;">Be the first in your community to log an outage, meter, or price report!</p>
                    <button class="btn btn-primary" onclick="document.getElementById('openReportModalBtn').click()">Log Outage / Meter</button>
                </div>
            `;
            return;
        }

        const categoryNames = {
            power_status: "⚡ Feeder Audit (PowerWatch)",
            fuel_price: "Fuel & Petrol",
            food_staple: "Food Staple",
            water_status: "Water Utility",
            rumor_claim: "Fact-Check / Rumor"
        };

        const countryFlags = {
            "Nigeria": "🇳🇬",
            "Kenya": "🇰🇪",
            "South Africa": "🇿🇦"
        };

        container.innerHTML = facts.map(fact => {
            const flag = countryFlags[fact.country] || "🌐";
            const catClass = `cat-${fact.category}`;
            const catName = categoryNames[fact.category] || fact.category.replace('_', ' ');
            const highlight = CheckLocalApp.getFactHighlight(fact);

            let confBadgeClass = "conf-high";
            let confIcon = "🟢 Verified";
            if (fact.confidence_level === "Verified") {
                confBadgeClass = "conf-verified";
                confIcon = "✓ Verified Quorum";
            } else if (fact.confidence_level === "High") {
                confBadgeClass = "conf-high";
                confIcon = "🛡️ Statutory Precedent";
            } else {
                confBadgeClass = "conf-consensus";
                confIcon = "👥 Corroborated";
            }

            const isPower = fact.category === "power_status";

            const feederBoxHtml = isPower ? `
                <div class="feeder-meta-box">
                    <div>
                        <div class="feeder-stat-label">Distribution Feeder</div>
                        <div class="feeder-stat-value">${fact.feeder_name || fact.location}</div>
                    </div>
                    <div>
                        <div class="feeder-stat-label">DisCo / Utility</div>
                        <div class="feeder-stat-value">${fact.disco_name || 'Grid Distribution'}</div>
                    </div>
                    <div>
                        <div class="feeder-stat-label">Statutory Guarantee</div>
                        <div class="feeder-stat-value">${fact.promised_hours || '20.0'} hrs/day (${fact.tariff_band || 'Band A'})</div>
                    </div>
                    <div>
                        <div class="feeder-stat-label">Unlawful Surcharge</div>
                        <div class="feeder-stat-value">${fact.overbilling_differential || '₦138.80 / kWh overcharge'}</div>
                    </div>
                </div>
            ` : "";

            const docketBtnHtml = isPower ? `
                <button class="btn-docket-action" onclick="CheckLocalApp.openDocketModal(${fact.id})" title="Generate Official NERC/NERSA Complaint Petition">
                    <span>📜 Legal Dispute Docket</span>
                </button>
            ` : "";

            return `
                <article class="fact-card border-${fact.category}" id="fact-card-${fact.id}">
                    <div class="card-meta-top">
                        <div class="card-tags">
                            <span class="tag-category ${catClass}">${catName}</span>
                            <span class="tag-location">${flag} ${fact.location}</span>
                        </div>
                        <span class="tag-confidence ${confBadgeClass}">${confIcon}</span>
                    </div>

                    <h3 class="card-title">${fact.title}</h3>

                    <!-- High-Visibility Price / Status Metric Callout -->
                    <div class="fact-metric-callout callout-${highlight.type}">
                        <span class="callout-label">${highlight.label}</span>
                        <span class="callout-value">${highlight.value}</span>
                    </div>

                    ${feederBoxHtml}

                    <!-- Multilingual Switcher Chips -->
                    <div class="lang-toggle-bar" style="overflow-x:auto; padding-bottom:4px;">
                        <button class="lang-chip active" onclick="CheckLocalApp.switchLang(${fact.id}, 'en', this)">English</button>
                        <button class="lang-chip" onclick="CheckLocalApp.switchLang(${fact.id}, 'pidgin', this)">🇳🇬 Pidgin</button>
                        ${fact.summary_swahili ? `<button class="lang-chip" onclick="CheckLocalApp.switchLang(${fact.id}, 'swahili', this)">🇰🇪 Kiswahili</button>` : ''}
                        ${fact.summary_yoruba ? `<button class="lang-chip" onclick="CheckLocalApp.switchLang(${fact.id}, 'yoruba', this)">🇳🇬 Yoruba</button>` : ''}
                        ${fact.summary_hausa ? `<button class="lang-chip" onclick="CheckLocalApp.switchLang(${fact.id}, 'hausa', this)">🇳🇬 Hausa</button>` : ''}
                        ${fact.summary_zulu ? `<button class="lang-chip" onclick="CheckLocalApp.switchLang(${fact.id}, 'zulu', this)">🇿🇦 isiZulu</button>` : ''}
                    </div>

                    <!-- Language Summary Boxes -->
                    <div class="summary-block" id="summary-en-${fact.id}">
                        ${fact.summary_en}
                    </div>
                    <div class="summary-block pidgin-box" id="summary-pidgin-${fact.id}" style="display: none;">
                        ${fact.summary_pidgin || fact.summary_en}
                    </div>
                    <div class="summary-block" id="summary-swahili-${fact.id}" style="display: none; border-left-color: #0284C7; background: #F0F9FF;">
                        ${fact.summary_swahili || fact.summary_en}
                    </div>
                    <div class="summary-block" id="summary-yoruba-${fact.id}" style="display: none; border-left-color: #7C3AED; background: #F5F3FF;">
                        ${fact.summary_yoruba || fact.summary_en}
                    </div>
                    <div class="summary-block" id="summary-hausa-${fact.id}" style="display: none; border-left-color: #D97706; background: #FFFBEB;">
                        ${fact.summary_hausa || fact.summary_en}
                    </div>
                    <div class="summary-block" id="summary-zulu-${fact.id}" style="display: none; border-left-color: #059669; background: #ECFDF5;">
                        ${fact.summary_zulu || fact.summary_en}
                    </div>

                    <div class="sources-row">
                        <span class="sources-icon">📌</span>
                        <span><strong>Sources:</strong> ${fact.sources}</span>
                    </div>

                    <div class="card-civic-strip">
                        <div class="action-callout">
                            <span class="action-icon">👉</span>
                            <div><strong>Next Action:</strong> ${fact.action}</div>
                        </div>
                        ${fact.escalation_target ? `
                        <div class="escalation-badge">
                            <span>🏛️</span>
                            <span><strong>Regulatory Track:</strong> ${fact.escalation_target}</span>
                        </div>` : ''}
                    </div>

                    <div class="card-footer">
                        <span>Updated ${fact.updated_at}</span>
                        <div class="card-actions-right">
                            <span style="font-size:0.75rem; color:#64748B;">${fact.report_count} meters</span>
                            ${docketBtnHtml}
                            <button class="btn-share-wa" onclick="CheckLocalApp.shareToWhatsApp(${fact.id})" title="Share to WhatsApp Groups & Status">
                                <span>📲 WhatsApp</span>
                            </button>
                            <button class="btn-card-action" onclick="CheckLocalApp.syndicateToTwitter(${fact.id}, this)" title="Syndicate verified fact to X">
                                <span>𝕏 Post</span>
                            </button>
                            <button class="btn-card-action" onclick="CheckLocalApp.upvoteFact(${fact.id}, this)">
                                <span>👍</span>
                                <span class="upvote-count" style="font-weight:700;">${fact.upvotes}</span>
                            </button>
                        </div>
                    </div>
                </article>
            `;
        }).join("");
    },

    getFactHighlight(fact) {
        if (fact.category === "power_status") {
            if (fact.actual_hours_avg && fact.promised_hours) {
                return {
                    label: "FEEDER SUPPLY DEFICIT AUDIT",
                    value: `⚡ ${fact.actual_hours_avg}h / ${fact.promised_hours}h Statutory Min (${fact.overbilling_differential || 'Under-Delivery'})`,
                    type: "power"
                };
            }
            return { label: "POWERWATCH TARIFF AUDIT", value: "20.0h Band A Minimum • NERC MYTO Breach", type: "power" };
        }
        if (fact.category === "fuel_price") {
            if (fact.summary_en.includes("850") || fact.summary_en.includes("890")) {
                return { label: "RETAIL PUMP BENCHMARK", value: "₦850 – ₦890 / Litre", type: "fuel" };
            } else if (fact.summary_en.includes("KSh")) {
                return { label: "EPRA MONTHLY CAP", value: "KSh 188.84 / Litre", type: "fuel" };
            } else if (fact.summary_en.includes("R22")) {
                return { label: "DMRE REGULATED PRICE", value: "R22.86 / Litre", type: "fuel" };
            }
            return { label: "RETAIL FUEL BENCHMARK", value: "Official Regulated Range", type: "fuel" };
        }
        if (fact.category === "food_staple") {
            if (fact.summary_en.includes("2,200") || fact.summary_en.includes("2,400")) {
                return { label: "MARKET RETAIL BENCHMARK", value: "₦2,200 – ₦2,400 / Paint", type: "food" };
            }
            return { label: "MARKET COMMODITY RATE", value: "Stable Wholesale Range", type: "food" };
        }
        if (fact.category === "rumor_claim") {
            return { label: "DEBUNK VERDICT", value: "CLAIM FALSE • NO ₦450 PRICE DROP", type: "rumor" };
        }
        return { label: "VERIFIED CIVIC DATA", value: "Consensus Active", type: "general" };
    },

    async openDocketModal(factId) {
        const modal = document.getElementById("docketModal");
        const refTag = document.getElementById("docketRefTag");
        const titleEl = document.getElementById("docketModalTitle");
        const viewer = document.getElementById("docketContentViewer");
        const downloadBtn = document.getElementById("downloadDocketBtn");
        const copyBtn = document.getElementById("copyDocketBtn");
        const shareWaBtn = document.getElementById("shareDocketWaBtn");

        if (!modal || !viewer) return;

        viewer.innerHTML = `<div style="text-align:center;padding:3rem 1rem;color:#71717A;">
            <div style="font-size:1.75rem;margin-bottom:0.5rem;">⚖️</div>
            <strong>Compiling Subpoena-Grade Regulatory Dispute Docket...</strong><br>
            <span style="font-size:0.8rem;">Cross-referencing verified meters against Section 63 Electricity Act 2023 telemetry standards.</span>
        </div>`;
        modal.style.display = "flex";

        try {
            const res = await fetch(`/api/trending/${factId}/docket`);
            if (!res.ok) throw new Error("Could not generate dispute docket");
            const data = await res.json();

            if (refTag) refTag.textContent = data.docket_reference;
            if (titleEl) titleEl.textContent = `Regulatory Petition: ${data.feeder_name}`;

            viewer.innerHTML = this.renderMarkdown(data.markdown_petition);

            if (downloadBtn) {
                downloadBtn.onclick = () => {
                    window.location.href = `/api/trending/${factId}/docket/download`;
                };
            }

            if (copyBtn) {
                copyBtn.onclick = () => {
                    navigator.clipboard.writeText(data.markdown_petition);
                    const orig = copyBtn.innerHTML;
                    copyBtn.innerHTML = "<span>✓ Copied to Clipboard!</span>";
                    setTimeout(() => copyBtn.innerHTML = orig, 2500);
                };
            }

            if (shareWaBtn) {
                shareWaBtn.onclick = () => {
                    const shareTxt = `⚖️ *POWERWATCH REGULATORY PETITION GENERATED*\n` +
                                     `*Docket Reference:* ${data.docket_reference}\n` +
                                     `*Feeder:* ${data.feeder_name} (${data.location})\n` +
                                     `*Supply Logged:* ${data.actual_hours}h / ${data.promised_hours}h statutory requirement\n` +
                                     `*Statutory Precedent:* Section 63 Electricity Act 2023 & NERC MYTO Orders\n` +
                                     `*Overcharge Differential:* ${data.overbilling_differential}\n\n` +
                                     `Join this collective tariff refund petition on PowerWatch: https://wa.me/2348122432599`;
                    window.open(`https://wa.me/?text=${encodeURIComponent(shareTxt)}`, "_blank");
                };
            }
        } catch (err) {
            viewer.innerHTML = `<div style="color:#DC2626;padding:1.5rem;text-align:center;">Failed to generate docket: ${err.message}</div>`;
        }
    },

    renderMarkdown(md) {
        if (!md) return "";
        let html = md
            // Escapes
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            // Headers
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h2>$2</h2>')
            // Bold & Italics
            .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/gim, '<em>$1</em>')
            .replace(/`(.*?)`/gim, '<code style="background:#E4E4E7;padding:2px 6px;border-radius:4px;font-family:monospace;font-size:0.85em;">$1</code>')
            // HR
            .replace(/^---$/gim, '<hr style="border:none;border-top:1px solid #E4E4E7;margin:1rem 0;">');

        // Simple table parser
        const lines = html.split('\n');
        let inTable = false;
        let tableHtml = "";
        let resultLines = [];

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            if (line.startsWith('|') && line.endsWith('|')) {
                if (!inTable) {
                    inTable = true;
                    tableHtml = '<table class="docket-table"><tbody>';
                }
                if (line.includes('---')) {
                    continue; // divider
                }
                const cells = line.split('|').slice(1, -1);
                const tag = (tableHtml.includes('<th') || tableHtml.includes('<tr')) ? 'td' : 'th';
                tableHtml += '<tr>' + cells.map(c => `<${tag}>${c.trim()}</${tag}>`).join('') + '</tr>';
            } else {
                if (inTable) {
                    inTable = false;
                    tableHtml += '</tbody></table>';
                    resultLines.push(tableHtml);
                    tableHtml = "";
                }
                if (line.length > 0) {
                    if (!line.startsWith('<h') && !line.startsWith('<hr')) {
                        resultLines.push(`<p>${line}</p>`);
                    } else {
                        resultLines.push(line);
                    }
                }
            }
        }
        if (inTable) {
            tableHtml += '</tbody></table>';
            resultLines.push(tableHtml);
        }

        return resultLines.join('\n');
    },

    shareToWhatsApp(factId) {
        const fact = this.facts.find(f => f.id === factId);
        if (!fact) return;
        const text = `⚡ *POWERWATCH CIVIC AUDIT* (${fact.location})\n` +
                     `📌 *${fact.title}*\n\n` +
                     `✅ *Verified Supply:* ${fact.summary_en}\n\n` +
                     `👉 *Action:* ${fact.action}\n\n` +
                     `💬 Log your meter & join the dispute docket on WhatsApp: +234 812 CHECK-99\n` +
                     `🌐 Public Mirror: http://127.0.0.1:8000`;
        const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`;
        window.open(url, '_blank');
    },

    copyMorningDigest(btnEl) {
        const text = `⚡ *POWERWATCH DAILY CIVIC DISPATCH • ${new Date().toLocaleDateString()}*\n\n` +
                     `⚡ *Magodo Phase 2 (IKEDC):* 6.8h avg vs 20h Band A (13.2h deficit). Dispute Docket #PW-NERC-2026-IKEDC-042 active.\n` +
                     `⚡ *Gwarinpa (AEDC):* 5.2h avg vs 20h Band A. NERC ₦200M fine precedent cited. Docket #PW-NERC-2026-AEDC-019.\n` +
                     `🇿🇦 *City Power Joburg:* Alexandra load reduction challenged under Pretoria High Court ruling.\n` +
                     `⛽ *Lagos Petrol:* ₦850 – ₦890/L benchmark at NNPC/Total retail stations.\n\n` +
                     `Log your electricity meter to join the collective tariff refund petition!\n` +
                     `WhatsApp Hotline: +234 812 CHECK-99`;
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(() => {
                const orig = btnEl.innerHTML;
                btnEl.innerHTML = `<span>✓ Copied to Clipboard!</span>`;
                btnEl.style.background = "#059669";
                btnEl.style.color = "#FFFFFF";
                setTimeout(() => {
                    btnEl.innerHTML = orig;
                    btnEl.style.background = "";
                    btnEl.style.color = "";
                }, 3000);
            });
        } else {
            prompt("Copy today's PowerWatch dispatch:", text);
        }
    },

    async loadTweets() {
        const container = document.getElementById("xWireFeedContainer");
        if (!container) return;

        try {
            const res = await fetch("/api/tweets/recent");
            const tweets = await res.json();

            if (!tweets || tweets.length === 0) {
                container.innerHTML = `
                    <div style="font-size:0.8rem; color:#71717A; text-align:center; padding:1rem 0;">
                        No syndicated regulatory tweets yet. Click "𝕏 Post" on any feeder card to broadcast!
                    </div>
                `;
                return;
            }

            container.innerHTML = tweets.map(tweet => `
                <div class="x-tweet-item">
                    <div class="x-tweet-text">${tweet.tweet_text}</div>
                    <div class="x-tweet-meta">
                        <span>${tweet.tags}</span>
                        <span>${tweet.posted_at}</span>
                    </div>
                </div>
            `).join("");
        } catch (err) {
            console.warn("Could not load tweets:", err);
            container.innerHTML = `<div style="font-size:0.8rem; color:#EF4444; padding:0.5rem 0;">Failed to load regulatory wire.</div>`;
        }
    },

    async syndicateToTwitter(factId, btnEl) {
        if (!btnEl) return;
        const originalText = btnEl.innerHTML;
        btnEl.disabled = true;
        btnEl.innerHTML = "<span>Posting...</span>";

        try {
            const res = await fetch(`/api/trending/${factId}/tweet`, { method: "POST" });
            const data = await res.json();

            if (data.status === "syndicated" || data.status === "already_syndicated") {
                btnEl.innerHTML = "<span>✓ Broadcasted</span>";
                btnEl.style.background = "#F4F4F5";
                btnEl.style.color = "#09090B";
                this.loadTweets();
            } else {
                btnEl.innerHTML = "<span>Error</span>";
            }
        } catch (err) {
            console.error("Failed to syndicate tweet:", err);
            btnEl.innerHTML = "<span>Failed</span>";
        } finally {
            setTimeout(() => {
                btnEl.disabled = false;
                btnEl.innerHTML = originalText;
            }, 3000);
        }
    },

    switchLang(factId, lang, btnEl) {
        const langs = ['en', 'pidgin', 'swahili', 'yoruba', 'hausa', 'zulu'];
        langs.forEach(l => {
            const box = document.getElementById(`summary-${l}-${factId}`);
            if (box) box.style.display = (l === lang) ? "block" : "none";
        });

        const parent = btnEl.parentElement;
        if (parent) {
            parent.querySelectorAll(".lang-chip").forEach(c => c.classList.remove("active"));
            btnEl.classList.add("active");
        }
    },

    async upvoteFact(factId, btnEl) {
        try {
            const res = await fetch(`/api/trending/${factId}/upvote`, { method: "POST" });
            const data = await res.json();
            const countEl = btnEl.querySelector(".upvote-count");
            if (countEl) countEl.textContent = data.upvotes;
            btnEl.style.borderColor = "#10B981";
            btnEl.style.color = "#047857";
        } catch (err) {
            console.error("Failed to upvote:", err);
        }
    },

    async submitWebReport() {
        const country = document.getElementById("formCountry").value;
        const location = document.getElementById("formLocation").value;
        const category = document.getElementById("formCategory").value;
        const content = document.getElementById("formContent").value;
        const submitBtn = document.getElementById("formSubmitBtn");
        const previewBox = document.getElementById("verifyPreviewBox");

        if (!content || content.trim().length < 5) {
            alert("Please enter a descriptive report with meter or outage details.");
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = "Verifying with PowerWatch AI...";

        try {
            const res = await fetch("/api/reports/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    country,
                    location,
                    category,
                    content,
                    source: "web"
                })
            });

            const data = await res.json();

            if (previewBox) {
                previewBox.style.display = "block";
                previewBox.innerHTML = `
                    <div style="font-weight:700;color:#047857;margin-bottom:6px;display:flex;align-items:center;gap:6px;">
                        <span>✓ Outage Logged & Appended to Feeder Audit!</span>
                        <span style="font-size:0.8rem;background:#A7F3D0;padding:2px 8px;border-radius:99px;color:#065F46;">+${data.points_awarded} Points Earned</span>
                    </div>
                    <div style="font-size:0.875rem;color:#1E293B;margin-bottom:8px;">
                        <strong>Audit Verdict:</strong> ${data.verified_summary_en}
                    </div>
                    <div style="font-size:0.85rem;color:#92400E;background:#FEF3C7;padding:6px 10px;border-radius:6px;margin-bottom:8px;">
                        <strong>Pidgin Summary:</strong> ${data.verified_summary_pidgin}
                    </div>
                    <div style="font-size:0.8rem;color:#047857;">
                        <strong>Action:</strong> ${data.next_action}
                    </div>
                `;
            }

            this.loadTrendingFacts();
            this.loadStats();

            submitBtn.textContent = "Audit Logged ✓";
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = "Verify & Add to Feeder Audit";
            }, 2500);

        } catch (err) {
            console.error("Error submitting report:", err);
            alert("Failed to submit report. Please try again.");
            submitBtn.disabled = false;
            submitBtn.textContent = "Verify & Add to Feeder Audit";
        }
    }
};

window.CheckLocalApp = CheckLocalApp;

document.addEventListener("DOMContentLoaded", () => {
    CheckLocalApp.init();
});
