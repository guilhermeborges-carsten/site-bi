// Sistema BI - Scripts Avançados
class SistemaBI {
  constructor() {
    this.isDarkMode = false;
    this.isVoiceEnabled = false;
    this.particles = [];
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.initParticles();
    this.initVoiceRecognition();
    this.init3DEffects();
    this.initKeyboardShortcuts();
    this.initAnimations();
    this.initThemeToggle();
    this.initPerformanceOptimizations();
  }

  // Configuração de event listeners
  setupEventListeners() {
    document.addEventListener('DOMContentLoaded', () => {
      this.setupIntersectionObserver();
      this.setupFormEnhancements();
      this.setupButtonEffects();
      this.setupSearchFunctionality();
      this.setupScrollEffects();
      this.setupTooltips();
      this.setupBackToTop();
      this.setupLoadingStates();
      this.setupHoverEffects();
      this.setupAccessibility();
      this.setupKeyboardShortcuts();
      this.setupNotifications();
    });
  }

  // Sistema de partículas interativas
  initParticles() {
    const canvas = document.createElement('canvas');
    canvas.id = 'particles-canvas';
    canvas.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: -1;
      opacity: 0.6;
    `;
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Criar partículas
    for (let i = 0; i < 50; i++) {
      this.particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        size: Math.random() * 3 + 1,
        color: `hsl(${Math.random() * 60 + 200}, 70%, 60%)`
      });
    }

    const animateParticles = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      this.particles.forEach(particle => {
        particle.x += particle.vx;
        particle.y += particle.vy;

        if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
        if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;

        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fillStyle = particle.color;
        ctx.fill();

        // Conectar partículas próximas
        this.particles.forEach(otherParticle => {
          const dx = particle.x - otherParticle.x;
          const dy = particle.y - otherParticle.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 100) {
            ctx.beginPath();
            ctx.moveTo(particle.x, particle.y);
            ctx.lineTo(otherParticle.x, otherParticle.y);
            ctx.strokeStyle = `rgba(102, 126, 234, ${0.1 * (1 - distance / 100)})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        });
      });

      requestAnimationFrame(animateParticles);
    };

    animateParticles();

    // Redimensionar canvas
    window.addEventListener('resize', () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });
  }

  // Reconhecimento de voz
  initVoiceRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'pt-BR';

      // Botão de ativação por voz
      const voiceButton = document.createElement('button');
      voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
      voiceButton.className = 'voice-btn';
      voiceButton.style.cssText = `
        position: fixed;
        bottom: 80px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        cursor: pointer;
        z-index: 1000;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
      `;

      voiceButton.addEventListener('click', () => {
        if (this.isVoiceEnabled) {
          recognition.stop();
          voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
          voiceButton.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
          this.isVoiceEnabled = false;
        } else {
          recognition.start();
          voiceButton.innerHTML = '<i class="fas fa-microphone-slash"></i>';
          voiceButton.style.background = 'linear-gradient(135deg, #f56565 0%, #e53e3e 100%)';
          this.isVoiceEnabled = true;
        }
      });

      recognition.onresult = (event) => {
        const command = event.results[0][0].transcript.toLowerCase();
        this.processVoiceCommand(command);
      };

      recognition.onend = () => {
        voiceButton.innerHTML = '<i class="fas fa-microphone"></i>';
        voiceButton.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        this.isVoiceEnabled = false;
      };

      document.body.appendChild(voiceButton);
    }
  }

  // Processar comandos de voz
  processVoiceCommand(command) {
    if (command.includes('novo chamado')) {
      window.location.href = '/novo_chamado';
    } else if (command.includes('dashboard')) {
      window.location.href = '/dashboard';
    } else if (command.includes('usuários')) {
      window.location.href = '/usuarios';
    } else if (command.includes('buscar')) {
      const searchInput = document.querySelector('input[type="text"], input[type="search"]');
      if (searchInput) searchInput.focus();
    } else if (command.includes('modo escuro')) {
      this.toggleDarkMode();
    } else if (command.includes('ajuda')) {
      this.showHelp();
    }
  }

  // Efeitos 3D - DESABILITADO
  init3DEffects() {
    // Animações 3D removidas para melhor usabilidade
  }

  // Atalhos de teclado avançados
  initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Ctrl/Cmd + K para busca
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="text"], input[type="search"]');
        if (searchInput) searchInput.focus();
      }
      
      // Ctrl/Cmd + D para modo escuro
      if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        this.toggleDarkMode();
      }
      
      // Ctrl/Cmd + N para novo chamado
      if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        window.location.href = '/novo_chamado';
      }
      
      // Ctrl/Cmd + H para ajuda
      if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
        e.preventDefault();
        this.showHelp();
      }
      
      // Escape para limpar busca
      if (e.key === 'Escape') {
        const searchInputs = document.querySelectorAll('input[type="text"], input[type="search"]');
        searchInputs.forEach(input => {
          if (input.value) {
            input.value = '';
            input.dispatchEvent(new Event('input'));
          }
        });
      }
    });
  }

  // Animações avançadas - DESABILITADO
  initAnimations() {
    // Animações de escala removidas para melhor usabilidade
  }

  // Toggle de tema escuro
  initThemeToggle() {
    const themeToggle = document.createElement('button');
    themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    themeToggle.className = 'theme-toggle';
    themeToggle.style.cssText = `
      position: fixed;
      bottom: 140px;
      right: 20px;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      cursor: pointer;
      z-index: 1000;
      box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
      transition: all 0.3s ease;
    `;

    themeToggle.addEventListener('click', () => {
      this.toggleDarkMode();
    });

    document.body.appendChild(themeToggle);
  }

  toggleDarkMode() {
    this.isDarkMode = !this.isDarkMode;
    document.body.classList.toggle('dark-mode');
    
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
      themeToggle.innerHTML = this.isDarkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    }

    this.showNotification(
      this.isDarkMode ? 'Modo escuro ativado' : 'Modo claro ativado',
      'info'
    );
  }

  // Otimizações de performance
  initPerformanceOptimizations() {
    // Lazy loading para imagens
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.remove('lazy');
          imageObserver.unobserve(img);
        }
      });
    });

    images.forEach(img => imageObserver.observe(img));

    // Debounce para eventos de scroll
    let scrollTimeout;
    window.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        this.updateScrollEffects();
      }, 16);
    });
  }

  // Efeitos de scroll
  updateScrollEffects() {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.main::before');
    
    if (parallax) {
      const speed = scrolled * 0.5;
      parallax.style.transform = `translateY(${speed}px)`;
    }
  }

  // Intersection Observer para animações
  setupIntersectionObserver() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    }, observerOptions);

    document.querySelectorAll('.card, .chamado-item, .card-metric').forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(30px)';
      el.style.transition = 'opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1), transform 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
      observer.observe(el);
    });
  }

  // Melhorias nos formulários
  setupFormEnhancements() {
    document.querySelectorAll('input, textarea, select').forEach(input => {
      // Auto-resize para textareas
      if (input.tagName === 'TEXTAREA') {
        input.addEventListener('input', function() {
          this.style.height = 'auto';
          this.style.height = this.scrollHeight + 'px';
        });
      }

      // Efeito de foco - DESABILITADO
      input.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
      });

      input.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
      });

      // Validação em tempo real
      input.addEventListener('input', function() {
        this.classList.toggle('valid', this.checkValidity());
        this.classList.toggle('invalid', !this.checkValidity() && this.value.length > 0);
      });
    });
  }

  // Efeitos nos botões
  setupButtonEffects() {
    document.querySelectorAll('button, .btn').forEach(button => {
      button.addEventListener('click', function(e) {
        // Efeito de ripple
        const ripple = document.createElement('span');
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        this.appendChild(ripple);
        
        setTimeout(() => {
          ripple.remove();
        }, 600);
      });
    });
  }

  // Funcionalidade de busca
  setupSearchFunctionality() {
    const searchInputs = document.querySelectorAll('input[type="text"], input[type="search"]');
    searchInputs.forEach(input => {
      input.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const items = document.querySelectorAll('.chamado-item, .table tbody tr');
        
        items.forEach(item => {
          const text = item.textContent.toLowerCase();
          if (text.includes(searchTerm)) {
            item.style.display = '';
            item.style.opacity = '1';
          } else {
            item.style.opacity = '0.3';
          }
        });
      });
    });
  }

  // Efeitos de scroll
  setupScrollEffects() {
    let ticking = false;
    
    const updateScroll = () => {
      const scrolled = window.pageYOffset;
      const parallax = document.querySelector('.main::before');
      
      if (parallax) {
        const speed = scrolled * 0.5;
        parallax.style.transform = `translateY(${speed}px)`;
      }
      
      ticking = false;
    };

    const requestTick = () => {
      if (!ticking) {
        requestAnimationFrame(updateScroll);
        ticking = true;
      }
    };

    window.addEventListener('scroll', requestTick);
  }

  // Tooltips personalizados
  setupTooltips() {
    const tooltipElements = document.querySelectorAll('[title]');
    tooltipElements.forEach(element => {
      element.addEventListener('mouseenter', function(e) {
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        tooltip.textContent = this.getAttribute('title');
        tooltip.style.cssText = `
          position: absolute;
          background: rgba(0, 0, 0, 0.9);
          color: white;
          padding: 8px 12px;
          border-radius: 8px;
          font-size: 12px;
          z-index: 1000;
          pointer-events: none;
          white-space: nowrap;
          opacity: 0;
          transition: opacity 0.3s ease;
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255,255,255,0.1);
        `;
        
        document.body.appendChild(tooltip);
        
        const rect = this.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
        
        setTimeout(() => {
          tooltip.style.opacity = '1';
        }, 10);
        
        this._tooltip = tooltip;
      });
      
      element.addEventListener('mouseleave', function() {
        if (this._tooltip) {
          this._tooltip.remove();
          this._tooltip = null;
        }
      });
    });
  }

  // Botão voltar ao topo
  setupBackToTop() {
    const backToTop = document.createElement('button');
    backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTop.className = 'back-to-top';
    backToTop.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 50px;
      height: 50px;
      border-radius: 50%;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      cursor: pointer;
      opacity: 0;
      visibility: hidden;
      transition: all 0.3s ease;
      z-index: 1000;
      box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    `;
    
    document.body.appendChild(backToTop);
    
    window.addEventListener('scroll', () => {
      if (window.pageYOffset > 300) {
        backToTop.style.opacity = '1';
        backToTop.style.visibility = 'visible';
      } else {
        backToTop.style.opacity = '0';
        backToTop.style.visibility = 'hidden';
      }
    });
    
    backToTop.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // Estados de loading
  setupLoadingStates() {
    const loadingStates = document.querySelectorAll('.btn[type="submit"]');
    loadingStates.forEach(button => {
      button.addEventListener('click', function() {
        if (this.closest('form').checkValidity()) {
          const originalText = this.innerHTML;
          this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando...';
          this.disabled = true;
          this.classList.add('loading');
          
          setTimeout(() => {
            this.innerHTML = originalText;
            this.disabled = false;
            this.classList.remove('loading');
          }, 2000);
        }
      });
    });
  }

  // Efeitos de hover
  setupHoverEffects() {
    document.querySelectorAll('.chamado-item, .card').forEach(item => {
      item.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-4px)';
      });
      
      item.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
      });
    });
  }

  // Melhorar acessibilidade
  setupAccessibility() {
    document.querySelectorAll('button, a, input, select, textarea').forEach(element => {
      if (!element.getAttribute('tabindex')) {
        element.setAttribute('tabindex', '0');
      }
    });

    // Navegação por teclado
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
      }
    });

    document.addEventListener('mousedown', () => {
      document.body.classList.remove('keyboard-navigation');
    });
  }

  // Sistema de notificações
  setupNotifications() {
    window.showNotification = (message, type = 'info') => {
      const notification = document.createElement('div');
      notification.className = `notification notification-${type}`;
      notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button class="notification-close"><i class="fas fa-times"></i></button>
      `;
      
      notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        transform: translateX(100%);
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.2);
        max-width: 400px;
      `;
      
      document.body.appendChild(notification);
      
      setTimeout(() => {
        notification.style.transform = 'translateX(0)';
      }, 100);
      
      // Botão de fechar
      const closeBtn = notification.querySelector('.notification-close');
      closeBtn.addEventListener('click', () => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
          notification.remove();
        }, 300);
      });
      
      // Auto-remover após 5 segundos
      setTimeout(() => {
        if (notification.parentNode) {
          notification.style.transform = 'translateX(100%)';
          setTimeout(() => {
            notification.remove();
          }, 300);
        }
      }, 5000);
    };
  }

  // Mostrar ajuda
  showHelp() {
    const helpModal = document.createElement('div');
    helpModal.className = 'help-modal';
    helpModal.innerHTML = `
      <div class="help-content">
        <h2><i class="fas fa-question-circle"></i> Ajuda - Atalhos de Teclado</h2>
        <div class="help-grid">
          <div class="help-item">
            <kbd>Ctrl/Cmd + K</kbd>
            <span>Buscar</span>
          </div>
          <div class="help-item">
            <kbd>Ctrl/Cmd + D</kbd>
            <span>Alternar modo escuro</span>
          </div>
          <div class="help-item">
            <kbd>Ctrl/Cmd + N</kbd>
            <span>Novo chamado</span>
          </div>
          <div class="help-item">
            <kbd>Ctrl/Cmd + H</kbd>
            <span>Mostrar ajuda</span>
          </div>
          <div class="help-item">
            <kbd>Escape</kbd>
            <span>Limpar busca</span>
          </div>
        </div>
        <button class="btn" onclick="this.parentElement.parentElement.remove()">Fechar</button>
      </div>
    `;
    
    helpModal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10000;
      backdrop-filter: blur(10px);
    `;
    
    const helpContent = helpModal.querySelector('.help-content');
    helpContent.style.cssText = `
      background: white;
      padding: 2rem;
      border-radius: 20px;
      max-width: 500px;
      width: 90%;
      text-align: center;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    `;
    
    document.body.appendChild(helpModal);
    
    helpModal.addEventListener('click', (e) => {
      if (e.target === helpModal) {
        helpModal.remove();
      }
    });
  }

  // Função para mostrar notificações
  showNotification(message, type = 'info') {
    if (window.showNotification) {
      window.showNotification(message, type);
    } else {
      alert(message);
    }
  }
}

