document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('preferences-form');
    const loadingState = document.getElementById('loading-state');
    const resultsContainerWrapper = document.getElementById('results-container');
    const resultsContainer = document.getElementById('results');
    const toast = document.getElementById('toast');
    const slider = document.getElementById('rating-slider');
    const sliderVal = document.getElementById('rating-val');
    const submitBtn = document.getElementById('submit-btn');

    const locSelect = document.getElementById('location');
    const cuiSelect = document.getElementById('cuisine');
    const budSelect = document.getElementById('budget');
    const matchCountEl = document.getElementById('match-count');
    const matchCountText = document.getElementById('match-count-text');

    // Track in-flight filter requests to avoid race conditions
    let filterRequestId = 0;

    // Update slider value UI
    slider.addEventListener('input', (e) => {
        sliderVal.textContent = parseFloat(e.target.value).toFixed(1) + '+';
    });

    // --- Helper: populate a <select> with options, preserving selection if valid ---
    function populateSelect(selectEl, items, placeholderText, valueKey, labelKey) {
        const currentValue = selectEl.value;
        // Remove all options except first placeholder
        selectEl.innerHTML = '';
        // Add placeholder
        const placeholder = document.createElement('option');
        placeholder.value = '';
        placeholder.textContent = placeholderText;
        selectEl.appendChild(placeholder);

        items.forEach(item => {
            const opt = document.createElement('option');
            if (typeof item === 'object') {
                opt.value = item[valueKey || 'value'];
                opt.textContent = item[labelKey || 'label'];
            } else {
                opt.value = item;
                // Capitalize for display
                opt.textContent = String(item).split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
            }
            selectEl.appendChild(opt);
        });

        // Restore previous selection if still valid
        const validValues = Array.from(selectEl.options).map(o => o.value);
        if (validValues.includes(currentValue)) {
            selectEl.value = currentValue;
        } else {
            selectEl.value = '';
        }
    }

    // --- Fetch filter options based on current selections ---
    async function updateFilterOptions() {
        const reqId = ++filterRequestId;
        const params = new URLSearchParams();
        if (locSelect.value) params.set('location', locSelect.value);
        if (budSelect.value) params.set('budget', budSelect.value);
        if (cuiSelect.value) params.set('cuisine', cuiSelect.value);

        try {
            const res = await fetch(`/api/filter-options?${params.toString()}`);
            // Discard stale responses
            if (reqId !== filterRequestId) return;

            if (res.ok) {
                const data = await res.json();

                populateSelect(locSelect, data.locations, 'Select location...');
                populateSelect(cuiSelect, data.cuisines, 'Select cuisine...');
                populateSelect(budSelect, data.budgets, 'Select budget...', 'value', 'label');

                // Update match count badge
                if (locSelect.value || cuiSelect.value || budSelect.value) {
                    matchCountText.textContent = `${data.match_count} restaurants match`;
                    matchCountEl.classList.remove('hidden');
                } else {
                    matchCountEl.classList.add('hidden');
                }
            }
        } catch (e) {
            console.error('Failed to fetch filter options', e);
        }
    }

    // --- Initial load: populate all dropdowns with full data ---
    async function initData() {
        try {
            const res = await fetch('/api/filter-options');
            if (res.ok) {
                const data = await res.json();
                populateSelect(locSelect, data.locations, 'Select location...');
                populateSelect(cuiSelect, data.cuisines, 'Select cuisine...');
                populateSelect(budSelect, data.budgets, 'Select budget...', 'value', 'label');
            }
        } catch (e) {
            console.error("Failed to load init data", e);
            showToast('Error connecting to backend API. Ensure server is running.', true);
        }
    }

    initData();

    // --- Cascading filter listeners ---
    locSelect.addEventListener('change', updateFilterOptions);
    cuiSelect.addEventListener('change', updateFilterOptions);
    budSelect.addEventListener('change', updateFilterOptions);

    // --- Form submission ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI states
        resultsContainerWrapper.classList.add('hidden');
        resultsContainer.innerHTML = ''; 
        submitBtn.disabled = true;
        loadingState.classList.remove('hidden');
        
        const payload = {
            location: locSelect.value,
            cuisine: cuiSelect.value,
            budget: budSelect.value,
            min_rating: parseFloat(slider.value),
            additional_preferences: document.getElementById('additional-preferences').value
        };
        
        try {
            const res = await fetch('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            if (res.ok) {
                const data = await res.json();
                loadingState.classList.add('hidden');
                
                if (data.candidates_found === 0) {
                    showToast('No restaurants match criteria. Try broadening preferences.', true);
                    submitBtn.disabled = false;
                    return;
                }
                
                renderResults(data.recommendations);
                resultsContainerWrapper.classList.remove('hidden');
                showToast(`Analyzed ${data.candidates_found} candidates. Here are the top matches!`);
            } else {
                throw new Error('API Error');
            }
        } catch (error) {
            loadingState.classList.add('hidden');
            showToast('Error fetching recommendations.', true);
        } finally {
            submitBtn.disabled = false;
        }
    });
    
    function renderResults(recs) {
        const template = document.getElementById('result-card-template');
        
        recs.forEach((rec, index) => {
            const clone = template.content.cloneNode(true);
            const article = clone.querySelector('article');
            
            clone.querySelector('.card-rank').textContent = '#' + rec.rank;
            clone.querySelector('.card-rating').textContent = rec.rating.toFixed(1);
            clone.querySelector('.card-name').textContent = rec.name;
            clone.querySelector('.card-cuisine').textContent = rec.cuisine;
            clone.querySelector('.card-cost').textContent = rec.cost_for_two;
            clone.querySelector('.card-explanation').textContent = rec.explanation;
            
            resultsContainer.appendChild(clone);
            
            // Trigger animation stagger
            setTimeout(() => {
                article.classList.add('visible');
            }, index * 150);
        });
    }
    
    function showToast(msg, isError = false) {
        const msgEl = document.getElementById('toast-message');
        const iconEl = toast.querySelector('.material-symbols-outlined');
        msgEl.textContent = msg;
        
        if (isError) {
            toast.classList.add('border-red-500/50');
            toast.classList.remove('border-primary/30');
            iconEl.textContent = 'error';
            iconEl.classList.add('text-red-500');
            iconEl.classList.remove('text-primary');
        } else {
            toast.classList.remove('border-red-500/50');
            toast.classList.add('border-primary/30');
            iconEl.textContent = 'info';
            iconEl.classList.remove('text-red-500');
            iconEl.classList.add('text-primary');
        }
        
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);
    }
});
