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

            let confBadgeClass = "conf-high";
            let confIcon = "🟢";
            if (fact.confidence_level === "Verified") {
                confBadgeClass = "conf-verified";
                confIcon = "✓ Verified";
            } else if (fact.confidence_level === "High") {
                confBadgeClass = "conf-high";
                confIcon = "🛡️ High Confidence";
            } else {
                confBadgeClass = "conf-consensus";
                confIcon = "👥 Community Consensus";
            }

            return `
                <article class="fact-card" id="fact-card-${fact.id}">
                    <div class="card-meta-top">
                        <div class="card-tags">
                            <span class="tag-category ${catClass}">${catName}</span>
                            <span class="tag-location">${flag} ${fact.location}</span>
                        </div>
                        <span class="tag-confidence ${confBadgeClass}">${confIcon}</span>
                    </div>

                    <h3 class="card-title">${fact.title}</h3>

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

                    <div class="action-callout">
                        <span class="action-icon">👉</span>
                        <div><strong>Next Action:</strong> ${fact.action}</div>
                    </div>

                    <div class="card-footer">
                        <span>Updated ${fact.updated_at}</span>
                        <div style="display:flex;align-items:center;gap:12px;">
                            <span>${fact.report_count} citizen reports</span>
                            <button class="btn-upvote" onclick="CheckLocalApp.upvoteFact(${fact.id}, this)">
                                <span>👍 Confirmed</span>
                                <span class="upvote-count">${fact.upvotes}</span>
                            </button>
                        </div>
                    </div>
                </article>
            `;
        }).join("");
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
