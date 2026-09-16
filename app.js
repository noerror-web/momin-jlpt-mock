/**
 * JLPT MOCK TEST SYSTEM - APPLICATION ENGINE (app.js)
 * Interactive Quiz Runner, Timer, Score Calculator, and Telegram Integration
 */

document.addEventListener('DOMContentLoaded', () => {
  // App State
  const state = {
    testData: null,
    flatQuestions: [],
    userAnswers: {},       // { questionId: selectedOptionIndex }
    flaggedQuestions: new Set(),
    currentIndex: 0,
    remainingSeconds: 0,
    timerInterval: null,
    isExamMode: true,
    studentInfo: { name: '', id: '' },
    telegramConfig: {
      botToken: localStorage.getItem('jlpt_tg_botToken') || '8863407575:AAFICc_QFXygIzV-3h_Ia4U7ZRmnaOdpy9Y',
      chatId: localStorage.getItem('jlpt_tg_chatId') || '5479582136'
    }
  };

  // DOM Element Handles
  const DOM = {
    // Header & Selectors
    testSelect: document.getElementById('testSelect'),
    modeExamBtn: document.getElementById('modeExamBtn'),
    modePracticeBtn: document.getElementById('modePracticeBtn'),
    openConfigBtn: document.getElementById('openConfigBtn'),
    tgConfigBadge: document.getElementById('tgConfigBadge'),

    // Screens
    welcomeScreen: document.getElementById('welcomeScreen'),
    examScreen: document.getElementById('examScreen'),
    resultScreen: document.getElementById('resultScreen'),

    // Welcome Elements
    welcomeTitle: document.getElementById('welcomeTitle'),
    welcomeDesc: document.getElementById('welcomeDesc'),
    statTimeLimit: document.getElementById('statTimeLimit'),
    statTotalQuestions: document.getElementById('statTotalQuestions'),
    statPassingScore: document.getElementById('statPassingScore'),
    studentNameInput: document.getElementById('studentName'),
    studentIdInput: document.getElementById('studentId'),
    startExamBtn: document.getElementById('startExamBtn'),

    // Exam Controls
    sectionTabsContainer: document.getElementById('sectionTabsContainer'),
    timerDisplay: document.getElementById('timerDisplay'),
    timerBox: document.getElementById('timerBox'),
    passageContainer: document.getElementById('passageContainer'),
    passageText: document.getElementById('passageText'),
    questionNumBadge: document.getElementById('questionNumBadge'),
    sectionTitleBadge: document.getElementById('sectionTitleBadge'),
    flagBtn: document.getElementById('flagBtn'),
    questionKanji: document.getElementById('questionKanji'),
    questionText: document.getElementById('questionText'),
    optionsContainer: document.getElementById('optionsContainer'),
    explanationBox: document.getElementById('explanationBox'),
    explanationText: document.getElementById('explanationText'),
    prevQBtn: document.getElementById('prevQBtn'),
    nextQBtn: document.getElementById('nextQBtn'),
    submitExamBtn: document.getElementById('submitExamBtn'),
    progressStatusText: document.getElementById('progressStatusText'),
    questionPalette: document.getElementById('questionPalette'),

    // Result Elements
    passFailBadge: document.getElementById('passFailBadge'),
    resultStudentHeading: document.getElementById('resultStudentHeading'),
    resultTestTitle: document.getElementById('resultTestTitle'),
    scorePercentValue: document.getElementById('scorePercentValue'),
    scoreRawValue: document.getElementById('scoreRawValue'),
    scoreRingProgress: document.getElementById('scoreRingProgress'),
    telegramStatusBox: document.getElementById('telegramStatusBox'),
    tgStatusMsg: document.getElementById('tgStatusMsg'),
    sectionBreakdownGrid: document.getElementById('sectionBreakdownGrid'),
    reviewAnswersBtn: document.getElementById('reviewAnswersBtn'),
    resendTgBtn: document.getElementById('resendTgBtn'),
    retakeExamBtn: document.getElementById('retakeExamBtn'),
    answerReviewSection: document.getElementById('answerReviewSection'),
    reviewQuestionsList: document.getElementById('reviewQuestionsList'),

    // Telegram Modal
    configModal: document.getElementById('configModal'),
    closeConfigBtn: document.getElementById('closeConfigBtn'),
    tgBotToken: document.getElementById('tgBotToken'),
    tgChatId: document.getElementById('tgChatId'),
    testTgConnectionBtn: document.getElementById('testTgConnectionBtn'),
    saveConfigBtn: document.getElementById('saveConfigBtn'),
    tgTestResult: document.getElementById('tgTestResult')
  };

  // --- INITIALIZATION ---
  function init() {
    updateTgBadge();
    loadTestJSON(DOM.testSelect.value);
    attachEventListeners();
  }

  function updateTgBadge() {
    if (state.telegramConfig.botToken && state.telegramConfig.chatId) {
      DOM.tgConfigBadge.classList.add('configured');
    } else {
      DOM.tgConfigBadge.classList.remove('configured');
    }
  }

  // --- LOAD TEST JSON ---
  async function loadTestJSON(filePath) {
    try {
      const response = await fetch(filePath);
      if (!response.ok) throw new Error('Failed to load test file');
      state.testData = await response.json();
      
      // Flatten questions list with section info attached
      state.flatQuestions = [];
      state.testData.sections.forEach(sec => {
        sec.questions.forEach(q => {
          state.flatQuestions.push({
            ...q,
            sectionId: sec.id,
            sectionTitle: sec.title,
            sectionWeight: sec.weight,
            passage: sec.passage || null
          });
        });
      });

      // Update Welcome View UI
      DOM.welcomeTitle.textContent = state.testData.title;
      DOM.welcomeDesc.textContent = `Official JLPT ${state.testData.level} format with automated score calculation and teacher alerts.`;
      DOM.statTimeLimit.textContent = `${state.testData.timeLimitMinutes} mins`;
      DOM.statTotalQuestions.textContent = `${state.flatQuestions.length} Questions`;
      DOM.statPassingScore.textContent = `${state.testData.passingScore} / ${state.testData.maxScore}`;

    } catch (err) {
      console.error('Error loading JSON:', err);
      alert('Unable to load test dataset. Please make sure the JSON file exists.');
    }
  }

  // --- EVENT LISTENERS ---
  function attachEventListeners() {
    // Select Test
    DOM.testSelect.addEventListener('change', (e) => loadTestJSON(e.target.value));

    // Mode Toggle
    DOM.modeExamBtn.addEventListener('click', () => setMode(true));
    DOM.modePracticeBtn.addEventListener('click', () => setMode(false));

    // Start Exam
    DOM.startExamBtn.addEventListener('click', startExam);

    // Exam Navigation
    DOM.prevQBtn.addEventListener('click', () => navigateQuestion(-1));
    DOM.nextQBtn.addEventListener('click', () => navigateQuestion(1));
    DOM.flagBtn.addEventListener('click', toggleFlagCurrentQuestion);
    DOM.submitExamBtn.addEventListener('click', () => {
      if (confirm('Are you sure you want to submit your exam now?')) {
        submitExam();
      }
    });

    // Result Actions
    DOM.reviewAnswersBtn.addEventListener('click', () => {
      DOM.answerReviewSection.classList.toggle('hidden');
      if (!DOM.answerReviewSection.classList.contains('hidden')) {
        renderAnswerReview();
      }
    });
    DOM.resendTgBtn.addEventListener('click', () => sendTelegramScoreNotification(calculateResults()));
    DOM.retakeExamBtn.addEventListener('click', resetToWelcome);

    // Config Modal
    DOM.openConfigBtn.addEventListener('click', () => {
      DOM.tgBotToken.value = state.telegramConfig.botToken;
      DOM.tgChatId.value = state.telegramConfig.chatId;
      DOM.configModal.classList.add('active');
    });
    DOM.closeConfigBtn.addEventListener('click', () => DOM.configModal.classList.remove('active'));
    DOM.saveConfigBtn.addEventListener('click', saveTelegramCredentials);
    DOM.testTgConnectionBtn.addEventListener('click', testTelegramConnection);

    // Filter Buttons in Review
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        renderAnswerReview(e.target.dataset.filter);
      });
    });
  }

  function setMode(isExam) {
    state.isExamMode = isExam;
    DOM.modeExamBtn.classList.toggle('active', isExam);
    DOM.modePracticeBtn.classList.toggle('active', !isExam);
  }

  // --- START EXAM ---
  function startExam() {
    const name = DOM.studentNameInput.value.trim();
    const id = DOM.studentIdInput.value.trim();

    if (!name || !id) {
      alert('Please enter your Name and Student ID before starting the examination.');
      return;
    }

    state.studentInfo = { name, id };
    state.userAnswers = {};
    state.flaggedQuestions.clear();
    state.currentIndex = 0;
    state.remainingSeconds = (state.testData.timeLimitMinutes || 45) * 60;

    // Switch View
    switchView('examScreen');
    buildSectionTabs();
    buildQuestionPalette();
    renderCurrentQuestion();
    startTimer();
  }

  function startTimer() {
    clearInterval(state.timerInterval);
    updateTimerDisplay();

    state.timerInterval = setInterval(() => {
      state.remainingSeconds--;
      updateTimerDisplay();

      if (state.remainingSeconds <= 0) {
        clearInterval(state.timerInterval);
        alert('⏰ Time is up! Your exam is being automatically submitted.');
        submitExam(true);
      }
    }, 1000);
  }

  function updateTimerDisplay() {
    const mins = Math.floor(state.remainingSeconds / 60);
    const secs = state.remainingSeconds % 60;
    DOM.timerDisplay.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

    if (state.remainingSeconds <= 300) { // 5 mins left
      DOM.timerBox.classList.add('warning');
    } else {
      DOM.timerBox.classList.remove('warning');
    }
  }

  // --- SECTION TABS & PALETTE ---
  function buildSectionTabs() {
    DOM.sectionTabsContainer.innerHTML = '';
    state.testData.sections.forEach((sec, idx) => {
      const btn = document.createElement('button');
      btn.className = `tab-btn ${idx === 0 ? 'active' : ''}`;
      btn.innerHTML = `<i class="fa-solid fa-layer-group"></i> ${sec.title}`;
      btn.addEventListener('click', () => jumpToSection(sec.id));
      DOM.sectionTabsContainer.appendChild(btn);
    });
  }

  function jumpToSection(sectionId) {
    const targetIdx = state.flatQuestions.findIndex(q => q.sectionId === sectionId);
    if (targetIdx !== -1) {
      state.currentIndex = targetIdx;
      renderCurrentQuestion();
    }
  }

  function buildQuestionPalette() {
    DOM.questionPalette.innerHTML = '';
    state.flatQuestions.forEach((q, idx) => {
      const btn = document.createElement('button');
      btn.className = 'palette-item';
      btn.dataset.index = idx;
      btn.textContent = idx + 1;
      btn.addEventListener('click', () => {
        state.currentIndex = idx;
        renderCurrentQuestion();
      });
      DOM.questionPalette.appendChild(btn);
    });
    updatePaletteState();
  }

  function updatePaletteState() {
    const buttons = DOM.questionPalette.querySelectorAll('.palette-item');
    buttons.forEach((btn, idx) => {
      const qId = state.flatQuestions[idx].id;
      btn.className = 'palette-item';
      if (idx === state.currentIndex) btn.classList.add('current');
      if (state.userAnswers[qId] !== undefined) btn.classList.add('answered');
      if (state.flaggedQuestions.has(qId)) btn.classList.add('flagged');
    });

    const answeredCount = Object.keys(state.userAnswers).length;
    DOM.progressStatusText.textContent = `${answeredCount} of ${state.flatQuestions.length} answered`;
  }

  // --- QUESTION RENDERING ---
  function renderCurrentQuestion() {
    const q = state.flatQuestions[state.currentIndex];

    // Update Meta badges
    DOM.questionNumBadge.textContent = `Question ${state.currentIndex + 1} of ${state.flatQuestions.length}`;
    DOM.sectionTitleBadge.textContent = q.sectionTitle;
    DOM.flagBtn.classList.toggle('flagged', state.flaggedQuestions.has(q.id));

    // Passage box (Furigana HTML)
    if (q.passageHtml || q.passage) {
      DOM.passageContainer.classList.remove('hidden');
      DOM.passageText.innerHTML = q.passageHtml || q.passage;
    } else {
      DOM.passageContainer.classList.add('hidden');
    }

    // Question Statement (Furigana HTML / Kanji)
    if (q.rubyHtml) {
      DOM.questionKanji.classList.add('hidden');
      DOM.questionText.innerHTML = q.rubyHtml;
    } else if (q.questionCardImage) {
      DOM.questionKanji.classList.remove('hidden');
      DOM.questionKanji.innerHTML = `
        <div class="question-snippet-card" style="background:#ffffff; border-radius:12px; padding:1.25rem; margin-bottom:1.5rem; text-align:center; box-shadow:0 8px 24px rgba(0,0,0,0.4);">
          <img src="${q.questionCardImage}" alt="Question Card" style="max-width:100%; max-height:280px; object-fit:contain; border-radius:6px; display:inline-block;" />
        </div>
      `;
      DOM.questionText.textContent = `Select your answer for Question ${state.currentIndex + 1}:`;
    } else if (q.kanji) {
      DOM.questionKanji.classList.remove('hidden');
      DOM.questionKanji.textContent = q.kanji;
      DOM.questionText.innerHTML = formatJapaneseText(q.text);
    } else {
      DOM.questionKanji.classList.add('hidden');
      DOM.questionText.innerHTML = formatJapaneseText(q.text);
    }

    // Options Grid
    DOM.optionsContainer.innerHTML = '';
    const letters = ['A', 'B', 'C', 'D'];
    const selectedOption = state.userAnswers[q.id];

    q.options.forEach((optText, optIdx) => {
      const card = document.createElement('div');
      card.className = 'option-card';
      if (selectedOption === optIdx) card.classList.add('selected');

      // Practice mode highlights
      if (!state.isExamMode && selectedOption !== undefined) {
        if (optIdx === q.answer) card.classList.add('correct-highlight');
        else if (selectedOption === optIdx && optIdx !== q.answer) card.classList.add('wrong-highlight');
      }

      card.innerHTML = `
        <div class="option-letter">${letters[optIdx] || optIdx + 1}</div>
        <div class="option-text">${optText}</div>
      `;

      card.addEventListener('click', () => selectOption(q.id, optIdx));
      DOM.optionsContainer.appendChild(card);
    });

    // Explanation Box (Practice mode)
    if (!state.isExamMode && selectedOption !== undefined) {
      DOM.explanationBox.classList.remove('hidden');
      DOM.explanationText.textContent = q.explanation || 'Correct Answer: Option ' + (q.answer + 1);
    } else {
      DOM.explanationBox.classList.add('hidden');
    }

    // Update Nav buttons
    DOM.prevQBtn.disabled = state.currentIndex === 0;
    DOM.nextQBtn.disabled = state.currentIndex === state.flatQuestions.length - 1;

    updatePaletteState();
  }

  function formatJapaneseText(text) {
    if (!text) return '';
    // Format bold markdown (**kanji**)
    return text.replace(/\*\*(.*?)\*\*/g, '<strong class="highlight-kanji">$1</strong>');
  }

  function selectOption(questionId, optionIdx) {
    state.userAnswers[questionId] = optionIdx;
    renderCurrentQuestion();
  }

  function navigateQuestion(direction) {
    const newIdx = state.currentIndex + direction;
    if (newIdx >= 0 && newIdx < state.flatQuestions.length) {
      state.currentIndex = newIdx;
      renderCurrentQuestion();
    }
  }

  function toggleFlagCurrentQuestion() {
    const qId = state.flatQuestions[state.currentIndex].id;
    if (state.flaggedQuestions.has(qId)) {
      state.flaggedQuestions.delete(qId);
    } else {
      state.flaggedQuestions.add(qId);
    }
    renderCurrentQuestion();
  }

  // --- EXAM SUBMISSION & SCORE EVALUATION ---
  function submitExam(autoSubmitted = false) {
    clearInterval(state.timerInterval);

    const results = calculateResults();
    displayResultsScreen(results);
    sendTelegramScoreNotification(results);
  }

  function calculateResults() {
    let totalScore = 0;
    let maxPossibleScore = state.testData.maxScore || 180;
    const sectionScores = {};

    state.testData.sections.forEach(sec => {
      let secCorrect = 0;
      sec.questions.forEach(q => {
        if (state.userAnswers[q.id] === q.answer) {
          secCorrect++;
        }
      });
      const secWeight = sec.weight || 60;
      const secScore = sec.questions.length > 0 
        ? Math.round((secCorrect / sec.questions.length) * secWeight)
        : 0;

      sectionScores[sec.id] = {
        title: sec.title,
        correct: secCorrect,
        total: sec.questions.length,
        score: secScore,
        maxScore: secWeight
      };

      totalScore += secScore;
    });

    const percentage = Math.round((totalScore / maxPossibleScore) * 100);
    const passingScore = state.testData.passingScore || 80;
    const passed = totalScore >= passingScore;

    const totalSecondsSpent = (state.testData.timeLimitMinutes * 60) - state.remainingSeconds;
    const minsSpent = Math.floor(totalSecondsSpent / 60);
    const secsSpent = totalSecondsSpent % 60;
    const timeSpentFormatted = `${minsSpent}m ${secsSpent}s`;

    return {
      studentName: state.studentInfo.name,
      studentId: state.studentInfo.id,
      testTitle: state.testData.title,
      level: state.testData.level,
      totalScore,
      maxPossibleScore,
      percentage,
      passed,
      timeSpentFormatted,
      sectionScores
    };
  }

  // --- DISPLAY RESULTS SCREEN ---
  function displayResultsScreen(results) {
    switchView('resultScreen');

    DOM.resultStudentHeading.textContent = `${results.studentName}'s Scorecard`;
    DOM.resultTestTitle.textContent = `${results.testTitle} (${results.level})`;
    
    if (results.passed) {
      DOM.passFailBadge.textContent = 'PASSED / 合格';
      DOM.passFailBadge.className = 'verdict-badge pass';
    } else {
      DOM.passFailBadge.textContent = 'FAILED / 不合格';
      DOM.passFailBadge.className = 'verdict-badge fail';
    }

    DOM.scorePercentValue.textContent = `${results.percentage}%`;
    DOM.scoreRawValue.textContent = `${results.totalScore} / ${results.maxPossibleScore}`;

    // Update Circle Progress stroke-dashoffset (max circumference = 326.7)
    const maxOffset = 326.7;
    const offset = maxOffset - (maxOffset * (results.percentage / 100));
    DOM.scoreRingProgress.style.strokeDashoffset = offset;

    // Render Section Bars
    DOM.sectionBreakdownGrid.innerHTML = '';
    Object.values(results.sectionScores).forEach(sec => {
      const card = document.createElement('div');
      card.className = 'sec-score-card';
      const secPct = Math.round((sec.score / sec.maxScore) * 100);

      card.innerHTML = `
        <div class="sec-title">${sec.title}</div>
        <div class="sec-bar-bg">
          <div class="sec-bar-fill" style="width: ${secPct}%"></div>
        </div>
        <div class="sec-score-num">${sec.score} / ${sec.maxScore} (${sec.correct}/${sec.total} correct)</div>
      `;
      DOM.sectionBreakdownGrid.appendChild(card);
    });
  }

  // --- RENDER DETAILED ANSWER REVIEW ---
  function renderAnswerReview(filter = 'all') {
    DOM.reviewQuestionsList.innerHTML = '';

    state.flatQuestions.forEach((q, idx) => {
      const userAns = state.userAnswers[q.id];
      const isCorrect = userAns === q.answer;

      if (filter === 'correct' && !isCorrect) return;
      if (filter === 'wrong' && isCorrect) return;

      const card = document.createElement('div');
      card.className = `review-card ${isCorrect ? 'correct' : 'wrong'}`;

      const letters = ['A', 'B', 'C', 'D'];
      const userAnsText = userAns !== undefined ? `${letters[userAns]}: ${q.options[userAns]}` : 'Unanswered';
      const correctAnsText = `${letters[q.answer]}: ${q.options[q.answer]}`;

      card.innerHTML = `
        <div style="font-weight:700; color:var(--primary); margin-bottom:0.4rem;">
          Q${idx + 1}. [${q.sectionTitle}] ${q.kanji ? q.kanji : ''}
        </div>
        <div style="font-size:1.05rem; margin-bottom:0.75rem;">${q.text}</div>
        <div style="display:flex; gap:1rem; font-size:0.9rem; margin-bottom:0.5rem;">
          <span style="color: ${isCorrect ? 'var(--success)' : 'var(--danger)'};">
            <strong>Your Answer:</strong> ${userAnsText}
          </span>
          <span style="color: var(--success);">
            <strong>Correct Answer:</strong> ${correctAnsText}
          </span>
        </div>
        <div style="font-size:0.85rem; color:var(--text-muted); background:rgba(255,255,255,0.03); padding:0.6rem; border-radius:6px;">
          💡 ${q.explanation || 'No explanation available.'}
        </div>
      `;
      DOM.reviewQuestionsList.appendChild(card);
    });
  }

  // --- TELEGRAM PUSH NOTIFICATION ---
  async function sendTelegramScoreNotification(results) {
    const token = state.telegramConfig.botToken;
    const chatId = state.telegramConfig.chatId;

    if (!token || !chatId) {
      DOM.tgStatusMsg.innerHTML = '⚠️ Telegram credentials not configured. <a href="#" id="openModalLink">Set up now</a>';
      document.getElementById('openModalLink')?.addEventListener('click', () => DOM.configModal.classList.add('active'));
      return;
    }

    DOM.tgStatusMsg.textContent = '📤 Sending score report to Telegram...';

    // Format rich Telegram markdown payload
    const messageText = `
🎓 *NEW JLPT MOCK TEST SUBMISSION* 🎓
━━━━━━━━━━━━━━━━━━━━
👤 *Student Name:* ${escapeMarkdown(results.studentName)}
🆔 *Student ID:* ${escapeMarkdown(results.studentId)}
📘 *Test Title:* ${escapeMarkdown(results.testTitle)} (${results.level})
⏰ *Time Spent:* ${results.timeSpentFormatted}

📊 *TOTAL SCORE:* ${results.totalScore} / ${results.maxPossibleScore} (${results.percentage}%)
🏆 *STATUS:* ${results.passed ? '✅ PASSED / 合格' : '❌ FAILED / 不合格'}

*Section Performance:*
${Object.values(results.sectionScores).map(sec => `• ${escapeMarkdown(sec.title)}: ${sec.score}/${sec.maxScore} (${sec.correct}/${sec.total})`).join('\n')}
━━━━━━━━━━━━━━━━━━━━
📅 *Submitted:* ${new Date().toLocaleString()}
`.trim();

    try {
      // First attempt serverless / API backend endpoint (Vercel route or local server)
      const response = await fetch('/api/send-score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          botToken: token,
          chatId: chatId,
          message: messageText
        })
      });

      if (response.ok) {
        DOM.tgStatusMsg.innerHTML = '✅ Score report successfully pushed to Telegram!';
      } else {
        // Fallback to direct client call if serverless function not running
        await sendDirectTelegramCall(token, chatId, messageText);
      }
    } catch (err) {
      console.warn('Backend API proxy failed, trying direct Telegram API fallback:', err);
      await sendDirectTelegramCall(token, chatId, messageText);
    }
  }

  async function sendDirectTelegramCall(token, chatId, text) {
    try {
      const url = `https://api.telegram.org/bot${token}/sendMessage`;
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: chatId,
          text: text,
          parse_mode: 'Markdown'
        })
      });

      const data = await res.json();
      if (data.ok) {
        DOM.tgStatusMsg.innerHTML = '✅ Score report pushed directly to Telegram!';
      } else {
        throw new Error(data.description || 'Failed to send message');
      }
    } catch (err) {
      console.error('Telegram notification error:', err);
      DOM.tgStatusMsg.textContent = `❌ Telegram send failed: ${err.message}`;
    }
  }

  function escapeMarkdown(text) {
    return text ? text.replace(/[_*\[\]()~`>#+-=|{}.!]/g, '\\$&') : '';
  }

  // --- TELEGRAM CONFIG & TEST CONNECTION ---
  function saveTelegramCredentials() {
    const token = DOM.tgBotToken.value.trim();
    const chatId = DOM.tgChatId.value.trim();

    state.telegramConfig.botToken = token;
    state.telegramConfig.chatId = chatId;

    localStorage.setItem('jlpt_tg_botToken', token);
    localStorage.setItem('jlpt_tg_chatId', chatId);

    updateTgBadge();
    DOM.configModal.classList.remove('active');
    alert('Telegram Bot settings saved successfully!');
  }

  async function testTelegramConnection() {
    const token = DOM.tgBotToken.value.trim();
    const chatId = DOM.tgChatId.value.trim();

    if (!token || !chatId) {
      showTgFeedback('Please enter both Bot Token and Chat ID', false);
      return;
    }

    showTgFeedback('Testing connection...', null);

    try {
      const url = `https://api.telegram.org/bot${token}/sendMessage`;
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: chatId,
          text: '🔔 *JLPT Mock Test Bot Test Connection Successful!*',
          parse_mode: 'Markdown'
        })
      });

      const data = await res.json();
      if (data.ok) {
        showTgFeedback('✅ Connection successful! Test message sent to Telegram.', true);
      } else {
        showTgFeedback(`❌ Connection error: ${data.description}`, false);
      }
    } catch (err) {
      showTgFeedback(`❌ Network error: ${err.message}`, false);
    }
  }

  function showTgFeedback(msg, isSuccess) {
    DOM.tgTestResult.classList.remove('hidden', 'success', 'error');
    DOM.tgTestResult.textContent = msg;
    if (isSuccess === true) DOM.tgTestResult.classList.add('success');
    if (isSuccess === false) DOM.tgTestResult.classList.add('error');
  }

  // --- HELPER ROUTING ---
  function switchView(screenId) {
    DOM.welcomeScreen.classList.remove('active');
    DOM.examScreen.classList.remove('active');
    DOM.resultScreen.classList.remove('active');

    DOM[screenId].classList.add('active');
  }

  function resetToWelcome() {
    clearInterval(state.timerInterval);
    switchView('welcomeScreen');
  }

  // Run Init
  init();
});
