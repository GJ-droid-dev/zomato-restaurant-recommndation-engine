document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('preferences-form');
    const loadingState = document.getElementById('loading-state');
    const resultsContainerWrapper = document.getElementById('results-container');
    const resultsContainer = document.getElementById('results');
    const toast = document.getElementById('toast');
    const slider = document.getElementById('rating-slider');
    const sliderVal = document.getElementById('rating-val');
    const submitBtn = document.getElementById('submit-btn');

    // Update slider value UI
    slider.addEventListener('input', (e) => {
        sliderVal.textContent = parseFloat(e.target.value).toFixed(1) + '+';
    });
    
    // Fetch locations and cuisines on load from FastAPI
    async function initData() {
        try {
            const locRes = await fetch('/api/locations');
            if (locRes.ok) {
                const data = await locRes.json();
                const locSelect = document.getElementById('location');
                data.locations.forEach(loc => {
                    const opt = document.createElement('option');
                    opt.value = loc;
                    opt.textContent = loc;
                    locSelect.appendChild(opt);
                });
            }
            
            const cuiRes = await fetch('/api/cuisines');
            if (cuiRes.ok) {
                const data = await cuiRes.json();
                const cuiSelect = document.getElementById('cuisine');
                data.cuisines.forEach(cui => {
                    const opt = document.createElement('option');
                    opt.value = cui;
                    // Capitalize for UI
                    opt.textContent = cui.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                    cuiSelect.appendChild(opt);
                });
            }
        } catch (e) {
            console.error("Failed to load init data", e);
            showToast('Error connecting to backend API. Ensure server is running.', true);
        }
    }
    
    initData();

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI states
        resultsContainerWrapper.classList.add('hidden');
        resultsContainer.innerHTML = ''; 
        submitBtn.disabled = true;
        loadingState.classList.remove('hidden');
        
        const payload = {
            location: document.getElementById('location').value,
            cuisine: document.getElementById('cuisine').value,
            budget: document.getElementById('budget').value,
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
