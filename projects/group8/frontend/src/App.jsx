import React, { useState } from 'react';
import { Tabs, Form, Input, Button, Upload, Select, message, Card, Typography, Divider } from 'antd';
import * as api from './api';
import './App.css';
import UserProfile from './components/UserProfile';
import SpeechModule from './components/SpeechModule';

const { TabPane } = Tabs;
const { Title, Paragraph } = Typography;

// 语言选择
const LANGS = ['英语', '日语', '法语', '德语', '西班牙语'];

// 工具函数：等级字母转数字
function levelToInt(lv) {
  if (typeof lv === 'number') return lv;
  switch (lv) {
    case 'A': return 5;
    case 'B': return 4;
    case 'C': return 3;
    case 'D': return 2;
    case 'E': return 1;
    default: return 1;
  }
}

function App() {
  const [user, setUser] = useState(null); // 登录用户档案
  const [level, setLevel] = useState(null); // 能力测试等级
  const [quiz, setQuiz] = useState(null); // 能力测试题目
  const [quizAnswers, setQuizAnswers] = useState([]);
  const [quizStep, setQuizStep] = useState(0);
  const [quizResult, setQuizResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // 个性化学习交互式词汇-故事-语法
  const [vocabList, setVocabList] = useState([]);
  const [selectedVocab, setSelectedVocab] = useState([]);
  const [story, setStory] = useState('');
  const [grammar, setGrammar] = useState('');
  // 用loading统一控制按钮禁用
  const [personalLoading, setPersonalLoading] = useState(false);

  // 1. 用单一state替换历史state
  const [correctionResult, setCorrectionResult] = useState(null);
  const [slangResult, setSlangResult] = useState(null);
  const [vocabResult, setVocabResult] = useState(null);
  const [storyResult, setStoryResult] = useState(null);
  const [grammarResult, setGrammarResult] = useState(null);
  const [imgDescResult, setImgDescResult] = useState(null);

  const onGenerateVocab = async () => {
    try {
      let vocabLevel = level;
      if (typeof vocabLevel === 'string' && !isNaN(Number(vocabLevel))) vocabLevel = parseInt(vocabLevel);
      if (typeof vocabLevel !== 'number' || isNaN(vocabLevel)) vocabLevel = 1;
      const { data } = await api.generateVocab({ lang: testLang, level: vocabLevel });
      setVocabList(data.vocab || []);
      setSelectedVocab([]);
      setStory('');
      setGrammar('');
      setVocabResult({ vocab: data.vocab || [], lang: testLang, level: vocabLevel });
    } catch {
      window.message && window.message.error ? window.message.error('生成词汇失败') : alert('生成词汇失败');
    }
  };

  const onGenerateStory = async () => {
    if (!selectedVocab.length) {
      window.message && window.message.error ? window.message.error('请先选择词汇') : alert('请先选择词汇');
      return;
    }
    // 类型保护：level 为空时默认 1，并做字母转数字
    let storyLevel = levelToInt(level);
    // 调试：打印参数
    console.log('onGenerateStory params:', { lang: testLang, level: storyLevel, vocab: selectedVocab });
    try {
      const { data } = await api.generateStory({ lang: testLang, level: storyLevel, vocab: selectedVocab });
      console.log('generateStory 返回数据:', data);
      setStory(data.story || '');
      setGrammar('');
      setStoryResult({ vocab: [...selectedVocab], story: data.story || '', lang: testLang, level: storyLevel });
    } catch (e) {
      console.error('生成故事失败，异常信息：', e);
      window.message && window.message.error ? window.message.error('生成故事失败') : alert('生成故事失败');
    }
  };

  const onExtractGrammar = async () => {
    if (!story) {
      window.message && window.message.error ? window.message.error('请先生成故事') : alert('请先生成故事');
      return;
    }
    try {
      const { data } = await api.extractGrammar({ lang: testLang, story });
      setGrammar(data.grammar || '');
      setGrammarResult({ story, grammar: data.grammar || '', lang: testLang });
    } catch {
      window.message && window.message.error ? window.message.error('提取语法失败') : alert('提取语法失败');
    }
  };

  // 句子纠错
  const [correctionInput, setCorrectionInput] = useState('');
  // 俚语学习
  const [slangTopic, setSlangTopic] = useState('');
  // 看图说话
  const [imgUrl, setImgUrl] = useState('');
  // 语言选择
  const [testLang, setTestLang] = useState('英语');
  const [chooseLang, setChooseLang] = useState(false); // 登录后是否选择语言

  // 能力测试语言切换弹窗
  const [showQuizLangDialog, setShowQuizLangDialog] = useState(false);
  const renderQuizLangDialog = () => (
    <div className="quiz-loading-dialog">
      <div className="quiz-loading-box">
        <div className="quiz-loading-title">切换测试语言</div>
        <div className="quiz-loading-text">请选择你要进行能力测试的语言</div>
        <div style={{ margin: '24px 0' }}>
          {LANGS.map(l => (
            <button key={l} className="main-btn" style={{ margin: 8 }} onClick={() => {
              setTestLang(l);
              setShowQuizLangDialog(false);
              fetchQuiz(l);
            }}>{l}</button>
          ))}
        </div>
        <button className="main-btn" style={{ marginTop: 8 }} onClick={() => setShowQuizLangDialog(false)}>取消</button>
      </div>
    </div>
  );

  // 登录后，进入能力测试
  const handleLogin = (profile) => {
    setUser(profile);
    setLevel(null);
    setQuiz(null);
    setQuizAnswers([]);
    setQuizStep(0);
    setQuizResult(null);
    setTestLang('英语');
    setChooseLang(true); // 登录后先选择语言
  };

  // 获取能力测试题目
  const fetchQuiz = async (lang = testLang) => {
    setLoading(true);
    const res = await api.languageQuiz({ lang, level: 1 });
    setQuiz(res.data);
    setLoading(false);
  };

  // 提交能力测试答案
  const handleQuizSubmit = async () => {
    setLoading(true);
    const user_answers = quizAnswers.join(',');
    // 新增：将题目和正确答案一起传给后端
    const quizPayload = {
      questions: quiz.questions,
      user_answers: quizAnswers
    };
    const res = await api.languageQuizGrade({ lang: testLang, level: 1, quizPayload });
    setQuizResult(res.data);
    setLevel(res.data.level || 'E');
    await api.addHistory({ user_id: user.user_id, module: 'tests', record: { answers: quizAnswers, result: res.data } });
    setLoading(false);
  };

  // 获取词汇
  const handleGetVocab = async () => {
    setPersonalLoading(true);
    let levelInt = level;
    if (typeof level === 'string' && !isNaN(Number(level))) levelInt = parseInt(level);
    if (typeof levelInt !== 'number' || isNaN(levelInt)) levelInt = 1;
    const res = await api.generateVocab({ lang: testLang, level: levelInt });
    setVocabList(res.data.vocab || []);
    setSelectedVocab([]);
    setStory('');
    setGrammar('');
    setPersonalLoading(false);
  };
  // 生成故事
  const handleStory = async () => {
    if (!selectedVocab.length) return;
    setPersonalLoading(true);
    // level需为字符串或数字，vocab需为非空数组
    let storyLevel = level;
    if (typeof storyLevel === 'undefined' || storyLevel === null || storyLevel === '') storyLevel = 1;
    const res = await api.generateStory({ lang: testLang, level: storyLevel, vocab: [...selectedVocab] });
    setStory(res.data.story || '');
    setGrammar('');
    setPersonalLoading(false);
  };
  // 提取语法
  const handleGrammar = async () => {
    if (!story) return;
    setPersonalLoading(true);
    const res = await api.extractGrammar({ lang: testLang, story });
    setGrammar(res.data.grammar || '');
    setPersonalLoading(false);
  };

  // 句子纠错
  const handleCorrection = async () => {
    if (!correctionInput) return;
    setPersonalLoading(true);
    const res = await api.correctSentence({ sentence: correctionInput, lang: testLang, native_lang: '中文' });
    setCorrectionResult({ input: correctionInput, result: res.data });
    setPersonalLoading(false);
  };

  // 俚语学习
  const handleSlang = async () => {
    if (!slangTopic) return;
    setSlangLoading(true);
    const res = await api.generateSlang({ topic: slangTopic, lang: testLang, native_lang: '中文' });
    setSlangResult({ topic: slangTopic, result: res.data });
    setSlangLoading(false);
  };

  // 看图说话
  const handleImgDesc = async () => {
    if (!imgUrl) return;
    setPersonalLoading(true);
    const res = await api.describeImage({ image_urls: [imgUrl], prompt: `请用${testLang}描述图片内容` });
    setImgDescResult({ url: imgUrl, desc: { baidu: res.data.baidu || '', ali: res.data.ali || '' } });
    setPersonalLoading(false);
  };

  // 角色对话模块
  const [roleChatHistory, setRoleChatHistory] = useState([]);
  const [roleInput, setRoleInput] = useState('');
  const [roleType, setRoleType] = useState('老师');
  const [roleLoading, setRoleLoading] = useState(false);
  const ROLE_LIST = ['老师', '同学', '本地人'];
  const handleRoleChat = async () => {
    if (!roleInput.trim()) return;
    setRoleLoading(true);
    const newHistory = [...roleChatHistory, { role: 'user', content: roleInput }];
    setRoleChatHistory(newHistory);
    setRoleInput('');
    try {
      const res = await api.roleChat({ lang: testLang, role: roleType, history: newHistory });
      setRoleChatHistory([...newHistory, { role: 'ai', content: res.data.reply }]);
    } catch {
      setRoleChatHistory([...newHistory, { role: 'ai', content: '对话失败，请重试' }]);
    }
    setRoleLoading(false);
  };
  const renderRoleChat = () => (
    <div className="quiz-result-box">
      <div className="quiz-result-title">角色对话</div>
      <div style={{ marginBottom: 12, display: 'flex', alignItems: 'center', gap: 12 }}>
        <span>选择角色：</span>
        <div style={{ display: 'flex', gap: 8 }}>
          {ROLE_LIST.map(r => (
            <button
              key={r}
              className={`role-btn${r === roleType ? ' selected' : ''}`}
              style={{
                // 样式全部交给CSS
              }}
              onClick={() => setRoleType(r)}
            >{r}</button>
          ))}
        </div>
      </div>
      <div style={{ minHeight: 120, background: '#f7fafd', borderRadius: 8, padding: 12, marginBottom: 12, maxHeight: 220, overflowY: 'auto' }}>
        {roleChatHistory.length === 0 && <div style={{ color: '#aaa' }}>和{roleType}开始多轮对话吧！</div>}
        {roleChatHistory.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.role === 'user' ? 'right' : 'left', margin: '6px 0' }}>
            <span style={{ color: msg.role === 'user' ? '#185a9d' : '#43cea2', fontWeight: 500 }}>{msg.role === 'user' ? '我' : roleType}：</span>
            <span>{msg.content}</span>
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <input className="vocab-btn" style={{ flex: 1 }} placeholder={`和${roleType}对话...`} value={roleInput} onChange={e => setRoleInput(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') handleRoleChat(); }} disabled={roleLoading} />
        <button className="main-btn" onClick={handleRoleChat} disabled={roleLoading || !roleInput.trim()}>{roleLoading ? '发送中...' : '发送'}</button>
      </div>
    </div>
  );

  // 渲染能力测试界面
  const renderQuiz = () => {
    if (!quiz || !Array.isArray(quiz.questions) || !quiz.questions || quiz.questions.length === 0) {
      return (
        <div className="quiz-loading-dialog">
          <div className="quiz-loading-box">
            <div className="quiz-loading-title">能力测评准备中</div>
            <div className="quiz-loading-text">正在加载能力测试题目...</div>
            <div className="quiz-loading-spinner"></div>
          </div>
        </div>
      );
    }
    return (
      <div className="quiz-container">
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: 32 }}>
          <div className="app-title-pro">多语言智能教学系统</div>
          <div className="app-subtitle-pro">AI驱动 · 多语言学习平台</div>
          <button className="main-btn" style={{ margin: '18px 0 0 0', fontSize: 16 }} onClick={() => setShowQuizLangDialog(true)}>
            当前测试语言：{testLang}（点击切换）
          </button>
        </div>
        {(Array.isArray(quiz.questions) ? quiz.questions : []).map((q, idx) => (
          <div key={idx} className="quiz-question">
            <div style={{ fontWeight: 600 }}>
              <span className="quiz-dimension">{q.dimension || `题目${idx + 1}`}</span> {idx + 1}. {q.question}
            </div>
            {(Array.isArray(q.options) ? q.options : []).map((opt, i) => (
              <button
                key={i}
                type="button"
                className={`option-btn${quizAnswers[idx] === opt ? ' selected' : ''}`}
                onClick={() => {
                  const arr = [...quizAnswers];
                  arr[idx] = opt;
                  setQuizAnswers(arr);
                }}
                style={{ display: 'block', width: '100%', margin: '8px 0' }}
              >
                {opt}
              </button>
            ))}
                      </div>
                    ))}
        <button className="main-btn" onClick={handleQuizSubmit} disabled={loading || quizAnswers.length !== quiz.questions.length}>
          {loading ? '提交中...' : '提交测试'}
        </button>
                  </div>
    );
  };

  // 渲染个性化学习和专项训练入口
  const renderPersonalized = () => (
    <div className="main-modules">
      <h2>个性化学习</h2>
      <button className="main-btn" onClick={onGenerateVocab} disabled={loading}>生成词汇</button>
                <div style={{ margin: '16px 0' }}>
                  {vocabList.map((v, i) => (
          <button
                      key={i}
            className={`vocab-btn${selectedVocab.includes(v) ? ' selected' : ''}`}
                      onClick={() => {
                        setSelectedVocab(selectedVocab.includes(v)
                          ? selectedVocab.filter(x => x !== v)
                          : [...selectedVocab, v]);
                      }}
          >{v}</button>
                  ))}
                </div>
      <button className="main-btn" onClick={onGenerateStory} disabled={selectedVocab.length === 0 || loading}>生成小故事</button>
                {story && (
        <div className="quiz-result-box" style={{ marginTop: 24 }}>
          <div className="quiz-result-title">小故事</div>
          <div style={{ whiteSpace: 'pre-wrap', color: '#185a9d' }}>{story}</div>
        </div>
                )}
      <button className="main-btn" onClick={onExtractGrammar} disabled={!story || loading}>提取语法点</button>
                {grammar && (
        <div className="quiz-result-box" style={{ marginTop: 24 }}>
          <div className="quiz-result-title">语法点</div>
          <div style={{ whiteSpace: 'pre-wrap', color: '#43cea2' }}>{grammar}</div>
        </div>
                )}
              </div>
  );

  // 主界面模块切换
  const MODULES = [
    {
      key: 'personalized',
      title: '个性化学习',
      icon: (
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="16" fill="url(#a)"/><path d="M10 22v-2a4 4 0 0 1 8 0v2" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><circle cx="14" cy="14" r="2" fill="#fff"/><defs><linearGradient id="a" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse"><stop stopColor="#43cea2"/><stop offset="1" stopColor="#185a9d"/></linearGradient></defs></svg>
      ),
      desc: '根据你的水平智能推送词汇、语法、听说读写内容',
    },
    {
      key: 'correction',
      title: '句子纠错',
      icon: (
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect width="32" height="32" rx="16" fill="url(#b)"/><path d="M10 16l4 4 8-8" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><defs><linearGradient id="b" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse"><stop stopColor="#ffb347"/><stop offset="1" stopColor="#ffcc33"/></linearGradient></defs></svg>
      ),
      desc: '智能检测并纠正你的句子错误',
    },
    {
      key: 'slang',
      title: '俚语学习',
      icon: (
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect width="32" height="32" rx="16" fill="url(#c)"/><path d="M16 10v8M16 18l-4-4m4 4l4-4" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><defs><linearGradient id="c" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse"><stop stopColor="#43cea2"/><stop offset="1" stopColor="#f7971e"/></linearGradient></defs></svg>
      ),
      desc: '掌握地道表达，提升口语能力',
    },
    {
      key: 'vision',
      title: '看图说话',
      icon: (
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect width="32" height="32" rx="16" fill="url(#d)"/><circle cx="16" cy="16" r="6" stroke="#fff" strokeWidth="2"/><defs><linearGradient id="d" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse"><stop stopColor="#2193b0"/><stop offset="1" stopColor="#6dd5ed"/></linearGradient></defs></svg>
      ),
      desc: '用目标语言描述图片内容，提升表达',
    },
    {
      key: 'rolechat',
      title: '角色对话',
      icon: (
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect width="32" height="32" rx="16" fill="url(#e)"/><path d="M10 22v-2a4 4 0 0 1 8 0v2" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><circle cx="16" cy="14" r="4" stroke="#fff" strokeWidth="2"/><defs><linearGradient id="e" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse"><stop stopColor="#185a9d"/><stop offset="1" stopColor="#43cea2"/></linearGradient></defs></svg>
      ),
      desc: '与AI老师/同学/本地人多轮对话',
    },
    {
      key: 'speech',
      title: '语音识别与合成',
      icon: (
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><rect width="32" height="32" rx="16" fill="url(#f)"/><path d="M16 10v8M16 18l-4-4m4 4l4-4" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/><circle cx="16" cy="22" r="2" fill="#fff"/><defs><linearGradient id="f" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse"><stop stopColor="#43cea2"/><stop offset="1" stopColor="#185a9d"/></linearGradient></defs></svg>
      ),
      desc: '上传音频识别文本，或输入文本合成语音',
    },
  ];

  const [activeModule, setActiveModule] = useState('personalized');
  const renderMainModules = () => (
    <>
      <div className="main-modules-grid">
        {MODULES.map(mod => (
          <div
            key={mod.key}
            className={`module-card-pro${activeModule === mod.key ? ' module-card-pro-active' : ''}`}
            onClick={() => setActiveModule(mod.key)}
          >
            <div className="module-card-pro-icon">{mod.icon}</div>
            <div className="module-card-pro-title">{mod.title}</div>
            <div className="module-card-pro-desc">{mod.desc}</div>
          </div>
        ))}
      </div>
      <div style={{ marginTop: 32 }}>
        {activeModule === 'personalized' && renderPersonalized()}
        {activeModule === 'correction' && (
          <div className="quiz-result-box">
            <div className="quiz-result-title">句子纠错</div>
            <input className="vocab-btn" style={{ width: '80%', marginBottom: 12 }} placeholder="请输入要纠错的句子" value={correctionInput} onChange={e => setCorrectionInput(e.target.value)} />
            <button className="main-btn" onClick={handleCorrection} disabled={personalLoading}>纠错</button>
            {correctionResult && (
  <div style={{ marginTop: 16, display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
    <div style={{ minWidth: 180, color: '#888', fontSize: 13, marginBottom: 4 }}>输入：{correctionResult.input}</div>
    {['doubao', 'baidu', 'ali'].map(model => (
      correctionResult.result[model] && (
        <div key={model} style={{ minWidth: 220, background: '#f7fafd', borderRadius: 10, padding: 16, boxShadow: '0 2px 8px #185a9d22' }}>
          <div style={{ fontWeight: 600, color: '#185a9d', marginBottom: 8 }}>{model.toUpperCase()}模型</div>
          <div style={{ color: '#333', whiteSpace: 'pre-wrap' }}>{correctionResult.result[model]}</div>
        </div>
      )
    ))}
  </div>
)}
          </div>
        )}
        {activeModule === 'slang' && (
          <div className="quiz-result-box">
            <div className="quiz-result-title">俚语生成</div>
            <input className="vocab-btn" style={{ width: '80%', marginBottom: 12 }} placeholder="请输入主题词（如friend）" value={slangTopic} onChange={e => setSlangTopic(e.target.value)} />
            <button className="main-btn" onClick={handleSlang} disabled={slangLoading}>生成俚语</button>
            {slangResult && (
  <div style={{ marginTop: 16, display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
    <div style={{ minWidth: 180, color: '#888', fontSize: 13, marginBottom: 4 }}>主题：{slangResult.topic}</div>
    {['doubao', 'baidu', 'ali'].map(model => (
      slangResult.result[model] && (
        <div key={model} style={{ minWidth: 220, background: '#f7fafd', borderRadius: 10, padding: 16, boxShadow: '0 2px 8px #43cea222' }}>
          <div style={{ fontWeight: 600, color: '#43cea2', marginBottom: 8 }}>{model.toUpperCase()}模型</div>
          <div style={{ color: '#333', whiteSpace: 'pre-wrap' }}>{slangResult.result[model]}</div>
        </div>
      )
    ))}
    {slangResult.result.web && slangResult.result.web.slangs && (
      <div style={{ minWidth: 220, background: '#fffbe6', borderRadius: 10, padding: 16, boxShadow: '0 2px 8px #f7971e22' }}>
        <div style={{ fontWeight: 600, color: '#f7971e', marginBottom: 8 }}>网页抓取</div>
        <ul style={{ paddingLeft: 16, margin: 0 }}>
          {slangResult.result.web.slangs.map((s, i) => (
            <li key={i} style={{ marginBottom: 6 }}>
              <a href={s.url} target="_blank" rel="noopener noreferrer" style={{ color: '#185a9d', textDecoration: 'underline' }}>{s.title}</a>
            </li>
          ))}
        </ul>
      </div>
    )}
  </div>
)}
          </div>
        )}
        {activeModule === 'vision' && (
          <div className="quiz-result-box">
            <div className="quiz-result-title">看图说话</div>
            <input className="vocab-btn" style={{ width: '80%', marginBottom: 12 }} placeholder="请输入图片URL" value={imgUrl} onChange={e => setImgUrl(e.target.value)} />
            <button className="main-btn" onClick={handleImgDesc} disabled={personalLoading}>生成图片描述</button>
            {imgUrl && <div style={{ margin: '20px 0' }}><img src={imgUrl} alt="预览" style={{ maxWidth: 320, borderRadius: 12, boxShadow: '0 2px 8px #185a9d22' }} /></div>}
            {imgDescResult && (
  <div style={{ marginTop: 16, background: '#fffbe6', borderRadius: 10, padding: 16, boxShadow: '0 2px 8px #f7971e22' }}>
    <div style={{ color: '#f7971e', fontWeight: 600, marginBottom: 8 }}>图片URL：{imgDescResult.url}</div>
    <div style={{ color: '#185a9d', marginBottom: 8 }}><b>百度：</b>{imgDescResult.desc.baidu}</div>
    <div style={{ color: '#43cea2' }}><b>阿里：</b>{imgDescResult.desc.ali}</div>
  </div>
)}
          </div>
        )}
        {activeModule === 'rolechat' && renderRoleChat()}
        {activeModule === 'speech' && <SpeechModule />}
      </div>
    </>
  );

  // 语言选择弹窗
  const renderLangSelect = () => (
    <div className="quiz-loading-dialog">
      <div className="quiz-loading-box">
        <div className="quiz-loading-title">请选择测试语言</div>
        <div className="quiz-loading-text">请选择你要进行能力测试的语言</div>
        <div style={{ margin: '24px 0' }}>
          {LANGS.map(l => (
            <button key={l} className="main-btn" style={{ margin: 8 }} onClick={() => {
              setTestLang(l);
              setChooseLang(false);
              fetchQuiz(l);
            }}>{l}</button>
          ))}
              </div>
      </div>
    </div>
  );

  // UI流程控制
  if (!user) {
    return <UserProfile onLogin={handleLogin} />;
  }
  if (chooseLang) return renderLangSelect();
  if (!level) {
    return (
      <div className="app-bg app-bg-quiz">
        <div className="main-content-wide">{renderQuiz()}</div>
      </div>
    );
  }
  // 已登录且完成能力测试
  return (
    <div className="app-bg app-bg-quiz">
      <header className="app-header-pro">
        <div className="app-title-pro">多语言智能教学系统</div>
        <div className="app-subtitle-pro">AI驱动 · 多语言学习平台</div>
        {level && (
          <div className="user-level-badge">
            <span className="user-level-letter">测评等级：{level}</span>
          </div>
        )}
      </header>
      <div className="main-content-wide">{renderMainModules()}</div>
    </div>
  );
}

export default App;

