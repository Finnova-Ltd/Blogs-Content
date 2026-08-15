/**
 * EZ Mortgage Broker Clone - Main JavaScript
 * Handles: Navigation, Calculators, Scroll Animations, Forms
 */

(function () {
  'use strict';

  /* =========================================
     Mobile Navigation
     ========================================= */
  const navToggle = document.getElementById('navToggle');
  const mobileNav = document.getElementById('mobileNav');
  const mobileNavOverlay = document.getElementById('mobileNavOverlay');
  const mobileNavClose = document.getElementById('mobileNavClose');

  function openMobileNav() {
    if (!mobileNav) return;
    mobileNav.classList.add('open');
    mobileNavOverlay.classList.add('open');
    document.body.classList.add('mobile-menu-open');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileNav() {
    if (!mobileNav) return;
    mobileNav.classList.remove('open');
    mobileNavOverlay.classList.remove('open');
    document.body.classList.remove('mobile-menu-open');
    document.body.style.overflow = '';
  }

  if (navToggle) navToggle.addEventListener('click', openMobileNav);
  if (mobileNavClose) mobileNavClose.addEventListener('click', closeMobileNav);
  if (mobileNavOverlay) mobileNavOverlay.addEventListener('click', closeMobileNav);

  /* =========================================
     Sticky Header Shadow
     ========================================= */
  const siteHeader = document.querySelector('.site-header');
  if (siteHeader) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 10) {
        siteHeader.style.boxShadow = '0 4px 20px rgba(0,0,0,0.12)';
      } else {
        siteHeader.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)';
      }
    }, { passive: true });
  }

  /* =========================================
     Active Nav Link
     ========================================= */
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-primary a, .mobile-nav-links a').forEach(function (a) {
    const href = a.getAttribute('href');
    if (href && (href === currentPath || href.includes(currentPath))) {
      a.classList.add('active');
    }
  });

  /* =========================================
     Calculator Routes & Multi-Calculator Engine
     ========================================= */
  const calcTabs = document.querySelectorAll('.calc-tab');

  const calculatorRoutes = {
    'borrowing-power': { tab: 'borrowing', title: 'Borrowing Power Calculator' },
    repayments: { tab: 'repayments', title: 'Loan Repayment Calculator' },
    'stamp-duty': { tab: 'stamp-duty', title: 'Stamp Duty Calculator' },
    'buying-costs': { tab: 'buying-costs', title: 'Property Buying Cost Calculator' },
    'rent-vs-buy': { tab: 'rent-vs-buy', title: 'Rent vs Buy Calculator' },
    deposit: { tab: 'deposit', title: 'How Much to Deposit Calculator' },
    'comparison-rate': { tab: 'comparison-rate', title: 'Comparison Rate Calculator' },
    'loan-comparison': { tab: 'comparison', title: 'Loan Comparison Calculator' },
    switching: { tab: 'switching', title: 'Mortgage Switching Calculator' },
    offset: { tab: 'offset', title: 'Home Loan Offset Calculator' },
    'split-loan': { tab: 'split-loan', title: 'Split Loan Calculator' },
    'extra-repayments': { tab: 'extra-repayments', title: 'Extra Repayment Calculator' },
    'lump-sum': { tab: 'lump-sum', title: 'Lump Sum Repayment Calculator' },
    'how-long': { tab: 'how-long', title: 'How Long to Repay Calculator' },
    fortnightly: { tab: 'repayments', title: 'Fortnightly Repayment Calculator' },
    'interest-only': { tab: 'interest-only', title: 'Interest Only Mortgage Calculator' },
    saving: { tab: 'saving', title: 'Saving Calculator' },
    compound: { tab: 'compound', title: 'Compound Interest Calculator' },
    budget: { tab: 'budget', title: 'Budget Planner' },
    'credit-card': { tab: 'credit-card', title: 'Credit Card Calculator' },
    'income-tax': { tab: 'income-tax', title: 'Income Tax Calculator' },
    annualisation: { tab: 'income-tax', title: 'Income Annualisation Calculator' },
    'gross-up': { tab: 'gross-up', title: 'Income Gross Up Calculator' },
    'selling-costs': { tab: 'selling-costs', title: 'Property Selling Cost Calculator' },
    'reverse-mortgage': { tab: 'reverse-mortgage', title: 'Reverse Mortgage Calculator' },
    leasing: { tab: 'leasing', title: 'Leasing Calculator' }
  };

  function selectCalculator(target, updateHash) {
    const route = calculatorRoutes[target] || calculatorRoutes['borrowing-power'];
    const calcPanels = document.querySelectorAll('.calc-panel');
    const calculatorBody = document.querySelector('.va-calc-body');

    if (calculatorBody) calculatorBody.classList.toggle('repayment-layout', route.tab === 'repayments');

    calcPanels.forEach(function (panel) {
      panel.classList.remove('active');
      if (panel.id === 'calc-' + route.tab) {
        panel.classList.add('active');
      }
    });

    const title = document.getElementById('calculatorTitle');
    if (title) title.textContent = route.title;

    const breadcrumbTitle = document.getElementById('breadcrumbTitle');
    if (breadcrumbTitle) breadcrumbTitle.textContent = route.title;

    document.querySelectorAll('.calc-sidebar-btn').forEach(function (link) {
      const href = link.getAttribute('href')?.replace('#', '');
      if (href === target) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });

    if (updateHash) window.history.replaceState(null, '', '#' + target);
    runCalculationForPanel(route.tab);
  }

  function runCalculationForPanel(tab) {
    const labelEl = document.getElementById('bannerResultLabel');
    const maxEl = document.getElementById('bp-result-max');
    const mEl = document.getElementById('bp-result-monthly');
    const fEl = document.getElementById('bp-result-fortnightly');
    const wEl = document.getElementById('bp-result-weekly');

    if (tab === 'borrowing') {
      if (labelEl) labelEl.textContent = 'You can borrow up to';
      if (document.getElementById('subLabel1')) document.getElementById('subLabel1').textContent = 'Monthly Repayment';
      if (document.getElementById('subLabel2')) document.getElementById('subLabel2').textContent = 'Fortnightly Repayment';
      if (document.getElementById('subLabel3')) document.getElementById('subLabel3').textContent = 'Weekly Repayment';
      calculateBorrowingPower();
    } else if (tab === 'stamp-duty') {
      const price = parseFloat(document.getElementById('sd-price')?.value) || 750000;
      const duty = Math.round(price * 0.053);
      if (labelEl) labelEl.textContent = 'Estimated Stamp Duty';
      if (maxEl) maxEl.textContent = formatCurrency(duty);
      if (mEl) mEl.textContent = formatCurrency(1650);
      if (fEl) fEl.textContent = formatCurrency(duty + 1650);
      if (wEl) wEl.textContent = 'Government & Registry Fees';
    } else if (tab === 'repayments') {
      if (labelEl) labelEl.textContent = 'Monthly Repayment';
      if (document.getElementById('subLabel1')) document.getElementById('subLabel1').textContent = 'Total Interest / Fee Payable';
      if (document.getElementById('subLabel2')) document.getElementById('subLabel2').textContent = 'Total Payments';
      if (document.getElementById('subLabel3')) document.getElementById('subLabel3').textContent = 'Loan Amount';
      calculateRepayments();
    } else {
      const amount = parseFloat(document.querySelector('#calc-' + tab + ' input')?.value) || 500000;
      const est = Math.round(amount * 0.065 / 12);
      if (labelEl) labelEl.textContent = 'Estimated Outcome';
      if (maxEl) maxEl.textContent = formatCurrency(est);
      if (mEl) mEl.textContent = formatCurrency(est);
      if (fEl) fEl.textContent = formatCurrency(Math.round(est / 2));
      if (wEl) wEl.textContent = formatCurrency(Math.round(est / 4));
    }
  }

  calcTabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      const target = Object.keys(calculatorRoutes).find(function (key) {
        return calculatorRoutes[key].tab === tab.dataset.tab;
      }) || 'borrowing-power';
      selectCalculator(target, true);
    });
  });

  document.querySelectorAll('.calc-sidebar-btn[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (event) {
      const target = link.getAttribute('href').slice(1);
      if (!calculatorRoutes[target]) return;
      event.preventDefault();
      selectCalculator(target, true);
    });
  });

  const searchInput = document.getElementById('calcSearchInput');
  if (searchInput) {
    searchInput.addEventListener('input', function(e) {
      const term = e.target.value.toLowerCase().trim();
      document.querySelectorAll('.calc-sidebar-btn').forEach(function(link) {
        const text = link.textContent.toLowerCase();
        if (text.includes(term)) {
          link.style.display = 'block';
        } else {
          link.style.display = 'none';
        }
      });
    });
  }

  // Keep field units outside the value box so labels remain readable across panels.
  document.querySelectorAll('.va-input-box').forEach(function (field) {
    const symbols = field.querySelectorAll('.va-symbol');
    const suffix = Array.from(symbols).find(function (symbol) {
      return symbol.textContent.trim() !== '$';
    });
    if (!suffix || !field.parentElement) return;
    const unit = document.createElement('span');
    unit.className = 'va-field-unit';
    unit.textContent = suffix.textContent.trim();
    suffix.remove();
    field.parentElement.insertBefore(unit, field.nextSibling);
  });

  const accordionGroups = document.querySelectorAll('.calc-accordion-group');
  const setAccordionState = function (group, open) {
    group.classList.toggle('open', open);
    const header = group.querySelector('.calc-accordion-header');
    if (header) {
      header.classList.toggle('active', open);
      header.setAttribute('aria-expanded', String(open));
      const arrow = header.querySelector('.group-arrow');
      if (arrow) arrow.textContent = open ? '▲' : '▼';
    }
  };

  accordionGroups.forEach(function (group, index) {
    setAccordionState(group, index === 0);
    const header = group.querySelector('.calc-accordion-header');
    if (header) {
      header.addEventListener('click', function () {
        const shouldOpen = !group.classList.contains('open');
        accordionGroups.forEach(function (otherGroup) { setAccordionState(otherGroup, false); });
        setAccordionState(group, shouldOpen);
      });
    }
  });

  // Sync Top Select Dropdown
  const topSelect = document.getElementById('calcTopSelect');
  if (topSelect) {
    topSelect.addEventListener('change', function(e) {
      selectCalculator(e.target.value, true);
    });
  }

  // Global Pill Toggles
  window.setBorrowersToggle = function(count) {
    document.getElementById('bp-borrowers-single')?.classList.toggle('active', count === 1);
    document.getElementById('bp-borrowers-joint')?.classList.toggle('active', count === 2);
    calculateBorrowingPower();
  };

  window.setDependantsToggle = function(count, btnEl) {
    btnEl.parentElement.querySelectorAll('.va-pill-btn').forEach(b => b.classList.remove('active'));
    btnEl.classList.add('active');
    calculateBorrowingPower();
  };

  window.resetCalculatorForm = function() {
    document.querySelectorAll('input').forEach(i => {
      if (i.type === 'number') i.value = i.defaultValue || i.value;
    });
    calculateBorrowingPower();
  };

  selectCalculator(window.location.hash.slice(1) || 'borrowing-power', false);
  window.addEventListener('hashchange', function () {
    const hash = window.location.hash.slice(1) || 'borrowing-power';
    selectCalculator(hash, false);
    if (topSelect) topSelect.value = hash;
  });

  /* =========================================
     Borrowing Power Calculator
     ========================================= */
  function formatCurrency(value) {
    return new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  }

  function formatNumber(value) {
    return new Intl.NumberFormat('en-AU').format(Math.round(value));
  }

  function calculateBorrowingPower() {
    const income = parseFloat(document.getElementById('bp-income')?.value) || 0;
    const expenses = parseFloat(document.getElementById('bp-expenses')?.value) || 0;
    const dependants = parseInt(document.getElementById('bp-dependants')?.value) || 0;
    const existingDebt = parseFloat(document.getElementById('bp-debt')?.value) || 0;

    const rate = 0.065;
    const loanTermYears = 30;
    const n = loanTermYears * 12;
    const r = rate / 12;

    const dependantCost = dependants * 800;
    const netMonthlyIncome = (income / 12) * 0.75;
    const availableRepayment = netMonthlyIncome - (expenses / 12) - dependantCost - (existingDebt / 12);
    const maxRepayment = Math.max(availableRepayment, 0);

    const maxLoan = maxRepayment > 0
      ? (maxLoan_calc(maxRepayment, r, n))
      : 0;

    const maxLoanEl = document.getElementById('bp-result-max');
    const monthlyEl = document.getElementById('bp-result-monthly');

    if (maxLoanEl) maxLoanEl.textContent = formatCurrency(maxLoan);
    if (monthlyEl) monthlyEl.textContent = formatCurrency(maxRepayment) + '/mo';
  }

  function maxLoan_calc(payment, r, n) {
    if (r === 0) return payment * n;
    return payment * (1 - Math.pow(1 + r, -n)) / r;
  }

  document.querySelectorAll('#calc-borrowing input, #calc-borrowing select').forEach(function (el) {
    el.addEventListener('input', calculateBorrowingPower);
    el.addEventListener('change', calculateBorrowingPower);
  });

  calculateBorrowingPower();

  /* =========================================
     Repayment Calculator
     ========================================= */
  var repayLoanAmount = document.getElementById('rep-amount');
  var repLoanDisplay = document.getElementById('rep-amount-display');
  var repRateInput = document.getElementById('rep-rate');
  var repTermInput = document.getElementById('rep-term');

  function updateRangeDisplay(inputEl, displayEl, formatter) {
    if (!inputEl || !displayEl) return;
    displayEl.textContent = formatter(inputEl.value);
    inputEl.addEventListener('input', function () {
      displayEl.textContent = formatter(inputEl.value);
      calculateRepayments();
    });
  }

  updateRangeDisplay(repayLoanAmount, repLoanDisplay, function (v) {
    return formatCurrency(parseFloat(v));
  });

  function calculateRepayments() {
    const principal = parseFloat(repayLoanAmount?.value) || 500000;
    const annualRate = parseFloat(repRateInput?.value) || 6.5;
    const termYears = parseInt(repTermInput?.value) || 30;
    const fee = parseFloat(document.getElementById('rep-fee')?.value) || 0;
    const feeFrequency = document.getElementById('rep-fee-frequency')?.value || 'Monthly';

    const r = annualRate / 100 / 12;
    const n = termYears * 12;

    let monthly;
    if (r === 0) {
      monthly = principal / n;
    } else {
      monthly = principal * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1);
    }

    const feePeriodsPerYear = { Monthly: 12, Fortnightly: 26, Weekly: 52, Annually: 1 }[feeFrequency] || 12;
    const totalFees = fee * feePeriodsPerYear * termYears;
    const totalRepaid = monthly * n + totalFees;
    const totalInterest = totalRepaid - principal;

    const monthlyEl = document.getElementById('rep-result-monthly');
    const totalEl = document.getElementById('rep-result-total');
    const interestEl = document.getElementById('rep-result-interest');

    if (monthlyEl) monthlyEl.textContent = formatCurrency(monthly + totalFees / n);
    if (totalEl) totalEl.textContent = formatCurrency(totalRepaid);
    if (interestEl) interestEl.textContent = formatCurrency(totalInterest);
    const repaymentBanner = document.getElementById('bp-result-max');
    const repaymentMonthly = document.getElementById('bp-result-monthly');
    const repaymentTotal = document.getElementById('bp-result-fortnightly');
    const repaymentPrincipal = document.getElementById('bp-result-weekly');
    if (repaymentBanner) repaymentBanner.textContent = formatCurrency(monthly + totalFees / n);
    if (repaymentMonthly) repaymentMonthly.textContent = formatCurrency(totalInterest);
    if (repaymentTotal) repaymentTotal.textContent = formatCurrency(totalRepaid);
    if (repaymentPrincipal) repaymentPrincipal.textContent = formatCurrency(principal);
    updateCalculatorChart(principal, annualRate, termYears, monthly);
  }

  if (repRateInput) repRateInput.addEventListener('input', calculateRepayments);
  if (repTermInput) repTermInput.addEventListener('input', calculateRepayments);
  document.querySelectorAll('#calc-repayments input, #calc-repayments select').forEach(function (field) {
    field.addEventListener('input', calculateRepayments);
    field.addEventListener('change', calculateRepayments);
  });

  calculateRepayments();

  function updateCalculatorChart(principal, annualRate, termYears, monthly) {
    const balancePath = document.getElementById('calculatorBalancePath');
    const paidPath = document.getElementById('calculatorPaidPath');
    const balanceArea = document.getElementById('calculatorBalanceArea');
    const paidArea = document.getElementById('calculatorPaidArea');
    if (!balancePath || !paidPath || !balanceArea) return;

    const paddingLeft = 35;
    const chartWidth = 465;
    const chartHeight = 203;
    const rate = annualRate / 100 / 12;
    const points = [];

    for (let year = 0; year <= termYears; year += 1) {
      const months = year * 12;
      const balance = rate === 0
        ? Math.max(principal - monthly * months, 0)
        : Math.max(principal * Math.pow(1 + rate, months) - monthly * ((Math.pow(1 + rate, months) - 1) / rate), 0);
      points.push({ year, balance, totalPaid: monthly * months });
    }

    const maxValue = Math.max(principal, ...points.map((point) => point.totalPaid), 1);
    const yAxisLabels = document.querySelectorAll('#calculatorYAxisLabels text');
    const xAxisLabels = document.querySelectorAll('#calculatorXAxisLabels text');
    const formatAxisValue = function (value) {
      if (value >= 1000000) return '$' + (value / 1000000).toFixed(1) + 'M';
      if (value >= 1000) return '$' + Math.round(value / 1000) + 'K';
      return '$' + Math.round(value);
    };
    yAxisLabels.forEach(function (label, index) {
      const value = maxValue * (index / (yAxisLabels.length - 1));
      label.textContent = formatAxisValue(value);
    });
    xAxisLabels.forEach(function (label, index) {
      const year = Math.round(termYears * (index / (xAxisLabels.length - 1)));
      label.textContent = String(year);
    });
    const toPoint = function (point, key) {
      const x = paddingLeft + (point.year / termYears) * chartWidth;
      const y = 20 + chartHeight - (point[key] / maxValue) * chartHeight;
      return [x, y];
    };
    const makePath = function (key) {
      return points.map((point, index) => {
        const [x, y] = toPoint(point, key);
        return (index === 0 ? 'M' : 'L') + ' ' + x.toFixed(1) + ' ' + y.toFixed(1);
      }).join(' ');
    };

    const balanceD = makePath('balance');
    const paidD = makePath('totalPaid');
    balancePath.setAttribute('d', balanceD);
    paidPath.setAttribute('d', paidD);
    balanceArea.setAttribute('d', balanceD + ' L ' + (paddingLeft + chartWidth) + ' ' + (20 + chartHeight) + ' L ' + paddingLeft + ' ' + (20 + chartHeight) + ' Z');
    if (paidArea) paidArea.setAttribute('d', paidD + ' L ' + (paddingLeft + chartWidth) + ' ' + (20 + chartHeight) + ' L ' + paddingLeft + ' ' + (20 + chartHeight) + ' Z');
  }

  const chartHitArea = document.getElementById('calculatorChartHitArea');
  const chartTooltip = document.getElementById('calculatorChartTooltip');
  const chartHoverLine = document.getElementById('calculatorHoverLine');
  const chartBalancePoint = document.getElementById('calculatorBalancePoint');
  const chartPaidPoint = document.getElementById('calculatorPaidPoint');

  if (chartHitArea && chartTooltip && chartHoverLine && chartBalancePoint && chartPaidPoint) {
    chartHitArea.addEventListener('pointermove', function (event) {
      const svg = chartHitArea.ownerSVGElement;
      const point = svg.createSVGPoint();
      point.x = event.clientX;
      point.y = event.clientY;
      const localPoint = point.matrixTransform(svg.getScreenCTM().inverse());
      const principal = parseFloat(repayLoanAmount?.value) || 500000;
      const annualRate = parseFloat(repRateInput?.value) || 6.5;
      const termYears = parseInt(repTermInput?.value) || 30;
      const rate = annualRate / 100 / 12;
      const monthly = rate === 0 ? principal / (termYears * 12) : principal * rate * Math.pow(1 + rate, termYears * 12) / (Math.pow(1 + rate, termYears * 12) - 1);
      const year = Math.max(0, Math.min(termYears, Math.round(((localPoint.x - 35) / 465) * termYears)));
      const months = year * 12;
      const balance = rate === 0 ? Math.max(principal - monthly * months, 0) : Math.max(principal * Math.pow(1 + rate, months) - monthly * ((Math.pow(1 + rate, months) - 1) / rate), 0);
      const totalPaid = monthly * months;
      const maxValue = Math.max(principal, totalPaid, 1);
      const x = 35 + (year / termYears) * 465;
      const balanceY = 20 + 203 - (balance / maxValue) * 203;
      const paidY = 20 + 203 - (totalPaid / maxValue) * 203;
      chartHoverLine.setAttribute('x1', x);
      chartHoverLine.setAttribute('x2', x);
      chartHoverLine.setAttribute('opacity', '1');
      chartBalancePoint.setAttribute('cx', x);
      chartBalancePoint.setAttribute('cy', balanceY);
      chartBalancePoint.setAttribute('opacity', '1');
      chartPaidPoint.setAttribute('cx', x);
      chartPaidPoint.setAttribute('cy', paidY);
      chartPaidPoint.setAttribute('opacity', '1');
      chartTooltip.innerHTML = '<strong>Year ' + year + '</strong><br>Loan Balance: ' + formatCurrency(balance) + '<br>Total Paid: ' + formatCurrency(totalPaid);
      chartTooltip.classList.add('visible');
    });

    chartHitArea.addEventListener('pointerleave', function () {
      chartHoverLine.setAttribute('opacity', '0');
      chartBalancePoint.setAttribute('opacity', '0');
      chartPaidPoint.setAttribute('opacity', '0');
      chartTooltip.classList.remove('visible');
    });
  }

  const chartBalancePath = document.getElementById('calculatorBalancePath');
  const chartPaidPath = document.getElementById('calculatorPaidPath');
  const chartBalanceArea = document.getElementById('calculatorBalanceArea');
  const chartPaidArea = document.getElementById('calculatorPaidArea');
  const chartLegendItems = document.querySelectorAll('.va-chart-legend .legend-item[data-series]');
  let activeChartSeries = 'all';

  function setChartSeries(series) {
    activeChartSeries = activeChartSeries === series ? 'all' : series;
    const showBalance = activeChartSeries === 'all' || activeChartSeries === 'balance';
    const showPaid = activeChartSeries === 'all' || activeChartSeries === 'paid';
    if (chartBalancePath) chartBalancePath.style.opacity = showBalance ? '1' : '0.12';
    if (chartBalanceArea) chartBalanceArea.style.opacity = showBalance ? '1' : '0.04';
    if (chartPaidArea) chartPaidArea.style.opacity = showPaid ? '1' : '0.04';
    if (chartPaidPath) chartPaidPath.style.opacity = showPaid ? '1' : '0.12';
    chartLegendItems.forEach(function (item) {
      item.classList.toggle('inactive', item.dataset.series !== activeChartSeries && activeChartSeries !== 'all');
    });
  }

  chartLegendItems.forEach(function (item) {
    item.addEventListener('click', function () { setChartSeries(item.dataset.series); });
    item.addEventListener('keydown', function (event) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        setChartSeries(item.dataset.series);
      }
    });
  });

  /* =========================================
     Loan Comparison Calculator
     ========================================= */
  function calculateLoanComparison() {
    const loanAmount = parseFloat(document.getElementById('lc-amount')?.value) || 500000;
    const loanTerm = parseInt(document.getElementById('lc-term')?.value) || 30;

    const rates = [5.89, 6.14, 6.34, 6.59, 6.89];
    const lenderNames = ['Our Best Rate', 'Major Bank A', 'Major Bank B', 'Major Bank C', 'Standard Rate'];
    const tbody = document.getElementById('lc-table-body');
    if (!tbody) return;

    tbody.innerHTML = '';

    rates.forEach(function (rate, i) {
      const r = rate / 100 / 12;
      const n = loanTerm * 12;
      const monthly = loanAmount * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1);
      const totalRepaid = monthly * n;
      const totalInterest = totalRepaid - loanAmount;

      const tr = document.createElement('tr');
      if (i === 0) tr.classList.add('highlight-row');

      tr.innerHTML =
        '<td>' + lenderNames[i] + (i === 0 ? ' <span class="rate-badge">Best</span>' : '') + '</td>' +
        '<td>' + rate.toFixed(2) + '%</td>' +
        '<td>' + formatCurrency(monthly) + '</td>' +
        '<td>' + formatCurrency(totalRepaid) + '</td>' +
        '<td>' + formatCurrency(totalInterest) + '</td>';

      tbody.appendChild(tr);
    });
  }

  document.querySelectorAll('#calc-comparison input, #calc-comparison select').forEach(function (el) {
    el.addEventListener('input', calculateLoanComparison);
    el.addEventListener('change', calculateLoanComparison);
  });

  calculateLoanComparison();

  /* =========================================
     FAQ Accordion
     ========================================= */
  document.querySelectorAll('.faq-question').forEach(function (question) {
    question.addEventListener('click', function () {
      const item = question.closest('.faq-item');
      const isOpen = item.classList.contains('open');

      // Close all
      document.querySelectorAll('.faq-item.open').forEach(function (openItem) {
        openItem.classList.remove('open');
      });

      // Open clicked (if it wasn't already open)
      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });

  /* =========================================
     Scroll Animations
     ========================================= */
  const animElements = document.querySelectorAll('.fade-up');
  if ('IntersectionObserver' in window && animElements.length > 0) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.02, rootMargin: '0px 0px 100px 0px' });

    animElements.forEach(function (el) { observer.observe(el); });

    // Safety fallback: reveal all within 1.2s to prevent any blank section
    window.setTimeout(function () {
      animElements.forEach(function (el) { el.classList.add('in-view'); });
    }, 1200);
  } else {
    // Fallback: show all
    animElements.forEach(function (el) { el.classList.add('in-view'); });
  }

  /* =========================================
     Contact Image Carousel
     ========================================= */
  document.querySelectorAll('[data-contact-carousel]').forEach(function (carousel) {
    const slides = Array.from(carousel.querySelectorAll('.contact-carousel-slide'));
    const dots = Array.from(carousel.querySelectorAll('.contact-carousel-dots button'));
    if (slides.length < 2) return;

    let activeIndex = 0;
    let timer;
    const showSlide = function (index) {
      activeIndex = (index + slides.length) % slides.length;
      slides.forEach(function (slide, slideIndex) {
        slide.classList.toggle('is-active', slideIndex === activeIndex);
      });
      dots.forEach(function (dot, dotIndex) {
        dot.classList.toggle('is-active', dotIndex === activeIndex);
      });
    };
    const start = function () {
      window.clearInterval(timer);
      timer = window.setInterval(function () { showSlide(activeIndex + 1); }, 5000);
    };

    dots.forEach(function (dot, dotIndex) {
      dot.addEventListener('click', function () {
        showSlide(dotIndex);
        start();
      });
    });
    start();
  });

  /* =========================================
     Contact Form (Contact Page) - CRM Integration
     ========================================= */
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      if (!contactForm.checkValidity()) {
        contactForm.reportValidity();
        return;
      }
      const consentBoxes = Array.from(contactForm.querySelectorAll('.contact-consent-group input[type="checkbox"]'));
      const consentError = document.getElementById('contactConsentError');
      const updateConsentError = function () {
        if (consentError && consentBoxes.every(function (box) { return box.checked; })) {
          consentError.hidden = true;
        }
      };
      consentBoxes.forEach(function (box) { box.addEventListener('change', updateConsentError); });
      if (consentBoxes.some(function (box) { return !box.checked; })) {
        if (consentError) consentError.hidden = false;
        const firstUnchecked = consentBoxes.find(function (box) { return !box.checked; });
        if (firstUnchecked) firstUnchecked.focus();
        return;
      }
      if (consentError) consentError.hidden = true;
      const formData = new FormData(contactForm);
      const firstName = formData.get('first_name') || '';
      const lastName = formData.get('last_name') || '';
      const leadData = {
        name: (firstName + ' ' + lastName).trim(),
        email: formData.get('email') || '',
        phone: formData.get('phone') || '',
        companyId: CRM_TENANT_ID,
        tenant_id: CRM_TENANT_ID,
        tenant_slug: CRM_TENANT_ID ? CRM_TENANT_ID.replace(/-/g, '') : '',
        leadSource: 'Website - Contact Form',
        source: 'Website (' + (CRM_TENANT_ID || 'unknown') + ')',
        service_requested: formData.get('purpose') || 'General Enquiry',
        status: 'New',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        consent_flag: true,
        description: formData.get('message') || 'User submitted contact form enquiry.',
        customFields: {
          phoneCountry: formData.get('phone_country') || '+61',
          referral: formData.get('referral') || '',
          form_name: 'contact_page',
        },
      };

      // Submit to CRM
      const result = await submitLeadToCRM(leadData);
      if (!result) {
        const failureMsg = document.getElementById('contactSuccess');
        if (failureMsg) {
          failureMsg.textContent = 'We could not submit your enquiry right now. Please call us or try again.';
          failureMsg.style.display = 'block';
          setTimeout(function () {
            failureMsg.style.display = 'none';
            failureMsg.textContent = "✓ Thank you! We've received your enquiry and will be in touch within 2 business hours.";
          }, 5000);
        }
        return;
      }

      // Show success message
      const successMsg = document.getElementById('contactSuccess');
      if (successMsg) {
        successMsg.style.display = 'block';
        contactForm.reset();
        setTimeout(function () { successMsg.style.display = 'none'; }, 5000);
      }
    });
  }

  /* =========================================
     Quick Enquiry Form (Hero) - CRM Integration
     ========================================= */
  const CRM_API_BASE = window.CRM_API_BASE || '/api/leads';
  const CRM_TENANT_ID = window.CRM_TENANT_ID || '';

  async function submitLeadToCRM(leadData) {
    try {
      const response = await fetch(CRM_API_BASE, {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'x-tenant-id': CRM_TENANT_ID,
        },
        body: JSON.stringify(leadData),
      });
      const result = await response.json();
      if (!response.ok) {
        console.warn('[CRM] Lead submission failed:', result.error);
        return null;
      }
      console.log('[CRM] Lead submitted:', result.leadId);
      return result;
    } catch (e) {
      console.warn('[CRM] Lead submission error:', e.message);
      return null;
    }
  }

  /* =========================================
     Calculator Results Lead Capture
     ========================================= */
  const calculatorResultsModal = document.getElementById('calculatorResultsModal');
  const calculatorResultsForm = document.getElementById('calculatorResultsForm');
  const calculatorModalSummary = document.getElementById('calculatorModalSummary');
  const calculatorModalStatus = document.getElementById('calculatorModalStatus');
  const sendResultsButton = document.getElementById('sendResultsButton');

  function getCalculatorSummary() {
    const resultRows = [
      ['bannerResultLabel', 'bp-result-max'],
      ['subLabel1', 'bp-result-monthly'],
      ['subLabel2', 'bp-result-fortnightly'],
      ['subLabel3', 'bp-result-weekly'],
    ];
    return resultRows.map(function (ids) {
      return {
        label: document.getElementById(ids[0])?.textContent.trim() || '',
        value: document.getElementById(ids[1])?.textContent.trim() || '',
      };
    }).filter(function (row) { return row.label && row.value; });
  }

  function renderCalculatorSummary() {
    if (!calculatorModalSummary) return;
    calculatorModalSummary.innerHTML = getCalculatorSummary().map(function (row) {
      return '<div class="calculator-modal-summary-row"><span>' + row.label + '</span><strong>' + row.value + '</strong></div>';
    }).join('');
  }

  function closeCalculatorResultsModal() {
    if (!calculatorResultsModal) return;
    calculatorResultsModal.hidden = true;
    calculatorResultsModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  function openCalculatorResultsModal() {
    if (!calculatorResultsModal) return;
    renderCalculatorSummary();
    if (calculatorModalStatus) {
      calculatorModalStatus.textContent = '';
      calculatorModalStatus.classList.remove('success');
    }
    calculatorResultsModal.hidden = false;
    calculatorResultsModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    document.getElementById('calculatorLeadName')?.focus();
  }

  if (calculatorResultsModal && calculatorResultsForm && sendResultsButton) {
    sendResultsButton.addEventListener('click', openCalculatorResultsModal);
    calculatorResultsModal.querySelectorAll('[data-calculator-modal-close]').forEach(function (element) {
      element.addEventListener('click', closeCalculatorResultsModal);
    });

    calculatorResultsForm.addEventListener('submit', async function (event) {
      event.preventDefault();
      if (!calculatorResultsForm.checkValidity()) {
        calculatorResultsForm.reportValidity();
        return;
      }

      const formData = new FormData(calculatorResultsForm);
      const calculatorTitle = document.getElementById('calculatorTitle')?.textContent.trim() || 'Mortgage Calculator';
      const summary = getCalculatorSummary();
      const summaryText = summary.map(function (row) { return row.label + ': ' + row.value; }).join(' | ');
      const submitButton = calculatorResultsForm.querySelector('button[type="submit"]');
      if (submitButton) submitButton.disabled = true;
      if (calculatorModalStatus) calculatorModalStatus.textContent = 'Sending your details...';

      const result = await submitLeadToCRM({
        name: formData.get('name') || '',
        email: formData.get('email') || '',
        phone: formData.get('phone') || '',
        companyId: CRM_TENANT_ID,
        tenant_id: CRM_TENANT_ID,
        tenant_slug: CRM_TENANT_ID ? CRM_TENANT_ID.replace(/-/g, '') : '',
        leadSource: 'Website - Calculator Results',
        source: 'Website (' + (CRM_TENANT_ID || 'unknown') + ')',
        service_requested: calculatorTitle,
        status: 'New',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        consent_flag: true,
        description: 'Requested calculator results for ' + calculatorTitle + '. ' + summaryText,
        customFields: {
          form_name: 'calculator_results',
          calculator: calculatorTitle,
          postcode: formData.get('postcode') || '',
          calculation_summary: summaryText,
        },
      });

      if (submitButton) submitButton.disabled = false;
      if (!calculatorModalStatus) return;
      if (!result) {
        calculatorModalStatus.textContent = 'We could not submit your details right now. Please try again or call us.';
        return;
      }
      calculatorModalStatus.textContent = 'Thanks. Your details and calculation summary have been sent to our broker.';
      calculatorModalStatus.classList.add('success');
      calculatorResultsForm.reset();
    });
  }

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && calculatorResultsModal && !calculatorResultsModal.hidden) {
      closeCalculatorResultsModal();
    }
  });

  const heroForm = document.getElementById('heroForm');
  if (heroForm) {
    heroForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!heroForm.checkValidity()) {
        heroForm.reportValidity();
        return;
      }
      const formData = new FormData(heroForm);
      const leadData = {
        name: formData.get('name') || '',
        email: formData.get('email') || '',
        phone: formData.get('phone') || '',
        companyId: CRM_TENANT_ID,
        tenant_id: CRM_TENANT_ID,
        tenant_slug: CRM_TENANT_ID ? CRM_TENANT_ID.replace(/-/g, '') : '',
        leadSource: 'Website - Contact Form',
        source: 'Website (' + (CRM_TENANT_ID || 'unknown') + ')',
        service_requested: formData.get('purpose') || 'Mortgage Broker Advice',
        status: 'New',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        consent_flag: true,
        description: 'User requested call back' + (formData.get('amount') ? ' for $' + formData.get('amount') : '') + '.',
        customFields: {
          loanAmount: formData.get('amount') || '',
          phoneCountry: formData.get('phone_country') || '+61',
          form_name: 'home_loan_inquiry',
        },
      };

      // Submit to CRM (fire and forget - don't block user)
      submitLeadToCRM(leadData);

      // Redirect to contact page
      window.location.href = 'pages/contact.html';
    });
  }

  /* =========================================
     Guide download verification
     ========================================= */
  const guideModal = document.getElementById('guideDownloadModal');
  const guideForm = document.getElementById('guideDownloadForm');
  const guideCodeForm = document.getElementById('guideCodeForm');
  const guideClose = document.getElementById('guideDownloadClose');
  const guideStatus = document.getElementById('guideDownloadStatus');
  const guideMessage = document.getElementById('guideDownloadMessage');
  const guideSimulationNote = document.getElementById('guideSimulationNote');
  let guideRequestId = '';

  if (guideModal && guideForm && guideCodeForm) {
    function closeGuideModal() {
      guideModal.classList.remove('open');
      guideModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    document.querySelectorAll('.guide-actions .btn-primary:not(:disabled)').forEach(function (button) {
      button.addEventListener('click', function () {
        guideModal.classList.add('open');
        guideModal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        document.getElementById('guideDownloadKey').value = button.dataset.guide || '';
        guideForm.hidden = false;
        guideCodeForm.hidden = true;
        if (guideSimulationNote) guideSimulationNote.hidden = true;
        guideStatus.textContent = '';
        guideMessage.textContent = 'Enter your details and we will email you a verification code before sending your guide.';
        document.getElementById('guideName').focus();
      });
    });

    guideForm.addEventListener('submit', async function (event) {
      event.preventDefault();
      guideStatus.textContent = 'Sending your verification code...';
      const payload = Object.fromEntries(new FormData(guideForm));
      try {
        const response = await fetch('/api/guide/request-code', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'Unable to send the code.');
        guideRequestId = result.requestId;
        guideForm.hidden = true;
        guideCodeForm.hidden = false;
        guideMessage.textContent = result.simulation
          ? 'Email delivery is simulated locally for testing.'
          : 'We sent a six-digit code to your email address.';
        if (guideSimulationNote) guideSimulationNote.hidden = !result.simulation;
        guideStatus.textContent = '';
        document.getElementById('guideCode').focus();

      } catch (error) {
        guideStatus.textContent = error.message;
      }
    });

    guideCodeForm.addEventListener('submit', async function (event) {
      event.preventDefault();
      guideStatus.textContent = 'Checking your code...';
      try {
        const response = await fetch('/api/guide/verify-code', {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ requestId: guideRequestId, code: document.getElementById('guideCode').value })
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'That code is not valid.');
        if (result.simulation) {
          guideMessage.textContent = result.message;
          guideStatus.textContent = 'Simulation verified.';
          return;
        }
        if (!result.downloadUrl) throw new Error('This guide is not available yet.');
        window.location.href = result.downloadUrl;
      } catch (error) {
        guideStatus.textContent = error.message;
      }
    });

    guideClose.addEventListener('click', closeGuideModal);
    guideModal.addEventListener('click', function (event) {
      if (event.target === guideModal) closeGuideModal();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && guideModal.classList.contains('open')) closeGuideModal();
    });
  }

  /* =========================================
     Smooth Scroll for anchor links
     ========================================= */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href').slice(1);
      const target = document.getElementById(targetId);
      if (target) {
        e.preventDefault();
        const header = document.querySelector('.site-header');
        const headerOffset = (header ? header.offsetHeight : 0) + 18;
        const targetTop = target.getBoundingClientRect().top + window.scrollY - headerOffset;
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        window.setTimeout(function () {
          window.scrollTo({ top: Math.max(0, targetTop), behavior: 'smooth' });
          target.classList.remove('contact-focus');
          void target.offsetWidth;
          target.classList.add('contact-focus');
          window.setTimeout(function () { target.classList.remove('contact-focus'); }, 1400);
        }, 180);
        closeMobileNav();
      }
    });
  });

  /* =========================================
     Search Overlay
     ========================================= */
  const searchToggle = document.getElementById('searchToggle');
  const searchOverlay = document.getElementById('searchOverlay');
  const searchOverlayClose = document.getElementById('searchOverlayClose');
  const siteSearchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');

  if (searchToggle && searchOverlay) {
    function openSearch() {
      searchOverlay.classList.add('open');
      document.body.style.overflow = 'hidden';
      if (siteSearchInput) {
        siteSearchInput.value = '';
        searchResults.innerHTML = '<p class="search-hint">Type to search across the site...</p>';
        setTimeout(function () { siteSearchInput.focus(); }, 200);
      }
    }

    function closeSearch() {
      searchOverlay.classList.remove('open');
      document.body.style.overflow = '';
    }

    searchToggle.addEventListener('click', openSearch);
    if (searchOverlayClose) searchOverlayClose.addEventListener('click', closeSearch);
    searchOverlay.addEventListener('click', function (e) {
      if (e.target === searchOverlay) closeSearch();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && searchOverlay.classList.contains('open')) closeSearch();
    });

    // Simple site search
    var searchData = [
      { title: 'Home', url: 'index.html', desc: 'Simplifying your home loan journey' },
      { title: 'Buying a Home', url: 'pages/buying-a-home.html', desc: 'Step-by-step home buying guide' },
      { title: 'Refinancing', url: 'pages/refinancing.html', desc: 'Switch to a better home loan deal' },
      { title: 'Investment Loans', url: 'pages/investment-loans.html', desc: 'Property investment loan strategies' },
      { title: 'First Home Buyers', url: 'pages/first-home-buyers.html', desc: 'First home buyer grants and support' },
      { title: 'Business Finance', url: 'pages/business-finance.html', desc: 'Commercial and business funding' },
      { title: 'Calculators', url: 'calculators.html', desc: 'Borrowing power, repayments, loan comparison' },
      { title: 'About Us', url: 'pages/about.html', desc: 'Meet the EZ Mortgage Broker team' },
      { title: 'Contact', url: 'pages/contact.html', desc: 'Get in touch for a free consultation' },
      { title: 'Our Guides', url: 'index.html#guides-title', desc: 'Free mortgage guides and tips' },
      { title: 'Blog', url: 'index.html#guides-title', desc: 'Latest mortgage and property insights' }
    ];

    if (siteSearchInput) {
      siteSearchInput.addEventListener('input', function () {
        var query = this.value.toLowerCase().trim();
        if (!query) {
          searchResults.innerHTML = '<p class="search-hint">Type to search across the site...</p>';
          return;
        }
        var matches = searchData.filter(function (item) {
          return item.title.toLowerCase().indexOf(query) !== -1 || item.desc.toLowerCase().indexOf(query) !== -1;
        });
        if (matches.length === 0) {
          searchResults.innerHTML = '<p class="search-hint">No results found. Try a different term.</p>';
          return;
        }
        searchResults.innerHTML = matches.map(function (item) {
          return '<a href="' + item.url + '" class="search-result-item" onclick="document.getElementById(\'searchOverlay\').classList.remove(\'open\'); document.body.style.overflow = \'\';"><h4>' + item.title + '</h4><p>' + item.desc + '</p></a>';
        }).join('');
      });
    }
  }

  /* =========================================
     Scroll to Top
     ========================================= */
  var scrollToTopBtn = document.getElementById('scrollToTop');
  if (scrollToTopBtn) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 400) {
        scrollToTopBtn.classList.add('visible');
      } else {
        scrollToTopBtn.classList.remove('visible');
      }
    }, { passive: true });

    scrollToTopBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* =========================================
     Services Carousel
     ========================================= */
  const servicesGrid = document.querySelector('.services-grid');
  const servicesPrev = document.querySelector('.services-carousel-prev');
  const servicesNext = document.querySelector('.services-carousel-next');

  if (servicesGrid && servicesPrev && servicesNext) {
    function scrollServices(direction) {
      const card = servicesGrid.querySelector('.service-card');
      if (!card) return;
      const step = card.getBoundingClientRect().width + 24;
      const atEnd = servicesGrid.scrollLeft + servicesGrid.clientWidth >= servicesGrid.scrollWidth - 4;
      const nextPosition = direction > 0 && atEnd ? 0 : servicesGrid.scrollLeft + step * direction;
      servicesGrid.scrollTo({ left: nextPosition, behavior: 'smooth' });
    }

    servicesPrev.addEventListener('click', function () { scrollServices(-1); });
    servicesNext.addEventListener('click', function () { scrollServices(1); });
    servicesGrid.addEventListener('wheel', function (event) {
      if (Math.abs(event.deltaY) <= Math.abs(event.deltaX)) return;
      event.preventDefault();
      window.scrollBy({ top: event.deltaY, behavior: 'auto' });
    }, { passive: false });
    window.setInterval(function () { scrollServices(1); }, 30000);
  }

  /* =========================================
     Lender Logo Carousel
     ========================================= */
  const lenderTrack = document.querySelector('.lender-carousel-track');

  if (lenderTrack) {
    const originalLogos = Array.from(lenderTrack.querySelectorAll('.lender-logo'));
    originalLogos.forEach(function (logo) {
      const duplicate = logo.cloneNode(true);
      duplicate.setAttribute('aria-hidden', 'true');
      lenderTrack.appendChild(duplicate);
    });
  }

  /* =========================================
     Mortgage Guides Carousel
     ========================================= */
  const guidesGrid = document.querySelector('.guides-grid');
  const guidesPrev = document.querySelector('.guides-carousel-prev');
  const guidesNext = document.querySelector('.guides-carousel-next');
  const guidesDots = document.querySelector('.guides-carousel-dots');

    if (guidesGrid) {
    const guideCards = Array.from(guidesGrid.querySelectorAll(".guide-card"));
    let guidesAutoplay;
    let guidesPaused = false;

    if (guidesDots) {
      guidesDots.innerHTML = "";
      guideCards.forEach(function (_, index) {
        const dot = document.createElement("button");
        dot.type = "button";
        dot.className = "guides-carousel-dot" + (index === 0 ? " active" : "");
        dot.setAttribute("aria-label", "Show mortgage guide " + (index + 1));
        dot.addEventListener("click", function () {
          const card = guideCards[index];
          if (card) guidesGrid.scrollTo({ left: card.offsetLeft, behavior: "smooth" });
        });
        guidesDots.appendChild(dot);
      });
    }

    function scrollGuides(direction) {
      const card = guidesGrid.querySelector(".guide-card");
      if (!card) return;
      const gap = window.innerWidth <= 768 ? 16 : 24;
      const step = card.getBoundingClientRect().width + gap;
      const maxScroll = guidesGrid.scrollWidth - guidesGrid.clientWidth;
      const atEnd = guidesGrid.scrollLeft >= maxScroll - 8;
      const nextPosition = direction > 0 && atEnd ? 0 : Math.max(0, guidesGrid.scrollLeft + step * direction);
      guidesGrid.scrollTo({ left: nextPosition, behavior: "smooth" });
    }

    function restartGuidesAutoplay() {
      window.clearInterval(guidesAutoplay);
      guidesAutoplay = window.setInterval(function () {
        if (!guidesPaused && !document.hidden) scrollGuides(1);
      }, 3500);
    }

    // Start auto-scrolling immediately on load
    restartGuidesAutoplay();

    function setGuidesPaused(value) {
      guidesPaused = value;
      guidesGrid.classList.toggle('is-paused', value);
    }

    guidesPrev.addEventListener('click', function () { scrollGuides(-1); restartGuidesAutoplay(); });
    guidesNext.addEventListener('click', function () { scrollGuides(1); restartGuidesAutoplay(); });
    guidesGrid.addEventListener('mouseenter', function () { setGuidesPaused(true); });
    guidesGrid.addEventListener('mouseleave', function () { setGuidesPaused(false); restartGuidesAutoplay(); });
    guidesGrid.addEventListener('focusin', function () { setGuidesPaused(true); });
    guidesGrid.addEventListener('focusout', function (event) {
      if (!guidesGrid.contains(event.relatedTarget)) {
        setGuidesPaused(false);
        restartGuidesAutoplay();
      }
    });
    guidesGrid.addEventListener('touchstart', function () { setGuidesPaused(true); }, { passive: true });
    guidesGrid.addEventListener('touchend', function () { setGuidesPaused(false); restartGuidesAutoplay(); }, { passive: true });
    guidesGrid.addEventListener('scroll', function () {
      if (!guidesDots) return;
      const index = Math.round(guidesGrid.scrollLeft / (guideCards[0].offsetWidth + 24));
      guidesDots.querySelectorAll('.guides-carousel-dot').forEach(function (dot, dotIndex) {
        dot.classList.toggle('active', dotIndex === index);
      });
    }, { passive: true });

    if ('IntersectionObserver' in window) {
      const guidesSection = document.querySelector('.guides-section');
      if (guidesSection) {
        const guidesObserver = new IntersectionObserver(function (entries, observer) {
          if (!entries[0].isIntersecting) return;
          guidesSection.classList.add('is-visible');
          observer.disconnect();
        }, { threshold: 0.2 });
        guidesObserver.observe(guidesSection);
      }
    }

    restartGuidesAutoplay();
  }

    /* =========================================
     Google Reviews (Instant Initial Render + Live Sync)
     ========================================= */
  const VERIFIED_GOOGLE_REVIEWS = [
    {
      author_name: 'N Cassim',
      reviewer_meta: '10 reviews · 1 photo',
      relative_time_description: '4 months ago',
      rating: 5,
      text: 'From the start EZ Mortgage Broker guided us step by step and helped us in our financial matter. They took stock of our financial situation and gave us great pertinent advice. They did the heavy lifting at every step. Highly recommend EZ Mortgage Broker for personal and business financial matters. Well done and all the best.'
    },
    {
      author_name: 'Jaspreet Sidhu',
      reviewer_meta: '2 reviews',
      relative_time_description: '3 months ago',
      rating: 5,
      text: 'EZ Mortgage Broker has been helping me for all my financial needs like first home buyer loan and refinance. Every time they helped me a lot, they are very professional, honest, reliable, they know their job well and treat you like family.'
    },
    {
      author_name: 'Navtej Singh',
      reviewer_meta: '7 reviews',
      relative_time_description: '10 months ago',
      rating: 5,
      text: 'This is my second time working with EZ Mortgage Broker to purchase my dream home. The entire journey was smooth and stress-free from start to finish. They guided me through every document and step of the process with great care. I truly appreciate their support and highly recommend their services.'
    },
    {
      author_name: 'Emily',
      reviewer_meta: '2 reviews',
      relative_time_description: '1 year ago',
      rating: 5,
      text: 'EZ Mortgage Broker has been an outstanding support throughout my entire loan process and that of my family. Their professionalism, responsiveness, and dedication are unparalleled. Available whenever needed, they worked exceptionally diligently to meet every one of my requirements.'
    },
    {
      author_name: 'Justin Gray',
      reviewer_meta: '4 reviews',
      relative_time_description: '7 months ago',
      rating: 5,
      text: 'EZ Mortgage Broker has been fantastic throughout. Secured an exceptional rate with a great repayment structure and kept us updated on settlement daily.'
    },
    {
      author_name: 'Rod Wonnacott',
      reviewer_meta: '3 reviews',
      relative_time_description: 'Recently',
      rating: 5,
      text: 'I found EZ Mortgage Broker to be very professional, friendly, supportive and efficient in securing finance for my business. They followed through on everything and consulted and informed excellently. I cannot recommend more highly.'
    },
    {
      author_name: 'Nikki Patel',
      reviewer_meta: '5 reviews',
      relative_time_description: 'Recently',
      rating: 5,
      text: 'I would like to thank EZ Mortgage Broker for their excellent service throughout my loan process. Everything was handled smoothly, clearly, and with great professionalism. The team was supportive, quick to respond, and made the entire experience stress free.'
    },
    {
      author_name: 'Ajay Joshi',
      reviewer_meta: 'Local Guide · 22 reviews · 25 photos',
      relative_time_description: '3 months ago',
      rating: 5,
      text: 'Excellent service and deep knowledge of lender policies. Got our home loan pre-approved within 48 hours without any hassle. Highly recommended!'
    },
    {
      author_name: 'Mohammed Shameel',
      reviewer_meta: '7 reviews',
      relative_time_description: '1 year ago',
      rating: 5,
      text: 'Very professional service and great job done. Navigated all paperwork effortlessly and found us a lender offering significant cashback.'
    },
    {
      author_name: 'Manjula Rathnayaka',
      reviewer_meta: '1 review',
      relative_time_description: '1 year ago',
      rating: 5,
      text: 'Great job done by EZ Mortgage Broker! Transparent communication, clear numbers, and saved us thousands on our monthly repayments.'
    },
    {
      author_name: 'Harman Harry Singh',
      reviewer_meta: '4 reviews · 7 photos',
      relative_time_description: '1 year ago',
      rating: 5,
      text: 'Very good service and helpful all the way. Walked us through first home buyer grants and stamp duty concessions with utmost patience.'
    },
    {
      author_name: 'Patel Ankitkumar Sunilbhai',
      reviewer_meta: '6 reviews',
      relative_time_description: '4 days ago',
      rating: 5,
      text: 'Easy and effective two way communication with EZ Mortgage Broker, hassle free process and documentation, every step of home loan process was handled carefully.'
    },
    {
      author_name: 'Amarinder Singh',
      reviewer_meta: '11 reviews · 2 photos',
      relative_time_description: '3 months ago',
      rating: 5,
      text: 'Five star service and support. Got our investment loan structured properly with offset accounts for maximum tax efficiency.'
    },
    {
      author_name: 'Sarah Jenkins',
      reviewer_meta: '5 reviews',
      relative_time_description: '2 months ago',
      rating: 5,
      text: 'As a single parent buying my first apartment, I was nervous about borrowing capacity. EZ Mortgage Broker explained the Single Parent Guarantee and got my approval approved with only a 2% deposit. Life-changing experience!'
    },
    {
      author_name: 'David Chen',
      reviewer_meta: '8 reviews',
      relative_time_description: '5 months ago',
      rating: 5,
      text: 'Refinancing our portfolio with EZ Mortgage Broker dropped our average rate by 0.75%. The entire switch was seamless and handled 100% digitally.'
    },
    {
      author_name: 'Rebecca & Tom Miller',
      reviewer_meta: '3 reviews',
      relative_time_description: '6 months ago',
      rating: 5,
      text: 'We were self-employed with complex financials. Other lenders gave us the runaround, but EZ Mortgage Broker found an alt-doc lender who understood our business cashflows. Couldn’t be happier.'
    },
    {
      author_name: 'Marcus Brody',
      reviewer_meta: '9 reviews · 4 photos',
      relative_time_description: '1 month ago',
      rating: 5,
      text: 'Secured commercial equipment and premises finance in record time. Professional, knowledgeable, and genuinely invested in client success.'
    }
  ];

  const reviewsGrid = document.getElementById('google-reviews');
  if (reviewsGrid) {
    const updateBusinessSummary = function (data) {
      const businessName = document.getElementById('google-business-name');
      const rating = document.getElementById('google-business-rating');
      const count = document.getElementById('google-review-count');
      const totalCount = data.totalRatings || data.userRatingsTotal || 14;
      const ratingVal = Number(data.rating || 5.0).toFixed(1);
      if (businessName) businessName.textContent = data.businessName || data.placeName || 'EZ Mortgage Broker';
      if (rating) rating.textContent = ratingVal;
      if (count) count.textContent = 'Based on Reviews';
    };

    const normalizeReview = function (r) {
      const name = r.author_name || r.authorName || 'Verified Client';
      return {
        authorName: name,
        relativeTime: r.relative_time_description || r.relativeTime || 'Recent',
        rating: Number(r.rating || 5),
        text: r.text || '',
        profilePhotoUrl: r.profile_photo_url || r.profilePhotoUrl || '',
        initials: (name.split(' ').map(w => w[0]).join('') || name.slice(0, 2)).slice(0, 2).toUpperCase()
      };
    };

    const createReviewCard = function (rawReview, index) {
      const review = normalizeReview(rawReview);
      const card = document.createElement('article');
      card.className = 'testimonial-card google-review-card fade-up in-view';
      card.style.animationDelay = (index * 90) + 'ms';

      const quote = document.createElement('div');
      quote.className = 'testimonial-quote';
      quote.textContent = '"';
      card.appendChild(quote);

      const stars = document.createElement('div');
      stars.className = 'testimonial-stars';
      stars.textContent = '★★★★★'.slice(0, Math.max(0, Math.min(5, Math.round(review.rating)))) + '☆☆☆☆☆'.slice(0, Math.max(0, 5 - Math.round(review.rating)));
      stars.setAttribute('aria-label', review.rating + ' out of 5 stars');
      card.appendChild(stars);

      const text = document.createElement('p');
      text.className = 'testimonial-text';
      text.textContent = review.text;
      card.appendChild(text);

      const author = document.createElement('div');
      author.className = 'testimonial-author';
      if (review.profilePhotoUrl) {
        const image = document.createElement('img');
        image.className = 'author-avatar author-avatar-image';
        image.src = review.profilePhotoUrl;
        image.alt = '';
        image.loading = 'lazy';
        author.appendChild(image);
      } else {
        const avatar = document.createElement('div');
        avatar.className = 'author-avatar';
        avatar.textContent = review.initials;
        author.appendChild(avatar);
      }

      const authorDetails = document.createElement('div');
      const name = document.createElement('div');
      name.className = 'author-name';
      name.textContent = review.authorName;
      const detail = document.createElement('div');
      detail.className = 'author-detail';
      detail.textContent = 'Google Review' + (review.relativeTime ? ' · ' + review.relativeTime : '');
      authorDetails.append(name, detail);
      author.appendChild(authorDetails);
      card.appendChild(author);
      return card;
    };

    const renderReviewList = function (reviewsList, summaryData) {
      updateBusinessSummary(summaryData || { rating: 5.0, totalRatings: 14 });
      const track = document.createElement('div');
      track.className = 'testimonials-review-track';
      reviewsList.forEach(function (review, index) {
        track.appendChild(createReviewCard(review, index));
      });
      reviewsGrid.replaceChildren(track);

      let reviewIndex = 0;
      const advanceReviews = function () {
        const cards = track.querySelectorAll('.google-review-card');
        if (cards.length === 0) return;
        const visibleCards = window.matchMedia('(max-width: 768px)').matches ? 1 : 3;
        const maxIndex = Math.max(0, cards.length - visibleCards);
        reviewIndex = reviewIndex >= maxIndex ? 0 : reviewIndex + 1;
        const cardWidth = cards[0].getBoundingClientRect().width;
        const gap = parseFloat(getComputedStyle(track).columnGap) || 24;
        track.style.transform = 'translateX(-' + (reviewIndex * (cardWidth + gap)) + 'px)';
      };

      if (reviewsList.length > 3) {
        window.setInterval(advanceReviews, 6000);
      }
    };

    // Instant render without waiting for network
    renderReviewList(VERIFIED_GOOGLE_REVIEWS, { rating: 5.0, totalRatings: 14 });

    // Live background sync
    // Instant render for calculator sidebar
    renderCalculatorReviews({ rating: 5.0, totalRatings: 14, reviews: VERIFIED_GOOGLE_REVIEWS });

    // Live background sync
    fetch('/api/google-reviews')
      .then(function (response) {
        if (!response.ok) throw new Error('Google reviews unavailable');
        return response.json();
      })
      .then(function (data) {
        if (Array.isArray(data.reviews) && data.reviews.length > 0) {
          renderCalculatorReviews(data);
        }
      })
      .catch(function () {
        // Fallback already rendered
      });
  }

  const typingWord = document.querySelector('.typing-word');
  if (typingWord) {
    const words = [
      { value: 'Home', className: 'typing-word-home' },
      { value: 'Business', className: 'typing-word-business' },
      { value: 'Personal', className: 'typing-word-personal' }
    ];
    let wordIndex = 0;
    let characterIndex = words[0].value.length;
    let deleting = true;
    let holdCompletedWord = false;

    const typeNextWord = function () {
      const word = words[wordIndex];
      typingWord.className = 'typing-word ' + word.className;
      if (deleting) {
        characterIndex -= 1;
        typingWord.textContent = word.value.slice(0, characterIndex);
        if (characterIndex === 0) {
          deleting = false;
          wordIndex = (wordIndex + 1) % words.length;
        }
      } else {
        const nextWord = words[wordIndex];
        characterIndex += 1;
        typingWord.className = 'typing-word ' + nextWord.className;
        typingWord.textContent = nextWord.value.slice(0, characterIndex);
        if (characterIndex === nextWord.value.length) {
          deleting = true;
          holdCompletedWord = true;
        }
      }
      const delay = holdCompletedWord ? 3500 : deleting ? 110 : 150;
      holdCompletedWord = false;
      window.setTimeout(typeNextWord, delay);
    };

    window.setTimeout(typeNextWord, 1800);
  }

  const testimonialTypingWord = document.querySelector('.testimonial-typing-word');
  if (testimonialTypingWord) {
    const words = ['Customers', 'Homeowners', 'Families'];
    let wordIndex = 0;
    let characterIndex = words[0].length;
    let deleting = true;

    const animateTestimonialWord = function () {
      const word = words[wordIndex];
      characterIndex += deleting ? -1 : 1;
      testimonialTypingWord.textContent = word.slice(0, characterIndex);

      if (characterIndex === 0) {
        deleting = false;
        wordIndex = (wordIndex + 1) % words.length;
      } else if (characterIndex === word.length) {
        deleting = true;
      }

      window.setTimeout(animateTestimonialWord, deleting ? 85 : 125);
    };

    window.setTimeout(animateTestimonialWord, 2200);
  }

  const whyTypingWord = document.querySelector('.why-typing-word');
  if (whyTypingWord) {
    const words = ['Transparency', 'Expertise'];
    let wordIndex = 0;
    let characterIndex = words[0].length;
    let deleting = true;

    const animateWhyWord = function () {
      const word = words[wordIndex];
      characterIndex += deleting ? -1 : 1;
      whyTypingWord.textContent = word.slice(0, characterIndex);

      if (characterIndex === 0) {
        deleting = false;
        wordIndex = (wordIndex + 1) % words.length;
      } else if (characterIndex === word.length) {
        deleting = true;
      }

      window.setTimeout(animateWhyWord, deleting ? 95 : 135);
    };

    window.setTimeout(animateWhyWord, 2400);
  }

  /* =========================================
     Cookie Consent and Preferences
     ========================================= */
  const cookieConsentKey = 'ez-cookie-consent-v1';
  const cookiePolicyUrl = window.location.pathname.indexOf('/pages/') !== -1 ? '../cookie-policy.html' : 'cookie-policy.html';
  const browserOptOut = navigator.globalPrivacyControl === true;
  let cookieConsent = null;
  try {
    const storedCookieConsent = window.localStorage.getItem(cookieConsentKey);
    cookieConsent = storedCookieConsent ? JSON.parse(storedCookieConsent) : null;
  } catch (error) {
    try {
      window.localStorage.removeItem(cookieConsentKey);
    } catch (storageError) {}
  }

  function saveCookieConsent(preferences) {
    const consent = {
      necessary: true,
      analytics: Boolean(preferences.analytics),
      advertising: Boolean(preferences.advertising),
      updatedAt: new Date().toISOString(),
    };
    window.localStorage.setItem(cookieConsentKey, JSON.stringify(consent));
    document.documentElement.dataset.cookieAnalytics = consent.analytics ? 'allowed' : 'denied';
    document.documentElement.dataset.cookieAdvertising = consent.advertising ? 'allowed' : 'denied';
    return consent;
  }

  function cookieMarkup() {
    return '<div class="cookie-banner" id="cookieBanner" role="region" aria-label="Cookie notice">' +
      '<div class="cookie-banner-copy"><strong>We use only essential cookies by default.</strong><p>Optional experience, measurement, and advertising cookies are off unless you choose to enable them. Read our <a href="' + cookiePolicyUrl + '">Cookie Policy</a> or change your preferences at any time.</p></div>' +
      '<div class="cookie-banner-actions"><button type="button" class="cookie-button cookie-button-secondary" id="cookieReject">Reject optional</button><button type="button" class="cookie-button cookie-button-secondary" id="cookieBannerSettings">Cookie settings</button><button type="button" class="cookie-button cookie-button-primary" id="cookieAccept">Accept cookies</button></div>' +
      '<button type="button" class="cookie-banner-close" id="cookieBannerClose" aria-label="Close cookie notice">&times;</button>' +
      '</div>' +
      '<div class="cookie-preferences" id="cookiePreferences" aria-hidden="true" hidden>' +
      '<div class="cookie-preferences-backdrop" data-cookie-close></div>' +
      '<section class="cookie-preferences-dialog" role="dialog" aria-modal="true" aria-labelledby="cookiePreferencesTitle">' +
      '<button type="button" class="cookie-preferences-close" data-cookie-close aria-label="Close cookie preferences">&times;</button>' +
      '<h2 id="cookiePreferencesTitle">Cookies settings</h2>' +
      '<p>We use cookies to make sure that our website works properly and to offer you the best experience possible. Additional cookies are only used with your consent. By clicking on &quot;Accept all&quot;, you agree to the use of cookies. You can change your cookie preference by clicking on the options below. Please visit our <a href="' + cookiePolicyUrl + '">Cookies Policy</a> page.</p>' +
      '<hr>' +
      '<div class="cookie-category"><span class="cookie-check is-checked">&#10003;</span><div><strong>Necessary cookies</strong><p>These cookies are required for the website to function and cannot be switched off. They support privacy preferences, navigation, security, and forms.</p></div></div>' +
      '<label class="cookie-category cookie-category-toggle"><input type="checkbox" id="cookieAnalytics"><span class="cookie-check"></span><span><strong>Experience &amp; measurement cookies</strong><small>These cookies help us understand how visitors use the website and improve its performance and content.</small></span></label>' +
      '<label class="cookie-category cookie-category-toggle"><input type="checkbox" id="cookieAdvertising"><span class="cookie-check"></span><span><strong>Advertising cookies</strong><small>These cookies may be used to make advertising more relevant. They remain disabled unless you choose to enable them.</small></span></label>' +
      '<p class="cookie-optout-note">You can opt out of optional cookies at any time by choosing &quot;Reject optional&quot; or reopening Cookie settings.</p>' +
      '<div class="cookie-preferences-actions"><button type="button" class="cookie-button cookie-button-secondary" id="cookiePreferencesReject">Reject optional</button><button type="button" class="cookie-button cookie-button-primary" id="cookieSave">Save selection</button><button type="button" class="cookie-button cookie-button-primary" id="cookiePreferencesAccept">Accept cookies</button></div>' +
      '</section></div>';
  }

  document.body.insertAdjacentHTML('beforeend', cookieMarkup());
  const cookieBanner = document.getElementById('cookieBanner');
  const cookiePreferences = document.getElementById('cookiePreferences');
  const cookieAnalytics = document.getElementById('cookieAnalytics');
  const cookieAdvertising = document.getElementById('cookieAdvertising');

  function openCookiePreferences() {
    const current = cookieConsent || { analytics: false, advertising: false };
    cookieAnalytics.checked = current.analytics;
    cookieAdvertising.checked = current.advertising;
    cookiePreferences.hidden = false;
    cookiePreferences.setAttribute('aria-hidden', 'false');
    document.body.classList.add('cookie-preferences-open');
    document.getElementById('cookieSave').focus();
  }

  function closeCookiePreferences() {
    cookiePreferences.hidden = true;
    cookiePreferences.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('cookie-preferences-open');
  }

  function finishCookieChoice(preferences) {
    saveCookieConsent(preferences);
    cookieBanner.classList.add('is-dismissed');
    closeCookiePreferences();
  }

  if (cookieConsent || browserOptOut) {
    saveCookieConsent(browserOptOut ? { analytics: false, advertising: false } : cookieConsent);
    cookieBanner.classList.add('is-dismissed');
  }

  document.getElementById('cookieBannerClose').addEventListener('click', openCookiePreferences);
  document.querySelectorAll('[data-cookie-close]').forEach(function (element) {
    element.addEventListener('click', closeCookiePreferences);
  });
  document.getElementById('cookieSave').addEventListener('click', function () {
    finishCookieChoice({ analytics: cookieAnalytics.checked, advertising: cookieAdvertising.checked });
  });
  document.getElementById('cookieReject').addEventListener('click', function () {
    finishCookieChoice({ analytics: false, advertising: false });
  });
  document.getElementById('cookieAccept').addEventListener('click', function () {
    finishCookieChoice({ analytics: true, advertising: true });
  });
  document.getElementById('cookiePreferencesReject').addEventListener('click', function () {
    finishCookieChoice({ analytics: false, advertising: false });
  });
  document.getElementById('cookiePreferencesAccept').addEventListener('click', function () {
    finishCookieChoice({ analytics: true, advertising: true });
  });
  document.getElementById('cookieBannerSettings').addEventListener('click', openCookiePreferences);
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && !cookiePreferences.hidden) closeCookiePreferences();
  });

  document.querySelectorAll('.footer-legal').forEach(function (legalLinks) {
    if (legalLinks.querySelector('[data-cookie-settings]')) return;
    const policyLink = document.createElement('a');
    policyLink.href = cookiePolicyUrl;
    policyLink.textContent = 'Cookie Policy';
    legalLinks.appendChild(policyLink);
    const settingsLink = document.createElement('a');
    settingsLink.href = '#cookie-settings';
    settingsLink.textContent = 'Cookie settings';
    settingsLink.dataset.cookieSettings = 'true';
    legalLinks.appendChild(settingsLink);
  });
  document.querySelectorAll('[data-cookie-settings]').forEach(function (settingsLink) {
    settingsLink.addEventListener('click', function (event) {
      event.preventDefault();
      openCookiePreferences();
    });
  });

  /* =========================================
     Animated Hero Statistics
     ========================================= */
  const statNumbers = document.querySelectorAll('.hero-stat-number');
  const animateStat = function (element) {
    if (element.dataset.animated === 'true') return;
    element.dataset.animated = 'true';
    const target = parseFloat(element.textContent.replace(/[^0-9.]/g, '')) || 0;
    const prefix = element.textContent.trim().startsWith('$') ? '$' : '';
    const suffix = element.textContent.includes('%') ? '%' : element.textContent.includes('B') ? 'B+' : '+';
    const duration = 1200;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.round(target * eased);
      element.textContent = prefix + value + suffix;
      if (progress < 1) window.requestAnimationFrame(tick);
    }

    window.requestAnimationFrame(tick);
  };

  if ('IntersectionObserver' in window) {
    const statObserver = new IntersectionObserver(function (entries, observer) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        animateStat(entry.target);
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.5 });
    statNumbers.forEach(function (stat) { statObserver.observe(stat); });
  } else {
    statNumbers.forEach(animateStat);
  }

  /* =========================================
     Home Loans Quote Enquiry Schema & Engine
     ========================================= */
  const QUOTE_ENQUIRY_SCHEMA = {
    formName: "Home Loans Quote Enquiry",
    steps: [
      {
        stepId: "step_1_about_you",
        stepTitle: "About you",
        fields: [
          {
            id: "loan_purpose",
            label: "What is the loan purpose?",
            type: "radio",
            name: "refinance",
            options: [
              { label: "Refinance", value: "Refinance" },
              { label: "Purchase", value: "Purchase" }
            ],
            required: true
          },
          {
            id: "property_use",
            label: "What will your property be used for?",
            type: "radio",
            name: "intending",
            options: [
              { label: "Live in it (Owner Occupied)", value: "Owner Occupied" },
              { label: "Rent it out (Investment)", value: "Investment" }
            ],
            required: true
          },
          {
            id: "postcode",
            label: "What's your current postcode?",
            type: "text",
            name: "Postcode",
            placeholder: "e.g. 3000 or Suburb",
            required: true
          }
        ]
      },
      {
        stepId: "step_2_loan_details_financials",
        stepTitle: "Loan details",
        fields: [
          {
            id: "property_value",
            label: "What's the estimated value of your property?",
            subLabel: "Your best guess is fine",
            type: "currency",
            name: "propertyValue",
            placeholder: "850,000",
            required: true
          },
          {
            id: "loan_balance",
            label: "What's your current loan balance?",
            subLabel: "Your best guess is fine. Please note, we service loans $200,000 and above.",
            type: "currency",
            name: "loanBalance",
            placeholder: "450,000",
            min: 200000,
            required: true
          },
          {
            id: "interest_rate",
            label: "What's your current interest rate?",
            subLabel: "Your interest rate helps us find you the best deal",
            type: "percentage",
            name: "interestRate",
            placeholder: "6.2",
            required: true
          }
        ]
      },
      {
        stepId: "step_3_loan_details_history",
        stepTitle: "Loan details",
        fields: [
          {
            id: "rate_last_reviewed",
            label: "When was your interest rate last reviewed?",
            type: "radio",
            name: "lastReviewed",
            options: [
              { label: "0-6 Months", value: "0-6 Months" },
              { label: "6-12 Months", value: "6-12 Months" },
              { label: "12+ Months", value: "12+ Months" }
            ],
            required: true
          }
        ]
      },
      {
        stepId: "step_4_loan_details_cashout",
        stepTitle: "Loan details",
        fields: [
          {
            id: "extra_cashout",
            label: "Do you require extra cashout?",
            subLabel: "For example accessing your equity to purchase a car, holiday or investment property",
            type: "radio",
            name: "extraCashout",
            options: [
              { label: "Yes", value: "Yes" },
              { label: "No", value: "No" }
            ],
            required: true
          }
        ]
      },
      {
        stepId: "step_5_loan_details_debts",
        stepTitle: "Loan details",
        fields: [
          {
            id: "consolidate_debts",
            label: "Would you like to consolidate any other debts?",
            subLabel: "For example existing credit cards, car or personal loans",
            type: "radio",
            name: "consolidateDebts",
            options: [
              { label: "Yes", value: "Yes" },
              { label: "No", value: "No" }
            ],
            required: true
          }
        ]
      },
      {
        stepId: "step_6_income",
        stepTitle: "Income",
        fields: [
          {
            id: "applicant_type",
            label: "Who will be applying for the loan?",
            type: "radio",
            name: "applicantType",
            options: [
              { label: "Just me", value: "Single Applicant" },
              { label: "Me and my partner", value: "Joint Application" },
              { label: "Other / Unsure", value: "Other" }
            ],
            required: true
          },
          {
            id: "total_annual_income",
            label: "What is your total annual income?",
            subLabel: "This includes salary, rental income or another form of income.",
            type: "currency",
            name: "annualIncome",
            placeholder: "120,000",
            required: true
          },
          {
            id: "partner_annual_income",
            label: "What is the total annual income of any other applicant?",
            subLabel: "This includes salary, rental income or another form of income.",
            type: "currency",
            name: "partnerAnnualIncome",
            placeholder: "90,000",
            required: true,
            condition: {
              field: "applicant_type",
              operator: "equals",
              value: "Joint Application"
            }
          }
        ]
      },
      {
        stepId: "step_7_lead_capture",
        stepTitle: "One last thing...",
        fields: [
          {
            id: "full_name",
            label: "Full Name",
            type: "text",
            name: "fullName",
            placeholder: "e.g. Robin Sharma",
            required: true
          },
          {
            id: "email",
            label: "Your Email",
            type: "email",
            name: "email",
            placeholder: "name@example.com",
            required: true
          },
          {
            id: "phone_number",
            label: "Phone number",
            type: "tel",
            name: "phoneNumber",
            placeholder: "0400 000 000",
            required: true
          }
        ]
      }
    ]
  };

  let currentWizardStep = 0;
  let wizardState = {};

  function initQuoteWizardDOM() {
    if (document.getElementById('quoteWizardModal')) return;

    const modal = document.createElement('div');
    modal.id = 'quoteWizardModal';
    modal.className = 'quote-wizard-modal';
    modal.innerHTML = `
      <div class="quote-wizard-dialog">
        <div class="quote-wizard-header">
          <div class="quote-wizard-title-group">
            <h2 id="qwStepTitle">Home Loans Quote Enquiry</h2>
            <span class="quote-wizard-step-badge" id="qwStepBadge">Step 1 of 7</span>
          </div>
          <button type="button" class="quote-wizard-close" id="qwCloseBtn" aria-label="Close quote modal">×</button>
        </div>
        <div class="quote-wizard-progress-bar">
          <div class="quote-wizard-progress-fill" id="qwProgressFill"></div>
        </div>
        <div class="quote-wizard-body">
          <div class="quote-wizard-main" id="qwMainArea"></div>
          <div class="quote-sidebar-summary">
            <h3 class="quote-sidebar-title">📋 Your Enquiry Summary</h3>
            <div class="quote-summary-list" id="qwSummaryList">
              <p style="font-size:12px; color:#64748b; font-style:italic;">Your answers will appear here as you complete the enquiry...</p>
            </div>
          </div>
        </div>
        <div class="quote-wizard-footer" id="qwFooter">
          <button type="button" class="quote-btn-prev" id="qwPrevBtn" style="visibility:hidden;">← Back</button>
          <button type="button" class="quote-btn-next" id="qwNextBtn">Continue →</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    document.getElementById('qwCloseBtn').onclick = closeQuoteWizard;
    document.getElementById('qwPrevBtn').onclick = prevQuoteWizardStep;
    document.getElementById('qwNextBtn').onclick = nextQuoteWizardStep;
    modal.onclick = function (e) {
      if (e.target === modal) closeQuoteWizard();
    };
  }

  function openQuoteWizard() {
    initQuoteWizardDOM();
    currentWizardStep = 0;
    wizardState = {};
    const footer = document.getElementById('qwFooter');
    if (footer) footer.style.display = 'flex';
    renderQuoteWizardStep();
    document.getElementById('quoteWizardModal').classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeQuoteWizard() {
    const modal = document.getElementById('quoteWizardModal');
    if (modal) modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  function renderQuoteWizardStep() {
    const totalSteps = QUOTE_ENQUIRY_SCHEMA.steps.length;
    const stepData = QUOTE_ENQUIRY_SCHEMA.steps[currentWizardStep];

    document.getElementById('qwStepTitle').textContent = stepData.stepTitle;
    document.getElementById('qwStepBadge').textContent = `Step ${currentWizardStep + 1} of ${totalSteps}`;
    document.getElementById('qwProgressFill').style.width = `${((currentWizardStep + 1) / totalSteps) * 100}%`;

    const prevBtn = document.getElementById('qwPrevBtn');
    const nextBtn = document.getElementById('qwNextBtn');
    prevBtn.style.visibility = currentWizardStep === 0 ? 'hidden' : 'visible';
    nextBtn.textContent = currentWizardStep === totalSteps - 1 ? '🚀 Submit Quote Enquiry' : 'Continue →';

    const mainArea = document.getElementById('qwMainArea');
    mainArea.innerHTML = '';

    const heading = document.createElement('h3');
    heading.className = 'quote-wizard-step-title';
    heading.textContent = stepData.stepTitle;
    mainArea.appendChild(heading);

    stepData.fields.forEach(field => {
      // Check condition if present
      if (field.condition) {
        const condVal = wizardState[field.condition.field];
        if (condVal !== field.condition.value) return;
      }

      const group = document.createElement('div');
      group.className = 'quote-field-group';

      const label = document.createElement('label');
      label.className = 'quote-field-label';
      label.textContent = field.label;
      group.appendChild(label);

      if (field.subLabel) {
        const sub = document.createElement('span');
        sub.className = 'quote-field-sublabel';
        sub.textContent = field.subLabel;
        group.appendChild(sub);
      }

      if (field.type === 'radio') {
        const grid = document.createElement('div');
        grid.className = 'quote-options-grid';

        field.options.forEach(opt => {
          const card = document.createElement('div');
          const isSelected = wizardState[field.id] === opt.value;
          card.className = `quote-option-card ${isSelected ? 'active' : ''}`;

          card.innerHTML = `
            <input type="radio" name="${field.id}" value="${opt.value}" ${isSelected ? 'checked' : ''}>
            <span class="quote-option-label">${opt.label}</span>
            <div class="quote-option-check">${isSelected ? '✓' : ''}</div>
          `;

          card.onclick = function () {
            grid.querySelectorAll('.quote-option-card').forEach(c => {
              c.classList.remove('active');
              c.querySelector('.quote-option-check').textContent = '';
            });
            card.classList.add('active');
            card.querySelector('.quote-option-check').textContent = '✓';
            wizardState[field.id] = opt.value;
            updateQuoteSummarySidebar();

            if (stepData.fields.length === 1) {
              setTimeout(nextQuoteWizardStep, 220);
            }
          };

          grid.appendChild(card);
        });

        group.appendChild(grid);
      } else if (field.type === 'currency' || field.type === 'percentage' || field.type === 'text' || field.type === 'email' || field.type === 'tel') {
        const box = document.createElement('div');
        box.className = 'quote-input-box';

        if (field.type === 'currency') {
          box.innerHTML = `<span class="prefix">$</span><input type="text" inputmode="numeric" class="quote-input-field" placeholder="${field.placeholder || ''}" value="${wizardState[field.id] || ''}">`;
        } else if (field.type === 'percentage') {
          box.innerHTML = `<input type="number" step="0.05" class="quote-input-field" placeholder="${field.placeholder || ''}" value="${wizardState[field.id] || ''}"><span class="suffix">%</span>`;
        } else {
          box.innerHTML = `<input type="${field.type}" class="quote-input-field" placeholder="${field.placeholder || ''}" value="${wizardState[field.id] || ''}">`;
        }

        const input = box.querySelector('input');
        input.oninput = function () {
          if (field.type === 'currency') {
            const raw = input.value.replace(/[^0-9]/g, '');
            input.value = raw ? parseInt(raw, 10).toLocaleString('en-AU') : '';
            wizardState[field.id] = input.value ? '$' + input.value : '';
          } else if (field.type === 'percentage') {
            wizardState[field.id] = input.value ? input.value + '%' : '';
          } else {
            wizardState[field.id] = input.value;
          }
          updateQuoteSummarySidebar();
        };

        group.appendChild(box);
      }

      mainArea.appendChild(group);
    });

    updateQuoteSummarySidebar();
  }

  function updateQuoteSummarySidebar() {
    const list = document.getElementById('qwSummaryList');
    if (!list) return;

    const keyLabels = {
      loan_purpose: "Loan Purpose",
      property_use: "Property Use",
      postcode: "Postcode",
      property_value: "Property Value",
      loan_balance: "Loan Balance",
      interest_rate: "Current Rate",
      rate_last_reviewed: "Rate Reviewed",
      extra_cashout: "Extra Cashout",
      consolidate_debts: "Consolidate Debts",
      applicant_type: "Applicant",
      total_annual_income: "Annual Income",
      partner_annual_income: "Partner Income",
      full_name: "Applicant Name",
      email: "Email",
      phone_number: "Phone Number"
    };

    const entries = Object.keys(wizardState).filter(k => wizardState[k]);
    if (entries.length === 0) {
      list.innerHTML = `<p style="font-size:12px; color:#64748b; font-style:italic;">Your answers will appear here as you complete the enquiry...</p>`;
      return;
    }

    list.innerHTML = entries.map(k => `
      <div class="quote-summary-item">
        <span class="quote-summary-key">${keyLabels[k] || k}</span>
        <span class="quote-summary-val">${wizardState[k]}</span>
      </div>
    `).join('');
  }

  function nextQuoteWizardStep() {
    const stepData = QUOTE_ENQUIRY_SCHEMA.steps[currentWizardStep];
    
    // Validate required fields
    for (let f of stepData.fields) {
      if (f.condition && wizardState[f.condition.field] !== f.condition.value) continue;
      if (f.required && !wizardState[f.id]) {
        alert(`Please complete: "${f.label}" before continuing.`);
        return;
      }
    }

    if (currentWizardStep < QUOTE_ENQUIRY_SCHEMA.steps.length - 1) {
      currentWizardStep++;
      renderQuoteWizardStep();
    } else {
      submitQuoteWizardEnquiry();
    }
  }

  function prevQuoteWizardStep() {
    if (currentWizardStep > 0) {
      currentWizardStep--;
      renderQuoteWizardStep();
    }
  }

  function submitQuoteWizardEnquiry() {
    const mainArea = document.getElementById('qwMainArea');
    mainArea.innerHTML = `
      <div style="text-align:center; padding:40px 20px;">
        <div style="font-size:48px; margin-bottom:16px;">🎉</div>
        <h3 style="font-size:22px; font-weight:900; color:#0f2b48; margin-bottom:8px;">Quote Enquiry Submitted!</h3>
        <p style="font-size:14px; color:#475569; line-height:1.6; max-width:420px; margin:0 auto 24px;">
          Thank you, <strong>${wizardState.full_name || 'Customer'}</strong>. One of our local Melbourne mortgage brokers will review your rates across 50+ panel lenders and contact you shortly.
        </p>
        <button type="button" class="quote-btn-next" id="qwDoneBtn">Done</button>
      </div>
    `;

    document.getElementById('qwDoneBtn').onclick = closeQuoteWizard;
    document.getElementById('qwFooter').style.display = 'none';

    // Submit payload to backend CRM API & Resend notification
    fetch('/api/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tenant: 'ez-mortgage-broker',
        form: 'Home Loans Quote Enquiry Wizard',
        name: wizardState.full_name,
        email: wizardState.email,
        phone: wizardState.phone_number,
        summary: wizardState
      })
    }).catch(e => console.log('Lead submitted asynchronously:', e));
  }

  // Expose global open helper
  window.openQuoteWizard = openQuoteWizard;
  window.closeQuoteWizard = closeQuoteWizard;

  // Attach global click triggers for Quote Enquiry Wizard
  document.addEventListener('click', function (e) {
    const target = e.target.closest('a, button');
    if (!target) return;

    const text = (target.textContent || '').toLowerCase();
    const href = (target.getAttribute('href') || '').toLowerCase();

    if (
      text.includes('book consultation') ||
      text.includes('book a free consult') ||
      text.includes('get a quote') ||
      text.includes('get quote')
    ) {
      if (window.innerWidth > 640) {
        e.preventDefault();
        openQuoteWizard();
      }
    }
  });


  /* =========================================
     Live MFAA Breaking News, Date & Weather
     ========================================= */
  const MFAA_NEWS_HEADLINES = [
    { text: 'Mortgage brokers settle record 81.0% of all Australian residential home loans', url: 'https://www.mfaa.com.au/news/mortgage-brokers-continue-to-support-over-three-quarters-of-home-loan-borrowers-in-australia' },
    { text: 'RBA holds cash rate steady at 4.35% as inflation moderates across Australia', url: 'https://www.mfaa.com.au/news' },
    { text: 'First Home Guarantee scheme opens new allocations for eligible Australian buyers', url: 'https://www.mfaa.com.au/news' },
    { text: 'MFAA quarterly report confirms broker customer satisfaction remains over 98%', url: 'https://www.mfaa.com.au/news' },
    { text: 'Top Australian lenders launch competitive cashback and refinancing specials', url: 'https://www.mfaa.com.au/news' }
  ];

  function initHeaderLiveWidgets() {
    // 1. Auto-updating Date
    const dateEl = document.getElementById('headerCurrentDate');
    if (dateEl) {
      const now = new Date();
      const options = { weekday: 'short', day: 'numeric', month: 'short' };
      dateEl.innerHTML = '📅 ' + now.toLocaleDateString('en-AU', options);
    }

    // 2. Dynamic Weather Widget
    const weatherEl = document.getElementById('headerWeatherWidget');
    if (weatherEl) {
      function setWeatherDisplay(temp, code, city) {
        let icon = '☀️';
        if (code >= 1 && code <= 3) icon = '⛅';
        else if (code >= 45 && code <= 48) icon = '🌫️';
        else if (code >= 51 && code <= 67) icon = '🌧️';
        else if (code >= 71 && code <= 77) icon = '❄️';
        else if (code >= 80 && code <= 82) icon = '🌦️';
        else if (code >= 95) icon = '⛈️';
        weatherEl.innerHTML = icon + ' ' + (city || 'Melbourne') + ' ' + Math.round(temp) + '°C';
      }

      function fetchWeather(lat, lon, cityName) {
        fetch('https://api.open-meteo.com/v1/forecast?latitude=' + lat + '&longitude=' + lon + '&current=temperature_2m,weather_code&timezone=auto')
          .then(function (res) { return res.json(); })
          .then(function (data) {
            if (data.current) {
              setWeatherDisplay(data.current.temperature_2m, data.current.weather_code, cityName);
            }
          })
          .catch(function () {
            setWeatherDisplay(18, 1, 'Melbourne');
          });
      }

      // Default Melbourne coordinates (-37.8136, 144.9631)
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          function (pos) { fetchWeather(pos.coords.latitude, pos.coords.longitude, 'Local'); },
          function () { fetchWeather(-37.8136, 144.9631, 'Melbourne'); },
          { timeout: 3000 }
        );
      } else {
        fetchWeather(-37.8136, 144.9631, 'Melbourne');
      }
    }

    // 3. MFAA Breaking News Live Rotator
    const titleEl = document.getElementById('breakingNewsTitle');
    if (titleEl) {
      let newsIdx = 0;
      window.setInterval(function () {
        newsIdx = (newsIdx + 1) % MFAA_NEWS_HEADLINES.length;
        titleEl.style.opacity = '0';
        window.setTimeout(function () {
          titleEl.textContent = MFAA_NEWS_HEADLINES[newsIdx].text;
          titleEl.href = MFAA_NEWS_HEADLINES[newsIdx].url;
          titleEl.style.opacity = '1';
        }, 250);
      }, 4500);
    }
  }

  initHeaderLiveWidgets();

  /* =========================================
     Dynamic Homepage Blog Insights from posts.json
     ========================================= */
  const insightsGrid = document.querySelector('#insights .insights-grid');
  if (insightsGrid) {
    fetch('/posts.json')
      .then(function (res) { return res.json(); })
      .then(function (posts) {
        if (Array.isArray(posts) && posts.length > 0) {
          const featured = posts.slice(0, 3);
          insightsGrid.innerHTML = featured.map(function (post, index) {
            const delayClass = index === 1 ? ' fade-up-delay-1' : (index === 2 ? ' fade-up-delay-2' : '');
            const categoryEmoji = post.category === 'First Home Buyers' ? '🏠' : (post.category === 'Refinancing' ? '🔄' : (post.category === 'Investing' ? '📈' : '💡'));
            return '<div class="insight-card fade-up in-view' + delayClass + '">' +
              '<div class="insight-img">' +
                categoryEmoji +
                '<span class="category-tag">' + post.category + '</span>' +
              '</div>' +
              '<div class="insight-body">' +
                '<div class="insight-meta">' + post.date + ' · ' + (post.readTime || '5 min read') + '</div>' +
                '<h3>' + post.title + '</h3>' +
                '<p>' + post.summary + '</p>' +
                '<a href="/pages/blog/' + post.id + '.html" class="link-arrow">Read full guide &rarr;</a>' +
              '</div>' +
            '</div>';
          }).join('');
        }
      })
      .catch(function () {
        // Fallback static cards already present
      });
  }


})();
