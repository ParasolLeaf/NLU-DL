import React, { useState, useRef } from 'react';
import { Input, Card, Typography, message, Divider, Select, Radio } from 'antd';
import { SoundOutlined, AudioOutlined } from '@ant-design/icons';
import { speechRecognize, speechSynthesize } from '../api';
import './SpeechModule.css';

const { Title } = Typography;
const { Option } = Select;

// 简单发音错误检测（示例）
function detectPronunciationErrors(text) {
  const errors = [];
  if (/\b(s|z|S|Z)\b/.test(text)) {
    errors.push('可能存在 th 发成 s/z 的问题');
  }
  // 可扩展更多规则
  return errors;
}

// 合成语音参数只允许普通话/英语，语速正常/慢速
const ACCENT_OPTIONS = [
  { value: 'zh', label: '普通话' },
  { value: 'en', label: '英语' },
];
const SPEED_OPTIONS = [
  { value: 'normal', label: '正常语速' },
  { value: 'slow', label: '慢速' },
];

const VOICE_OPTIONS = [
  { value: 'Cherry', label: 'Cherry（美音，女）' },
  { value: 'Ethan', label: 'Ethan（美音，男）' },
  { value: 'Chelsie', label: 'Chelsie（英音，女）' },
  { value: 'Akira', label: 'Akira（日语，男）' },
  { value: 'Miyu', label: 'Miyu（日语，女）' },
];

export default function SpeechModule() {
  const [recognizedText, setRecognizedText] = useState('');
  const [pronunciationAdvice, setPronunciationAdvice] = useState([]);
  const [ttsText, setTtsText] = useState('');
  const [ttsAudio, setTtsAudio] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ttsSpeed, setTtsSpeed] = useState('normal');
  const [ttsAccent, setTtsAccent] = useState('zh');
  const audioRef = useRef();
  const [audioUrl, setAudioUrl] = useState('');
  const [ttsVoice, setTtsVoice] = useState('Cherry');

  // 语音识别
  const handleRecognize = async () => {
    setLoading(true);
    let url = audioUrl.trim();
    if (!url) {
      // 用默认示例URL
      url = 'https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav';
    }
    const res = await speechRecognize(url);
    setRecognizedText(res.text || '');
    // 检测发音错误
    const advice = detectPronunciationErrors(res.text || '');
    setPronunciationAdvice(advice);
    setLoading(false);
  };

  // 语音合成
  const handleSynthesize = async () => {
    if (!ttsText) return message.warning('请输入要合成的文本');
    setLoading(true);
    const slow = ttsSpeed === 'slow';
    const res = await speechSynthesize(ttsText, ttsVoice, slow);
    if (res.audio_b64) {
      setTtsAudio('data:audio/mp3;base64,' + res.audio_b64);
    }
    setLoading(false);
  };

  return (
    <Card className="quiz-result-box" style={{ maxWidth: 480, margin: '0 auto', borderRadius: 16, boxShadow: '0 2px 12px #185a9d22' }}>
      <Title level={3} style={{ color: '#185a9d', marginBottom: 24, textAlign: 'center' }}>
        <SoundOutlined style={{ marginRight: 8 }} />语音识别与合成
      </Title>
      <div style={{ marginBottom: 24 }}>
        <div style={{ fontWeight: 500, marginBottom: 8 }}>输入音频公网URL（如OSS链接）：</div>
        <Input
          value={audioUrl}
          onChange={e => setAudioUrl(e.target.value)}
          placeholder="请输入音频公网URL（如OSS链接），留空则用官方示例"
          style={{ width: '100%', marginBottom: 8 }}
        />
        <button
          className="main-btn"
          onClick={handleRecognize}
          disabled={loading}
        >
          <AudioOutlined /> 识别语音
        </button>
        <div className="speech-result">
          <span style={{ fontWeight: 500 }}>识别结果：</span>
          <span>{recognizedText}</span>
        </div>
        {pronunciationAdvice.length > 0 && (
          <div style={{ color: '#ff6600', marginTop: 8 }}>
            <b>发音建议：</b>{pronunciationAdvice.map((a, i) => <div key={i}>{a}</div>)}
          </div>
        )}
      </div>
      <Divider />
      <div style={{ marginBottom: 16 }}>
        <div style={{ fontWeight: 500, marginBottom: 8 }}>输入文本（合成语音）：</div>
        <Input
          value={ttsText}
          onChange={e => setTtsText(e.target.value)}
          placeholder="请输入要合成的文本"
          style={{ width: '100%', marginBottom: 8 }}
        />
        <div style={{ marginBottom: 8, display: 'flex', gap: 8 }}>
          <Select value={ttsVoice} onChange={setTtsVoice} style={{ width: 220 }}>
            {VOICE_OPTIONS.map(opt => <Select.Option key={opt.value} value={opt.value}>{opt.label}</Select.Option>)}
          </Select>
          <Select value={ttsSpeed} onChange={setTtsSpeed} style={{ width: 100 }}>
            {SPEED_OPTIONS.map(opt => <Select.Option key={opt.value} value={opt.value}>{opt.label}</Select.Option>)}
          </Select>
        </div>
        <button
          className="main-btn"
          onClick={handleSynthesize}
          disabled={!ttsText || loading}
        >
          <SoundOutlined /> 合成语音
        </button>
        {ttsAudio && (
          <audio ref={audioRef} src={ttsAudio} controls className="speech-audio" />
        )}
      </div>
    </Card>
  );
} 