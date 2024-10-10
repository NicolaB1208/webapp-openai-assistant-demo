import React from 'react';
import ReactDOM from 'react-dom';
import Chatbot from './components/chatbot';
import Footer from './components/footer';
import Header from './components/header';
import './style.css';

function App() {
  return (
    <div className="main-container"> {/* New wrapper div */}
      <Header />
      <div className="container-wrapper">
        <div className="container">
          <Chatbot />
        </div>
      </div>
      <Footer />
    </div>
  );
}

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
