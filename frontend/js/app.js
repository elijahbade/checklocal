/**
 * CheckLocal Main Web Mirror Application
 * OSF x Andela Hackathon: "Information You Can Trust"
 */

const CheckLocalApp = {
    currentCountry: "all",
    currentCategory: "all",
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

            if (elFacts) elFacts.textContent = data.verified_facts;
            if (elReports) elReports.textContent = data.total_submissions;
            if (elTrust) elTrust.textContent = data.community_trust_score;
            if (elSpeed) elSpeed.textContent = data.avg_response_time;
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
            container.innerHTML = `<div style="text-align:center;padding:2rem;color:#64748B;">Failed to load trending facts. Check backend status.</div>`;
        }
    },

    renderFacts(facts) {
        const container = document.getElementById("factsFeedContainer");
        if (!container) return;

        if (!facts || facts.length === 0) {
            container.innerHTML = `
                <div style="background:white;border-radius:12px;padding:3rem 1.5rem;text-align:center;border:1px dashed #CBD5E1;">
                    <div style="font-size:2rem;margin-bottom:0.5rem;">🔍</div>
                    <h3 style="font-size:1.1rem;font-weight:700;color:#1E293B;margin-bottom:0.4rem;">No reports found in this category</h3>
                    <p style="color:#64748B;font-size:0.875rem;margin-bottom:1.25rem;">Be the first in your community to verify or submit a report!</p>
                    <button class="btn btn-primary" onclick="document.getElementById('openReportModalBtn').click()">Submit Report</button>
                </div>
            `;
            return;
        }

        const categoryNames = {
            fuel_price: "Fuel & Petrol",
            food_staple: "Food Staple",
            power_status: "Power & Disco",
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
                confIcon = "🛡️ High Confidence";
            } else {
                confBadgeClass = "conf-consensus";
                confIcon = "👥 Community Consensus";
            }

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
                            <span><strong>Escalation Dispatched:</strong> ${fact.escalation_target}</span>
                        </div>` : ''}
                    </div>

                    <div class="card-footer">
                        <span>Updated ${fact.updated_at}</span>
                        <div class="card-actions-right">
                            <span style="font-size:0.75rem; color:#64748B;">${fact.report_count} reports</span>
                            <button class="btn-share-wa" onclick="CheckLocalApp.shareToWhatsApp(${fact.id})" title="Share to WhatsApp Groups & Status">
                                <span>📲 Share to WhatsApp</span>
                            </button>
                            <button class="btn-card-action" onclick="CheckLocalApp.syndicateToTwitter(${fact.id}, this)" title="Syndicate verified fact to X">
                                <span>𝕏 Post</span>
                            </button>
                            <button class="btn-card-action" onclick="CheckLocalApp.upvoteFact(${fact.id}, this)">
                                <span>👍 Confirmed</span>
                                <span class="upvote-count" style="font-weight:700;">${fact.upvotes}</span>
                            </button>
                        </div>
                    </div>
                </article>
            `;
        }).join("");
    },

    getFactHighlight(fact) {
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
            } else if (fact.summary_en.includes("KSh 130")) {
                return { label: "UNGA RETAIL CEILING", value: "KSh 130 – 145 / 2kg Maize Meal", type: "food" };
            }
            return { label: "MARKET COMMODITY RATE", value: "Stable Wholesale Range", type: "food" };
        }
        if (fact.category === "power_status") {
            return { label: "GRID UTILITY STATUS", value: "Feeder Under Repair • Est. 4:00 PM", type: "power" };
        }
        if (fact.category === "water_status") {
            return { label: "MUNICIPAL WATER STATUS", value: "Main Pipe Repairs • Tanker Support", type: "water" };
        }
        if (fact.category === "rumor_claim") {
            return { label: "DEBUNK VERDICT", value: "CLAIM FALSE • NO ₦450 PRICE DROP", type: "rumor" };
        }
        return { label: "VERIFIED CIVIC DATA", value: "Consensus Active", type: "general" };
    },

    shareToWhatsApp(factId) {
        const fact = this.facts.find(f => f.id === factId);
        if (!fact) return;
        const text = `🚨 *CHECKLOCAL CIVIC FACT-CHECK* (${fact.location})\n` +
                     `📌 *${fact.title}*\n\n` +
                     `✅ *Verified:* ${fact.summary_en}\n\n` +
                     `👉 *Action:* ${fact.action}\n\n` +
                     `💬 Check any local claim via WhatsApp: +234 812 CHECK-99\n` +
                     `🌐 Public Mirror: http://127.0.0.1:8000`;
        const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`;
        window.open(url, '_blank');
    },

    copyMorningDigest(btnEl) {
        const text = `☀️ *CHECKLOCAL MORNING STREET DIGEST • ${new Date().toLocaleDateString()}*\n\n` +
                     `⛽ *Lagos Petrol (Ikeja, Alausa):* ₦850 – ₦890/L (Normal flow at NNPC/Total). Roadside black market blacklisted at ₦1,200.\n` +
                     `🌾 *Mile 12 Garri:* White Garri at ₦2,200–₦2,400 / paint bucket.\n` +
                     `🚨 *Debunk:* FG has NOT reversed fuel to ₦450. Beware viral voice note.\n` +
                     `🇰🇪 *Nairobi Super Petrol:* KSh 188.84/L under EPRA monthly ceiling.\n\n` +
                     `Forward to your family, neighborhood and church groups!\n` +
                     `Verify any local rumor via WhatsApp: +234 812 CHECK-99`;
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
            prompt("Copy today's morning digest:", text);
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
                        No syndicated tweets yet. Click "𝕏 Post" on any verified card to broadcast!
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
            container.innerHTML = `<div style="font-size:0.8rem; color:#EF4444; padding:0.5rem 0;">Failed to load X wire.</div>`;
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
                // Refresh tweet feed
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
            alert("Please enter a descriptive report to verify.");
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = "Verifying with AI...";

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

            // Display instant verification preview in modal
            if (previewBox) {
                previewBox.style.display = "block";
                previewBox.innerHTML = `
                    <div style="font-weight:700;color:#047857;margin-bottom:6px;display:flex;align-items:center;gap:6px;">
                        <span>✓ Report Verified & Added to Trending Feed!</span>
                        <span style="font-size:0.8rem;background:#A7F3D0;padding:2px 8px;border-radius:99px;color:#065F46;">+${data.points_awarded} Points Earned</span>
                    </div>
                    <div style="font-size:0.875rem;color:#1E293B;margin-bottom:8px;">
                        <strong>Verified Summary:</strong> ${data.verified_summary_en}
                    </div>
                    <div style="font-size:0.85rem;color:#92400E;background:#FEF3C7;padding:6px 10px;border-radius:6px;margin-bottom:8px;">
                        <strong>Nigerian Pidgin:</strong> ${data.verified_summary_pidgin}
                    </div>
                    <div style="font-size:0.8rem;color:#047857;">
                        <strong>Action Recommended:</strong> ${data.next_action}
                    </div>
                `;
            }

            // Refresh feed in background
            this.loadTrendingFacts();
            this.loadStats();

            // Reset form button
            submitBtn.textContent = "Report Submitted ✓";
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.textContent = "Verify & Publish Report";
            }, 2500);

        } catch (err) {
            console.error("Error submitting report:", err);
            alert("Failed to submit report. Please try again.");
            submitBtn.disabled = false;
            submitBtn.textContent = "Verify & Publish Report";
        }
    }
};

window.CheckLocalApp = CheckLocalApp;

document.addEventListener("DOMContentLoaded", () => {
    CheckLocalApp.init();
});
