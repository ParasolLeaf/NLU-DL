import React, { useState } from 'react';
import { registerUser, getUserProfile } from '../api';

const UserProfile = ({ onLogin }) => {
  const [userId, setUserId] = useState('');
  const [info, setInfo] = useState({ name: '', email: '' });
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!userId) return alert('请输入用户ID');
    setLoading(true);
    const res = await getUserProfile({ user_id: userId });
    setLoading(false);
    if (res.data.user_id) {
      onLogin(res.data);
    } else {
      alert(res.data.error || '未找到用户');
    }
  };

  const handleRegister = async () => {
    if (!userId) return alert('请输入用户ID');
    if (!info.name) return alert('请输入姓名');
    setLoading(true);
    const res = await registerUser({ user_id: userId, info });
    setLoading(false);
    if (res.data.success) {
      alert('注册成功，请登录');
      setIsRegister(false);
    } else {
      alert(res.data.error || '注册失败');
    }
  };

  return (
    <div className="login-bg-pro">
      <div className="login-card-pro">
        <div className="login-title-pro">多语言智能教学系统</div>
        <div className="login-subtitle-pro">AI驱动 · 多语言学习平台</div>
        <h2 className="login-form-title-pro">{isRegister ? '注册新用户' : '用户登录'}</h2>
        <input
          className="login-input-pro"
          placeholder="用户ID"
          value={userId}
          onChange={e => setUserId(e.target.value)}
        />
        {isRegister && (
          <>
            <input
              className="login-input-pro"
              placeholder="姓名"
              value={info.name}
              onChange={e => setInfo({ ...info, name: e.target.value })}
            />
            <input
              className="login-input-pro"
              placeholder="邮箱"
              value={info.email}
              onChange={e => setInfo({ ...info, email: e.target.value })}
            />
          </>
        )}
        <button
          className="login-btn-pro"
          onClick={isRegister ? handleRegister : handleLogin}
          disabled={loading}
        >
          {loading ? '处理中...' : isRegister ? '注册' : '登录'}
        </button>
        <div className="login-switch-pro">
          {isRegister ? (
            <span>已有账号？ <span className="login-link-pro" onClick={() => setIsRegister(false)}>去登录</span></span>
          ) : (
            <span>没有账号？ <span className="login-link-pro" onClick={() => setIsRegister(true)}>注册新用户</span></span>
          )}
        </div>
      </div>
      <div className="login-footer-pro">© 2025 多语言智能教学系统</div>
    </div>
  );
};

export default UserProfile; 