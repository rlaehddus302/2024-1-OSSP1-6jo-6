import React from 'react';
import './App.css';
// Header 컴포넌트 정의
function Header() {
  return (
    <header>
      <nav class="top-bar">
        {/* 로고와 메뉴 아이템들을 여기에 배치 */
        'test-header'}
      </nav>
    </header>
  );
}

// MainContent 컴포넌트 정의
function MainContent() {
  return (
    <main>
      <div className="content">
        {/* 페이지의 메인 콘텐츠를 여기에 배치 */
        'test main'}
      </div>
    </main>
  );
}

// App 컴포넌트 정의 - 전체 앱을 구성
function App() {
  return (
    <div className="App">
      <Header />
      <MainContent />
    </div>
  );
}

export default App;
