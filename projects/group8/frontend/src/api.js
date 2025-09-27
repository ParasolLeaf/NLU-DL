import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// 语言能力测试
export const languageTest = (data) => {
  const formData = new FormData();
  formData.append('mode', data.mode);
  formData.append('user_input', data.user_input);
  formData.append('lang', data.lang);
  return api.post('/api/language_test/', formData);
};

// 个性化学习内容
export const learningTask = (data) => {
  const formData = new FormData();
  formData.append('level', data.level);
  formData.append('lang', data.lang);
  return api.post('/api/learning_task/', formData).then(res => ({ data: { doubao: res.data.doubao } }));
};

// 句子纠错
export const correctSentence = (data) => {
  const formData = new FormData();
  formData.append('sentence', data.sentence);
  formData.append('lang', data.lang);
  formData.append('native_lang', data.native_lang);
  return api.post('/api/correct_sentence/', formData).then(res => ({ data: { baidu: res.data.baidu } }));
};

// 俚语生成
export const generateSlang = (data) => {
  const formData = new FormData();
  formData.append('topic', data.topic);
  formData.append('lang', data.lang);
  formData.append('native_lang', data.native_lang);
  return api.post('/api/generate_slang/', formData).then(res => ({ data: { doubao: res.data.doubao, baidu: res.data.baidu, ali: res.data.ali, web: res.data.web } }));
};

// 图片描述（只返回百度和阿里）
export const describeImage = ({ image_urls, prompt }) => {
  const formData = new FormData();
  image_urls.forEach(url => formData.append('image_urls', url));
  formData.append('prompt', prompt);
  return api.post('/api/describe_image/', formData).then(res => ({ data: { baidu: res.data.baidu, ali: res.data.ali } }));
};

// 个性化学习：生成词汇
export const generateVocab = (data) => {
  const formData = new FormData();
  formData.append('lang', data.lang);
  formData.append('level', data.level);
  return api.post('/api/generate_vocab/', formData);
};
// 个性化学习：生成故事
export const generateStory = (data) => {
  const formData = new FormData();
  formData.append('lang', data.lang);
  formData.append('level', data.level);
  formData.append('vocab', JSON.stringify(data.vocab));
  // 调试：打印 FormData 内容
  for (let pair of formData.entries()) {
    console.log('generateStory FormData:', pair[0], pair[1]);
  }
  return api.post('/api/generate_story/', formData);
};
// 个性化学习：提取语法点
export const extractGrammar = (data) => {
  const formData = new FormData();
  formData.append('lang', data.lang);
  formData.append('story', data.story);
  return api.post('/api/extract_grammar/', formData);
};

// 语音识别
export const speechToText = (formData) => {
  return api.post('/api/speech_to_text/', formData);
};

// 用户统计
export const userStats = (data) => {
  const formData = new FormData();
  formData.append('user_id', data.user_id);
  return api.post('/api/user_stats/', formData);
};

// AI自动出选择题
export const languageQuiz = (data) => {
  const formData = new FormData();
  formData.append('lang', data.lang);
  formData.append('level', data.level);
  return api.post('/api/language_quiz/', formData).then(res => {
    return { data: { questions: res.data.questions || [] } };
  });
};
// AI选择题评级
export const languageQuizGrade = (data) => {
  const formData = new FormData();
  formData.append('lang', data.lang);
  formData.append('level', data.level);
  if (data.quizPayload) {
    formData.append('quiz_payload', JSON.stringify(data.quizPayload));
  } else {
    formData.append('user_answers', data.user_answers);
  }
  return api.post('/api/language_quiz_grade/', formData).then(res => ({ data: res.data }));
};

// 用户注册
export const registerUser = (data) => {
  const formData = new FormData();
  formData.append('user_id', data.user_id);
  formData.append('info', JSON.stringify(data.info));
  return api.post('/api/register_user/', formData);
};

// 获取用户档案
export const getUserProfile = (data) => {
  const formData = new FormData();
  formData.append('user_id', data.user_id);
  return api.post('/api/get_user_profile/', formData);
};

// 更新用户档案
export const updateUserProfile = (data) => {
  const formData = new FormData();
  formData.append('user_id', data.user_id);
  formData.append('updates', JSON.stringify(data.updates));
  return api.post('/api/update_user_profile/', formData);
};

// 添加历史记录
export const addHistory = (data) => {
  const formData = new FormData();
  formData.append('user_id', data.user_id);
  formData.append('module', data.module);
  formData.append('record', JSON.stringify(data.record));
  return api.post('/api/add_history/', formData);
};

export const roleChat = (data) => {
  const formData = new FormData();
  formData.append('lang', data.lang);
  formData.append('role', data.role);
  formData.append('history', JSON.stringify(data.history));
  return api.post('/api/role_chat/', formData);
};

export async function speechRecognize(audioUrl) {
  const formData = new FormData();
  formData.append('audio_url', audioUrl);
  const res = await fetch('/api/speech_recognize/', {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    console.error('speechRecognize接口请求失败:', res.status, res.statusText);
    const text = await res.text();
    console.error('响应内容:', text);
    throw new Error('speechRecognize接口请求失败: ' + res.status);
  }
  try {
    const json = await res.json();
    return json;
  } catch (e) {
    const text = await res.text();
    console.error('speechRecognize返回非JSON:', text);
    throw new Error('speechRecognize返回非JSON: ' + text);
  }
}

export async function speechSynthesize(text, voice = 'Cherry', slow = false) {
  const formData = new FormData();
  formData.append('text', text);
  formData.append('voice', voice);
  formData.append('slow', slow);
  const res = await fetch('/api/speech_synthesize/', {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    console.error('speechSynthesize接口请求失败:', res.status, res.statusText);
    const text = await res.text();
    console.error('响应内容:', text);
    throw new Error('speechSynthesize接口请求失败: ' + res.status);
  }
  try {
    const json = await res.json();
    return json;
  } catch (e) {
    const text = await res.text();
    console.error('speechSynthesize返回非JSON:', text);
    throw new Error('speechSynthesize返回非JSON: ' + text);
  }
} 