// Inicializar o sistema
const sistemaBI = new SistemaBI();

// Adicionar CSS para efeitos avançados
const advancedStyles = document.createElement('style');
advancedStyles.textContent = `
  .ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: scale(0);
    animation: ripple-animation 0.6s linear;
    pointer-events: none;
  }
  
  @keyframes ripple-animation {
    to {
      transform: scale(1);
      opacity: 0;
    }
  }
  
  .custom-tooltip {
    animation: tooltip-fade-in 0.3s ease;
  }
  
  @keyframes tooltip-fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  .back-to-top:hover,
  .voice-btn:hover,
  .theme-toggle:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }
  
  .notification {
    animation: notification-slide-in 0.3s ease;
  }
  
  @keyframes notification-slide-in {
    from { transform: translateX(100%); }
    to { transform: translateX(0); }
  }
  
  .help-grid {
    display: grid;
    gap: 1rem;
    margin: 1.5rem 0;
  }
  
  .help-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: #f7fafc;
    border-radius: 8px;
  }
  
  kbd {
    background: #2d3748;
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.9rem;
  }
  
  .dark-mode {
    filter: invert(1) hue-rotate(180deg);
  }
  
  .dark-mode img,
  .dark-mode video {
    filter: invert(1) hue-rotate(180deg);
  }
  
  .loading::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    animation: loading 1.5s infinite;
  }
  
  @keyframes loading {
    0% { left: -100%; }
    100% { left: 100%; }
  }
  
  .focused {
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
  }
  
  .valid {
    border-color: #48bb78 !important;
  }
  
  .invalid {
    border-color: #f56565 !important;
  }
  
  .keyboard-navigation *:focus {
    outline: 2px solid #667eea !important;
    outline-offset: 2px !important;
  }
  
  .animated {
    animation: bounce-in 0.6s ease;
  }
  
  @keyframes bounce-in {
    0% { opacity: 0; }
    50% { opacity: 0.5; }
    70% { opacity: 0.7; }
    100% { opacity: 1; }
  }
`;

document.head.appendChild(advancedStyles); 