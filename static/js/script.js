// Particle Animation
const canvas = document.getElementById('particleCanvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.size = Math.random() * 2 + 1;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }

    draw() {
        ctx.fillStyle = 'rgba(0, 255, 136, 0.5)';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

const particles = [];
const particleCount = 100;

for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
}

function connectParticles() {
    for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 120) {
                ctx.strokeStyle = `rgba(0, 255, 136, ${0.15 * (1 - distance / 120)})`;
                ctx.lineWidth = 0.5;
                ctx.beginPath();
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.stroke();
            }
        }
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });

    connectParticles();
    requestAnimationFrame(animate);
}

animate();

// Stock Analysis Logic
const analyzeBtn = document.getElementById('analyzeBtn');
const stockSymbol = document.getElementById('stockSymbol');
const period = document.getElementById('period');
const loading = document.getElementById('loading');
const errorDiv = document.getElementById('error');

if (analyzeBtn) {
    analyzeBtn.addEventListener('click', analyzeStock);
    
    stockSymbol.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeStock();
        }
    });
}

async function analyzeStock() {
    const symbol = stockSymbol.value.trim();
    const selectedPeriod = period.value;
    
    if (!symbol) {
        showError('Please enter a stock symbol');
        return;
    }
    
    hideError();
    loading.classList.remove('hidden');
    analyzeBtn.disabled = true;
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                symbol: symbol,
                period: selectedPeriod
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
        } else {
            // Store results in session storage
            sessionStorage.setItem('analysisResults', JSON.stringify(data));
            // Open results in same tab
            window.location.href = '/results';
        }
    } catch (error) {
        showError('Network error. Please check your connection and try again.');
    } finally {
        loading.classList.add('hidden');
        analyzeBtn.disabled = false;
    }
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    errorDiv.classList.add('hidden');
}

function displayResults(data) {
    const container = document.getElementById('resultsContainer');
    
    let html = `
        <div class="company-header">
            <h1 class="company-name">${data.company_info.name}</h1>
            <div class="company-details">
                <div><strong>Symbol:</strong> ${data.symbol}</div>
                <div><strong>Sector:</strong> ${data.company_info.sector}</div>
                <div><strong>Industry:</strong> ${data.company_info.industry}</div>
            </div>
        </div>
        
        <div class="overall-score-box">
            <div class="score-value">${data.overall_score}/10</div>
            <div class="recommendation">${data.recommendation}</div>
            <div class="recommendation-reason">${data.reason}</div>
        </div>
        
        <h2 style="color: #00ff88; margin: 30px 0 20px; font-size: 1.5rem;">Quantitative Parameters</h2>
        <div class="parameters-grid">
    `;
    
    for (const [param, details] of Object.entries(data.scores)) {
        const scoreWidth = (details.score / 10) * 100;
        html += `
            <div class="parameter-card">
                <div class="param-name">${param}</div>
                <div class="param-value">${details.value}</div>
                <div class="param-score-bar">
                    <div class="param-score-fill" style="width: ${scoreWidth}%"></div>
                </div>
                <div class="param-score-text">Score: ${details.score}/10 (Weight: ${details.weight})</div>
            </div>
        `;
    }
    
    html += `</div>`;
    
    if (data.price_chart) {
        html += `
            <h2 style="color: #00ff88; margin: 30px 0 20px; font-size: 1.5rem;">Price Analysis</h2>
            <div class="chart-container">
                <img src="data:image/png;base64,${data.price_chart}" alt="Price Chart">
            </div>
        `;
    }
    
    if (data.volume_chart) {
        html += `
            <div class="chart-container">
                <img src="data:image/png;base64,${data.volume_chart}" alt="Volume Chart">
            </div>
        `;
    }
    
    container.innerHTML = html;
}
